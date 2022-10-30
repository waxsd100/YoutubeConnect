#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright © 2021 wakokara
This software is released under the MIT License, see LICENSE.
"""

# Gateway Data channel list
CHANNELS = [
    {"channel_name": "########", "video_id": "########"},
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

# Number of retries on failure(TODO 未実装）
MAX_RETRY = 3

# 送信するチャット文字列の全角から半角変換を無効化する (is_answer など記号チェック漏れ起きる可能性があります)
DISABLE_ZEN_TO_HAN = False

# 全角から半角変換を無効化する(英字 / 記号)
DISABLE_ZEN_TO_HAN_FOR_ASCII = False

# 全角から半角変換を無効化する(カタカナ)
DISABLE_ZEN_TO_HAN_FOR_KANA = True

# 全角から半角変換を無効化する(数字)
DISABLE_ZEN_TO_HAN_FOR_DIGIT = False
