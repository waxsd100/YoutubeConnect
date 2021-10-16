import re


def create_message(name, text):
    """
    送信用データを作成
    :param name:
    :param text:
    :return:
    """
    return str(f'{{from:"YouTube",name:"{name}",text:["{text}"]}}')


def trim_message(message):
    """
    必要のないメッセージ文字列を削除する
    :param message:
    :return:
    """
    m = replace_half_space(message)
    m = delete_emoji_message(m)
    m = m.strip('"')
    m = m.strip("'")
    return m


def delete_emoji_message(message):
    """
    :emoji:形式のemoji を削除する
    :param message:
    :return:
    """
    p = r'\:(.*?)\:'  # 非貪欲マッチ（最小マッチ）
    for m in re.findall(p, message):
        message = message.replace(f":{m}:", ' ')
    return message


def replace_half_space(message):
    """
    タブ文字と全角空白 を半角スペースに変換する
    :param message:
    :return:
    """
    return " ".join(message.split())
