"""
---> Simple Filter <---
@register.filter
def to_uppercase(value): # Use -> {{ some_variable|to_uppercase }}
    if not isinstance(value, str):
        return value
    return value.upper()
    

---> Filter with Arguments <---
@register.filter
def truncate_chars(value, num_chars): # Use -> {{ some_variable|truncate_chars:10 }}
    if not isinstance(value, str) or not isinstance(num_chars, int):
        return value
    return value[:num_chars] + "..." if len(value) > num_chars else value
"""
from datetime import timedelta
from django import template

register = template.Library()

@register.filter
def readtime(seconds): # Use -> {{ some_variable|to_uppercase }}
    if not seconds:
        return "1 Minute"

    # Handle timedelta
    if isinstance(seconds, timedelta):
        total_seconds = int(seconds.total_seconds())
    else:
        try:
            total_seconds = int(seconds)
        except (TypeError, ValueError):
            return "1 Minute"

    if total_seconds < 60:
        return "1 Minute"

    minutes = total_seconds // 60

    if minutes < 60:
        return f"{minutes} Minute{'s' if minutes != 1 else ''}"

    hours = minutes // 60
    return f"{hours} Hour{'s' if hours != 1 else ''}"
    