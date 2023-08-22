from django import template
register = template.Library()
bad_words = [
    'плохая',
    'плохой',
    'bad',
    'гнилой'
]
@register.filter(name='Censor')

def Censor(value):

    for n in bad_words:
        value = value.lower().replace(n.lower(), '***')
    return value

