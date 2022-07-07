class RconClientModel:
    """
    Youtubeメッセージ受信時呼び出されるときの親クラス<br>
    このメソッド内で関数定義することで superChat, textMessage, superSticker, newSponsor で呼び出せる共通処理を書くことができる。
    """

    def __init__(self, rcon):
        self.__rcon = rcon

    def send_view_chat_command(self, chat):
        rc = self.__rcon
        data = chat.json()
        rc.exec(f"say {data}")

    @property
    def rcon(self):
        return self.__rcon

    @rcon.setter
    def rcon(self, rcon):
        self.__rcon = rcon
