import chromadb

#  NEW WAY: create persistent client directly
client = chromadb.PersistentClient(path="mydb")  # saves to "mydb" folder

# Create or get collection
collection = client.get_or_create_collection("my_notes")

# Add a document
collection.add(
    documents=["ChromaDB is a modern vector database."],
    ids=["1"]
)

print(" Document saved to disk!")
