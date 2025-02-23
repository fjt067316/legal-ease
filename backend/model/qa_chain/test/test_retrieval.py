import os, sys, torch
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# weird import issues
import query_answer
from sentence_transformers import SentenceTransformer

# https://stackoverflow.com/questions/76958817/streamlit-your-system-has-an-unsupported-version-of-sqlite3-chroma-requires-sq
# __import__('pysqlite3')
# import sys
# sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import chromadb # this import must be after the magic stuff before

queries = [
    # "what is a landlord allowed to put in a lease agreement?\n",
    # "what are the contents of a lease agreement\n",
    "am I allowed a pet?",
    "when can a landlord enter my unit?"
    # "how can I end my lease early?",
]

expected_citations = []

# also add expected rta chapter
test_queries = {
    "am I allowed a pet?" : [126], # indicies of expected citation
    "Can I be evicted for having an animal?": [373, 374, 375],
    "Can I be charged a security deposit?": [],
    "Can my landlord not use my rent deposit for last month rent?" : [1008],
    "Can I be charged a key deposit for a sublet?" : [674],
    "Can I be charged a key deposit by a landlord?" : [671],
    "Can I be charged a rent deposit?": [554],
    "Does my landlord have to pay my deposit back?" : [564],
    "Can the landlord use my deposit for last month rent?": [563], 
    "Does the landlord have to pay interest on my deposit?": [559],
    "How much can a rent deposit be?": [555],
}

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
if torch.backends.mps.is_available():
    device = torch.device("mps")

def score_query(query, citations):
    '''
        Returns the number of correct citations out of the total returned citations
    '''
    pass


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    chroma_client = chromadb.PersistentClient(path=script_dir+"../../../../db_store/") # local persistent db
    
    model_name = "jinaai/jina-embeddings-v2-base-en"
    embed_model = SentenceTransformer(model_name, trust_remote_code=True, device=device)

    for query in queries:

        citations, distances, scores, ids = query_answer.retrieve_citations(query, chroma_client, embed_model)
        # scores = query_answer.get_ranks(query, citations)
        # print(citations)

        print(f"{query}\n")
        for score, citation, distance, id in zip(scores, citations, distances, ids):
            print(f"{id} {score} {distance} {citation}\n")
