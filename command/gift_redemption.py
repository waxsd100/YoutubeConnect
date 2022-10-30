from library.rcon_server import RconServer
from model.rcon_client_model import RconClientModel


class GiftPurchase(RconClientModel):
    """
    メンバーシップギフト送信(誰かが送信した)時の処理
    """

    def __init__(self, rcon: RconServer):
        super().__init__(rcon)
        self.__rcon = rcon

    pass
