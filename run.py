from fastapi import FastAPI, Body, Header, File
from models.user import User
from models.author import Author
from models.book import Book

from starlette.status import HTTP_201_CREATED

from starlette.responses import Response

app = FastAPI()


@app.post("/user", status_code=HTTP_201_CREATED)
async def post_user(user: User, x_custom: str = Header(...)):
    return {"request body": user, "request custom header": x_custom}

@app.get("/user")
async def get_user_validation(password: str = None):
    return {"parameter": password}


@app.get("/book/{isbn}", response_model = Book, response_model_exclude=["author"])
async def get_book_with_isbn(isbn: str):
    author_dict = {
        "name": "author1",
        "book": ["book1", "Book2"]
    }

    book_dict = {
        "isbn": isbn,
        "name": "book1",
        "year": 2020,
        "author": author_dict
    }
    book1 = Book(**book_dict)
    #return {"parametro dinámico":isbn}
    return book1


@app.get("/author/{id}/book")
async def get_authors_books(id: int,category: str , order: str = 'asc'):
    return {"orden": order, "id": id, "categoría": category }

@app.patch("/author/name")
async def patch_author_name(name: str = Body(..., embed=True)):
    return {"name in the body": name} #embed=True toma el parametro name como key y el body del json como clave

@app.post("/user/author")
async def post_user_and_author(user: User, author: Author, bookstore_name: str = Body(..., embed=True)):
    return {"user": user, "author": author, "parametro extra": bookstore_name}

@app.post("/user/photo")
async def upload_user_photo(response: Response, profile_photo: bytes = File(...)):
    #instalar python-multipart y usarlo con multipartform en insomnia
    response.headers["x-file-size"]=str(len(profile_photo))
    response.set_cookie(key='cool_cookie', value="test")
    return {"file size": len(profile_photo)}


