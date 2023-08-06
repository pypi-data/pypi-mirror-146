from django import template

register = template.Library()


@register.filter()
def multiply(value, arg):
    return float(value) * arg
@register.filter()
def totale(value):
    tot = 0
    qt = 0
    for key,values in value:
        tot += float(values['price'])*values['quantity']
        qt+=values['quantity']

    return tot
