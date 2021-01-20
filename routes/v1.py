from fastapi import FastAPI, Body, Header, File, Depends, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_401_UNAUTHORIZED
from starlette.responses import Response
from fastapi.security import OAuth2PasswordRequestForm

from utils.security import authenticate_user, create_jwt_token, check_jwt_token
from models.user import User
from models.author import Author
from models.book import Book
from models.jwt_user import JWTUser


app__v1 = FastAPI(openapi_prefix="/v1")


@app__v1.post("/user", status_code=HTTP_201_CREATED)
async def post_user(user: User, x_custom: str = Header(...), jwt: bool = Depends(check_jwt_token)):
    return {"request body": user, "request custom header": x_custom}

@app__v1.get("/user")
async def get_user_validation(password: str = None):
    return {"parameter": password}


@app__v1.get("/book/{isbn}", response_model = Book, response_model_exclude=["author"])
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


@app__v1.get("/author/{id}/book")
async def get_authors_books(id: int,category: str , order: str = 'asc'):
    return {"orden": order, "id": id, "categoría": category }

@app__v1.patch("/author/name")
async def patch_author_name(name: str = Body(..., embed=True)):
    return {"name in the body": name} #embed=True toma el parametro name como key y el body del json como clave

@app__v1.post("/user/author")
async def post_user_and_author(user: User, author: Author, bookstore_name: str = Body(..., embed=True)):
    return {"user": user, "author": author, "parametro extra": bookstore_name}

@app__v1.post("/user/photo")
async def upload_user_photo(response: Response, profile_photo: bytes = File(...)):
    #instalar python-multipart y usarlo con multipartform en insomnia
    response.headers["x-file-size"]=str(len(profile_photo))
    response.set_cookie(key='cool_cookie', value="test")
    return {"file size": len(profile_photo)}


@app__v1.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()): #multiform request
    jwt_user_dict = {"username": form_data.username, "password": form_data.password}
    jwt_user = JWTUser(**jwt_user_dict)

    user = authenticate_user(jwt_user)
    print(user)
    if user is False:
        raise HTTPException(status_code = HTTP_401_UNAUTHORIZED)

    jwt_token = create_jwt_token(user)
    return {"token": jwt_token}