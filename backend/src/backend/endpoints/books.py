from fastapi import APIRouter

books = APIRouter()

@books.get("/books")
def getBooks(): 
    return "Libros obtenidos"