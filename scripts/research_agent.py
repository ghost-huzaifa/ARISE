import sys
import json
import logging
from typing import List, Dict, Any
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import requests
import xml.etree.ElementTree as ET

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

class ResearchAgent:
    def __init__(self):
        self.memory = Memory()
        self.api_base = "http://export.arxiv.org/api/query?"
        
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
        
    def search_papers(self, keywords: List[str], max_results: int = 10) -> ResearchTask:
        task = self.create_task(f"Search papers for keywords: {keywords}")
        task.status = TaskStatus.IN_PROGRESS
        
        try:
            query = self._formulate_query(keywords, max_results)
            papers = self._fetch_papers(query)
            
            for paper in papers:
                paper_id = paper['id']
                self.memory.add_paper(paper_id, paper)
            
            task.status = TaskStatus.COMPLETED
            task.result = papers
            task.completed_at = datetime.now()
            
        except Exception as e:
            logger.error(f"Error in search_papers: {str(e)}")
            task.status = TaskStatus.FAILED
            task.result = str(e)
            
        return task
    
    def _formulate_query(self, keywords: List[str], max_results: int) -> str:
        query_string = " OR ".join(f'ti:"{keyword}" OR abs:"{keyword}"' for keyword in keywords)
        return f'search_query={query_string}&start=0&max_results={max_results}'
    
    def _fetch_papers(self, query: str) -> List[Dict]:
        response = requests.get(f"{self.api_base}{query}")
        if response.status_code != 200:
            raise Exception(f"API request failed with status {response.status_code}")
            
        root = ET.fromstring(response.content)
        papers = []
        ns = {'arxiv': 'http://www.w3.org/2005/Atom'}
        
        for entry in root.findall('arxiv:entry', ns):
            paper = {
                'id': entry.find('arxiv:id', ns).text.strip(),
                'title': entry.find('arxiv:title', ns).text.strip(),
                'authors': [author.find('arxiv:name', ns).text.strip() 
                          for author in entry.findall('arxiv:author', ns)],
                'abstract': entry.find('arxiv:summary', ns).text.strip(),
                'published': entry.find('arxiv:published', ns).text.strip(),
                'link': entry.find('arxiv:id', ns).text.strip()
            }
            papers.append(paper)
            
        return papers

if __name__ == "__main__":
    keywords = sys.argv[1:]
    if not keywords:
        print(json.dumps({"error": "No keywords provided"}))
        sys.exit(1)
        
    try:
        agent = ResearchAgent()
        task = agent.search_papers(keywords)
        
        if task.status == TaskStatus.COMPLETED:
            print(json.dumps({"papers": task.result}))
        else:
            print(json.dumps({"error": task.result}))
            sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)