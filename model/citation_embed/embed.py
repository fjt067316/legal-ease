from tqdm import tqdm
import docx
from transformers import AutoTokenizer, AutoModel
import torch

'''
The embeddings are generated from rta_penis which has the same placement of the PENIS keyword as the rta file
however it has changed wording to allow for better semantic encoding of the document sections
'''

'''
Utility functions for reading and chunking doc
'''
def read_docx(file_path):
    doc = docx.Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)


def chunk_text(text):
    # Split the text using the delimiter
    chunks = text.split("PENIS")
    
    # Strip leading and trailing whitespaces from each chunk
    chunks = [chunk.strip() for chunk in chunks]
    
    return chunks

'''
Generate embeddings for text chunks
'''
def get_embeddings(text_chunks):
    model_name = 'bert-base-uncased'
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
    
    embeddings = []
    for chunk in tqdm(text_chunks, desc="Processing chunks"): # progress bar with tqdm
        inputs = tokenizer(chunk, return_tensors='pt', truncation=True, padding=True)
        outputs = model(**inputs)
        embeddings.append(outputs.last_hidden_state.mean(dim=1).detach().tolist())
    return embeddings

'''
Save results
'''
import json

def save_embeddings_to_json(embeddings, text_chunks, file_path):
    embedding_dict = {}
    for embedding, text in zip(embeddings, text_chunks):
        # Convert the numpy array to a list and then to a string to use as a JSON key
        embedding_key = json.dumps(embedding)
        embedding_dict[embedding_key] = text
    
    with open(file_path, 'w') as f:
        json.dump(embedding_dict, f, indent=4)
        
'''
Main

The keyword PENIS is used to denote citation sections in the rta

Use rta_penis for the actual unmodified citations and rta_mod for the modified wording citations used for 
generating embeddings
'''
import os

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    embedding_text = '/rta/rta_mod.docx'
    citation_text = '/rta/rta_penis.docx'
    print(script_dir)
    embed_path = script_dir + embedding_text
    original_path = script_dir + citation_text
    
    output_json_path = '../embeddings.json'
    text_mod = read_docx(embed_path)
    text_orig = read_docx(original_path)

    text_chunks_mod = chunk_text(text_mod)
    text_chunks_orig = chunk_text(text_orig)

    embeddings = get_embeddings(text_chunks_mod)
    save_embeddings_to_json(embeddings, text_chunks_orig, output_json_path)  