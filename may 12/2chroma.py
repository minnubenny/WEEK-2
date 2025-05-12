import chromadb
from chromadb.config import Settings

# Create a Chroma client using default (in-memory) settings
client = chromadb.Client(Settings())

# Create or get a collection
collection = client.get_or_create_collection(name="my_collection")

# Add some documents with IDs and optional metadata
collection.add(
    documents=["Artificial Intelligence is the simulation of human intelligence.",
               "Machine Learning is a subset of AI focused on learning from data."],
    metadatas=[{"category": "AI"}, {"category": "ML"}],
    ids=["doc1", "doc2"]
)

# Query the database for similar content
results = collection.query(
    query_texts=["What is AI?"],  # Your search input
    n_results=1  # Number of results to return
)

print("Query Results:", results)
