from fastapi import FastAPI, Header
from models.user import User
from starlette.status import HTTP_201_CREATED
from starlette.responses import Response


app__v2 = FastAPI(openapi_prefix="/v2")

@app__v2.post("/user", status_code=HTTP_201_CREATED)
async def post_user(user: User, x_custom: str = Header(...)):
    return {"request body": user, "request custom header": x_custom, "version": "v2"}
