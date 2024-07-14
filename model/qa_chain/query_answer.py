import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from citation_embed.embed import get_embeddings

'''
Takes in the entire user query and will retrieve the citations and create the prompt for the model
'''
def query_answer(query, db_client):
    pass
    
    

'''
Re-Ranker takes user query and citations and generates a relevance score for them
higher score is better
'''
from transformers import AutoTokenizer, AutoModel
from FlagEmbedding import FlagReranker

def get_ranks(query, citations):
    model_name = 'BAAI/bge-reranker-large'
    
    # Initialize FlagReranker
    reranker = FlagReranker(model_name, use_fp16=True)
    ranks = [ [query, citation] for citation in citations ]
    # Compute scores using FlagReranker
    scores = reranker.compute_score(ranks)
    
    if not isinstance(scores, list): # if its just a float convert to list of 1 item
        scores = [scores]
        
    return scores

'''
Filter citations based on ranking of another model
If citations is below threshold then discard
'''
def filter_citations(query, citations: tuple, distances, threshold=-9): # passing in distances is for debugging purposes and not needed
    # citations is a tuple of (citation, distance)
    scores = get_ranks(query, citations)
    
    # filter citations based on scores
    filtered_citations = [citation for citation, score in zip(citations, scores) if score >= threshold]
    filtered_distances = [distance for distance, score in zip(distances, scores) if score >= threshold]
    return filtered_citations, filtered_distances


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
    v1 = collection.get(["127"], include=['embeddings', 'documents', 'metadatas'])
    # print(v1)
    results = collection.query(
        query_embeddings=query_vector,
        n_results=30,  # Number of results temporarily'
        # where_document={'$contains': "pet"}
    )
    # print(results)
    citations, distances = filter_citations(query, results['documents'][0], results['distances'][0])
    return citations, distances