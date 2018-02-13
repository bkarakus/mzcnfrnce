from django import template
register = template.Library()

@register.filter(name='add_placeholder')
def add_placeholder(field):
    return field.as_widget(attrs={"placeholder":field.label})