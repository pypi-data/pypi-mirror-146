# JPWorkdays

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

>>> jpworkdays.workdays_between(datetime.date(2021, 1, 1), datetime.date(2021, 1, 5))
[datetime.date(2021, 1, 4), datetime.date(2021, 1, 5)]

# str型での日付入力も受け付けます(YYYY-MM-DD形式)
>>> jpworkdays.workdays_between(datetime.date(2021, 10, 20), "2021-10-26")
[datetime.date(2021, 10, 20), datetime.date(2021, 10, 21), datetime.date(2021, 10, 22), datetime.date(2021, 10, 25), datetime.date(2021, 10, 26)]
```

### 指定した日付以降で指定した数の営業日を取得

```python
>>> jpworkdays.workdays_from_date(datetime.date(2022, 4, 30), 5)
[datetime.date(2022, 5, 2), datetime.date(2022, 5, 6), datetime.date(2022, 5, 9), datetime.date(2022, 5, 10), datetime.date(2022, 5, 11)]

# 同様にstr型での日付入力が可能です(YYYY-MM-DD形式)
>>> jpworkdays.workdays_from_date("2021-12-01", 5)
[datetime.date(2021, 12, 1), datetime.date(2021, 12, 2), datetime.date(2021, 12, 3), datetime.date(2021, 12, 6), datetime.date(2021, 12, 7)]
```
