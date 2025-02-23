

doc_ids = ["1", "3"]  # Replace with the actual ID you want to search for

results = collection.get(ids=doc_ids)

# Display the citation along with the document ID
if results and "documents" in results and results["documents"]:
    print(f"Document ID: {doc_id}")
    print(f"Citation: {results['documents'][0]}")
else:
    print("No document found for the given ID.")