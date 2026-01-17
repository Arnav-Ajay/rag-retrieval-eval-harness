# evaluation.py → PDF → chunks

from retriever import retrieve_similar_documents
import pandas as pd

# Retrieval evaluation
def run_retrieval_evaluation(args, vector_store, inspect_k=50):
    """
    Evaluate whether gold chunks are retrieved within inspection depth
    and generation-critical Top-K.
    """
    
    print("[INFO] Running retrieval evaluation...\n")

    questions_df = pd.read_csv(args.questions_csv)
    evaluation_results = []
    GENERATION_TOP_K = 4

    required_cols = {
        "question_id",
        "question_text",
        "gold_chunk_id",
        "gold_doc_id",
    }

    if not required_cols.issubset(questions_df.columns):
        raise ValueError(
            f"Questions CSV must contain columns: {required_cols}"
        )



    for _, row in questions_df.iterrows():
        question_id = row["question_id"]
        question_text = row["question_text"]
        gold_chunk_id = int(row["gold_chunk_id"])
        gold_doc_id = row["gold_doc_id"]

        results = retrieve_similar_documents(vector_store, question_text, top_k=inspect_k)
        
        retrieved_chunk_ids = [chunk_id for chunk_id, _, _, _ in results]
        retrieved_chunk_ids_str = "|".join(map(str, retrieved_chunk_ids))
        
        evaluation_results.append({
            "question_id": question_id,
            "question": question_text,
            "gold_chunk_id": gold_chunk_id,
            "gold_doc_id": gold_doc_id,
            "retrieved_chunk_ids": retrieved_chunk_ids_str,

        })

    # Save evaluation results to CSV
    eval_output_path = args.eval_output
    pd.DataFrame(evaluation_results).to_csv(eval_output_path, index=False)    
    print(f"[SUCCESS] Retrieval evaluation results saved to {eval_output_path}\n")