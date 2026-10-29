from fastapi import FastAPI

app = FastAPI(title="BioChemVerse API")

@app.get("/health")
def health():
    return {"status": "ok"}
filePath">
C:\laragon\www\BioChemVerse\backend\python\main.py