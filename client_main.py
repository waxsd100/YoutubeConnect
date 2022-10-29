#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import hashlib
import json
import logging
import sys

import pytchat
from pytchat import config

from const import API_ENDPOINT, \
    CHANNELS, isOpenBrowser
from library.browser_util import get_web_driver, open_browser
from library.gateway_server import GatewayServer
from library.util import get_current_time

global retry
gw = GatewayServer()


async def gateway_exec(cn, cid, vid):
    loop = asyncio.get_running_loop()
    chat = None
    try:
        print(f"[{get_current_time()}] Start:[{cn}] https://www.youtube.com/watch?v={vid}")
        chat = pytchat.create(video_id=vid, logger=config.logger(__name__, logging.DEBUG))
        u_key = 0
        headers = {}
        if isOpenBrowser:
            driver = get_web_driver()
            open_browser(driver=driver, url=f"https://www.youtube.com/live_chat?v={vid}")

        while chat.is_alive():
            async for c in chat.get().async_items():
                u_key += 1
                uuid = hashlib.md5(c.id.encode()).hexdigest()
                data = json.loads(c.json())
                data['uuid'] = uuid
                data['u_key'] = u_key
                print(data)
                response = gw.post_json(f"{API_ENDPOINT}/ping", headers, data)
                response_json = response.json()
                # response_id = response_json["id"]

                # send_text = parse_send_message(c.message)

                # if send_text is None:
                #     # パースした結果全て空白だった場合送信しない
                #     print(f"[{c.datetime}] This message was not sent: {chat.author.name} {c.message}")
                #     continue
                # pass
                #
                # # 放送者判定
                # is_chat_owner = c.author.isVerified
                # # 公式バッチ持ち判定
                # is_verified = c.author.isVerified
                # # メンバーシップ判定
                # is_chat_sponsor = c.author.isVerified
                # # モデレーター判定
                # is_chat_moderator = c.author.isVerified

                # user_name = replace_space_to_mcspace(c.author.name)
                # channel_name = replace_space_to_mcspace(cn)
                #
                # # Storageコマンド用Jsonを定義
                # command_data = json.dumps({
                #     'from': 'YouTube',
                #     'channel_id': cid,
                #     'channel_name': channel_name,
                #     'chat_type': c.type,
                #     'id': id,
                #     'name': user_name,
                #     'text': [send_text]
                # }, ensure_ascii=False)
                #
                # # 送信するコマンド内容を定義
                # # message = f"data modify storage mc_comment_viewer: new_comments append value {command_data}"
                # message = f"say {channel_name} [{user_name}]: {send_text}"
                #
                # # Gatewayへの送信データを定期
                # data = {"id": u_key, "dt": c.datetime, "video_id": vid, "channel_id": cid, "payload": message}
                #
                # # Gatewayへデータ送信
                # response = gw.post_json(f"{API_ENDPOINT}/", headers, data)
                # response_json = response.json()
                # response_id = response_json["id"]
                #
                # if u_key == response_id:
                #     if response.status_code == requests.codes.ok:
                #         # 成功時
                #         print(
                #             f"{response.status_code} [{c.datetime}] {u_key} {id} {c.type} {c.author.name}: {c.message} {c.amountString}")
                #     elif response.status_code == 400:
                #         # 送信したデータに異常がある
                #         print(f"{response.status_code} No send Message: {chat.author.name} / {chat.message}",
                #               file=sys.stderr)
                #     else:
                #         # サーバ上でexceptionが発生した
                #         print(f"{response.status_code} Gateway Server Error: {chat.author.name} / {chat.message}",
                #               file=sys.stderr)
                # else:
                #     # 送信したデータとレスポンスが一致していない(データ抜けの可能性)
                #     print(f"{response.status_code} Send ID is missmatch: {response_json}", file=sys.stderr)
    except Exception as ex:
        # print(type(e), str(e), file=sys.stderr)
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
    for k in CHANNELS:
        cn = CHANNELS[k]["channel_name"]
        cid = CHANNELS[k]["channel_id"]
        vid = CHANNELS[k]["video_id"]
        tasks.append(gateway_exec(cn, cid, vid))
    res = asyncio.gather(*tasks, return_exceptions=True)
    loop.run_until_complete(res)

    # TARGET_ID = int(input(f'Enter number: '))
    # if TARGET_ID > len(CHANNELS) - 1:
    #     print(f"The input content is abnormal (0 ～ {len(CHANNELS) - 1}): {TARGET_ID}", file=sys.stderr)
    #     exit(1)
    #
    # vid = CHANNELS[TARGET_ID]["video_id"]
    # cid = CHANNELS[TARGET_ID]["channel_id"]
    # cn = CHANNELS[TARGET_ID]["channel_name"]
    # print("Start")
    # asyncio.run(gateway_exec())


if __name__ == '__main__':
    main()
