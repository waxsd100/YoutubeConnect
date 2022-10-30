from library.rcon_server import RconServer
from model.rcon_client_model import RconClientModel


class SuperChat(RconClientModel):
    """
    スーパチャット受信時の処理
    """

    def __init__(self, rcon: RconServer):
        super().__init__(rcon)
        self.__rcon = rcon

    pass
