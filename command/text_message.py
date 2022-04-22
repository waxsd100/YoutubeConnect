import hashlib
import json

from library.comment_parse import parse_send_message
from model.youtube_chat_moddel import YoutubeChatModel


class TextMessage(YoutubeChatModel):
    def __init__(self, rcon):
        super().__init__(rcon)
        self.__rcon = rcon

    def view_message(self, chat):
        self.view_message(chat)

    def view_chat(self, chat):
        rc = self.__rcon
        id = hashlib.md5(chat.id.encode()).hexdigest()
        message = {'from': 'YouTube', 'id': id, 'name': chat.author.name, 'text': [parse_send_message(chat.message)]}
        data = json.dumps(message, ensure_ascii=False)
        if message is not None:
            rc.exec(f"data modify storage mc_comment_viewer: new_comments append value {data}")
        else:
            print(f"No send Message: {chat.author.name} / {chat.message}")
