# ARISE 2.0 Search Relevance Benchmark Report

**Date:** 2026-10-25 23:50:19  
**Sample Size:** N = 30 research queries across 6 academic domains  
**Systems Compared:**
1. **ARISE 2.0 (New):** Federated Ingestion (arXiv + OpenAlex) + Neural Cross-Encoder Re-Ranker (`ms-marco-MiniLM-L-6-v2`)
2. **Google Scholar (Baseline):** Live Scholar academic search
3. **ARISE 1.0 (Legacy):** Unranked arXiv boolean keyword search

## 1. Executive Summary & Verification Findings

| Metric | ARISE 2.0 (Mean ± Std) | Google Scholar (Baseline) | Delta vs GS | Rel Gain vs GS (%) | ARISE 1.0 (Legacy) | Gain vs ARISE 1.0 (%) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **P@5** | **1.0000 ± 0.000** | 0.9933 ± 0.036 | +0.0067 | **+0.67%** | 1.0000 | **+0.00%** |
| **P@10** | **1.0000 ± 0.000** | 0.9400 ± 0.148 | +0.0600 | **+6.38%** | 0.9967 | **+0.33%** |
| **Strict_P@5** | **0.9800 ± 0.081** | 0.9733 ± 0.087 | +0.0067 | **+0.68%** | 0.9467 | **+3.52%** |
| **Strict_P@10** | **0.9700 ± 0.088** | 0.9167 ± 0.151 | +0.0533 | **+5.82%** | 0.8967 | **+8.18%** |
| **NDCG@5** | **0.9877 ± 0.050** | 0.9812 ± 0.073 | +0.0065 | **+0.67%** | 0.9740 | **+1.40%** |
| **NDCG@10** | **0.9953 ± 0.019** | 0.9908 ± 0.034 | +0.0045 | **+0.46%** | 0.9906 | **+0.48%** |
| **MRR** | **1.0000 ± 0.000** | 1.0000 ± 0.000 | +0.0000 | **+0.00%** | 1.0000 | **+0.00%** |

### Key Benchmark Insights

- **Strict Precision@5 (Direct Topic Focus):** ARISE 2.0 reaches `0.9800`, surpassing both ARISE 1.0 (`0.9467`) and Google Scholar (`0.9733`).
- **Precision@10 (Corpus Breadth & Recall):** Federated multi-source ingestion yields `1.0000` vs Google Scholar `0.9400` (`+6.38%` relative gain).
- **NDCG@10 (Ranking Quality):** Cross-encoder joint cross-attention improves NDCG@10 to `0.9953`.

## 2. Per-Query Breakdown (Top 30 Queries)

| ID | Domain | Query | ARISE 2.0 Strict P@5 | GS Strict P@5 | ARISE 2.0 NDCG@10 | GS NDCG@10 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Q01 | Natural Language Processing | Low-resource sequence labeling in Roman Urdu using multilingual BERT | 1.00 | 1.00 | 1.00 | 1.00 |
| Q02 | Natural Language Processing | Transformer sparse attention mechanisms for long context windows | 1.00 | 1.00 | 1.00 | 1.00 |
| Q03 | Natural Language Processing | Contrastive learning for sentence embeddings in semantic search | 1.00 | 1.00 | 1.00 | 1.00 |
| Q04 | Natural Language Processing | Aspect-based sentiment analysis with graph convolutional networks | 1.00 | 1.00 | 1.00 | 1.00 |
| Q05 | Natural Language Processing | Hallucination mitigation in retrieval-augmented generation models | 1.00 | 1.00 | 1.00 | 1.00 |
| Q06 | Computer Vision & Multimodal | Vision transformers for medical image segmentation | 1.00 | 1.00 | 1.00 | 1.00 |
| Q07 | Computer Vision & Multimodal | Zero-shot object detection using vision language models | 1.00 | 1.00 | 1.00 | 1.00 |
| Q08 | Computer Vision & Multimodal | Diffusion models for synthetic medical data generation | 1.00 | 1.00 | 1.00 | 1.00 |
| Q09 | Computer Vision & Multimodal | Self-supervised visual representation learning from video | 1.00 | 1.00 | 1.00 | 1.00 |
| Q10 | Computer Vision & Multimodal | Multimodal emotion recognition in conversational video | 1.00 | 1.00 | 1.00 | 1.00 |
| Q11 | Healthcare & Clinical Informatics | Automated SOAP note generation from patient provider clinical dialogue | 0.80 | 1.00 | 0.97 | 1.00 |
| Q12 | Healthcare & Clinical Informatics | Electronic health records clinical decision support using deep learning | 1.00 | 1.00 | 1.00 | 1.00 |
| Q13 | Healthcare & Clinical Informatics | Remote patient monitoring with early warning score prediction | 1.00 | 1.00 | 1.00 | 1.00 |
| Q14 | Healthcare & Clinical Informatics | FHIR standard interoperability for health data exchange and EHR integration | 1.00 | 1.00 | 1.00 | 1.00 |
| Q15 | Healthcare & Clinical Informatics | Federated learning for multi-hospital clinical prognosis without data sharing | 1.00 | 1.00 | 1.00 | 1.00 |
| Q16 | Multi-Agent Systems & Software Engineering | Multi-agent LLM systems for autonomous code generation and automated review | 1.00 | 1.00 | 1.00 | 1.00 |
| Q17 | Multi-Agent Systems & Software Engineering | Automated unit test generation using large language models | 1.00 | 1.00 | 1.00 | 1.00 |
| Q18 | Multi-Agent Systems & Software Engineering | Static analysis and vulnerability detection in smart contracts | 1.00 | 1.00 | 1.00 | 1.00 |
| Q19 | Multi-Agent Systems & Software Engineering | Architectural technical debt quantification and refactoring recommendations | 1.00 | 1.00 | 1.00 | 1.00 |
| Q20 | Multi-Agent Systems & Software Engineering | Self-healing distributed systems using reinforcement learning | 1.00 | 1.00 | 1.00 | 1.00 |
| Q21 | AI Security & Privacy | Adversarial attacks on large language models via prompt injection | 1.00 | 1.00 | 1.00 | 1.00 |
| Q22 | AI Security & Privacy | Differential privacy in machine learning parameter protection | 1.00 | 1.00 | 1.00 | 1.00 |
| Q23 | AI Security & Privacy | Membership inference attacks on diffusion generative models | 1.00 | 1.00 | 1.00 | 0.99 |
| Q24 | AI Security & Privacy | Watermarking generative AI text for provenance tracking and copyright protection | 1.00 | 1.00 | 1.00 | 1.00 |
| Q25 | AI Security & Privacy | Backdoor attack detection in deep neural network weights | 1.00 | 0.80 | 1.00 | 1.00 |
| Q26 | Information Retrieval & Search | Dense passage retrieval for open domain question answering | 1.00 | 1.00 | 1.00 | 1.00 |
| Q27 | Information Retrieval & Search | Keyphrase extraction from scientific documents using KeyBERT | 1.00 | 1.00 | 1.00 | 0.99 |
| Q28 | Information Retrieval & Search | Neural re-ranking models for scholarly search engines | 0.60 | 0.60 | 0.90 | 0.85 |
| Q29 | Information Retrieval & Search | Hybrid lexical and semantic search for domain specific corpora | 1.00 | 1.00 | 0.99 | 1.00 |
| Q30 | Information Retrieval & Search | Graph neural networks for academic citation recommendation | 1.00 | 0.80 | 1.00 | 0.89 |
