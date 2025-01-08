import pickle

from google.cloud import storage

from config.config import *
from model.index_retrieval import IndexHandler
from model.qa_system import QASystem


def load_chunks_and_metadata_from_gcs(bucket_name, prefix="chunks/"):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blobs = bucket.list_blobs()  # Get all blobs, regardless of prefix

    chunks, metadatas = [], []
    for blob in blobs:
        # Check if "chunks/" is part of the path
        if "chunks/" in blob.name and blob.name.endswith(".txt"):  # Adjust file extension if needed
            content = blob.download_as_text()
            metadata = blob.metadata
            chunks.append(content)
            metadatas.append(metadata)

    return chunks, metadatas


def save_data_local(filename, all_chunks, all_metadata):
    """
    Save all_chunks and all_metadata as a serialized file.
    """
    with open(filename, 'wb') as file:
        pickle.dump({"chunks": all_chunks, "metadata": all_metadata}, file)
    print(f"Data saved to {filename}")


def interactive_chat(qa_system):
    print("\n--- Interactive Chat System ---")
    print("Type 'exit' to end the session.")

    while True:
        # Prompt for user input
        user_question = input("\nYour Question: ")

        # Exit condition
        if user_question.lower() in ["exit", "quit"]:
            print("Exiting chat. Goodbye!")
            break

        # Get the response
        try:
            answer = qa_system.ask_question(user_question)
            print(f"\nAnswer: {answer}")
        except Exception as e:
            print(f"Error processing your question: {e}")


def main():
    if "chunks_metadata.pkl" not in os.listdir():
        all_chunks, all_metadata = load_chunks_and_metadata_from_gcs(GCP_BUCKET_NAME)
        save_data_local("chunks_metadata.pkl", all_chunks, all_metadata)
    else:
        with open("chunks_metadata.pkl", 'rb') as file:
            data = pickle.load(file)
            all_chunks = data["chunks"]
            all_metadata = data["metadata"]


    print(f"Loaded {len(all_chunks)} chunks and {len(all_metadata)} metadata from GCS")

    index_handler = IndexHandler(
        project_id=GCP_PROJECT_ID,
        region=GCP_REGION,
        bucket_name=GCP_BUCKET_NAME,
        dimensions=ME_DIMENSIONS
    )

    # Deploy Index
    vector_store = index_handler.deploy_index(all_chunks, all_metadata)

    # Initialize QA System
    qa_system = QASystem(vector_store)

    # Start interactive chat
    interactive_chat(qa_system)


if __name__ == "__main__":
    main()
