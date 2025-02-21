import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# weird import issues
import query_answer
from dotenv import load_dotenv
load_dotenv()
use_pysqlite3_binary = os.getenv('unsupported_sqlite')

# https://stackoverflow.com/questions/76958817/streamlit-your-system-has-an-unsupported-version-of-sqlite3-chroma-requires-sq
if use_pysqlite3_binary:
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import chromadb # this import must be after the magic stuff before

queries = [
    # "what is a landlord allowed to put in a lease agreement?\n",
    # "what are the contents of a lease agreement\n",
    "am I allowed a pet?",
    "can my landlord evict me for a pet",
    "can a landlord reject me for having a cat?",
    # "can I have a girl over?",
    "can I end my lease early?"
    # "when can a landlord enter my unit?"
    # "how can I end my lease early?",
]

from dotenv import load_dotenv
from transformers import AutoModelForCausalLM, AutoTokenizer
from sentence_transformers import SentenceTransformer
import torch
# Load environment variables from .env file
load_dotenv()

# Get the Hugging Face API token
access_token = os.getenv('HUGGINGFACE_API_TOKEN')

if not access_token:
    raise ValueError("HUGGINGFACE_API_TOKEN not found in environment variables.")

model_id = "microsoft/Phi-3-mini-4k-instruct" # mistralai/Mixtral-8x7B-v0.1"

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
if torch.backends.mps.is_available():
    device = torch.device("mps")
tokenizer = AutoTokenizer.from_pretrained(model_id, token=access_token, trust_remote_code=True, torch_dtype=torch.float16, device_map = device, low_cpu_mem_usage=True) # , device_map = 'auto'
model = AutoModelForCausalLM.from_pretrained(model_id, token=access_token, trust_remote_code=True, torch_dtype=torch.float16, device_map = device, low_cpu_mem_usage=True)

model.to(device)
model_name = "jinaai/jina-embeddings-v2-base-en"
embed_model = SentenceTransformer(model_name, trust_remote_code=True, device=device)

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    chroma_client = chromadb.PersistentClient(path=script_dir+"../../../../db_store/") # local persistent db

    for query in queries:
        print("retrieving query")
        resp = query_answer.query_answer(query, chroma_client, model, tokenizer, embed_model)
        # print(citations)
        print(resp)
        # print(f"{query} : \n RESPONSE: {resp}\n")

        # print(f"len resp {len(resp)} resp: \n{resp}")
