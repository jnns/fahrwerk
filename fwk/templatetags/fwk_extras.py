import warnings
import json
from datetime import date, datetime, timedelta, time

import requests

from django import template
try:
    from constance import config as settings
except ImportError:
    from django.conf import settings
from django.utils import timezone
from constance import config

register = template.Library()


def get_holidays(country="BE", year=None):
    """
    Return German holidays for a given country in a given year.

    The queried API is kindly provided by jarmedia.de who use Wikipedia as a
    data source. The returned output is a list of ``datetime.date`` objects.
    """

    HOLIDAY_BACKEND_URL = "http://feiertage.jarmedia.de/api/"

    payload = { 'jahr': year or date.today().year }
    if country:
        payload.update({ 'nur_land': country })

    r = requests.get(HOLIDAY_BACKEND_URL, params=payload)
    r.raise_for_status()  # raise exception in case of bad result

    return json.dumps(sorted([i["datum"] for i in r.json().values()]))


def holidays():
    if not config.FWK_DAYS_CLOSED:
        config.FWK_DAYS_CLOSED = get_holidays()

    string_list = json.loads(config.FWK_DAYS_CLOSED)

    # dates are returned in ISO-format ("YYYY-MM-DD") and need to be int-
    # casted and split
    date_list = sorted([ date(*map(int, i.split("-"))) for i in string_list ])

    # get a fresh list of holidays if no current dates are configured
    if not date.today().year in set([d.year for d in date_list]):
        config.FWK_DAYS_CLOSED = None
        holidays()

    return date_list


def opening_hours(weekday):
    warnings.warn("Please use `opening_hours_aware()` instead of `opening_hours()`")

    OPENING_HOURS = config.FWK_OPENING_HOURS
    if isinstance(OPENING_HOURS, basestring):
        OPENING_HOURS = json.loads(OPENING_HOURS)
    return [time(**{
        'hour': int(i.split(":")[0]),
        'minute': int(i.split(":")[1])
    }) for i in OPENING_HOURS[weekday]]

def opening_hours_aware():
    OPENING_HOURS = config.FWK_OPENING_HOURS
    if isinstance(OPENING_HOURS, basestring):
        OPENING_HOURS = json.loads(OPENING_HOURS)

        week = []

        for i in range(0, 7):
            now = timezone.now()
            next_day = now + timedelta(days=i)
            weekday = next_day.strftime("%a")

            day = []
            for h in OPENING_HOURS[weekday]:
                # convert "12:37" notation to time object
                t = time(*map(int, h.split(":")))
                # create timezone-aware datetime object
                day.append(
                    timezone.get_default_timezone().localize(datetime.combine(next_day, t))
                )
            week.append(day)

        return week



@register.inclusion_tag("fwk/_opening_hours_reminder.html")
def opening_hours_reminder():

    # Traverse through all days of the week because it's possible that we're
    # only open one day of the week.
    for i in range(0, 7):
        now = timezone.now()
        today = now.date()
        next_day = now + timedelta(days=i)
        weekday = next_day.strftime("%a")

        # Receive timezone-aware opening hours
        opening_hrs = opening_hours(weekday)

        # Add date information to opening hours
        opening_dts = [datetime.combine(next_day, h) for h in opening_hrs]
        opening_dts = [timezone.get_default_timezone().localize(o) for o in opening_dts]

        if not opening_dts:
            continue

        # If opening hours match the current time, just display that we're
        # open (unless it's a holiday):
        if opening_dts[0] < now < opening_dts[1] and today not in holidays():
            # remind the client about the late surcharge
            if opening_dts[1] - now < timedelta(hours=1):
                return {'late_surcharge': True, 'closing': opening_dts[1]}
            return

        # There are opening hours specified for the future
        elif now < opening_dts[0] and opening_dts[0].date() not in holidays():
            context = {
                'open_again': opening_dts[0],
            }

            if opening_dts[0].date() == today:
                context.update({'open_later_today': True})

            return context

