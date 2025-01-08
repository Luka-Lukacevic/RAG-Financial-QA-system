from config.config import *
from data.data_handler import DataHandler
from storage_handler import StorageHandler

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "rag-question-answering-system-80cff12c214a.json"


def run_data_pipeline():
    data_handler = DataHandler(api_key=SEC_API_KEY)
    storage_handler = StorageHandler(project_id=GCP_PROJECT_ID, bucket_name=GCP_BUCKET_NAME)

    companies = ["AAPL", "MSFT", "GOOG", "AMZN", "META"]
    all_chunks, all_metadata = [], []

    for ticker in companies:
        filings = data_handler.get_latest_filings(ticker)
        for filing in filings:
            content = data_handler.extract_filing_content(filing)
            if content:
                chunks = data_handler.chunk_document(content["page_content"])
                all_chunks.extend(chunks)
                all_metadata.extend([content["metadata"]] * len(chunks))

    # Save chunks to GCS
    for i, chunk in enumerate(all_chunks):
        save_path = f"{all_metadata[i]['company_name']}/chunks/{all_metadata[i]['date']}_{i}.txt"
        storage_handler.upload_to_gcs(chunk, all_metadata[i], save_path)
        # save_path = f"chunks/{i}.txt"
        # storage_handler.upload_to_gcs(chunk, all_metadata[i], save_path)


if __name__ == "__main__":
    run_data_pipeline()