# app.py → glue + debug prints
import os
import argparse
from ingest import load_pdf, chunk_texts
from retriever import create_vector_store, retrieve_similar_documents
from evaluation import run_retrieval_evaluation
import csv

def export_chunks_csv(all_chunks, output_path):
    """
    Export chunk text and document provenance for inspection/debugging.
    """
    
    with open(output_path, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['chunk_id', 'doc_id', 'text']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for chunk_id, chunk_info in all_chunks.items():
            writer.writerow({
                'chunk_id': chunk_id,
                'doc_id': chunk_info['doc_id'],
                'text': chunk_info['text']
            })

    print(f"[SUCCESS] Chunks exported to: {output_path}")

def print_corpus_diagnostics(corpus_diagnostics, all_chunks):
    print("\n[INFO] Corpus Diagnostics:\n")
    
    for doc, chunk_count in corpus_diagnostics.items():
        print(f"Document: {doc} | Chunks: {chunk_count}")
            
    print(f"\nTotal chunks across corpus: {len(all_chunks)}\n")
    print("Chunk ID → Document ID mapping:")
    for chunk_id, chunk_info in all_chunks.items():
        print(f"Chunk ID: {chunk_id} | Document ID: {chunk_info['doc_id']}")
        
    print("\n[SUCCESS] Corpus Diagnostics Complete.\n")

def main():
    """
    Orchestrates corpus ingestion, chunking, retrieval indexing,
    and optional retrieval evaluation or diagnostics.
    """    
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf-dir", default=r"data/input_pdfs/", help="Directory containing input PDF documents.") # Path to directory containing PDFs
    
    parser.add_argument("--export-chunks", action="store_true", help="Export chunks to CSV for debugging")
    parser.add_argument("--chunks-csv", default=r"data/chunks_and_questions/chunks_output.csv", help="Path to chunks exported csv")

    parser.add_argument("--run-retrieval-eval", action="store_true", help="Run retrieval evaluation")
    parser.add_argument("--questions-csv", default=r"data/chunks_and_questions/question_input.csv", help="Path to questions csv")
    parser.add_argument("--eval-output", default=r"data/results_and_summaries/questions_retrieval_results.csv", help="output to output evaluation results")
    
    parser.add_argument("--corpus-diag", action="store_true", help="Print basic corpus diagnostics (chunk counts and ID mappings).")
    
    args = parser.parse_args()
    pdf_path = args.pdf_dir
    all_chunks = {}
    global_chunk_id = 0
    corpus_diagnostics = {}
    
    for filename in sorted(os.listdir(pdf_path)):
        if filename.endswith(".pdf"):
            pdf_text = load_pdf(os.path.join(pdf_path, filename))
            chunks = chunk_texts(pdf_text)
            corpus_diagnostics[filename] = len(chunks)
            for _, chunk_text in chunks.items():
                # Attach document provenance to each global chunk
                all_chunks[global_chunk_id] = {
                    "doc_id": filename,
                    "text": chunk_text
                }

                global_chunk_id += 1

                if global_chunk_id >= 1000:
                    print("⚠️ Chunk limit reached. Corpus truncated for controlled diagnostic evaluation.\n")
                    break
    
    if not all_chunks:
        raise RuntimeError("No PDF documents were ingested. Check --pdf-dir.")

    # Export chunks to CSV for debugging
    if args.export_chunks and args.chunks_csv:
        print("\n")
        export_chunks_csv(all_chunks, args.chunks_csv)

    # Corpus diagnostics
    if args.corpus_diag:
        print_corpus_diagnostics(corpus_diagnostics, all_chunks)

    vector_store = create_vector_store(all_chunks)
    # Retrieval evaluation placeholder
    if args.run_retrieval_eval:
        
        run_retrieval_evaluation(args, vector_store)
        return

if __name__ == "__main__":
    main()