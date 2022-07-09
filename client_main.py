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

from const import API_ENDPOINT, \
    CHANNELS, API_TIMEOUT, isOpenBrowser
from library.browser_util import get_web_driver, open_browser
from library.comment_parse import parse_send_message, replace_space_to_mcspace

global TARGET_ID
global chat, vid, cid, cn


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


@resend
def send_data(session, url, headers, json, timeout):
    return session.post(
        url=url,
        headers=headers,
        json=json,
        timeout=timeout
    )


async def gateway_exec():
    global chat, TARGET_ID
    try:
        session = requests.Session()
        chat = pytchat.create(video_id=vid, logger=config.logger(__name__, logging.DEBUG))
        ukey = 0
        headers = {}
        if isOpenBrowser:
            driver = get_web_driver()
            open_browser(driver=driver, url=f"https://www.youtube.com/live_chat?v={vid}")

        while chat.is_alive():
            async for c in chat.get().async_items():
                ukey += 1
                id = hashlib.md5(c.id.encode()).hexdigest()
                send_text = parse_send_message(c.message)
                if send_text is None:
                    # パースした結果全て空白だった場合送信しない
                    print(f"[{c.datetime}] This message was not sent: {chat.author.name} {c.message}")
                    continue
                pass

                # 放送者判定
                is_chat_owner = c.author.isVerified
                # 公式バッチ持ち判定
                is_verified = c.author.isVerified
                # メンバーシップ判定
                is_chat_sponsor = c.author.isVerified
                # モデレーター判定
                is_chat_moderator = c.author.isVerified
                
                user_name = replace_space_to_mcspace(c.author.name)
                channel_name = replace_space_to_mcspace(cn)

                # Storageコマンド用Jsonを定義
                command_data = json.dumps({
                    'from': 'YouTube',
                    'channel_id': cid,
                    'channel_name': channel_name,
                    'chat_type': c.type,
                    'id': id,
                    'name': user_name,
                    'text': [send_text]
                }, ensure_ascii=False)

                # 送信するコマンド内容を定義
                # message = f"data modify storage mc_comment_viewer: new_comments append value {command_data}"
                message = f"say {channel_name} [{user_name}]: {send_text}"

                # Gatewayへの送信データを定期
                data = {"id": ukey, "dt": c.datetime, "vid": vid, "payload": message}

                # Gatewayへデータ送信
                response = send_data(session, API_ENDPOINT, headers, data, API_TIMEOUT)
                response_json = response.json()
                response_id = response_json["id"]

                if ukey == response_id:
                    if response.status_code == requests.codes.ok:
                        # 成功時
                        print(f"[{c.datetime}]  {ukey} {id} {c.type} {c.author.name}: {c.message} {c.amountString}")
                    elif response.status_code == 400:
                        # 送信したデータに異常がある
                        print(f"No send Message: {chat.author.name} / {chat.message}", file=sys.stderr)
                    else:
                        # サーバ上でexceptionが発生した
                        print(f"Gateway Server Error: {chat.author.name} / {chat.message}", file=sys.stderr)
                else:
                    # 送信したデータとレスポンスが一致していない(データ抜けの可能性)
                    print(f"Send ID is missmatch: {response_json}", file=sys.stderr)
    except Exception as e:
        print(type(e), str(e), file=sys.stderr)
    finally:
        chat.terminate()
        if isOpenBrowser:
            driver.close()
            driver.quit()


if __name__ == '__main__':
    global vid, cid, cn
    print(f"受信する放送を選んでください (0 ～ {len(CHANNELS) - 1})")
    for k in CHANNELS:
        print(f'{k} : {CHANNELS[k]["channel_name"]} / https://www.youtube.com/watch?v={CHANNELS[k]["video_id"]}')

    TARGET_ID = int(input(f'Enter number: '))
    if TARGET_ID > len(CHANNELS) - 1:
        print(f"The input content is abnormal (0 ～ {len(CHANNELS) - 1}): {TARGET_ID}", file=sys.stderr)
        exit(1)

    vid = CHANNELS[TARGET_ID]["video_id"]
    cid = CHANNELS[TARGET_ID]["channel_id"]
    cn = CHANNELS[TARGET_ID]["channel_name"]
    print("Start")
    asyncio.run(gateway_exec())
