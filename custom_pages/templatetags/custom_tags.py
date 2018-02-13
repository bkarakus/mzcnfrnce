from django.template.loader import get_template
from django.template.context import Context
from django.template.defaultfilters import stringfilter

from mezzanine.pages.models import Page
from mezzanine import template

from bootstrapform.templatetags.bootstrap import is_checkbox, is_file, is_radio, is_multiple_checkbox

register = template.Library()

@register.filter
def add_placeholder(field):
    if not is_checkbox(field) and not is_multiple_checkbox(field) \
       and not is_radio(field) and not is_file(field):
        field.field.widget.attrs['placeholder'] = field.label
        return field

@register.filter(is_safe=True)
@stringfilter
def address(value):
    """
    Adds slashes before quotes. Useful for escaping strings in CSV, for
    example. Less useful for escaping JavaScript; use the ``escapejs``
    filter instead.
    """
    return value.replace('|', '<br >')

@register.assignment_tag(takes_context=True)
def get_page(context, page_slug):
    try:
        page = Page.objects.get(slug=page_slug)
        page = page.get_content_model()
    except:
        page = None
    return page

@register.assignment_tag(takes_context=True)
def get_page_with_children(context, page_slug):
    try:
        page = Page.objects.get(slug=page_slug)
        page = page.get_content_model()
    except:
        page = None
    else:
        rel = [m.__name__.lower() for m in Page.get_content_models()]
        page.published_children = Page.objects.published().filter(parent=page).order_by('_order').select_related(*rel)
    return page

@register.render_tag
def render_page(context, token):
    page_slug, template_name = token.split_contents()[1:]
    context['page'] = get_page_with_children(context, page_slug)
    t = get_template(template_name)
    return t.render(Context(context))

@register.assignment_tag(takes_context=True)
def get_page_children(context, page=None):
    children = None
    if isinstance(page, str):
        page = Page.objects.get(slug=page)

    if not page and 'page' in context:
        page = context['page']

    if page:
        rel = [m.__name__.lower() for m in Page.get_content_models()]
        children = Page.objects.published().filter(parent=page).order_by('_order').select_related(*rel)
    
    return children