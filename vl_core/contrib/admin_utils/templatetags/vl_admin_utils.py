from django import template
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from sass_processor.processor import sass_processor

register = template.Library()


@register.simple_tag
def theming_url():
    return getattr(settings, 'ADMIN_TOOLS_THEMING_CSS', sass_processor('vl_admin_utils/theming.scss'))


@register.simple_tag
def admin_favicon_url():
    return getattr(settings, 'ADMIN_FAVICON_URL', staticfiles_storage.url('vl_admin_utils/favicon.svg'))
