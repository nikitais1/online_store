from django import template

register = template.Library()


@register.filter()
def mymedia(value):
    if value:
        return f'/media/{value}'
    return '#'


@register.filter()
def my_description(value):
    return value[:100]
