import json

from fastapi import FastAPI
from starlette import status
from starlette.responses import JSONResponse

from library.rcon_server import RconServer
from model.rcon_client_model import RconClientModel

app = FastAPI()
global client


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


@app.post("/ping")
async def ping(c):
    print(json.dumps(c))
    print(f"[{c.datetime}] {c.type} {c.author.name}: {c.message} {c.amountString}")
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=c)


@app.post("/send/{comment}")
# x_channel_id: Union[str, None] = Header(default=None)
async def send(comment: dict, send_media: str):
    global client
    try:
        if comment.id is None:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                content={"error": "id is not set."})
        if comment.dt is None:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                content={"error": "dt is not set."})
        if comment.video_id is None:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                content={"error": "vid is not set."})
        if comment.payload is None:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                content={"error": "payload is not set."})
        id = comment.id
        dt = comment.dt
        vid = comment.video_id
        cid = comment.channel_id
        payload = comment.payload
        # TODO スパチャなど対応する
        client.send_command(f"{comment.payload}")
        print(f"{vid} {id}: {dt} {payload}")
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"id": id, "dt": dt, "video_id": vid, "channel_id": cid, "payload": payload})
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
