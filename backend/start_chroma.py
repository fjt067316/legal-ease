import json
import os

# https://stackoverflow.com/questions/76958817/streamlit-your-system-has-an-unsupported-version-of-sqlite3-chroma-requires-sq
from dotenv import load_dotenv
load_dotenv()
use_pysqlite3_binary = os.getenv('unsupported_sqlite')

# https://stackoverflow.com/questions/76958817/streamlit-your-system-has-an-unsupported-version-of-sqlite3-chroma-requires-sq
if use_pysqlite3_binary:
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import chromadb # this import must be after the magic stuff before
from model.qa_chain.semantic_router.route import routes
import shutil

'''
This file is responsible for deploying chromaDB instances 

https://cookbook.chromadb.dev/core/collections/#creating-a-collection
'''

class ChromaLocal:
    def __init__(self):
        '''
        Load data into chroma db
        https://docs.trychroma.com/guides
        '''
        # self.chroma_client = chromadb.Client()
        
        # imported routes from route.py
        collection_names = [route.name for route in routes]
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        db_store_path = os.path.join(script_dir, "db_store")
        
        if os.path.exists(db_store_path):
            shutil.rmtree(db_store_path)
            print(f"Deleted Chroma DB store at: {db_store_path}")
            
        self.chroma_client = chromadb.PersistentClient(path=script_dir+"/db_store/") # local persistent db
                
        for name in collection_names:
            
            collection = self.chroma_client.create_collection(name=name, metadata={"hnsw:space": "cosine"})
            embed_path = script_dir + f'/model/embeddings/{name}_embeddings.json'

            # read embeddings data
            with open(embed_path, 'r') as f:
                data = json.load(f)

            i = 0
            # store data in ChromaDB
            for key, value in data.items():
                vector = json.loads(key)
                collection.add(
                    embeddings=[vector],
                    metadatas=[{"citation": value}],
                    documents=[value],
                    ids=[str(i)]
                )
                i += 1
                


if __name__ == "__main__":
    chroma_instance = ChromaLocal()