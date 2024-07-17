import json
import os

# https://stackoverflow.com/questions/76958817/streamlit-your-system-has-an-unsupported-version-of-sqlite3-chroma-requires-sq
# __import__('pysqlite3')
# import sys
# sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import chromadb # this import must be after the magic stuff before

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
        
        # must be the same names as in route.py
        collection_names = ["Exemptions_And_Introduction", "Tenancy_Agreement", "Responsibilities_Of_A_Landlord"]
        
        script_dir = os.path.dirname(os.path.abspath(__file__))

        self.chroma_client = chromadb.PersistentClient(path=script_dir+"/db_store/") # local persistent db

        for name in collection_names:
            
            collection = self.chroma_client.create_collection(name=name, metadata={"hnsw:space": "cosine"})
            embed_path = script_dir + f'/embeddings/{name}_embeddings.json'

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