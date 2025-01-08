import os

from dotenv import load_dotenv

load_dotenv()

SEC_API_KEY = os.getenv('SEC_API_KEY')
GCP_PROJECT_ID = os.getenv('PROJECT_ID')
GCP_REGION = os.getenv('REGION')
GCP_BUCKET_NAME = os.getenv('BUCKET_NAME')
ME_INDEX_NAME = f"{GCP_PROJECT_ID}-me-index"
ME_DIMENSIONS = 768
