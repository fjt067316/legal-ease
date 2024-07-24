import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from citation_embed.embed import get_embeddings

'''
Takes in the entire user query and will retrieve the citations and create the prompt for the model
'''

import torch

def query_answer(query, db_client, model, tokenizer, embedding_model):
    # retrieve citations
    # citations = db_client.get_citations(query)  # This is a placeholder; the actual implementation may vary
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    max_new_tokens = 150


    citations, _ = retrieve_citations(query, db_client, embedding_model)
    citations_formatted = "\n".join(f"{i+1}. {citation}" for i, citation in enumerate(citations))
    print(citations_formatted)

    # Step 2: Create the prompt by combining the query and the retrieved citation info
    prompt = f"""
You're a legal assistant here to answer a question.
Given a user's question and relevent citations, respond to the user's question while referencing the citations.
If none of the citations answer the question, then say you don't know.
Keep your answer concise and to the point. Reference citations like so (1).
Don't type out any other questions or irrelevent text to the users question after completing your answer.
User Question: {query}
Citations: {citations_formatted}
Answer: """
    
    print("tokenizing")
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    print("generating")
    outputs = model.generate(**inputs, max_new_tokens=max_new_tokens, repetition_penalty=1.05)

    # Step 6: Decode the response
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return answer[len(prompt):]


'''
Re-Ranker takes user query and citations and generates a relevance score for them
higher score is better
'''
from FlagEmbedding import FlagReranker

def get_ranks(query, citations):
    model_name = 'BAAI/bge-reranker-large'
    if not citations:
        raise ValueError("Citations list is empty. Provide at least one citation.")
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

lower distance better
high (more positive) score better
'''
def filter_citations(query, citations, distances, score_threshold=-2.5, distance_threshold=0.4):
       # Filter based on the distance threshold
    filtered_citations_distances = [(citation, distance) for citation, distance in zip(citations, distances) if distance <= distance_threshold]
    
    # Unzip filtered results
    filtered_citations, filtered_distances = zip(*filtered_citations_distances) if filtered_citations_distances else ([], [])
    
    # Compute scores for the filtered citations
    scores = get_ranks(query, filtered_citations)
    
    # Combine citations, distances, and scores into a single list of tuples
    combined = [(citation, distance, score) for citation, distance, score in zip(citations, distances, scores)]
    
    # Filter based on the threshold
    filtered_combined = [(citation, distance, score) for citation, distance, score in combined if score >= score_threshold]
    
    # Sort by score in descending order
    # filtered_combined.sort(key=lambda x: x[2], reverse=True)
    
    # Unzip the sorted results
    filtered_citations, filtered_distances, scores = zip(*filtered_combined) if filtered_combined else ([], [], [])
    return list(filtered_citations), list(filtered_distances), list(scores)


'''
Takes in the original user query and returns citations

TODO
    - handle searching entire rta if no collections exist
'''
from qa_chain.semantic_router.route import identify_collections, routes

def retrieve_citations(query, db_client, embedding_model=None):
    names, scores = identify_collections(query)
    
    try:
        collections = []
        for name in names:
            collections.append(db_client.get_collection(name=name))
    except:
        print("No Collections found searching entire rta")
        collections = []
        for route in routes:
            collections.append(db_client.get_collection(name=route.name))

    query_vector = get_embeddings([query], embedding_model) # expects a list of strings
    '''
    collection.query(
        query_embeddings=[[11.1, 12.1, 13.1],[1.1, 2.3, 3.2], ...],
        n_results=10,
        where={"metadata_field": "is_equal_to_this"},
        where_document={"$contains":"search_string"}
    )
    '''
    # v1 = collection.get(["127"], include=['embeddings', 'documents', 'metadatas'])
    # print(v1)
    all_citations = []
    all_distances = []
    all_scores = []
    
    for collection in collections:
        results = collection.query(
            query_embeddings=query_vector,
            n_results=4,  # Number of results temporarily'
            # where_document={'$contains': "pet"}
        )

        citations, distances, scores = filter_citations(query, results['documents'][0], results['distances'][0])

        # extend all_citations and all_distances with the current iteration's citations and distances
        all_citations.extend(citations)
        all_distances.extend(distances)
        all_scores.extend(scores)
    
    # sort citations based on score
    combined_all = list(zip(all_citations, all_distances, all_scores))
    combined_all.sort(key=lambda x: x[2], reverse=True)
    all_citations, all_distances, all_scores = zip(*combined_all) if combined_all else ([], [], [])

    # print(results)
    # return results['documents'][0], results['distances'][0]
    return list(all_citations), list(all_distances)