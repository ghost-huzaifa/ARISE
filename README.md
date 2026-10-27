# ARISE: Autonomous Research, Inference, Synthesis, and Exploration

[![Next.js](https://img.shields.io/badge/Frontend-Next.js%2014-black?logo=next.js)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Cross-Encoder](https://img.shields.io/badge/Re--ranking-Cross--Encoder%20(MiniLM)-blueviolet)](https://huggingface.co/cross-encoder/ms-marco-MiniLM-L-6-v2)
[![Corpus](https://img.shields.io/badge/Federated%20Sources-arXiv%20%2B%20OpenAlex-orange)](https://openalex.org/)

**ARISE** is an advanced AI research paper discovery and synthesis engine. It bridges the gap between raw keyword search and semantic academic literature discovery by unifying **federated multi-source ingestion** (arXiv preprints + OpenAlex peer-reviewed journals) with **dense cross-encoder neural re-ranking**.

---

## 🚀 Key Architectural Upgrades

- **Federated Ingestion Engine**: Dynamically queries arXiv and OpenAlex across 250M+ scholarly works, automatically extracting abstracts, peer-reviewed publication metadata, and citation statistics.
- **Deep Semantic Keyphrase Extraction**: Employs `KeyBERT` to isolate topical candidate keywords from natural language prompts without keyword drift.
- **Neural Cross-Encoder Re-Ranking**: Deploys a local `cross-encoder/ms-marco-MiniLM-L-6-v2` with hardware acceleration (Apple Silicon MPS / CUDA / CPU) to compute joint cross-attention between user query intent and candidate abstracts.
- **Relevance Confidence Scoring**: Normalizes raw logit cross-attention scores into calibrated matching percentages ($0\text{--}100\%$) displayed directly on paper cards.
- **Modern Researcher UI**: Next.js 14 interface featuring citation badges, source tags, full abstract modal dialogs, and external paper links.

---

## 🛠️ Architecture Flow

```
[User Natural Query / Research Question]
                  │
                  ▼
        [KeyBERT Extraction]
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
 [arXiv Atom API]    [OpenAlex Graph API]
 (Preprints)         (Peer-Reviewed)
        └─────────┬─────────┘
                  ▼
      [Candidate Pool Union]
                  │
                  ▼
 [Cross-Encoder Neural Re-Ranker]
 (Joint Query-Abstract Attention on MPS)
                  │
                  ▼
[Ranked Papers with Match % & Citations]
```

---

## 📦 Getting Started

### Prerequisites

- Node.js 18+ and npm/yarn
- Python 3.10+

### Step 1: Clone Repository

```bash
git clone https://github.com/ghost-huzaifa/ARISE.git
cd ARISE
```

### Step 2: Set Up Python Backend

```bash
cd server
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install scipy==1.13.1  # Recommended for macOS Apple Silicon
```

Start the FastAPI backend:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
API docs available at: `http://localhost:8000/docs`

### Step 3: Set Up Next.js Frontend

In a separate terminal:
```bash
cd ARISE
npm install
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## 📊 Evaluation & Verification

ARISE includes a reproducible benchmark suite under [`evaluation/`](file:///Users/macbookpro/dev/ARISE/evaluation/) measuring Precision@K, NDCG@K, and MRR across 30 standard academic research queries.

To re-run the benchmark:
```bash
./server/venv/bin/python3 evaluation/run_benchmark.py
```
Evaluation report is saved to [`evaluation/BENCHMARK_REPORT.md`](file:///Users/macbookpro/dev/ARISE/evaluation/BENCHMARK_REPORT.md).
