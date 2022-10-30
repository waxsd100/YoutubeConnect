import json
import sys

import mojimoji

from const import DISABLE_ZEN_TO_HAN_FOR_ASCII, DISABLE_ZEN_TO_HAN_FOR_DIGIT, DISABLE_ZEN_TO_HAN_FOR_KANA, \
    DISABLE_ZEN_TO_HAN
from library.comment_parse import parse_send_message, replace_space_to_mcspace
from library.rcon_server import RconServer
from model.rcon_client_model import RconClientModel


class TextMessage(RconClientModel):
    """
    メッセージ受信時の処理
    """

    def __init__(self, rcon: RconServer):
        super().__init__(rcon)
        self.__rcon = rcon

    pass

    def send_data_command(self, chat):
        """
        Datapack へのコマンド送信用処理
        :param chat: チャットデータ(データ定義はReadme参照)
        :return:
        """
        # from: 受信元定義(固定値)
        # id: ユーザごとのUUID
        # name: ユーザネーム
        # text: 送信データ
        rc = self.__rcon
        send_text = parse_send_message(chat['data']['message'])

        if DISABLE_ZEN_TO_HAN is False:
            send_text = mojimoji.zen_to_han(send_text, ascii=DISABLE_ZEN_TO_HAN_FOR_ASCII,
                                            kana=DISABLE_ZEN_TO_HAN_FOR_KANA,
                                            digit=DISABLE_ZEN_TO_HAN_FOR_DIGIT)

        if send_text is None:
            print(f"Chat Text is Empty: {chat['data']['message']}", file=sys.stderr)
        else:
            is_answer = False

            if send_text[0] == "#":
                is_answer = True
                send_text = send_text.removeprefix("#")

            message = {
                'from': 'YouTube',
                'datetime': chat['data']['datetime'],
                'channel_name': replace_space_to_mcspace(chat['channelName']),
                'user_id': chat['userId'],
                'name': replace_space_to_mcspace(chat['data']['author']['name']),
                'text': [send_text],  # TODO Arrayから普通のStringにしたい
                'is_answer': is_answer
            }
            data = json.dumps(message, ensure_ascii=False)
            if message is not None:
                rc.exec(f"data modify storage mc_comment_viewer: new_comments append value {data}")
            else:
                print(f"No send Message: {chat['data']['author']['name']} / {chat['data']['message']}")
