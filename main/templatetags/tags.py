from django import template

register = template.Library()


@register.filter(name='separator')
def thousand_separator(value):
    return "{:,}".format(value).replace(',', '.')
