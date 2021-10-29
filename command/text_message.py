from lib.comment_parse import make_send_json, parse_send_message


class TextMessage:
    def __init__(self, rcon):
        self.__rcon = rcon

    def view_chat(self, chat):
        rc = self.__rcon
        message = make_send_json(chat.author.name, parse_send_message(chat.message))
        if message is not None:
            rc.exec(f"data modify storage mc_comment_viewer: new_comments append value {message}")
        else:
            print(f"No send Message: {chat.author.name} / {chat.message}")

    def view_message(self, chat):
        rc = self.__rcon
        data = chat.json()
        rc.exec(f"say {data}")
