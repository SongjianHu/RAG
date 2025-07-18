from fastapi import FastAPI
from api.routers import qa

app = FastAPI(title="RAG竞赛问答API")

app.include_router(qa.router, prefix="/qa", tags=["QA"])

@app.get("/ping")
def ping():
    return {"msg": "pong"} 