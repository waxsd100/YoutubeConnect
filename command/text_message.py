import json
import sys

from library.comment_parse import parse_send_message, replace_space_to_mcspace, replace_hankaku_to_zenkaku
from library.rcon_server import RconServer
from library.util import unicode_width
from model.rcon_client_model import RconClientModel
from const import COMMAND_PREFIX

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
        send_text = chat['data']['message']
        send_text = parse_send_message(send_text)
        send_name = replace_space_to_mcspace(chat['data']['author']['name'])

        # 空文字判定
        if send_text is None and send_text != "":
            # 送信しない文字列の場合(絵文字のみなど)
            print(f"Chat Text is Empty: {chat['data']['message']}", file=sys.stderr)
        elif send_text == "":
            # 空文字の場合
            print(f"Chat Text is Empty: {chat}", file=sys.stderr)
        else:
            # チェック成功時
            is_answer = False
            # if replace_hankaku_to_zenkaku(send_text[0]) == "＃":
            if send_text[0] == "#" or send_text[0] == "＃" or send_text[0] == "♯":
                is_answer = True
                send_text = send_text.removeprefix("#").removeprefix("＃").removeprefix("♯")

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
                'name': send_name,
                'name_width': unicode_width(send_name),
                'text': send_text,
                'text_width': unicode_width(send_text),
                'chars': list(send_text),
                'is_answer': is_answer,
                'is_chat_owner': is_chat_owner,
                'is_verified': is_verified,
                'is_chat_sponsor': is_chat_sponsor,
                'is_chat_moderator': is_chat_moderator,
            }
            data = json.dumps(message, ensure_ascii=False)
            if message is not None:
                rc.exec(f"{COMMAND_PREFIX}{data}")
            else:
                print(f"No send Message: {chat['data']['author']['name']} / {chat['data']['message']}")
