import json
import sys

from library.comment_parse import parse_send_message, replace_space_to_mcspace, replace_hankaku_to_zenkaku
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

        if send_text is None and send_text is not "":
            print(f"Chat Text is Empty: {chat['data']['message']}", file=sys.stderr)
        elif send_text is "":
            print(f"Chat Text is Empty: {chat}", file=sys.stderr)
        else:
            is_answer = False
            if replace_hankaku_to_zenkaku(send_text[0]) == "＃":
                is_answer = True
                send_text = send_text.removeprefix("＃")

            # 放送者判定
            is_chat_owner = chat['data']["author"]["isChatOwner"]
            # 公式バッチ持ち判定
            is_verified = chat['data']["author"]["isVerified"]
            # メンバーシップ判定
            is_chat_sponsor = chat['data']["author"]["isChatSponsor"]
            # モデレーター判定
            is_chat_moderator = chat['data']["author"]["isChatModerator"]

            message = {
                'from': 'YouTube',
                'datetime': chat['data']['datetime'],
                'channel_name': replace_space_to_mcspace(chat['channelName']),
                'user_id': chat['userId'],
                'name': replace_space_to_mcspace(chat['data']['author']['name']),
                'text': [send_text],  # TODO Arrayから普通のStringにしたい
                'is_answer': is_answer,
                'is_chat_owner': is_chat_owner,
                'is_verified': is_verified,
                'is_chat_sponsor': is_chat_sponsor,
                'is_chat_moderator': is_chat_moderator,
            }
            data = json.dumps(message, ensure_ascii=False)
            if message is not None:
                rc.exec(f"data modify storage mc_comment_viewer: new_comments append value {data}")
            else:
                print(f"No send Message: {chat['data']['author']['name']} / {chat['data']['message']}")
