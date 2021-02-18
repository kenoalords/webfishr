from django import template
import numpy as np

register = template.Library()

def pricing(package, request):
    try:
        if request.location == 'NG':
            return f"N{package.sale_price:,}"
        else:
            return f"${package.sale_price_usd:,}"
    except Exception:
        return f"N{package.sale_price:,}"
register.filter('pricing', pricing)

def pricing_regular(package, request):
    try:
        if request.location == 'NG':
            return f"N{package.regular_price:,}"
        else:
            return f"${package.regular_price_usd:,}"
    except Exception:
        return f"N{package.regular_price:,}"
register.filter('pricing_regular', pricing_regular)
