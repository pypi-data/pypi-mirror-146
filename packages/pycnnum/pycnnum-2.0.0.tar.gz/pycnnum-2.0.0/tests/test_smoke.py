"""All tests for number conversions
"""

import pytest

from pycnnum import cn2num, num2cn


def _test_num2cn(num: int | float, cn_value: str, **kwargs) -> None:
    """Test number to Chinese string"""

    my_cn = num2cn(num, **kwargs)
    print(f"{num = }, {my_cn = }")
    assert my_cn == cn_value


@pytest.mark.parametrize(
    "num,cn_value",
    [(3.4, "三点四"), ("3.4", "三点四"), (101, "一百零一"), (1821010, "一百八十二万一千零一十")],
)
def test_num2cn(num: int | float, cn_value: str) -> None:
    """Test number to Chinese string"""

    _test_num2cn(num, cn_value)


def test_num2cn_special() -> None:
    """Test num2cn special cases"""
    _test_num2cn(0, "〇", alt_zero=True)
    _test_num2cn(0.22, "〇点二二", alt_zero=True, alt_two=True)
    _test_num2cn(2222, "两千两百二十二", alt_two=True)
    _test_num2cn(25, "二十五", alt_two=True)
    _test_num2cn(2401, "两千四百零一", alt_two=True)
    _test_num2cn(2401, "贰仟肆佰零壹", alt_two=True, capitalize=True)
    _test_num2cn(2401, "兩仟四佰零一", alt_two=True, traditional=True)
    _test_num2cn(101, "一百〇一", alt_zero=True)
    _test_num2cn(0.5, "〇点五", alt_zero=True)


def _test_cn2num(cn_value: str, num: int | float, **kwargs) -> None:
    """Test Chinese string to number"""

    my_num = cn2num(cn_value, **kwargs)
    print(f"{cn_value = }, {my_num = }")
    assert my_num == num


@pytest.mark.parametrize(
    "num,cn_value",
    [(3.4, "三点四"), (101, "一百零一"), (-101, "负一百零一"), (1821010, "一百八十二万一千零一十"), (-15, "负十五"), (0.5, "点五"), (0.25, "点二五")],
)
def test_cn2num(num: int | float, cn_value: str) -> None:
    """Test Chinese string to number"""

    _test_cn2num(cn_value, num)
