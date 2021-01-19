from pydantic import BaseModel
import enum
from fastapi import Query

from models.author import Author

class Book(BaseModel):
    isbn: str
    name: str
    author: Author
    year: int