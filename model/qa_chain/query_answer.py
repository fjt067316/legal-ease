import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from citation_embed.embed import get_embeddings

'''
Takes in the entire user query and will retrieve the citations and create the prompt for the model
'''
def query_answer(query, db_client):
    pass
    
'''
Takes in the original user query and returns citations

TODO
    - dynamics citations returned
'''
def retrieve_citations(query, db_client):
    try:
        collection = db_client.get_collection(name="rta_full")
    except:
        print("Collection 'rta_full' does not exist.")
        return []

    query_vector = get_embeddings(query)
    '''
    collection.query(
        query_embeddings=[[11.1, 12.1, 13.1],[1.1, 2.3, 3.2], ...],
        n_results=10,
        where={"metadata_field": "is_equal_to_this"},
        where_document={"$contains":"search_string"}
    )
    '''
    results = collection.query(
        query_embeddings=query_vector[0],
        n_results=5  # Number of results temporarily
    )

    citations = [result for result in results['documents'][0]]
    
    return citations, results['distances'][0]