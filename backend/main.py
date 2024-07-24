from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from model.qa_chain.query_answer import retrieve_citations, get_ranks
import chromadb
import os


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

def process_query(query):
    citations, distances = retrieve_citations(query, chroma_client)
    scores = get_ranks(query, citations)
    return citations, scores, distances

@app.post("/api/userQuery")
async def user_query(query: Query):
    try:
        citations, scores,distances = process_query(query.query)
        print(f"{query.query}\n")
        print(f"{citations, scores, distances }\n")
        return {"response": f"Response to the query: {citations}"}
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


