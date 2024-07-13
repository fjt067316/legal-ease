import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# weird import issues
import query_answer
import chromadb

queries = [
    "what is a landlord allowed to put in a lease agreement?\n",
    "what are the contents of a lease agreement\n",
    "am I allowed pets?\n"
]

def score_query(query, citations):
    '''
        Returns the number of correct citations out of the total returned citations
    '''
    pass

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    chroma_client = chromadb.PersistentClient(path=script_dir+"../../../db_store/") # local persistent db
    
    for query in queries:
        citations, distances = query_answer.retrieve_citations(query, chroma_client)
        print(f"{query}\n")
        for citation, distance in zip(citations, distances):
            print(f"{distance} {citation}\n")
    