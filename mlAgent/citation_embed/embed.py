from tqdm import tqdm
import docx
from transformers import AutoTokenizer, AutoModel
import torch

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
        embeddings.append(outputs.last_hidden_state.mean(dim=1).detach().numpy())
    return embeddings

'''
Save results
'''
import json

def save_embeddings_to_json(embeddings, text_chunks, file_path):
    embedding_dict = {}
    for embedding, text in zip(embeddings, text_chunks):
        # Convert the numpy array to a list and then to a string to use as a JSON key
        embedding_key = json.dumps(embedding.tolist())
        embedding_dict[embedding_key] = text
    
    with open(file_path, 'w') as f:
        json.dump(embedding_dict, f, indent=4)
        
'''
Main

The keyword PENIS is used to denote citation sections in the rta
'''
import os

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    relative_path = '/rta/rta_penis.docx'
    print(script_dir)
    file_path = script_dir + relative_path
    
    output_json_path = 'embeddings.json'
    text = read_docx(file_path)

    text_chunks = chunk_text(text)
    embeddings = get_embeddings(text_chunks)
    save_embeddings_to_json(embeddings, text_chunks, output_json_path)  