import emoji

from lib.comment_parse import trim_message, create_message


class TextMessage:
    def __init__(self, rcon):
        self.__rcon = rcon

    def view_chat(self, chat):
        rc = self.__rcon
        message = trim_message(chat.message)
        message = emoji.emojize(message, use_aliases=True)
        mes = create_message(chat.author.name, message)
        if mes:
            rc.exec(f"data modify storage mc_comment_viewer: new_comments append value {mes}")

    def view_message(self, chat):
        rc = self.__rcon
        data = chat.json()
        rc.exec(f"say {data}")
