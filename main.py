#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import functools
import hashlib
import json
import logging
import sys

import backoff
import pytchat
import requests
from pytchat import config

from command.gift_purchase import GiftRedemption
from command.gift_redemption import GiftPurchase
from command.new_sponsor import NewSponsor
from command.super_chat import SuperChat
from command.super_sticker import SuperSticker
from command.text_message import TextMessage
from const import YOUTUBE_VIDEO_ID, isOpenBrowser, API_TIMEOUT, CHANNEL_ID, CHANNEL_NAME
from define.enum_youtube import ChatType
from library.browser_util import get_web_driver, open_browser
from library.comment_parse import parse_send_message
from library.rcon_server import RconServer, disconnect_command, connect_command

global chat


def main():
    global chat
    chat = pytchat.create(video_id=YOUTUBE_VIDEO_ID, logger=config.logger(__name__, logging.DEBUG))
    rc = RconServer()
    try:
        rc.connect()
        connect_command(rc)
        while chat.is_alive():
            for c in chat.get().sync_items():
                chat_type = c.type
                id = hashlib.md5(c.id.encode()).hexdigest()
                if chat_type == ChatType.SUPER_CHAT.value:
                    # スーパチャット時のClass呼び出し処理
                    super_chat = SuperChat(rc)
                    super_chat.send_view_chat_command(c)
                    pass
                elif chat_type == ChatType.TEXT_MESSAGE.value:
                    # 通常チャット送信時のClass呼び出し処理
                    text_message = TextMessage(rc)
                    text_message.send_data_command(c)
                    pass
                elif chat_type == ChatType.SUPER_STICKER.value:
                    # スーパスティッカー送信時のClass呼び出し処理
                    super_sticker = SuperSticker(rc)
                    super_sticker.send_view_chat_command(c)
                    pass
                elif chat_type == ChatType.NEW_SPONSOR.value:
                    # メンバー登録時のClass呼び出し処理
                    new_sponsor = NewSponsor(rc)
                    new_sponsor.send_view_chat_command(c)
                    pass
                elif chat_type == ChatType.GIFT_REDEMPTION.value:
                    # メンバーシップギフト受信(誰かが受け取った)時のClass呼び出し処理
                    gift_redemption = GiftRedemption(rc)
                    gift_redemption.send_view_chat_command(c)
                    pass
                elif chat_type == ChatType.GIFT_PURCHASE.value:
                    # メンバーシップギフト送信(誰かが送信した)時のClass呼び出し処理
                    gift_purchase = GiftPurchase(rc)
                    gift_purchase.send_view_chat_command(c)
                    pass
                else:
                    print(f'Error: unsupported chat type {chat_type}', file=sys.stderr)
                print(f"{c.datetime} {id} {c.type} {c.author.name}: {c.message} {c.amountString}")
    except pytchat.ChatdataFinished:
        print("chat data finished")
    except Exception as e:
        print(type(e), str(e))
    finally:
        chat.terminate()
        disconnect_command(rc)
        rc.disconnect()


def resend(function):
    @functools.wraps(function)
    def wrapped(*args, **kwargs):
        def fatal_code(e):
            """Too many Requests(429)のときはリトライする。それ以外の4XXはretryしない"""
            if e.response is None:
                return True
            code = e.response.status_code
            return 400 <= code < 500 and code != 429

        return backoff.on_exception(
            backoff.expo,
            requests.exceptions.RequestException,
            jitter=backoff.full_jitter,
            max_time=300,
            giveup=fatal_code
        )(function)(*args, **kwargs)

    return wrapped


async def gateway_exec():
    global chat
    try:
        session = requests.Session()
        url = "http://127.0.0.1:8000/send"
        headers = {"TEST": "HELLO"}
        TARGET = 1

        vid = YOUTUBE_VIDEO_ID[TARGET]
        cid = CHANNEL_ID[TARGET]
        cn = CHANNEL_NAME[TARGET]

        driver = get_web_driver()
        open_browser(driver=driver, url=f"https://www.youtube.com/live_chat?v={vid}")

        chat = pytchat.create(video_id=vid, logger=config.logger(__name__, logging.DEBUG))
        ukey = 0
        while chat.is_alive():
            async for c in chat.get().async_items():
                ukey += 1
                id = hashlib.md5(c.id.encode()).hexdigest()
                data = json.dumps({
                    'from': 'YouTube',
                    'channel_id': cid,
                    'channel_name': cn,
                    'chat_type': c.type,
                    'id': id,
                    'name': c.author.name,
                    'text': [parse_send_message(c.message)]  # TODO Null Check
                }, ensure_ascii=False)
                message = f"data modify storage mc_comment_viewer: new_comments append value {data}"
                send_data = {"id": ukey, "dt": c.datetime, "vid": vid, "payload": message}
                print(data)
                # '{"id":1,"dt":"24","vid":"Japan","payload":""}'
                session.post(
                    url=url,
                    headers=headers,
                    json=send_data,
                    timeout=API_TIMEOUT
                )
                # {
                #     "id" : Int,
                #     "dt": Str,
                #     "vid": Str,
                #     "payload" : Str
                # }
                # print(f"{c.datetime} {id} {c.type} {c.author.name}: {c.message} {c.amountString}")
    except Exception as e:
        print(type(e), str(e))
    finally:
        chat.terminate()
        driver.close()
        driver.quit()


if __name__ == '__main__':
    print("Start")
    if isOpenBrowser:
        driver = get_web_driver()
        open_browser(driver=driver, url=f"https://www.youtube.com/live_chat?v={YOUTUBE_VIDEO_ID}")
    # main()
    asyncio.run(gateway_exec())
    if isOpenBrowser:
        driver.close()
        driver.quit()
