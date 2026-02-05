from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from AI-KIP Demo Environment"}

@app.get("/api/health")
def health_check():
    return {"status": "healthy"}
