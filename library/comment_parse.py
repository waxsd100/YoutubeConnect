import re

import emoji
import mojimoji

from const import SPACE_STRING


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

    # 絵文字がユニコード形式に変換されるのでコメントアウト
    # if DISABLE_HAN_TO_ZEN is False:
    #     message = replace_hankaku_to_zenkaku(message,
    #                                          DISABLE_HAN_TO_ZEN_FOR_ASCII,
    #                                          DISABLE_HAN_TO_ZEN_FOR_KANA,
    #                                          DISABLE_HAN_TO_ZEN_FOR_DIGIT)

    if message and message.strip() and is_only_mcspace(message) == False:
        return message
    return None


def make_send_json(author, message):
    """
    @deprecated
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
    @deprecated
    送信用データを作成(非推奨）
    :param name:
    :param text:
    :return:
    """
    return str(f'{{from:"YouTube",name:"{name}",text:["{text}"]}}')


def replace_zenkaku_to_hankaku(message: str, disabled_ascii=False, disabled_kana=False, disabled_digit=False):
    """
    メッセージを半角から全角へ変革する
    0123 -> ０１２３
    ｲﾛﾊﾆ -> イロハニ
    ABC#% -> ＡＢＣ＃％
    :param message:
    :return:
    @param message: 対象文字列
    @param disabled_ascii: 英字記号を変換を無効化するか
    @param disabled_kana: カタカナ変換を無効化するか
    @param disabled_digit: 数値変換を無効化するか
    """
    return mojimoji.zen_to_han(message, ascii=disabled_ascii, kana=disabled_kana, digit=disabled_digit)


def replace_hankaku_to_zenkaku(message: str, disabled_ascii=False, disabled_kana=False, disabled_digit=False):
    """
    メッセージを全角から半角へ変革する
    ０１２３ -> 0123
    イロハニ -> ｲﾛﾊﾆ
    ＡＢＣ＃％ -> ABC#%
    :param message:
    :return:
    @param message: 対象文字列
    @param disabled_ascii: 英字記号を変換を無効化するか
    @param disabled_kana: カタカナ変換を無効化するか
    @param disabled_digit: 数値変換を無効化するか
    """
    return mojimoji.han_to_zen(message, ascii=disabled_ascii, kana=disabled_kana, digit=disabled_digit)


def trim_message(message):
    """
    必要のないメッセージ文字列をスペースに変換する
    :param message:
    :return:
    """
    m = replace_half_space(message)
    m = m.replace('"', SPACE_STRING)
    m = m.replace("'", SPACE_STRING)
    return m


def delete_emoji_message(message):
    """
    :emoji:形式のemoji をスペースへ変換する
    :param message:
    :return:
    """
    p = r'\:(.*?)\:'  # 非貪欲マッチ（最小マッチ）
    for m in re.findall(p, message):
        message = message.replace(f":{m}:", SPACE_STRING)
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
    return message.replace(' ', SPACE_STRING)


def is_only_mcspace(message):
    """
    メッセージ内容がMinecraftSpace のみかを判定する
    :param message:
    :return:
    """
    m = message.strip(SPACE_STRING)
    return len(m) == 0
