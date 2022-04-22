#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib
import logging

import pytchat
from pytchat import config

from command.text_message import TextMessage
from const import YOUTUBE_VIDEO_ID, isOpenBrowser
from library.browser_util import get_web_driver, open_browser
from library.rcon_server import RconServer, disconnect_command, connect_command
from model.youtube_chat_moddel import YoutubeChatModel

global chat, rc


def init():
    try:
        global chat, rc
        chat = pytchat.create(video_id=YOUTUBE_VIDEO_ID, logger=config.logger(__name__, logging.DEBUG))
        rc = RconServer()
        rc.connect()
        YoutubeChatModel(rcon=rc)
    except Exception as e:
        print(e)


def main():
    init()
    text_message = TextMessage(rc)
    try:
        connect_command(rc)
        while chat.is_alive():
            for c in chat.get().sync_items():
                chat_type = c.type
                id = hashlib.md5(c.id.encode()).hexdigest()
                if chat_type == "superChat":
                    pass
                elif chat_type == "textMessage":
                    text_message.view_chat(c)
                    pass
                elif chat_type == "superSticker":
                    pass
                elif chat_type == "newSponsor":
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
