import time

from google.cloud import aiplatform
from langchain_google_vertexai import VectorSearchVectorStore, VertexAIEmbeddings


class IndexHandler:
    def __init__(self, project_id, region, bucket_name, dimensions):
        self.project_id = project_id
        self.region = region
        self.bucket_name = bucket_name
        self.dimensions = dimensions
        self.embeddings = VertexAIEmbeddings(model_name="textembedding-gecko@003")
        aiplatform.init(project=project_id, location=region)

    def find_existing_index(self):
        """
        Look for an existing index in the project and return the first one if found.
        Otherwise, return None.
        """
        matching_indexes = aiplatform.MatchingEngineIndex.list()
        for index in matching_indexes:
            # Optionally, you can set conditions here (e.g., check if the name contains certain keywords)
            print(f"Found index: {index.display_name} (Resource Name: {index.resource_name})")
            return index

        # If no matching index is found, return None
        print("No matching index found.")
        return None

    def deploy_index(self, texts, metadatas):
        # Step 1: Look for an existing index
        index = self.find_existing_index()

        # Step 2: Create a new index if no existing one is found
        if index is None:
            print("Creating new MatchingEngineIndex")
            index = aiplatform.MatchingEngineIndex.create_tree_ah_index(
                display_name="rag_index",
                dimensions=self.dimensions,
                distance_measure_type="DOT_PRODUCT_DISTANCE",
                approximate_neighbors_count=150
            )
            print(f"Created MatchingEngineIndex: {index.resource_name}")
        else:
            print(f"Reusing existing MatchingEngineIndex: {index.resource_name}")

        # Detect if the endpoint exists
        existing_endpoints = aiplatform.MatchingEngineIndexEndpoint.list()
        index_endpoint = None
        for endpoint in existing_endpoints:
            index_endpoint = endpoint
            print(f"Reusing existing MatchingEngineIndexEndpoint: {index_endpoint.resource_name}")
            break

        # If endpoint doesn't exist, create a new one
        if index_endpoint is None:
            print("Creating new MatchingEngineIndexEndpoint")
            index_endpoint = aiplatform.MatchingEngineIndexEndpoint.create(
                display_name="rag_index_endpoint",
                public_endpoint_enabled=True
            )
            print(f"Created MatchingEngineIndexEndpoint: {index_endpoint.resource_name}")

        # Check if the index is already deployed to the endpoint
        deployed = False
        for deployed_index in index_endpoint.deployed_indexes:
            if deployed_index.index == index.resource_name:
                print(f"Index {index.resource_name} is already deployed to endpoint {index_endpoint.resource_name}.")
                deployed = True
                break

        # If not deployed, deploy the index to the endpoint
        if not deployed:
            print("Deploying index to the endpoint...")
            deployed_index_id = "rag_deployed_index"

            deployment_operation = index_endpoint.deploy_index(
                index=index,
                deployed_index_id=deployed_index_id
            )
            print("Waiting for deployment to complete...")
            print(f"Deployed index {index.resource_name} to endpoint {index_endpoint.resource_name}.")

        # Initialize the VectorSearchVectorStore
        vector_store = VectorSearchVectorStore.from_components(
            project_id=self.project_id,
            region=self.region,
            gcs_bucket_name=self.bucket_name,
            embedding=self.embeddings,
            index_id=index.name,
            endpoint_id=index_endpoint.name
        )

        # Add data to the index in batches of 5000
        batch_size = 5000  # Optimized batch size
        for i in range(0, len(texts), batch_size):
            start_time = time.time()
            print(f"Processing batch {i // batch_size + 1} of {len(texts) // batch_size + 1}")
            vector_store.add_texts(texts[i:i + batch_size], metadatas[i:i + batch_size])
            print(f"Batch completed in {time.time() - start_time:.2f} seconds")
        return vector_store
