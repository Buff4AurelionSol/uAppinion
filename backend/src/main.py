from fastapi import FastAPI
from backend.endpoints.books import books

app = FastAPI()

app.include_router(books)



@app.get("/")
def read_root():
    return {"message": "API de uAppinnion funcionando"}