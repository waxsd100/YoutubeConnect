import hashlib
import json

from library.comment_parse import parse_send_message, replace_space_to_mcspace
from model.rcon_client_model import RconClientModel


class TextMessage(RconClientModel):
    """
    メッセージ受信時の処理
    """

    def __init__(self, rcon):
        super().__init__(rcon)
        self.__rcon = rcon

    pass

    def send_data_command(self, chat, channel_id, channel_name):
        """
        Datapack へのコマンド送信用処理
        :param chat: チャットデータ(データ定義はReadme参照)
        :return:
        """
        rc = self.__rcon
        id = hashlib.md5(chat.id.encode()).hexdigest()
        # from: 受信元定義(固定値)
        # id: ユーザごとのUUID
        # name: ユーザネーム
        # text: 送信データ

        message = {
            'from': 'YouTube',
            'channel_id': channel_id,
            'channel_name': replace_space_to_mcspace(channel_name),
            'chat_type': chat.type,
            'id': id,
            'name': replace_space_to_mcspace(chat.author.name),
            'text': [parse_send_message(chat.message)]
        }
        data = json.dumps(message, ensure_ascii=False)
        if message is not None:
            rc.exec(f"data modify storage mc_comment_viewer: new_comments append value {data}")
        else:
            print(f"No send Message: {chat.author.name} / {chat.message}")
