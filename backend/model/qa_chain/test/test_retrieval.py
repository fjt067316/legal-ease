import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# weird import issues
import query_answer
# https://stackoverflow.com/questions/76958817/streamlit-your-system-has-an-unsupported-version-of-sqlite3-chroma-requires-sq
# __import__('pysqlite3')
# import sys
# sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import chromadb # this import must be after the magic stuff before

q = ["when can a landlord evict me?"]
a = ["A landlord may give a tenant notice of termination of their tenancy on any of the following grounds:", "A landlord may give a tenant notice of termination of the tenancy if the tenant, another occupant of the rental unit or a person whom the tenant permits in the residential complex"]

queries = [
    # "what is a landlord allowed to put in a lease agreement?\n",
    # "what are the contents of a lease agreement\n",
    "am I allowed a pet?",
    "when can a landlord enter my unit?"
    # "how can I end my lease early?",
]

def score_query(query, citations):
    '''
        Returns the number of correct citations out of the total returned citations
    '''
    pass

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    chroma_client = chromadb.PersistentClient(path=script_dir+"../../../../db_store/") # local persistent db

    for query in queries:
        
        citations, distances = query_answer.retrieve_citations(query, chroma_client)
        scores = query_answer.get_ranks(query, citations)
        # print(citations)

        print(f"{query}\n")
        for score, citation, distance in zip(scores, citations, distances):
            print(f"{score} {distance} {citation}\n")
    