"""
---> Simple Tag <---
@register.simple_tag
def current_year(): # Use -> {% current_year %}
    from datetime import datetime
    return datetime.now().year


---> Tag with Arguments <---
@register.simple_tag
def multiply(value1, value2): # Use -> {% multiply 5 10 %}
    return value1 * value2
"""
from django import template

register = template.Library()

