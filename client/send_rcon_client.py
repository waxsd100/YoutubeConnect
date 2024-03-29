import sys

from command.gift_purchase import GiftRedemption
from command.gift_redemption import GiftPurchase
from command.new_sponsor import NewSponsor
from command.super_chat import SuperChat
from command.super_sticker import SuperSticker
from command.text_message import TextMessage
from define.enum_youtube import ChatType


class SendRconClient:

    @staticmethod
    async def send_rcon(chat: dict, args):
        rc = args
        chat_type = chat["data"]["type"]
        exec_chat_model = None

        # textMessage
        #     通常のチャットメッセージ
        # superSticker
        #     スーパースティッカー
        # superChat
        #     スーパチャット
        # newSponsor
        #     新規メンバー登録
        # giftRedemption
        #     メンバーシップギフト受け取り
        # giftPurchase
        #     メンバーシップギフト送信

        if chat_type == ChatType.SUPER_CHAT.value:
            # スーパチャット時のClass呼び出し処理
            exec_chat_model = SuperChat(rc)
            exec_chat_model = exec_chat_model.send_view_chat_command(chat)
            pass
        elif chat_type == ChatType.TEXT_MESSAGE.value:
            # 通常チャット送信時のClass呼び出し処理
            exec_chat_model = TextMessage(rc)
            exec_chat_model = exec_chat_model.send_data_command(chat)
            pass
        elif chat_type == ChatType.SUPER_STICKER.value:
            # スーパスティッカー送信時のClass呼び出し処理
            exec_chat_model = SuperSticker(rc)
            exec_chat_model = exec_chat_model.send_view_chat_command(chat)
            pass
        elif chat_type == ChatType.NEW_SPONSOR.value:
            # メンバー登録時のClass呼び出し処理
            exec_chat_model = NewSponsor(rc)
            exec_chat_model = exec_chat_model.send_view_chat_command(chat)
            pass
        elif chat_type == ChatType.GIFT_REDEMPTION.value:
            # メンバーシップギフト受信(誰かが受け取った)時のClass呼び出し処理
            exec_chat_model = GiftRedemption(rc)
            exec_chat_model = exec_chat_model.send_view_chat_command(chat)
            pass
        elif chat_type == ChatType.GIFT_PURCHASE.value:
            # メンバーシップギフト送信(誰かが送信した)時のClass呼び出し処理
            exec_chat_model = GiftPurchase(rc)
            exec_chat_model = exec_chat_model.send_view_chat_command(chat)
            pass
        else:
            print(f'Error: unsupported chat type {chat_type}', file=sys.stderr)
