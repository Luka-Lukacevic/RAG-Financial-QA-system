from google.cloud import storage


class StorageHandler:
    def __init__(self, project_id, bucket_name):
        self.client = storage.Client(project=project_id)
        if self.client.bucket(bucket_name).exists():
            self.bucket = self.client.get_bucket(bucket_name)

    def upload_to_gcs(self, content, metadata, save_path):
        blob = self.bucket.blob(save_path)
        blob.upload_from_string(content, timeout=300)
        blob.metadata = metadata
        blob.patch()
        print(f"Uploaded: {save_path}")
