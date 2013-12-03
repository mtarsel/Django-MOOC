from django import template

register = template.Library()

@register.filter
def lookup(dict, key):
    return dict[key]
