from tqdm import tqdm

'''
The embeddings are generated from rta_penis which has the same placement of the PENIS keyword as the rta file
however it has changed wording to allow for better semantic encoding of the document sections
'''

'''
Utility functions for reading and chunking doc
'''
import docx
import unicodedata
import re

def clean_text(text):
    # pattern = r'\d{4}, c\. \d+, .*?\. \d+, s\. \d+'
    # text = re.sub(pattern, '', text)
    # Normalize the text to NFC form
    text = unicodedata.normalize('NFC', text)
    
    # Replace non-printable characters with a space
    cleaned_text = ''.join(c if c.isprintable() else ' ' for c in text)
    
    # Remove extra whitespace
    cleaned_text = ' '.join(cleaned_text.split())
    
    return cleaned_text

def read_docx(file_path):
    doc = docx.Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    
    text = '\n'.join(full_text)
    cleaned_text = clean_text(text)
    
    return cleaned_text


def chunk_text(text):
    # Split the text using the delimiter
    chunks = text.split("PENIS")
    
    # Strip leading and trailing whitespaces from each chunk
    chunks = [chunk.strip() for chunk in chunks]
    
    return chunks

'''
Generate embeddings for text chunks
'''
from sentence_transformers import SentenceTransformer

def get_embeddings(text_chunks):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    model_name = "infgrad/stella_en_400M_v5" # "jinaai/jina-embeddings-v2-base-en"
    local_directory = script_dir + "/saved_models/stella_en_400M_v5" # "/saved_models/jina-v2"
    
    # Check if the model is saved locally
    if not os.path.exists(local_directory):
        os.makedirs(local_directory)
        # Download and save the model
        model = SentenceTransformer(model_name, trust_remote_code=True, device="cpu")
        model.save(local_directory)
    else:
        # Load the model from local directory
        model = SentenceTransformer(local_directory)
    
    # Set maximum sequence length
    model.max_seq_length = 1024
    
    # Generate embeddings
    embeddings = []
    
    # Process text chunks with tqdm for progress bar
    for chunk in tqdm(text_chunks, desc="Embedding chunks"): # progress bar with tqdm
        # Generate embeddings for each chunk
        embeddings.append(model.encode(chunk).tolist())
    
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
    embedding_text = '/rta_penis_wording_mod.docx'#'/rta/rta_mod.docx'
    citation_text = '/rta_mod_new.docx'#'/rta/rta_penis.docx'
    print(script_dir)
    embed_path = script_dir + embedding_text
    original_path = script_dir + citation_text
    
    output_json_path = '../embeddings.json'
    text_mod = read_docx(embed_path)
    text_orig = read_docx(original_path)

    text_chunks_mod = chunk_text(text_mod)
    text_chunks_orig = chunk_text(text_orig)
    
    # output_file = "chunked_text_output.txt"

    # with open(output_file, 'w', encoding='utf-8') as file:
    #     for chunk_mod, chunk_orig in zip(text_chunks_mod, text_chunks_orig):
    #         file.write(chunk_mod[:200] + '\n')
    #         file.write(chunk_orig[:200] + '\n\n')
    
    # print(f"{len(text_chunks_mod)} == {len(text_chunks_orig)}")
    
    embeddings = get_embeddings(text_chunks_mod)
    save_embeddings_to_json(embeddings, text_chunks_orig, output_json_path)  