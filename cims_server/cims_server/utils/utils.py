import datetime


def check_timestamp(timestamp):
    # 将时间戳转换为日期时间对象
    timestamp_datetime = datetime.datetime.fromtimestamp(timestamp)

    # 获取当前时间
    current_datetime = datetime.datetime.now()

    # 计算时间差
    time_difference = current_datetime - timestamp_datetime

    # 检查时间差是否大于3天
    if time_difference.days >= 3:
        return True
    else:
        return False
