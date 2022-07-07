from model.rcon_client_model import RconClientModel


class SuperSticker(RconClientModel):
    """
    スーパスティッカー受信時の処理
    """

    def __init__(self, rcon):
        super().__init__(rcon)
        self.__rcon = rcon

    pass
