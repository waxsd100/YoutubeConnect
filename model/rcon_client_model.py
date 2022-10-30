class RconClientModel:
    """
    Youtubeメッセージ受信時呼び出されるときの親クラス<br>
    このメソッド内で関数定義することで superChat, textMessage, superSticker, newSponsor で呼び出せる共通処理を書くことができる。
    """

    def __init__(self, rcon):
        self.callback_function = None
        self.__rcon = rcon

    def send_view_chat_command(self, data: str):
        """
        共通メソッド 送信したテキストメッセージをSayで送信する
        @param data: 送信テキストメッセージ
        @return:
        """
        rc = self.__rcon
        rc.exec(f"say {data}")

    def send_command(self, command):
        """
        共通メソッド 任意のコマンドメッセージを送信する( / は不要)
        @param command:
        @return:
        """
        rc = self.__rcon
        if command is None:
            return None
        return rc.exec(command)

# チャットタイプに応じて実行するメソッドを変えたい場合はcommand/フォルダ配下にある子クラスで定義すること
