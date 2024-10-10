from datetime import datetime, timedelta
import pytz
import schedule
import time
import ntplib
from pandas.tseries.offsets import BDay
#from workalendar.asia import China
from chinese_calendar import is_holiday

# 将日期调整到最近的工作日
def adjust_date_to_weekday(date):
    # cal = China()
    # print(cal)
    # 如果提供的日期是周末或者节假日，将其调整为最近的工作日
    while date.weekday() > 4 or is_holiday(date):  # 0 = Monday, 1=Tuesday, 2=Wednesday...
        date -= timedelta(days=1)  # 减去一天
    return date


def get_network_time():
    # 创建一个 NTPClient 对象
    client = ntplib.NTPClient()

    # 获取网络时间（UTC）
    response = client.request("pool.ntp.org")

    timestamp = response.tx_time
    network_time = datetime.fromtimestamp(timestamp)

    # 获取本地时区
    local_timezone = pytz.timezone("Asia/Shanghai")  # 例如 'Asia/Shanghai'
    # 从时区上获得的本地时间理论上与网络时间一致，可能存在一些网络延迟,但影响不大
    local_time = network_time.astimezone(local_timezone)

    # print(local_time.hour)
    # print(network_time.hour)
    return local_time


def get_local_time():
    local_time = datetime.now()
    return local_time
