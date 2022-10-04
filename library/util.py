import datetime


def get_current_time():
    """
    YYYY-MM-DD HH:mm:ss 形式の現在時間を返す
    @return:
    """
    dt_now = datetime.datetime.now()
    return dt_now.strftime('%Y-%m-%d %H:%M:%S')
