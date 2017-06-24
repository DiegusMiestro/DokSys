from django import template

register = template.Library()

@register.filter(name='joinby')
def joinby(objects, arg):
    temp = []
    for word in objects:
        temp.append(word.title)
    return arg.join(temp)
