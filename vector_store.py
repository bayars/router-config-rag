"""Vector store for semantic search using Nomic embeddings via Ollama."""

import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings
from typing import List, Dict
import ollama


class OllamaEmbeddingFunction(EmbeddingFunction):
    """Custom embedding function using Ollama with Nomic model."""

    def __init__(self, model_name: str = "nomic-embed-text"):
        """
        Initialize Ollama embedding function.

        Args:
            model_name: Name of the Ollama embedding model
        """
        self.model_name = model_name

    def __call__(self, input: Documents) -> Embeddings:
        """
        Generate embeddings for input documents.

        Args:
            input: List of documents to embed

        Returns:
            List of embeddings
        """
        embeddings = []
        for text in input:
            response = ollama.embeddings(model=self.model_name, prompt=text)
            embeddings.append(response['embedding'])
        return embeddings


class VectorStore:
    """Manages embeddings and similarity search using ChromaDB and Nomic embeddings via Ollama."""

    def __init__(self, collection_name: str = "srlinux_docs", persist_directory: str = "./chroma_db",
                 embedding_model: str = "nomic-embed-text"):
        """
        Initialize vector store with Nomic embeddings via Ollama.

        Args:
            collection_name: Name of the ChromaDB collection
            persist_directory: Directory to persist the database
            embedding_model: Ollama embedding model name
        """
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        self.embedding_model = embedding_model

        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(path=persist_directory)

        # Use Ollama Nomic embedding model
        self.embedding_function = OllamaEmbeddingFunction(model_name=embedding_model)

        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_function
        )

    def add_documents(self, chunks: List[Dict[str, str]]):
        """
        Add document chunks to the vector store.

        Args:
            chunks: List of document chunks with text and metadata
        """
        documents = [chunk["text"] for chunk in chunks]
        ids = [chunk["id"] for chunk in chunks]
        metadatas = [
            {
                "start_pos": chunk["start_pos"],
                "end_pos": chunk["end_pos"],
                "source": chunk.get("source", "unknown")
            }
            for chunk in chunks
        ]

        # Add to collection in batches to avoid memory issues
        batch_size = 100
        for i in range(0, len(documents), batch_size):
            batch_docs = documents[i:i + batch_size]
            batch_ids = ids[i:i + batch_size]
            batch_metadata = metadatas[i:i + batch_size]

            self.collection.add(
                documents=batch_docs,
                ids=batch_ids,
                metadatas=batch_metadata
            )
            print(f"Added batch {i // batch_size + 1}/{(len(documents) - 1) // batch_size + 1}")

        print(f"Added {len(documents)} documents to vector store")

    def search(self, query: str, n_results: int = 5) -> List[Dict]:
        """
        Search for relevant documents.

        Args:
            query: Search query
            n_results: Number of results to return

        Returns:
            List of relevant document chunks with metadata
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )

        # Format results
        formatted_results = []
        for i in range(len(results['documents'][0])):
            formatted_results.append({
                "text": results['documents'][0][i],
                "metadata": results['metadatas'][0][i],
                "distance": results['distances'][0][i] if 'distances' in results else None
            })

        return formatted_results

    def count(self) -> int:
        """Return the number of documents in the collection."""
        return self.collection.count()

    def clear(self):
        """Clear all documents from the collection."""
        self.client.delete_collection(name=self.collection_name)
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            embedding_function=self.embedding_function
        )
