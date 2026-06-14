from django import template
from urllib.parse import urlencode, urlparse, parse_qs
from collections import OrderedDict

register = template.Library()

@register.simple_tag(takes_context=True)
def query_transform(context, request_get, **kwargs):
    """
    Transform query parameters, preserving existing GET params and updating/overriding specified kwargs.
    Usage: ?{% query_transform request.GET page=2 category=1 %}
    """
    query_params = request_get.copy()
    
    for key, value in kwargs.items():
        if value:  # Only set if value is truthy
            query_params[key] = str(value)
        else:
            query_params.pop(key, None)  # Remove if empty
    
    # Remove page if not specified, but preserve others
    return urlencode(query_params)

