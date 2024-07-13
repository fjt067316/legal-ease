import chromadb
import json
import os

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
        
        script_dir = os.path.dirname(os.path.abspath(__file__))

        self.chroma_client = chromadb.PersistentClient(path=script_dir+"/db_store/") # local persistent db

        self.collection = self.chroma_client.get_or_create_collection(name="rta_full")
        embed_path = script_dir + '/embeddings.json'

        # read embeddings data
        with open(embed_path, 'r') as f:
            data = json.load(f)
        
        i = 0
        # store data in ChromaDB
        for key, value in data.items():
            vector = json.loads(key)
            self.collection.add(
                embeddings=[vector[0]],
                metadatas=[{"citation": value}],
                documents=[value],
                ids=[str(i)]
            )
            i += 1


if __name__ == "__main__":
    chroma_instance = ChromaLocal()