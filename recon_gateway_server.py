from fastapi import FastAPI
from pydantic import BaseModel

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


@app.post("/send")
# x_channel_id: Union[str, None] = Header(default=None)
async def send(comment: Comment):
    print(comment)
    return {"X-CHANNEL-ID values": "x_channel_id"}

# {
#     "id" : "",
#     "dt": "",
#     "vid": "",
#     "payload" : ""
# }
