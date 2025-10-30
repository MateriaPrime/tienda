# crea la carpeta catalogo/templatetags/ con __init__.py
from django import template
register = template.Library()

@register.filter
def mul(a, b):
    try:
        return float(a) * float(b)
    except (TypeError, ValueError):
        return ""
