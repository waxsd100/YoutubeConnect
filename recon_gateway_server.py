from fastapi import FastAPI
from pydantic import BaseModel
from starlette import status
from starlette.responses import JSONResponse

from library.rcon_server import RconServer
from model.rcon_client_model import RconClientModel

app = FastAPI()
global client


# リクエストbodyを定義
class Comment(BaseModel):
    id: int
    datetime: str
    user_id: str
    user_name: str
    message: str


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/")
async def root():
    return {"message": "Hello World"}


@app.post("/open")
async def open():
    global client
    rc = RconServer()
    rc.connect()
    client = RconClientModel(rc)


@app.post("/close")
async def close():
    global client
    rc = RconServer()
    rc.disconnect()
    client = RconClientModel(rc)


@app.post("/send")
async def ping(comment: Comment):
    if comment.id is None:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"error": "id is not set."})
    print(f"[{comment.datetime}] {comment.id} {comment.user_id} <{comment.user_name}> {comment.message}")
    return JSONResponse(status_code=status.HTTP_200_OK, content=comment.json())
