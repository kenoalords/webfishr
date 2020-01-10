from django import template
import numpy as np

register = template.Library()

def package_discount(regular_price, sale_price):
    if regular_price > sale_price:
        discount = int(round((regular_price - sale_price)/regular_price * 100, 0))
        return '%s%s' % (discount, '%')
    else:
        return ''

register.filter('package_discount', package_discount)
