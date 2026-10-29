from fastapi import FastAPI

app = FastAPI(title='BioChemVerse API')

@app.get('/health')
def health():
    return {'status': 'ok'}

