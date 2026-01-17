# RAG Retrieval Evaluation Harness

## What This Example Demonstrates

This repository provides a **minimal, runnable reference** for evaluating *retrieval behavior* in Retrieval-Augmented Generation (RAG) systems.

Most RAG examples focus on whether the system produces an answer.  
This example focuses on a prior question:

> **Did the system retrieve the right evidence in the first place?**

The goal is to make retrieval failures *observable* before changing chunking, reranking, or generation logic.

---

## Why Retrieval Evaluation Matters

When a RAG system refuses to answer or hallucinates, the root cause is often unclear.  
Common explanations include:

- the answer is missing from the corpus
- retrieval failed to surface relevant content
- relevant content exists but is ranked too low
- generation was starved of evidence

Without measuring retrieval behavior directly, these cases are indistinguishable.

This example isolates retrieval and provides simple, human-grounded diagnostics to answer those questions.

## What This Example Is (and Is Not)

This example:
- evaluates retrieval behavior only
- uses human-labeled relevant chunks
- inspects retrieval depth beyond Top-K

This example does NOT:
- optimize embeddings or ranking
- evaluate answer correctness
- claim general performance conclusions

## How It Works (High Level)

1. Documents are chunked using a fixed strategy
2. Each chunk is embedded and stored
3. Queries are executed against the vector store
4. Retrieved chunks are logged at multiple depths
5. Retrieval results are compared against human-labeled relevant chunks

## How to Run

```bash
pip install -r requirements.txt
python app.py --run-retrieval-eval
```

Outputs are written to data/results_and_summaries/.

