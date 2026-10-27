import logging
import math
import re
import urllib.parse
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import requests
import xml.etree.ElementTree as ET
import torch
from sentence_transformers import CrossEncoder

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress" 
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class ResearchTask:
    task_id: str
    description: str
    status: TaskStatus
    created_at: datetime
    completed_at: datetime = None
    result: Any = None

class Memory:
    def __init__(self):
        self.papers: Dict[str, Dict] = {}
        self.tasks: Dict[str, ResearchTask] = {}
        
    def add_paper(self, paper_id: str, paper_data: Dict):
        self.papers[paper_id] = paper_data
        
    def add_task(self, task: ResearchTask):
        self.tasks[task.task_id] = task
        
    def get_paper(self, paper_id: str) -> Dict:
        return self.papers.get(paper_id)
    
    def get_task(self, task_id: str) -> ResearchTask:
        return self.tasks.get(task_id)

class NeuralReRanker:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            device = "mps" if torch.backends.mps.is_available() else ("cuda" if torch.cuda.is_available() else "cpu")
            logger.info(f"Initializing Neural Cross-Encoder on device: {device}")
            cls._instance = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2", device=device)
        return cls._instance

    @classmethod
    def score_and_rank(cls, query: str, candidates: List[Dict[str, Any]], top_k: int = 12) -> List[Dict[str, Any]]:
        if not candidates:
            return []
            
        model = cls.get_instance()
        pairs = [[query, f"{c.get('title', '')}. {c.get('abstract', '')}"] for c in candidates]
        
        try:
            raw_scores = model.predict(pairs)
        except Exception as e:
            logger.error(f"Re-ranking error: {e}, falling back to unranked")
            return candidates[:top_k]

        for i, c in enumerate(candidates):
            score = float(raw_scores[i])
            c["raw_score"] = score
            # Sigmoidal normalization to calibrated match percentage 0-100%
            c["relevance_score"] = int(round(100.0 / (1.0 + math.exp(-score * 0.4))))

        ranked = sorted(candidates, key=lambda x: x["raw_score"], reverse=True)
        return ranked[:top_k]

