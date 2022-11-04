import datetime

from unicodedata import east_asian_width


def get_current_time():
    """
    YYYY-MM-DD HH:mm:ss 形式の現在時間を返す
    @return:
    """
    dt_now = datetime.datetime.now()
    return dt_now.strftime('%Y-%m-%d %H:%M:%S')


def unicode_width(s: str) -> int:
    """
    マルチバイトを考慮した文字幅を返します。
    :@param s: 対象文字列
    :@return: 文字幅
    """
    return sum([east_asian_width(c) in 'WF' and 2 or 1 for c in s])
