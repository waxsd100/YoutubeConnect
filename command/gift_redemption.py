from model.youtube_chat_moddel import YoutubeChatModel


class GiftPurchase(YoutubeChatModel):
    """
    メンバーシップギフト送信(誰かが送信した)時の処理
    """

    def __init__(self, rcon):
        super().__init__(rcon)
        self.__rcon = rcon

    pass
