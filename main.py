#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib
import logging

import pytchat
from pytchat import config

from command.gift_purchase import GiftRedemption
from command.gift_redemption import GiftPurchase
from command.new_sponsor import NewSponsor
from command.super_chat import SuperChat
from command.super_sticker import SuperSticker
from command.text_message import TextMessage
from const import YOUTUBE_VIDEO_ID, isOpenBrowser
from library.browser_util import get_web_driver, open_browser
from library.rcon_server import RconServer, disconnect_command, connect_command
from model.youtube_chat_moddel import YoutubeChatModel

global chat, rc


def main():
    global chat, rc
    chat = pytchat.create(video_id=YOUTUBE_VIDEO_ID, logger=config.logger(__name__, logging.DEBUG))
    rc = RconServer()
    rc.connect()
    YoutubeChatModel(rcon=rc)
    super_chat = SuperChat(rc)
    text_message = TextMessage(rc)
    super_sticker = SuperSticker(rc)
    new_sponsor = NewSponsor(rc)
    gift_redemption = GiftRedemption(rc)
    gift_purchase = GiftPurchase(rc)

    try:
        connect_command(rc)
        while chat.is_alive():
            for c in chat.get().sync_items():
                chat_type = c.type
                id = hashlib.md5(c.id.encode()).hexdigest()
                if chat_type == "superChat":
                    # スーパチャット時のClass呼び出し処理
                    super_chat.send_view_chat_command(c)
                    pass
                elif chat_type == "textMessage":
                    # 通常チャット送信時のClass呼び出し処理
                    text_message.send_data_command(c)
                    pass
                elif chat_type == "superSticker":
                    # スーパスティッカー送信時のClass呼び出し処理
                    super_sticker.send_view_chat_command(c)
                    pass
                elif chat_type == "newSponsor":
                    # メンバー登録時のClass呼び出し処理
                    new_sponsor.send_view_chat_command(c)
                    pass
                elif chat_type == "giftRedemption":
                    # メンバーシップギフト受信(誰かが受け取った)時のClass呼び出し処理
                    # TODO no member class
                    gift_redemption.send_view_chat_command(c)
                    pass
                elif chat_type == "giftPurchase":
                    # メンバーシップギフト送信(誰かが送信した)時のClass呼び出し処理
                    gift_purchase.send_view_chat_command(c)
                    pass

                print(f"{c.datetime} {id} {c.type} {c.author.name} {c.message} {c.amountString}")
    except pytchat.ChatdataFinished:
        print("chat data finished")
    except Exception as e:
        print(type(e), str(e))
    finally:
        chat.terminate()
        disconnect_command(rc)
        rc.disconnect()


if __name__ == '__main__':
    print("Start")
    if isOpenBrowser:
        driver = get_web_driver()
        open_browser(driver=driver, url=f"https://www.youtube.com/live_chat?v={YOUTUBE_VIDEO_ID}")
    main()
    if isOpenBrowser:
        driver.close()
        driver.quit()
