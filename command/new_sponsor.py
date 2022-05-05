from model.youtube_chat_moddel import YoutubeChatModel


class NewSponsor(YoutubeChatModel):
    """
    チャンネルメンバーシップ新規登録受信の処理
    """

    def __init__(self, rcon):
        super().__init__(rcon)
        self.__rcon = rcon

    pass
