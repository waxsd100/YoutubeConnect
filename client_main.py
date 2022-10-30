#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import hashlib
import json
import logging
import sys

import pytchat
from pytchat import config

from client.send_rcon_client import SendRconClient
from const import CHANNELS, isOpenBrowser
from library.browser_util import get_web_driver, open_browser
from library.rcon_server import RconServer
from library.util import get_current_time

global retry


async def create_chat(cn, vid, sender_func, *args):
    loop = asyncio.get_running_loop()
    chat = None
    try:
        print(f"[{get_current_time()}] Start:[{cn}] https://www.youtube.com/watch?v={vid}")
        chat = pytchat.create(video_id=vid, logger=config.logger(__name__, logging.DEBUG))
        u_key = 0
        if isOpenBrowser:
            driver = get_web_driver()
            open_browser(driver=driver, url=f"https://www.youtube.com/live_chat?v={vid}")

        while chat.is_alive():
            chat.raise_for_status()
            async for c in chat.get().async_items():
                # データごとのユニークなID(連番)
                u_key += 1
                # Userごと一意の固定長ID
                uuid = hashlib.md5(c.id.encode()).hexdigest()
                # チャットデータをもとに送信用データ作成
                data = {
                    "id": u_key,
                    "videoId": vid,
                    "channelName": cn,
                    "userId": uuid,
                    "data": json.loads(c.json())
                }
                # CallBack関数実行
                await sender_func(data, *args)
    except pytchat.ChatDataFinished:
        print("Chat data finished.")
    except Exception as ex:
        print(type(ex), str(ex), file=sys.stderr)
        trace = []
        tb = ex.__traceback__
        while tb is not None:
            trace.append({
                "filename": tb.tb_frame.f_code.co_filename,
                "name": tb.tb_frame.f_code.co_name,
                "lineno": tb.tb_lineno
            })
            tb = tb.tb_next
        print(str({
            'type': type(ex).__name__,
            'message': str(ex),
            'trace': trace
        }), file=sys.stderr)

        loop.stop()
    finally:
        chat.terminate()
        if isOpenBrowser:
            driver.close()
            driver.quit()
        loop.close()
    return


def main():
    loop = asyncio.get_event_loop()
    tasks = []

    # CallBackを指定
    # ドライバーを指定

    ## 特定のServerにPOSTする
    # callback = SendServerClient().send_server
    # args = GatewayServer()

    ## 特定のサーバにRconで送信する
    callback = SendRconClient.send_rcon
    args = RconServer()
    args.connect()

    for k in CHANNELS:
        cn = k["channel_name"]
        vid = k["video_id"]
        tasks.append(create_chat(cn, vid, callback, args))
    res = asyncio.gather(*tasks, return_exceptions=True)
    loop.run_until_complete(res)


if __name__ == '__main__':
    main()
