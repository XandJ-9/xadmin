#! usr/bin/python
# coding=utf-8

import datetime
import calendar


def formatStr2Date(dateStr, format='%Y%m%d'):
    """
    返回date
    将时间规格化，将String类型转化为date类型
    :param dateStr:
    :param format:
    :return:
    """
    return datetime.datetime.strptime(dateStr, format).date()


def formatStr2DateTime(dateStr, format='%Y%m%d%H%M%S'):
    """
    返回date
    将时间规格化，将String类型转化为date类型
    :param dateStr:
    :param format:
    :return:
    """
    return datetime.datetime.strptime(dateStr, format)


def formatStr2Date(dateStr, format='%Y%m%d'):
    """
    返回date
    将时间规格化，将String类型转化为date类型
    :param dateStr:
    :param format:
    :return:
    """
    return datetime.datetime.strptime(dateStr, format).date()

def getCurrentDate():
    """
    查询当前日期，返回类型date，如 2019-08-07
    :return:
    """
    return datetime.datetime.now().date()


def getCurrentTime():
    """
    :return:
    """
    return datetime.datetime.now()

def getTimeStamp(date):
    return datetime.datetime.timestamp(date)

def getNowTimestamp():
    return int(datetime.datetime.now().timestamp())

def getNDaysToday(ndays):
    """
    ndays:
    example:
    获取当前日期N天（负数向前推，正数向后推）的日期
    """
    return getNDaysDate(getCurrentDate(), ndays)

def getNDaysDate(date, ndays):
    """
    ndays:
    example:
    获取当前日期N天（负数向前推，正数向后推）的日期
    """
    ndate = date + datetime.timedelta(days=ndays)
    return ndate

def getNDaysDelta(date1, date2):
    """
    获取两个日期相差的天数，大的日期在前
    返回int，否则返回负数
    """
    return int((date1 - date2).days)


def getNMonthsToday(nMonths):
    """
    nMonths:参数传入的是正数表示往后 ，负数表示往前
    获取传入时间N个月的时间
    """
    return getNMonthsDate(getCurrentDate(), nMonths)

def getNMonthsDate(date, nMonths):
    """
    nMonths:参数传入的是正数表示往后 ，负数表示往前
    获取传入时间N个月的时间
    """
    month = date.month - 1 + nMonths
    year = int(date.year + month / 12)
    month = month % 12 + 1
    day = min(date.day, calendar.monthrange(year, month)[1])
    dateMonth = date.replace(year=year, month=month, day=day)
    return dateMonth


def getYearFirstDate(date):
    """
    获取年的第一天，返回date
    """
    return formatStr2Date(date.strftime('%Y') + '0101')

def getMonthFirstDate(date):
    """
    获取月的第一天，返回date
    """
    return formatStr2Date(date.strftime('%Y%m') + '01')

def getMonthLastDate(date):
    """
    计算传入日期的所属月的最后一天
    :param date:日期类型
    :return: 返回date
    """
    year = int(date.year)
    month = int(date.month)
    if month == 12:
        year += 1
        month = 1
    else:
        month += 1
    date_last = datetime.datetime(year, month, 1) - datetime.timedelta(1)
    return date_last.date()

def getWeekFirstDate(date):
    """
    获取周的第一天，返回date
    """
    dayscount = datetime.timedelta(days=date.isoweekday())
    dayfrom = date - dayscount + datetime.timedelta(days=1)
    return dayfrom

def getWeekLastDate(date):
    """
    获取周的最后一天，返回date
    """
    date_week = getWeekFirstDate(date) + datetime.timedelta(days=6)
    # 待完成
    return date_week

def getQuarterFirstDate(date):
    """
    计算传入日期的所属季度第一天
    :param date:
    :return:返回date类型
    """
    year = int(date.year)
    month = int(date.month)
    month_q = int((month - 1) / 3) * 3 + 1
    date_q_start = datetime.datetime(year, month_q, 1).date()
    return date_q_start

def getQuarterLastDate(date):
    """
    计算传入日期的所属季度最后一天
    :param date:
    :return:返回date类型
    """
    year = int(date.year)
    month = int(date.month)
    month_q = (int((month - 1) / 3) + 1) * 3
    date_q_start = datetime.datetime(year, month_q, 1)
    date_q_last = getMonthLastDate(date_q_start)
    return date_q_last
    
def getHalfaYearFirstDate(date):
    """
    计算传入日期的所属月的最后一天
    :param date:日期类型
    :return: 返回date
    """
    year = int(date.year)
    month = int(date.month)
    if month > 6:
        month = 7
    else:
        month = 1
    date_first = datetime.datetime(year, month, 1)
    return date_first.date()

def dateRange(start_date, end_date, step=1):
    """
    生成date类型的日期序列
    日期区间是[start_date, end_date]
    """
    days = (end_date - start_date).days + 1
    return [start_date + datetime.timedelta(i) for i in range(0, days, step)]

def get_date_dimension(date):
    """
    根据date日期(日期类型)，计算相关的时间维度数据

    :param date:传入的日期，date型
    :return:
    """
    row_date_dimension = pd.Series()
    row_date_dimension['DATE'] = date
    row_date_dimension['DATE_1D'] = getNDaysDate(date, -1)
    row_date_dimension['DATE_1W'] = getNDaysDate(date, -7)
    row_date_dimension['DATE_1M'] = getNMonthsDate(date, -1)
    row_date_dimension['DATE_2M'] = getNMonthsDate(date, -2)
    row_date_dimension['DATE_3M'] = getNMonthsDate(date, -3)
    row_date_dimension['DATE_6M'] = getNMonthsDate(date, -6)
    row_date_dimension['DATE_YTD'] = getYearFirstDate(date)
    row_date_dimension['DATE_1Y'] = getNMonthsDate(date, -12)
    row_date_dimension['DATE_2Y'] = getNMonthsDate(date, -12 * 2)
    row_date_dimension['DATE_3Y'] = getNMonthsDate(date, -12 * 3)
    row_date_dimension['DATE_5Y'] = getNMonthsDate(date, -12 * 5)

    row_date_dimension['DATE_MTD'] = getMonthFirstDate(date)
    row_date_dimension['DATE_WTD'] = getWeekFirstDate(date)
    row_date_dimension['DATE_QTD'] = getQuarterFirstDate(date)
    row_date_dimension['DATE_HTD'] = getHalfaYearFirstDate(date)
    # row_md_trade_cal = df_md_trade_cal.loc[end_date]
    # row_date_dimension = row_date_dimension.append(row_md_trade_cal)
    return row_date_dimension

if __name__ == '__main__':
    print(getCurrentDate())
    print(getNDaysToday(-5))
    print(getNDaysDate(getNDaysToday(-5), -2))
    print(getNDaysDelta(getNDaysToday(-5), getCurrentDate()))
    print(getNMonthsToday(1))
    print(getNMonthsDate(getCurrentDate(),-1))
    print(getNMonthsDate(formatStr2Date('20190228'), -1))
    print(getNMonthsDate(formatStr2Date('20190331'), -1))
    print(getNMonthsDate(formatStr2Date('20190331'), -1 * 12))
    # 如果想计算几年前的日期的话，用 计算月份数
    print(getYearFirstDate(getCurrentDate()))
    print(getMonthFirstDate(getCurrentDate()))
    print(getWeekFirstDate(getCurrentDate()))
    print(getWeekLastDate(getCurrentDate()))

    print(getMonthLastDate(getCurrentDate()))
    print(getQuarterLastDate(getCurrentDate()))
    print(getQuarterFirstDate(getCurrentDate()))
    print(getHalfaYearFirstDate(getCurrentDate()))

