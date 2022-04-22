import re

import emoji


def parse_send_message(message):
    """
    送信用Textメッセージを作成
    :param message:
    :return:
    """
    message = trim_message(message)
    message = emoji.emojize(message, use_aliases=True)
    message = delete_emoji_message(message)
    message = replace_space_to_mcspace(message)
    if message and message.strip() and message != "␣":
        return message
    return None


def make_send_json(author, message):
    """
    送信用Jsonデータを作成する(非推奨）
    :param author:
    :param message:
    :return:
    """
    mes = create_message(author, message)
    if mes and message is not None:
        return mes
    return None


def create_message(name, text):
    """
    送信用データを作成(非推奨）
    :param name:
    :param text:
    :return:
    """
    return str(f'{{from:"YouTube",name:"{name}",text:["{text}"]}}')


def trim_message(message):
    """
    必要のないメッセージ文字列をスペースに変換する
    :param message:
    :return:
    """
    m = replace_half_space(message)
    m = m.replace('"', '␣')
    m = m.replace("'", '␣')
    return m


def delete_emoji_message(message):
    """
    :emoji:形式のemoji を削除する
    :param message:
    :return:
    """
    p = r'\:(.*?)\:'  # 非貪欲マッチ（最小マッチ）
    for m in re.findall(p, message):
        message = message.replace(f":{m}:", '␣')
    return message


def replace_half_space(message):
    """
    タブ文字と全角空白 を半角スペースに変換する
    :param message:
    :return:
    """
    return " ".join(message.split())


def replace_space_to_mcspace(message):
    """
    タブ文字と全角空白 を半角スペースに変換する
    :param message:
    :return:
    """
    return message.replace(' ', '␣')
