# RAG Retrieval Evaluation Harness

This repository provides a **minimal, runnable reference** for evaluating *retrieval behavior* in Retrieval-Augmented Generation (RAG) systems.

Most RAG examples focus on whether the system produces an answer.  
This example focuses on an earlier and often unmeasured question:

> **Did the system retrieve the right evidence in the first place?**

The goal is to make retrieval failures *observable* before modifying chunking, reranking, or generation logic.

---

## Why Retrieval Evaluation Matters

When a RAG system refuses to answer or produces an incorrect response, the root cause is often unclear.  
Common explanations include:

- the answer is missing from the corpus
- retrieval failed to surface relevant content
- relevant content exists but is ranked too low
- generation was starved of evidence

Without measuring retrieval behavior directly, these cases are indistinguishable.

This example isolates retrieval and provides **simple, human-grounded diagnostics** to help determine where failures occur.

---

## What This Example Is (and Is Not)

### This example **does**:
- evaluate retrieval behavior in isolation
- use human-labeled relevant chunks
- inspect retrieval results beyond generation Top-K
- surface ranking depth and retrieval misses

### This example **does not**:
- optimize embeddings or ranking algorithms
- evaluate answer correctness
- use LLM-based grading
- claim general performance conclusions

---

## How It Works (High Level)

1. Documents are chunked using a fixed strategy
2. Each chunk is embedded and stored
3. Queries are executed against the vector store
4. Retrieved chunks are logged at multiple depths
5. Results are compared against human-labeled relevant chunks

No generation logic is required to observe retrieval behavior.

---

## How to Run

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```
---

### 2. Input PDFs and Chunking

Input PDFs are located in:

```
data/input_pdfs/
```

To inspect chunking output and document provenance:

```bash
python app.py --export-chunks
```

Chunks are exported to:

```
data/chunks_and_questions/chunks_output.csv
```

---

### 3. Evaluation Questions

Evaluation questions are manually created and stored in:

```
data/chunks_and_questions/question_input.csv
```

Each question is paired with a human-identified relevant chunk.

---

### 4. Run Retrieval Evaluation

```bash
python app.py --run-retrieval-eval
```

Evaluation results are written to:

```
data/results_and_summaries/
```

---

## Evaluation Outputs

The evaluation output CSV includes:

* `question_id`
* `gold_chunk_id`
* `gold_doc_id`
* `retrieved chunk IDs` (ordered by similarity)
* `rank of first relevant chunk` (manually entered)
* whether the relevant chunk appears in generation Top-K (manually entered)

These outputs make retrieval success and failure **explicit and inspectable**.

---

## Interpreting the Results

Common patterns you may observe:

* relevant chunks exist but are ranked below Top-K
* increasing inspection depth yields limited recovery
* retrieval failures explain generation refusal or hallucination

This example helps distinguish **retrieval starvation** from corpus absence.

---

## How to Extend This Example

This repository is intentionally minimal.

Possible extensions include:

* replacing the diagnostic embedding with a real model
* adding sparse or hybrid retrieval
* introducing reranking
* comparing retrieval strategies using the same evaluation harness

All improvements can be measured relative to the same baseline.

---

## Design Notes

* Retrieval logic is intentionally simple and transparent
* Embeddings are diagnostic, not production-grade
* No claims are made beyond observed artifacts
* Corpus diagnostics are optional and gated

The focus is **measurement before optimization**.

```

---