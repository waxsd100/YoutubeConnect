#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright © 2021 wakokara
This software is released under the MIT License, see LICENSE.
"""

# Gateway Data channel list
CHANNELS = [
    {"channel_name": "########", "video_id": "S-i967djITM"},
]

API_ENDPOINT = "http://127.0.0.1:8000"

# Gateway Server Timeout
API_TIMEOUT = 300

# 送信されるときのスペース文字の置換後文字列
SPACE_STRING = "␣"

# Rcon Server Host
RCON_HOST = "127.0.0.1"

# Rcon Server Port
RCON_PORT = 25575

# Rcon Server Password
RCON_PASSWORD = "my_password"

# Rcon Server Timeout
RCON_TIMEOUT = 5

# Debug
isOpenBrowser = True

# Number of retries on failure
RETRY_COUNT = 3

# チャット文字列を送信するコマンド形式
COMMAND_PREFIX = 'data modify storage comment_receiver: new_comments append value '

# # 送信するチャット文字列の半角から全角変換を無効化する
# # TODO 絵文字がユニコード形式に変換されるのでコメントアウト library/comment_parse.py L21
# DISABLE_HAN_TO_ZEN = False
#
# # 半角から全角変換を無効化する(英字 / 記号)
# DISABLE_HAN_TO_ZEN_FOR_ASCII = False
#
# # 半角から全角変換を無効化する(カタカナ)
# DISABLE_HAN_TO_ZEN_FOR_KANA = False
#
# # 半角から全角変換を無効化する(数字)
# DISABLE_HAN_TO_ZEN_FOR_DIGIT = False
