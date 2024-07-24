import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# weird import issues
import query_answer
from dotenv import load_dotenv
load_dotenv()
use_pysqlite3_binary = os.getenv('unsupported_sqlite')

# https://stackoverflow.com/questions/76958817/streamlit-your-system-has-an-unsupported-version-of-sqlite3-chroma-requires-sq
if use_pysqlite3_binary:
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import chromadb # this import must be after the magic stuff before

queries = [
    # "what is a landlord allowed to put in a lease agreement?\n",
    # "what are the contents of a lease agreement\n",
    "am I allowed a pet?",
    # "when can a landlord enter my unit?"
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
        print("retrieving query")
        resp = query_answer.query_answer(query, chroma_client)
        # print(citations)
        print(resp)
        # print(f"{query} : \n RESPONSE: {resp}\n")

        # print(f"len resp {len(resp)} resp: \n{resp}")
