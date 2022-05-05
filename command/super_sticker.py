from model.youtube_chat_moddel import YoutubeChatModel


class SuperSticker(YoutubeChatModel):
    """
    スーパスティッカー受信時の処理
    """

    def __init__(self, rcon):
        super().__init__(rcon)
        self.__rcon = rcon

    pass
