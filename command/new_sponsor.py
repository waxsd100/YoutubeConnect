from model.rcon_client_model import RconClientModel


class NewSponsor(RconClientModel):
    """
    チャンネルメンバーシップ新規登録受信の処理
    """

    def __init__(self, rcon):
        super().__init__(rcon)

    pass
