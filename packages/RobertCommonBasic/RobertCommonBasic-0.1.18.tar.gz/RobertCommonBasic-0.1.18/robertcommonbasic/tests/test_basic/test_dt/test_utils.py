from robertcommonbasic.basic.dt.utils import get_datetime, convert_time_by_timezone, get_timezone, parse_time


def test_time():
    tm = get_datetime('Asia/Shanghai').astimezone(get_timezone(str('UTC'))[0])
    utc = convert_time_by_timezone(get_datetime(), 'Asia/Shanghai', 'UTC')
    print(utc)


def test_parse_time():
    dt1 = parse_time('03/17/2022 10:33:00 AM')
    print(dt1)

    dt2 = parse_time('03/17/2022 10:33:00 PM')
    print(dt2)

    print()

test_time()