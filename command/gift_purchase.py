from model.rcon_client_model import RconClientModel


class GiftRedemption(RconClientModel):
    """
    メンバーシップギフト受信(誰かが受け取った)時の処理
    """

    def __init__(self, rcon):
        super().__init__(rcon)
        self.__rcon = rcon

    pass
