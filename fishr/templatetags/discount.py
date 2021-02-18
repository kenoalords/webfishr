from django import template
import numpy as np

register = template.Library()

def package_discount(package, request):
    if request.location == "NG":
        if package.regular_price > package.sale_price:
            discount = int(round((package.regular_price - package.sale_price)/package.regular_price * 100, 0))
            return '%s%s' % (discount, '%')
        else:
            return ''
    else:
        if package.regular_price_usd > package.sale_price_usd:
            discount = int(round((package.regular_price_usd - package.sale_price_usd)/package.regular_price_usd * 100, 0))
            return '%s%s' % (discount, '%')
        else:
            return ''
register.filter('package_discount', package_discount)
