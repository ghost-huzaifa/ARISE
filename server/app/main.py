import logging
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from keybert import KeyBERT
from .agent import ResearchAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="ARISE Research Paper API",
    description="Autonomous Research, Inference, Synthesis, and Exploration engine with Neural Cross-Encoder Re-Ranking"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global cached model instances
kw_model = None

def get_kw_model():
    global kw_model
    if kw_model is None:
        logger.info("Initializing cached KeyBERT keyword extractor...")
        kw_model = KeyBERT()
    return kw_model

class SearchRequest(BaseModel):
    prompt: str
    max_results: Optional[int] = 12

class PaperResponse(BaseModel):
    id: str
    title: str
    authors: List[str]
    abstract: str
    published: str
    link: str
    relevance_score: Optional[int] = None
    source: Optional[str] = "arXiv (Preprint)"
    citations: Optional[int] = None

class SearchResponse(BaseModel):
    papers: Optional[List[PaperResponse]] = None
    total_found: Optional[int] = None
    error: Optional[str] = None

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "ARISE Engine 2.0"}

@app.post("/search", response_model=SearchResponse)
async def search_papers(request: SearchRequest):
    try:
        logger.info(f"Received search query: '{request.prompt}' (max_results: {request.max_results})")
        agent = ResearchAgent()

        # Extract semantic keywords for first-stage lexical filtering
        kw_extractor = get_kw_model()
        extracted = kw_extractor.extract_keywords(request.prompt)
        keywords = [kw[0] for kw in extracted] if extracted else request.prompt.split()[:5]
        logger.info(f"Extracted candidate filter keywords: {keywords}")

        # Execute federated search + Cross-Encoder re-ranking
        task = agent.search_papers(
            keywords=keywords,
            max_results=request.max_results or 12,
            prompt=request.prompt
        )
        
        if task.status.value == "completed":
            results = task.result or []
            return SearchResponse(papers=results, total_found=len(results))
        else:
            raise HTTPException(status_code=500, detail=str(task.result))
            
    except Exception as e:
        logger.error(f"Search endpoint error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
