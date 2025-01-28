from keybert import KeyBERT
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from .agent import ResearchAgent
import logging

app = FastAPI(title="Research Paper API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

class SearchResponse(BaseModel):
    papers: Optional[List[PaperResponse]] = None
    error: Optional[str] = None

@app.post("/search", response_model=SearchResponse)
async def search_papers(request: SearchRequest):
    try:
        logging.info(request.prompt)
        agent = ResearchAgent()

        doc = request.prompt
        kw_model = KeyBERT()
        keywords = [kw[0] for kw in kw_model.extract_keywords(doc)]
        print(keywords)
        task = agent.search_papers(keywords, request.max_results)
        
        if task.status.value == "completed":
            return SearchResponse(papers=task.result)
        else:
            raise HTTPException(status_code=500, detail=task.result)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))