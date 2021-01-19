from pydantic import BaseModel
import enum
from fastapi import Query

#from models.book import Book si se importa book en author no se puede de nuevo importar author en book
from typing import List

class Author(BaseModel):
    name: str
    book: List[str]