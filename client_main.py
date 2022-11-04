#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import hashlib
import json
import logging
import sys
import time

import pytchat
from pytchat import config

from client.send_rcon_client import SendRconClient
from const import CHANNELS, isOpenBrowser, RETRY_COUNT
from library.browser_util import get_web_driver, open_browser
from library.rcon_server import RconServer
from library.util import get_current_time


# TODO retry_countがシャドーイングなので対処する
# TODO create_chat() のリトライ呼び出しが待機(await)していない

async def create_chat(cn, vid, sender_func, retry_count, *args):
    was_alive = False
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
            was_alive = True
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
        if was_alive:
            create_chat(cn, vid, sender_func, 0, args)
        elif retry_count < RETRY_COUNT:
            create_chat(cn, vid, sender_func, retry_count + 1, args)
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
        tasks.append(create_chat(cn, vid, callback, 0, args))
    res = asyncio.gather(*tasks, return_exceptions=True)
    loop.run_until_complete(res)

if __name__ == '__main__':
    while True:
        try:
            main()
            retry_count = 0
        except:
            retry_count += 1
            print('retrying...' + str(retry_count))
        time.sleep(5)

    # retry_count = 0
    # while retry_count < RETRY_COUNT:
    #     if main():
    #         retry_count = 0
    #     time.sleep(5)
    #     retry_count += 1
