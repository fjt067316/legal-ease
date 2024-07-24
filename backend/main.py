from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from model.qa_chain.query_answer import query_answer
import os
from dotenv import load_dotenv
load_dotenv()
use_pysqlite3_binary = os.getenv('unsupported_sqlite')

# https://stackoverflow.com/questions/76958817/streamlit-your-system-has-an-unsupported-version-of-sqlite3-chroma-requires-sq
if use_pysqlite3_binary:
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import chromadb


app = FastAPI()
script_dir = os.path.dirname(os.path.abspath(__file__))
chroma_client = chromadb.PersistentClient(path=script_dir+"/db_store/") # local persistent db

class Query(BaseModel):
    query: str

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to restrict origins as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

"""
ML Setup
"""
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from sentence_transformers import SentenceTransformer

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Get the Hugging Face API token
access_token = os.getenv('HUGGINGFACE_API_TOKEN')

llm_model = "microsoft/Phi-3-mini-4k-instruct"  # Replace with the desired model
embedding_model_name = "jinaai/jina-embeddings-v2-base-en"

# @app.on_event("startup")
# async def load_model():
#   global model, tokenizer, embedding_model, chroma_client

# Download and save the model
tokenizer = AutoTokenizer.from_pretrained(llm_model, token=access_token, trust_remote_code=True, torch_dtype=torch.float16, device_map = device, low_cpu_mem_usage=True) # , device_map = 'auto'
model = AutoModelForCausalLM.from_pretrained(llm_model, token=access_token, trust_remote_code=True, torch_dtype=torch.float16, device_map = device, low_cpu_mem_usage=True)
embedding_model = SentenceTransformer(embedding_model_name, trust_remote_code=True, device=device)

model.to(device)
embedding_model.to(device)
script_dir = os.path.dirname(os.path.abspath(__file__))
# tokenizer = AutoTokenizer.from_pretrained(llm_model)
# model = AutoModelForCausalLM.from_pretrained(llm_model).to("cuda")

"""
API Routes
"""
@app.post("/api/userQuery")
async def user_query(query: Query):
    try:
        response, citations = query_answer(query.query, chroma_client, model, tokenizer, embedding_model)
        print(response)
        return {"response": response, "citations" : citations}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/status")
async def status():
    return {"status": "Backend is running!"}


# Not needed for demo
# @app.get("/api/generate-api-key")
# async def generate_api_key_endpoint():
#     api_key = "api-key-fake"  # replace with actual key generation logic
#     return {"apiKey": api_key}


# @app.post("/api/validateLease")
# async def validate_lease_endpoint(file: UploadFile = File(None), leaseText: str = None):
#     try:
#         lease_text = (await file.read()).decode() if file else leaseText
#         if lease_text is None:
#             raise HTTPException(status_code=400, detail="No lease text provided")
#         details = lease_text  # replace with actual lease validation logic
#         return {"details": f"Validated lease text: {details}"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.post("/api/log")
# async def log_query(query: Query):
#     return {"response": f"thanks for logging : {query.query}"}

# @app.post("/api/feedback")
# async def feedback_query(query: Query):
#     return {"response": f"feedback response to : {query.query}"}


