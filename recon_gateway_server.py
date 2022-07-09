from fastapi import FastAPI
from pydantic import BaseModel
from starlette import status
from starlette.responses import JSONResponse

from library.rcon_server import RconServer
from model.rcon_client_model import RconClientModel

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# リクエストbodyを定義
class Comment(BaseModel):
    id: int
    dt: str
    vid: str
    payload: str


rc = RconServer()
rc.connect()
client = RconClientModel(rc)


@app.post("/send")
# x_channel_id: Union[str, None] = Header(default=None)
async def send(comment: Comment):
    try:
        if comment.id is None:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                content={"error": "id is not set."})
        if comment.dt is None:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                content={"error": "dt is not set."})
        if comment.vid is None:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                content={"error": "vid is not set."})
        if comment.payload is None:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                content={"error": "payload is not set."})
        id = comment.id
        dt = comment.dt
        vid = comment.vid
        payload = comment.payload
        client.send_command(f"{comment.payload}")
        print(f"{vid} {id}: {dt} {payload}")
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"id": id, "dt": dt, "vid": vid, "payload": payload})
    except Exception as e:
        print(type(e), str(e))
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"error": str(e)})

# {
#     "id" : "",
#     "dt": "",
#     "vid": "",
#     "payload" : ""
# }
