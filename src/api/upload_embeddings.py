"""
One-time script to upload embeddings to Azure AI Search index.

Usage:
    cd src
    python -m api.upload_embeddings

This script:
1. Creates the Azure Search index if it doesn't exist
2. Uploads embeddings from data/embeddings.csv to the index
"""
import asyncio
import os
from dotenv import load_dotenv
from azure.identity import AzureCliCredential
from azure.ai.inference.aio import EmbeddingsClient
from urllib.parse import urlparse

from .search_index_manager import SearchIndexManager


async def main():
    load_dotenv(override=True)

    # Get configuration from environment
    endpoint = os.environ.get('AZURE_AI_SEARCH_ENDPOINT')
    index_name = os.environ.get('AZURE_AI_SEARCH_INDEX_NAME', 'index_sample')
    embed_deployment = os.environ.get('AZURE_AI_EMBED_DEPLOYMENT_NAME', 'text-embedding-3-small')
    embed_dimensions = int(os.environ.get('AZURE_AI_EMBED_DIMENSIONS', '100'))
    project_endpoint = os.environ.get('AZURE_AI_PROJECT_ENDPOINT')

    if not endpoint:
        print("Error: AZURE_AI_SEARCH_ENDPOINT environment variable is not set")
        return

    if not project_endpoint:
        print("Error: AZURE_AI_PROJECT_ENDPOINT environment variable is not set")
        return

    print(f"Azure Search Endpoint: {endpoint}")
    print(f"Index Name: {index_name}")
    print(f"Embedding Model: {embed_deployment}")
    print(f"Dimensions: {embed_dimensions}")

    # Set up credentials
    tenant_id = os.getenv("AZURE_TENANT_ID")
    if tenant_id:
        azure_credential = AzureCliCredential(tenant_id=tenant_id)
    else:
        azure_credential = AzureCliCredential()

    # Create embeddings client
    inference_endpoint = f"https://{urlparse(project_endpoint).netloc}/models"
    embed_client = EmbeddingsClient(
        endpoint=inference_endpoint,
        credential=azure_credential,
        credential_scopes=["https://ai.azure.com/.default"],
    )

    # Create SearchIndexManager
    search_index_manager = SearchIndexManager(
        endpoint=endpoint,
        credential=azure_credential,
        index_name=index_name,
        dimensions=embed_dimensions,
        model=embed_deployment,
        embeddings_client=embed_client,
    )

    try:
        # Create Azure Search Index (if it does not yet exist)
        print(f"\nCreating index '{index_name}' if it doesn't exist...")
        await search_index_manager.ensure_index_created(vector_index_dimensions=embed_dimensions)
        print("Index ready.")

        # Check if index is empty
        if await search_index_manager.is_index_empty():
            # Upload embeddings to the index
            embeddings_path = os.path.join(os.path.dirname(__file__), 'data', 'embeddings.csv')
            print(f"\nUploading embeddings from {embeddings_path}...")
            await search_index_manager.upload_documents(embeddings_path)
            print("Embeddings uploaded successfully!")
        else:
            print("\nIndex already contains documents. Skipping upload.")
            print("To re-upload, delete the index first in Azure Portal.")
    finally:
        await search_index_manager.close()
        await embed_client.close()


if __name__ == "__main__":
    asyncio.run(main())
