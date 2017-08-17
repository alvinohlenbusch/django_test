from django import template
register = template.Library()

@register.filter(name='get')
def get(d, k):
    try:
        attr = getattr(d, k)
    except AttributeError:
        attr = d.get(k, 'default')
    
    return attr