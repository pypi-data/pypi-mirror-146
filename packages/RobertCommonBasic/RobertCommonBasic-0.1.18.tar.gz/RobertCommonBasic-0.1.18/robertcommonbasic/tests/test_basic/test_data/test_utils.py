
from robertcommonbasic.basic.data.utils import format_value

def test_format_value():

    print(f"format_value('1.234', '1') = {format_value('1.234', '1')}")
    print(f"format_value('1.234', '-2.0') = {format_value('1.234', '-2.0')}")
    print(f"format_value('-1.234', '2.0') = {format_value('-1.234', '2.0')}")
    print(f"format_value('-1.234', 'v*3') = {format_value('-1.234', 'v*3')}")
    print(f"format_value('测试', '1') = {format_value('测试', '1')}")
    print(f"format_value('测试', '1.2') = {format_value('测试', '1.2')}")
    print(f"format_value('1.234', '') = {format_value('1.234', '')}")

    print(f"format_value('1.234', 'int(v)') = {format_value('1.234', 'int(v)')}")
    print(f"format_value('1.234', 'int(v)') = {format_value('1.234', 'int(v)')}")
    print(f"format_value('2, 'bit(v, 1)') = {format_value('2', 'bit(v, 1)')}")   #取位操作
    print(f"format_value('35535, 'signed(v)') = {format_value('35535', 'signed(v)')}")  # 取位操作
    print(f"format_value('1.234', '1 if v == 20.1234 else 0') = {format_value('1.234', '1 if v == 1.234 else 0')}")

    print()

def test_format_value2():
    print(format_value('5.0', '1 if v == 5 else 0'))
    print(format_value('2', '_or(bit(v, 1), bit(v, 0), _and(bit(v, 0),bit(v, 1)))'))


test_format_value2()