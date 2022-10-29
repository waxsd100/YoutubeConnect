#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright © 2021 wakokara
This software is released under the MIT License, see LICENSE.
"""

# Gateway Data channel list
CHANNELS = {
    0: {"channel_name": "########", "channel_id": "########", "video_id": "lJA41wKuyzA"},
}

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
