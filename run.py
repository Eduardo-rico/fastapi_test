from fastapi import FastAPI


from routes.v1 import app__v1
from routes.v2 import app__v2


app = FastAPI()

app.mount("/v1", app__v1)
app.mount("/v2", app__v2)