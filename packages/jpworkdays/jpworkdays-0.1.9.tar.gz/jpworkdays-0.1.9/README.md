# JPWorkdays

![PyPI](https://img.shields.io/pypi/v/jpworkdays)
![GitHub](https://img.shields.io/github/license/discus0434/jp-workdays)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/jpworkdays)

国民の休日を考慮して営業日を取得するライブラリ

[JPHoliday](https://github.com/Lalcs/jpholiday)からのフォークです。

## Installation

```bash
pip install jpworkdays
```

## Sample Code (JPHolidayからの変更点のみ)

### 指定期間の営業日を取得

```python
import jpworkdays
import datetime

# 2021年1月1日から2021年1月5日までの営業日を取得
>>> jpworkdays.workdays_between(datetime.date(2021, 1, 1), datetime.date(2021, 1, 5))
[datetime.date(2021, 1, 4), datetime.date(2021, 1, 5)]

# str型での日付入力も可能です(YYYY-MM-DD形式)
# 2021年10月20日から2021年10月26日までの営業日を取得
>>> jpworkdays.workdays_between("2021-10-20", "2021-10-26")
[datetime.date(2021, 10, 20), datetime.date(2021, 10, 21), datetime.date(2021, 10, 22), datetime.date(2021, 10, 25), datetime.date(2021, 10, 26)]

# 期間の始端・終端指定が逆になっていてもOKです
>>> jpworkdays.workdays_between("2022-03-23", "2022-03-18")
[datetime.date(2022, 3, 18), datetime.date(2022, 3, 22), datetime.date(2022, 3, 23)]
```

### 指定した日付以降で指定した数の営業日を取得

```python
# 2022年4月30日以降の5営業日を取得
>>> jpworkdays.workdays_from_date(datetime.date(2022, 4, 30), 5)
[datetime.date(2022, 5, 2), datetime.date(2022, 5, 6), datetime.date(2022, 5, 9), datetime.date(2022, 5, 10), datetime.date(2022, 5, 11)]

# 同様にstr型での日付入力が可能です(YYYY-MM-DD形式)
# 2021年12月1日以降の5営業日を取得
>>> jpworkdays.workdays_from_date("2021-12-01", 5)
[datetime.date(2021, 12, 1), datetime.date(2021, 12, 2), datetime.date(2021, 12, 3), datetime.date(2021, 12, 6), datetime.date(2021, 12, 7)]

# 負の数で営業日を指定すると、指定した日付以前から指定した数の営業日を取得します
# 2022年4月28日以前の3営業日を取得
>>> jpworkdays.workdays_from_date(datetime.date(2022, 4, 28), -3)
[datetime.date(2022, 4, 28), datetime.date(2022, 4, 27), datetime.date(2022, 4, 26)]
```
