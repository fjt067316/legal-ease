import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from citation_embed.embed import get_embeddings

'''
Takes in the entire user query and will retrieve the citations and create the prompt for the model
'''

import torch
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

access_token = os.getenv('OPENAI_API_KEY')

def query_answer(query, db_client, model, tokenizer, embedding_model):
    # retrieve citations
    # citations = db_client.get_citations(query)  # This is a placeholder; the actual implementation may vary
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    if torch.backends.mps.is_available():
        device = torch.device("mps")
    max_new_tokens = 150


    citations, _, _, _ = retrieve_citations(query, db_client, embedding_model)
    citations_formatted = "\n".join(f"{i+1}. {citation}" for i, citation in enumerate(citations))
    print(f"citations: {citations_formatted}")

    # Step 2: Create the prompt by combining the query and the retrieved citation info
    prompt = f"""
You're a logical reasoning assistant here to answer a question.
Given a user's question and relevent citations, respond to the user's question while referencing the citations.
If none of the citations answer the question, then say you don't know.
Keep your answer concise and to the point. Reference citations like so (1).
Don't type out any other questions or irrelevent text to the users question after completing your answer.
User Question: {query}
Citations: {citations_formatted}
Answer: """
    
    # print("tokenizing")
    # inputs = tokenizer(prompt, return_tensors="pt").to(device)
    # print("generating")
    # outputs = model.generate(**inputs, max_new_tokens=max_new_tokens, repetition_penalty=1.05)

    # # Step 6: Decode the response
    # answer = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # return answer[len(prompt):], citations
    # msg = "test resp"
    # return msg, citations
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=500,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    # print(citations_formatted)
    # print(completion.choices[0].message.content)
    
    return completion.choices[0].message.content, citations


def lease_answer(lease_data):
    prompt = f"""
You're a logical reasoning assistant here to answer a question.
Given a user's lease information, identify any clauses that may be illegal, and respond in the form of a question from the tenant's perspective.
For example, if a clause in a user's lease states that the tenant are not allowed to have pets, you should respond with "Can I have pets?", or "Can a landlord ban pets?"
Your responses should only include questions. They should be concise and straight to the point.
Include at most one question. If there is more than one illegal clause, choose the one that is the most relevant or have the most severe monetary consequence.
If there are no blatantly illegal clauses, or if the lease is the Ontario Residential Tenancy Agreement (Standard Form of Lease), immediately return "No illegal clauses found."
Do not hallucinate illegal clauses if you are not sure. Only identify clauses that are obviously illegal. 
User Lease: {lease_data}
Answer: """

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=500,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return completion.choices[0].message.content

'''
Re-Ranker takes user query and citations and generates a relevance score for them
higher score is better
'''
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

lower distance better
high (more positive) score better
'''
def filter_citations(query, citations, distances, score_threshold=-3, distance_threshold=0.4):
       # Filter based on the distance threshold
    filtered_citations_distances = [(citation, distance) for citation, distance in zip(citations, distances) if distance <= distance_threshold]
    
    if not filtered_citations_distances:
        return [], [], []
    
    # Unzip filtered results
    filtered_citations, filtered_distances = zip(*filtered_citations_distances) if filtered_citations_distances else ([], [])
    
    # Compute scores for the filtered citations
    scores = get_ranks(query, filtered_citations)
    
    # Combine citations, distances, and scores into a single list of tuples
    filtered_combined = [(citation, distance, score) for citation, distance, score in zip(citations, distances, scores) if score >= score_threshold]
    # Filter based on the threshold
    # filtered_combined = [(citation, distance, score) for citation, distance, score in combined ]
    
    # Sort by score in descending order
    filtered_combined.sort(key=lambda x: x[2], reverse=True)
    
    # Unzip the sorted results
    filtered_citations, filtered_distances, scores = zip(*filtered_combined) if filtered_combined else ([], [], [])
    return list(filtered_citations), list(filtered_distances), list(scores)


'''
Takes in the original user query and returns citations

TODO
    - handle searching entire rta if no collections exist
'''
from qa_chain.semantic_router.route import identify_collections, routes

def retrieve_citations(query, db_client, embedding_model):
    print("indentifying collections")
    names, scores = identify_collections(query)
    print("retrieving citaitons")
    try:
        collections = []
        for name in names:
            collections.append(db_client.get_collection(name=name))
    except:
        print("No Collections found searching entire rta")
        collections = []
        for route in routes:
            collections.append(db_client.get_collection(name=route.name))
    print("query embedding")
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
    all_ids = []
    
    print("citation filtering")
    for collection in collections:
        results = collection.query(
            query_embeddings=query_vector,
            n_results=4,  # Number of results temporarily'
            # where_document={'$contains': "pet"}
        )
        
        # print(results)
        
        ids = results['ids'][0]

        citations, distances, scores = filter_citations(query, results['documents'][0], results['distances'][0])

        # extend all_citations and all_distances with the current iteration's citations and distances
        all_citations.extend(citations)
        all_distances.extend(distances)
        all_scores.extend(scores)
        all_ids.extend(ids)
    
    # sort citations based on score
    combined_all = list(zip(all_citations, all_distances, all_scores, all_ids))
    combined_all.sort(key=lambda x: x[2], reverse=True)
    all_citations, all_distances, all_scores, all_ids = zip(*combined_all) if combined_all else ([], [], [], [])

    # print(results)
    # return results['documents'][0], results['distances'][0]
    return list(all_citations), list(all_distances), list(all_scores), list(all_ids)