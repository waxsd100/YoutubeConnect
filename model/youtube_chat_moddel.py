class YoutubeChatModel:
    def __init__(self, rcon):
        self.__rcon = rcon

    def view_message(self, chat):
        rc = self.__rcon
        data = chat.json()
        rc.exec(f"say {data}")
