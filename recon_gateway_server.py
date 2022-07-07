from typing import Union

from fastapi import FastAPI
from fastapi import Header

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/send")
async def send(x_channel_id: Union[str, None] = Header(default=None)):
    return {"X-CHANNEL-ID values": x_channel_id}

# {
#     "id" : "",
#     "dt": "",
#     "vid": "",
#     "payload" : ""
# }
