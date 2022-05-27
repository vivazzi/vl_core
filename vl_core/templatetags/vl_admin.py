from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def get_block_name(context):
    if 'structure' not in context['request'].GET:
        return 'cms_js'
    return 'js'
