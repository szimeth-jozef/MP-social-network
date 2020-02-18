from django import template

register = template.Library()


@register.filter(name='indexOf')
def indexOf(value, index):
    return value[index]