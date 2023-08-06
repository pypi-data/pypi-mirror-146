# -*- coding: utf-8 -*-
from __future__ import annotations

from functools import singledispatch
from datetime import date, datetime, timedelta
import warnings

from . import registry
from . import holiday
from .exception import JPHolidayTypeError


def is_holiday_name(date: date | datetime | str) -> str | None:
    """
    その日の祝日名を返します。
    """

    # Covert
    date = _to_date(date)

    for holiday in registry.RegistryHolder.get_registry():
        if holiday.is_holiday_name(date):
            return holiday.is_holiday_name(date)

    return None


def is_holiday(date: date | datetime | str) -> bool:
    """
    その日が祝日かどうかを返します。
    """

    # Covert
    date = _to_date(value=date)

    for holiday in registry.RegistryHolder.get_registry():
        if holiday.is_holiday(date=date):
            return True

    return False


def year_holidays(year: int) -> list[tuple[date, str] | None]:
    """
    その年の祝日日、祝日名を返します。
    """
    date = datetime.date(year, 1, 1)

    output = []
    while date.year == year:
        name = is_holiday_name(date)
        if name is not None:
            output.append((date, name))

        date = date + timedelta(days=1)

    return output


def month_holidays(year: int, month: int) -> list[tuple[date, str] | None]:
    """
    その月の祝日日、祝日名を返します。
    """
    date = datetime.date(year, month, 1)

    output = []
    while date.month == month:
        name = is_holiday_name(date)
        if name is not None:
            output.append((date, name))

        date = date + timedelta(days=1)

    return output


def holidays(
    start_date: date | datetime | str,
    end_date: date | datetime | str,
    date_only: bool = False,
) -> list[tuple[date, str] | date | None]:
    """
    指定された期間の祝日日、祝日名を返します。
    """
    warnings.warn(
        "DeprecationWarning: Function 'jpholiday.holidays()' has moved to 'jpholiday.between()' in version '0.1.4' and will be removed in version '0.2'",
        UserWarning,
    )
    return between(start_date=start_date, end_date=end_date, date_only=date_only)


def between(
    start_date: date | datetime | str,
    end_date: date | datetime | str,
    date_only: bool = False,
) -> list[tuple[date, str] | date | None]:
    """
    指定された期間の祝日日、祝日名を返します。
    """

    # Covert
    start_date = _to_date(start_date)
    end_date = _to_date(end_date)

    output = []
    while start_date <= end_date:
        name = is_holiday_name(date=start_date)
        if name is not None:
            if date_only:
                output.append(start_date)
            else:
                output.append((start_date, name))

        start_date = start_date + timedelta(days=1)

    return output


def workdays_between(
    start_date: date | datetime | str,
    end_date: date | datetime | str,
    weekends: list[int] = [5, 6],
) -> list[date | None]:
    """指定された期間の営業日を返します。

    Parameters
    ----------
    start_date : date | datetime | str
        期間の開始日
    end_date : date | datetime | str
        期間の終了日
    weekends : list[int]
        週末として設定する曜日 by default [5, 6]

    Returns
    -------
    list[date | None]
        営業日のリスト

    """
    holidays = between(start_date=start_date, end_date=end_date, date_only=True)
    workdays = _workdays_between(
        start_date=start_date,
        end_date=end_date,
        holidays=holidays,
        weekends=weekends,
    )

    return workdays


def workdays_from_date(
    start_date: date | datetime | str,
    days: int,
    weekends: list[int] = [5, 6],
) -> list[date | None]:
    """指定された日付以降で指定された数の営業日を返します。

    Parameters
    ----------
    start_date : date | datetime | str
        期間の開始日
    days : int
        日数
    weekends : list[int]
        週末として設定する曜日 by default [5, 6]

    Returns
    -------
    list[date | None]
        営業日のリスト

    """
    # Covert
    start_date = _to_date(start_date)
    end_date = start_date + timedelta(days=days)

    holidays = between(start_date=start_date, end_date=end_date, date_only=True)
    workdays = _workdays_from_date(
        start_date=start_date,
        end_date=end_date,
        holidays=holidays,
        weekends=weekends,
    )

    return workdays


def _workdays_between(
    start_date: date | datetime | str,
    end_date: date | datetime | str,
    holidays: list[date | None],
    weekends: list[int],
):
    # Covert
    start_date = _to_date(start_date)
    end_date = _to_date(end_date)

    workdays = []
    while start_date <= end_date:
        if start_date.weekday() not in weekends and start_date not in holidays:
            workdays.append(start_date)
        start_date += timedelta(days=1)

    return workdays


def _workdays_from_date(
    start_date: date | datetime | str,
    end_date: date,
    holidays: list[date | None],
    weekends: list[int],
):
    workdays = []
    while start_date < end_date:
        if start_date.weekday() not in weekends and start_date not in holidays:
            workdays.append(start_date)
        else:
            end_date += timedelta(days=1)
        start_date += timedelta(days=1)

    return workdays


@singledispatch
def _to_date(value) -> None:
    """
    datetime型, str型をdate型へ変換
    それ以外は例外
    """
    raise JPHolidayTypeError("is type datetime or date isinstance only.")


@_to_date.register(date)
def _(value: date) -> date:
    return value


@_to_date.register(datetime)
def __(value: datetime) -> date:
    return value.date()


@_to_date.register(str)
def ___(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()
