#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

import pytchat
from pytchat import config
from selenium import webdriver
# from selenium.webdriver.chrome import service as cs
from selenium.webdriver.firefox import service as fs

from command.text_message import TextMessage
from const import YOUTUBE_VIDEO_ID, isOpenBrowser
from library.rcon_server import RconServer


def main(chat):
    try:
        rc = RconServer()
        rc.connect()
        text_message = TextMessage(rc)
        connect_command(rc)
        while chat.is_alive():
            for c in chat.get().sync_items():
                chat_type = c.type
                # id = hashlibrary.md5(c.id.encode()).hexdigest()
                # TODO ちゃんとオーバライドさせる
                if chat_type == "superChat":
                    pass
                elif chat_type == "textMessage":
                    text_message.view_message(c)
                    # text_message.view_chat(c)
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
        disconnect_command(rc)
        rc.disconnect()


def connect_command(rc):
    """
    初回コマンド送信用
    :param mcr: mcrcon instance
    :return: mcr response
    """
    # pass
    return rc.exec(f"say [Debug] Connect Server: https://www.youtube.com/watch?v={YOUTUBE_VIDEO_ID}")
    # return mcrcon.command(f"function #mc_comment_viewer:on")


def disconnect_command(rc):
    """
    初回コマンド送信用
    :param mcr: mcrcon instance
    :return: mcr response
    """
    return rc.exec(f"say [Debug] Disconnect Server: https://www.youtube.com/watch?v={YOUTUBE_VIDEO_ID}")
    # return mcrcon.command(f"function #mc_comment_viewer:on")


def get_web_driver():
    firefox_option = webdriver.FirefoxOptions()
    firefox_option.add_argument("--window-size=500,800")
    firefox_option.add_argument("--width=500")
    firefox_option.add_argument("--height=800")
    firefox_servie = fs.Service(executable_path="bin/geckodriver.exe")

    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--disable-gpu')
    # # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--no-sandbox')
    # chrome_servie = cs.Service(executable_path="bin/chromedriver.exe")

    return webdriver.Firefox(service=firefox_servie, options=firefox_option)
    # return webdriver.Chrome(service=chrome_servie, options=chrome_options)


def open_browser(driver, url):
    driver.get(url)
    driver.implicitly_wait(1)
    return driver


if __name__ == '__main__':
    chat = pytchat.create(video_id=YOUTUBE_VIDEO_ID, logger=config.logger(__name__, logging.DEBUG))
    if isOpenBrowser:
        driver = get_web_driver()
        open_browser(driver=driver, url=f"https://www.youtube.com/live_chat?v={YOUTUBE_VIDEO_ID}")
    main(chat)
    chat.terminate()
    if isOpenBrowser:
        driver.close()
        driver.quit()
