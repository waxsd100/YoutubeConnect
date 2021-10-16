#!/usr/bin/env python
# -*- coding: utf-8 -*-

### Copyright © 2021 wakokara
### This software is released under the MIT License, see LICENSE.
import hashlib
import logging

import emoji
import pytchat
from mcrcon import MCRcon
from pytchat import config
from selenium import webdriver
# from selenium.webdriver.chrome import service as cs
from selenium.webdriver.firefox import service as fs

from const import YOUTUBE_VIDEO_ID, RCON_PASSWORD, RCON_HOST, RCON_PORT, RCON_TIMEOUT


# require mcrcon, pytchat, emoji
def main(chat, mcr):
    message_start(mcr)
    try:
        while chat.is_alive():
            for c in chat.get().sync_items():
                id = hashlib.md5(c.id.encode()).hexdigest()
                print(f"{c.datetime} {id} {c.type} {c.author.name} {c.message} {c.amountString}")
                if c.type == "textMessage":
                    mes = create_message(c.author.name, c.message)
                    mes = trim_message(mes)
                    if mes:
                        send_mc(mcr, mes)
                else:
                    pass

    except pytchat.ChatdataFinished:
        print("chat data finished")
    except Exception as e:
        print(type(e), str(e))


def create_message(name, text):
    """
    送信用データを作成
    :param name:
    :param text:
    :return:
    """
    return f'{{from:"YouTube",name:"{name}",text:["{text}"]}}'


def trim_message(message):
    """
    必要のないメッセージ文字列を削除する
    :param message:
    :return:
    """
    # m = delete_emoji_message(m)
    m = replace_full_space_to_half_space(message)
    m = emoji.emojize(m, use_aliases=True)
    return m


def delete_emoji_message(message):
    """
    ::形式のemoji を削除する
    :param message:
    :return:
    """
    p = r'\:[^*]:\*'
    return message.replace(p, '')


def replace_full_space_to_half_space(message):
    """
    タブ文字と全角空白 を半角スペースに変換する
    :param message:
    :return:
    """
    table = str.maketrans({
        ' ': ' ',
        '\t': ' '
    })
    return message.translate(table)


def send_mc(mcr, data):
    """
    mc_comment_viewer に対してメッセージ送信する。
    :param mcr: mcrcon instance
    :param data: message data (string型のJson形式)
    :return: mcr response
    """
    return mcr.command(f"data modify storage mc_comment_viewer: new_comments append value "
                       f'{data}')


def message_start(mcr):
    """
    初回コマンド送信用
    :param mcr: mcrcon instance
    :return: mcr response
    """
    return mcr.command(f"say [Debug] Connect Server: https://www.youtube.com/watch?v={YOUTUBE_VIDEO_ID}")
    # return mcr.command(f"function #mc_comment_viewer:on")


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


if __name__ == '__main__':
    chat = pytchat.create(video_id=YOUTUBE_VIDEO_ID, logger=config.logger(__name__, logging.DEBUG))
    driver = get_web_driver()
    url = "https://www.youtube.com/live_chat?v=" + YOUTUBE_VIDEO_ID
    driver.get(url)
    driver.implicitly_wait(1)

    with MCRcon(host=RCON_HOST, password=RCON_PASSWORD, port=RCON_PORT, timeout=RCON_TIMEOUT) as mcr:
        main(chat, mcr)
    chat.terminate()
    driver.close()
    driver.quit()
