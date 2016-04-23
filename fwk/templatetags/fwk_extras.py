import datetime

from django import template
from django.conf import settings
from django.utils import timezone

register = template.Library()


def opening_hours(weekday):
    return [datetime.time(**{
        'hour': int(i.split(":")[0]),
        'minute': int(i.split(":")[1])
    }) for i in settings.FWK_OPENING_HOURS[weekday]]


@register.inclusion_tag("fwk/_opening_hours_reminder.html")
def opening_hours_reminder():

    # Traverse through all days of the week because it's possible that we're
    # only open one day of the week.
    for i in range(0, 7):
        now = timezone.now()
        today = now.date()
        next_day = now + datetime.timedelta(days=i)
        weekday = next_day.strftime("%a")

        # Receive timezone-aware opening hours
        opening_hrs = opening_hours(weekday)

        # Add date information to opening hours
        opening_dts = [datetime.datetime.combine(next_day, h) for h in opening_hrs]
        opening_dts = [timezone.get_default_timezone().localize(o) for o in opening_dts]

        # There are opening hours specified for this weekday, and if they
        # match the current time, just display that we're open.
        if opening_dts and opening_dts[0] < now < opening_dts[1]:
            return {'now_open': True}
        # There are opening hours specified, but they're not for today, so
        # they have to be for the next day that we're open. Display that.
        elif opening_dts and now < opening_dts[0]:

            context = {
                'now_open': False,
                'open_again': opening_dts[0],
            }

            if opening_dts[0].date() == today:
                context.update({'open_later_today': True})

            return context

