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
"A landlord may require a tenant to pay a rent deposit with respect to a tenancy if the landlord does so on or before entering into the tenancy agreement."
]
ids = [373]
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
if torch.backends.mps.is_available():
    device = torch.device("mps")
    
model_name = "jinaai/jina-embeddings-v2-base-en"
embed_model = SentenceTransformer(model_name, trust_remote_code=True, device=device)

from qa_chain.semantic_router.route import routes
from citation_embed.embed import get_embeddings


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    chroma_client = chromadb.PersistentClient(path=script_dir+"../../../../db_store/") # local persistent db
    collections = []
    
    for route in routes:
        collections.append(chroma_client.get_collection(name=route.name))
        
    # query_vector = get_embeddings([queries[0]], embed_model) # expects a list of strings

            
    for collection in collections:
        results = collection.get(
            where_document={'$contains': queries[0]}
        )
        
        if results['ids']:
            print(f"Results from collection {collection.name}:", results)

