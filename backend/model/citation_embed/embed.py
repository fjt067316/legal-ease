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
import torch

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


def chunk_text(text, keyword):
    # Split the text using the delimiter
    chunks = text.split(keyword)

    # Strip leading and trailing whitespaces from each chunk
    chunks = [chunk.strip() for chunk in chunks]

    return chunks

'''
Generate embeddings for text chunks
'''
from sentence_transformers import SentenceTransformer

def get_embeddings(text_chunks, model=None):
    if not model:
        

        if not model:
            device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            if torch.backends.mps.is_available():
                device = torch.device("mps")
            
            model_name = "jinaai/jina-embeddings-v2-base-en"
            model = SentenceTransformer(model_name, trust_remote_code=True, device=device)

            # Set maximum sequence length
            # model.max_seq_length = 2048

    # Generate embeddings
    embeddings = []
    # Process text chunks with tqdm for progress bar
    for chunk in tqdm(text_chunks, desc="Embedding chunks"):  # progress bar with tqdm
    # Generate embeddings for each chunk
        try:
            with torch.no_grad():
                embedding = model.encode(chunk).tolist()
                embeddings.append(embedding)
        except IndexError as e:
            print(f"IndexError for chunk: {chunk}\nError: {e}")
            continue
        except Exception as e:
            print(f"Unexpected error for chunk: {chunk}\nError: {e}")
            continue

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
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
        json.dump(embedding_dict, f, indent=4)

'''
Main

The keyword PENIS is used to denote citation sections in the rta

Use rta_p for the actual unmodified citations and rta_mod for the modified wording citations used for
generating embeddings
'''
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from qa_chain.semantic_router.route import routes

if __name__ == "__main__":
    collection_names = [route.name for route in routes]

    script_dir = os.path.dirname(os.path.abspath(__file__))
    embedding_text = '/rta_embed.docx'#'/rta/rta_mod.docx'
    citation_text = '/rta_citation.docx'#'/rta/rta_p.docx'
    print(script_dir)
    embed_path = script_dir + embedding_text
    original_path = script_dir + citation_text

    text_mod = read_docx(embed_path)
    text_orig = read_docx(original_path)

    collections_mod = chunk_text(text_mod, "ALABAMA_TURKEY")
    collections_orig = chunk_text(text_orig, "ALABAMA_TURKEY")

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    if torch.backends.mps.is_available():
        device = torch.device("mps")
    script_dir = os.path.dirname(os.path.abspath(__file__))

    model_name = "jinaai/jina-embeddings-v2-base-en"
    local_directory = script_dir + "/saved_models/jinaai/jina-embeddings-v2-base-en"

    # Check if the model is saved locally
    if not os.path.exists(local_directory):
        os.makedirs(local_directory)
        # Download and save the model
        model = SentenceTransformer(model_name, trust_remote_code=True, device=device)
        model.save(local_directory)
    else:
        # Load the model from local directory
        model = SentenceTransformer(model_name, trust_remote_code=True, device=device)

    model.to(device)

    for i, name in enumerate(collection_names):
        # output_json_path = f'../embeddings/{name}_embeddings.json'
        output_json_path = os.path.join(script_dir, f'../embeddings/{name}_embeddings.json')
        collection_mod = collections_mod[i]
        collection_orig = collections_orig[i]
        text_chunks_mod = chunk_text(collection_mod, "PENIS")
        text_chunks_orig = chunk_text(collection_orig, "PENIS")

        # output_file = "chunked_text_output.txt"

        # with open(output_file, 'w+', encoding='utf-8') as file:
        #     for chunk_mod, chunk_orig in zip(text_chunks_mod, text_chunks_orig):
        #         file.write(chunk_mod[:200] + '\n')
        #         file.write(chunk_orig[:200] + '\n\n')

        print(f"{len(text_chunks_mod)} == {len(text_chunks_orig)}")

        embeddings = get_embeddings(text_chunks_mod, model=model)
        save_embeddings_to_json(embeddings, text_chunks_orig, output_json_path)