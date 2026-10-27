import sys
import os
import json
import logging

# Add server directory to path if present
server_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "server")
if server_dir not in sys.path:
    sys.path.insert(0, server_dir)

try:
    from app.agent import ResearchAgent
except ImportError:
    from server.app.agent import ResearchAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    keywords = sys.argv[1:]
    if not keywords:
        print(json.dumps({"error": "No keywords provided"}))
        sys.exit(1)
        
    try:
        agent = ResearchAgent()
        prompt = " ".join(keywords)
        task = agent.search_papers(keywords=keywords, max_results=12, prompt=prompt)
        
        if task.status.value == "completed":
            print(json.dumps({"papers": task.result}))
        else:
            print(json.dumps({"error": str(task.result)}))
            sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)
