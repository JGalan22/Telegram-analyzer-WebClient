from django import template


register = template.Library()

@register.filter(name='obfuscate_string')
def obfuscate_string(value:str):
    list_words = value.split()
    result = ''
    for item in list_words:
      length = len(item)
      result = result + length*'*'+ ' '
    return result