class ResearchAgent:
    def __init__(self):
        self.memory = Memory()
        self.arxiv_base = "http://export.arxiv.org/api/query?"
        self.openalex_base = "https://api.openalex.org/works"
        
    def create_task(self, description: str) -> ResearchTask:
        task_id = f"task_{len(self.memory.tasks)}"
        task = ResearchTask(
            task_id=task_id,
            description=description,
            status=TaskStatus.PENDING,
            created_at=datetime.now()
        )
        self.memory.add_task(task)
        return task
        
    def search_papers(self, keywords: List[str], max_results: int = 12, prompt: Optional[str] = None) -> ResearchTask:
        search_query_desc = prompt if prompt else f"keywords: {keywords}"
        task = self.create_task(f"Search and rerank papers for: {search_query_desc}")
        task.status = TaskStatus.IN_PROGRESS
        
        try:
            candidate_pool: List[Dict[str, Any]] = []
            seen_titles = set()

            def normalize_title(t: str) -> str:
                return re.sub(r'[^a-zA-Z0-9]', '', t.lower())

            # 1. Fetch from arXiv (Preprints)
            arxiv_query = self._formulate_arxiv_query(keywords, max_results=max(max_results * 2, 15))
            arxiv_papers = self._fetch_arxiv_papers(arxiv_query)
            for p in arxiv_papers:
                norm = normalize_title(p["title"])
                if norm and norm not in seen_titles:
                    seen_titles.add(norm)
                    candidate_pool.append(p)

            # 2. Fetch from OpenAlex (Peer-reviewed journals/conferences)
            search_text = prompt if prompt else " ".join(keywords)
            openalex_papers = self._fetch_openalex_papers(search_text, max_results=max(max_results * 2, 15))
            for p in openalex_papers:
                norm = normalize_title(p["title"])
                if norm and norm not in seen_titles:
                    seen_titles.add(norm)
                    candidate_pool.append(p)

            logger.info(f"Candidate pool retrieved: {len(candidate_pool)} papers across arXiv & OpenAlex")

            # 3. Apply Cross-Encoder Neural Re-Ranking
            rerank_query = prompt if prompt else " ".join(keywords)
            ranked_papers = NeuralReRanker.score_and_rank(rerank_query, candidate_pool, top_k=max_results)

            for paper in ranked_papers:
                paper_id = paper['id']
                self.memory.add_paper(paper_id, paper)
            
            task.status = TaskStatus.COMPLETED
            task.result = ranked_papers
            task.completed_at = datetime.now()
            
        except Exception as e:
            logger.error(f"Error in search_papers: {str(e)}", exc_info=True)
            task.status = TaskStatus.FAILED
            task.result = str(e)
            
        return task
    
    def _formulate_arxiv_query(self, keywords: List[str], max_results: int) -> str:
        # Formulate disjunctive title/abstract query
        clean_kws = [k.replace('"', '').strip() for k in keywords if len(k.strip()) > 1]
        if not clean_kws:
            clean_kws = ["machine learning"]
        query_string = " OR ".join(f'ti:"{keyword}" OR abs:"{keyword}"' for keyword in clean_kws)
        return f'search_query={urllib.parse.quote(query_string)}&start=0&max_results={max_results}'
    
    def _fetch_arxiv_papers(self, query: str) -> List[Dict]:
        try:
            response = requests.get(f"{self.arxiv_base}{query}", timeout=15)
            if response.status_code != 200:
                logger.warning(f"arXiv API failed with status {response.status_code}")
                return []
                
            root = ET.fromstring(response.content)
            papers = []
            ns = {'arxiv': 'http://www.w3.org/2005/Atom'}
            
            for entry in root.findall('arxiv:entry', ns):
                title_elem = entry.find('arxiv:title', ns)
                summary_elem = entry.find('arxiv:summary', ns)
                published_elem = entry.find('arxiv:published', ns)
                id_elem = entry.find('arxiv:id', ns)
                
                title = title_elem.text.strip().replace("\n", " ") if title_elem is not None else "Untitled"
                abstract = summary_elem.text.strip().replace("\n", " ") if summary_elem is not None else ""
                published = published_elem.text.strip() if published_elem is not None else datetime.now().isoformat()
                link = id_elem.text.strip() if id_elem is not None else ""

                authors = [author.find('arxiv:name', ns).text.strip() 
                           for author in entry.findall('arxiv:author', ns) 
                           if author.find('arxiv:name', ns) is not None]

                paper = {
                    'id': link or f"arxiv_{len(papers)}",
                    'title': title,
                    'authors': authors,
                    'abstract': abstract,
                    'published': published,
                    'link': link,
                    'source': 'arXiv (Preprint)',
                    'citations': None
                }
                papers.append(paper)
                
            return papers
        except Exception as e:
            logger.error(f"Error fetching from arXiv: {e}")
            return []

    def _fetch_openalex_papers(self, query: str, max_results: int) -> List[Dict]:
        try:
            url = f"{self.openalex_base}?search={urllib.parse.quote_plus(query)}&per-page={max_results}"
            headers = {"User-Agent": "ARISE-Research-Engine/2.0 (mailto:ghost-huzaifa@users.noreply.github.com)"}
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code != 200:
                logger.warning(f"OpenAlex API failed with status {response.status_code}")
                return []

            data = response.json()
            papers = []
            for item in data.get("results", []):
                title = item.get("title") or "Untitled"
                
                # Reconstruct abstract from inverted index if present
                abstract = ""
                inv_index = item.get("abstract_inverted_index")
                if inv_index and isinstance(inv_index, dict):
                    word_positions = []
                    for word, positions in inv_index.items():
                        for pos in positions:
                            word_positions.append((pos, word))
                    word_positions.sort()
                    abstract = " ".join(w for _, w in word_positions)
                
                authors = []
                for auth in item.get("authorships", []):
                    author_name = auth.get("author", {}).get("display_name")
                    if author_name:
                        authors.append(author_name)

                pub_year = item.get("publication_year")
                published_str = f"{pub_year}-01-01T00:00:00Z" if pub_year else datetime.now().isoformat()
                
                doi = item.get("doi")
                landing_page = item.get("primary_location", {}).get("landing_page_url")
                link = doi or landing_page or item.get("id") or ""

                papers.append({
                    'id': item.get("id") or f"openalex_{len(papers)}",
                    'title': title,
                    'authors': authors,
                    'abstract': abstract,
                    'published': published_str,
                    'link': link,
                    'source': 'OpenAlex (Peer-Reviewed)',
                    'citations': item.get("cited_by_count", 0)
                })

            return papers
        except Exception as e:
            logger.error(f"Error fetching from OpenAlex: {e}")
            return []
