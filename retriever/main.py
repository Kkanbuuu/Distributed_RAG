from fastapi import FastAPI
from pydantic import BaseModel
from retriever import SimpleRetriever

class QueryRequest(BaseModel):
    query_text: str
    top_k: int = 5

app = FastAPI()
retriever = SimpleRetriever(data_dir='data')

@app.get("/")
def root():
    return {"message": "Simple Retriever is running!"}

@app.get("/load_data")
def load_data():
    retriever._load_data()
    return {"message": "Data loaded successfully.", "num_documents": len(retriever.documents)}

@app.post("/query")
def query(req: QueryRequest):
    results = retriever.query(req.query_text, top_k=req.top_k)
    return {"query": req.query_text, "results": results}