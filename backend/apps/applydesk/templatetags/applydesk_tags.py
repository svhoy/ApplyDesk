from django import template

from apps.applydesk.services.time_format import format_duration

register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, [])


@register.filter
def duration_hours(value):

    if value < 24:
        return f"{value:.1f} h"

    return f"{value / 24:.1f} d"


@register.filter
def format_duration_filter(value):
    return format_duration(value)
