from fastapi import FastAPI
from app.routes import analyze
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AI Code Intelligence Platform")

app.include_router(analyze.router)

@app.get("/")
def home():
    return {"message": "Backend running 🚀"}



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# uvicorn app.main:app --reload