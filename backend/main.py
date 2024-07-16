from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
import chromadb
import query_answer  # Ensure this is correctly imported import must be after the magic stuff before

app = FastAPI()

class Query(BaseModel):
    query: str

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to restrict origins as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def process_user_query(query_text: str):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    chroma_client = chromadb.PersistentClient(path=os.path.join(script_dir, "../../../db_store/"))  # local persistent db
    citations, distances = query_answer.retrieve_citations(query_text, chroma_client)
    scores = query_answer.get_ranks(query_text, citations)
    response_data = [
        {"score": score, "distance": distance, "citation": citation}
        for score, citation, distance in zip(scores, citations, distances)
    ]
    return response_data

@app.get("/api/status")
async def status():
    return {"status": "Backend is running!"}

@app.get("/api/generate-api-key")
async def generate_api_key_endpoint():
    api_key = "api-key-fake"  # replace with actual key generation logic
    return {"apiKey": api_key}

@app.post("/api/userQuery")
async def user_query(query: Query):
    try:
        response = process_user_query(query.query)
        return {"response": f"Response to the query: {response}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/validateLease")
async def validate_lease_endpoint(file: UploadFile = File(None), leaseText: str = None):
    try:
        lease_text = (await file.read()).decode() if file else leaseText
        if lease_text is None:
            raise HTTPException(status_code=400, detail="No lease text provided")
        details = lease_text  # replace with actual lease validation logic
        return {"details": f"Validated lease text: {details}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/log")
async def log_query(query: Query):
    return {"response": f"thanks for logging : {query.query}"}

@app.post("/api/feedback")
async def feedback_query(query: Query):
    return {"response": f"feedback response to : {query.query}"}


