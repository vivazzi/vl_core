from cms.extensions.toolbar import ExtensionToolbar
from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool
from cms.toolbar.items import Break
from cms.cms_toolbars import ADMIN_MENU_IDENTIFIER, ADMINISTRATION_BREAK, PAGE_MENU_IDENTIFIER, LANGUAGE_MENU_IDENTIFIER
from cms.utils.urlutils import admin_reverse
from django.conf import settings
from django.urls import reverse, NoReverseMatch
from django.utils.translation import gettext_lazy as _

from vl_core.constants import PAGE_MENU_LAST_BREAK_BEFORE_DELETE_PAGE


def remove_items(admin_menu):
    need_to_delete_items = [str(item) for item in (_('Users'), _('User settings'))]
    for item in admin_menu.items:
        for i, need_to_delete_item in enumerate(need_to_delete_items):
            if need_to_delete_item == getattr(item, 'name', '').replace('...', ''):
                admin_menu.remove_item(item)
                del need_to_delete_items[i]
                break

        if not need_to_delete_items:
            break


@toolbar_pool.register
class ExtendAdminMenuToolbar(CMSToolbar):

    def populate(self):
        if len(settings.LANGUAGES) == 1:
            language_menu = self.toolbar.get_menu(LANGUAGE_MENU_IDENTIFIER)
            if language_menu:
                self.toolbar.remove_item(language_menu)

        admin_menu = self.toolbar.get_or_create_menu(ADMIN_MENU_IDENTIFIER, _('Site settings'))

        remove_items(admin_menu)

        admin_menu.add_sideframe_item(_('Page types'), url=admin_reverse('cms_pagetype_changelist'), position=1)

        position = admin_menu.find_first(Break, identifier=ADMINISTRATION_BREAK).index + 1

        user_menu = admin_menu.get_or_create_menu('user_menu', _('Users and groups'), position=position)
        user_menu.add_sideframe_item(_('Users'), url=reverse(f'admin:{settings.AUTH_USER_MODEL.split(".")[0]}_user_changelist'))
        user_menu.add_sideframe_item(_('Groups'), url=reverse('admin:auth_group_changelist'))
        user_menu.add_break()
        user_menu.add_sideframe_item(_('User settings'), url=admin_reverse('cms_usersettings_change'))

        tech_menu = admin_menu.get_or_create_menu('tech_menu', _('Technical settings'), position=position + 1)
        tech_menu.add_link_item('SEO', url=reverse('vl_seo:seo'))
        tech_menu.add_link_item(_('Site utils'), url=reverse('vl_site_utils:utils'))
        tech_menu.add_link_item(_('Data size and backups'), url=reverse('vl_backup:backup_dashboard'))

        # help
        help_menu = self.toolbar.get_or_create_menu('help_menu', _('Help'))
        try:
            help_menu.add_modal_item(_('Site administration'), url=reverse('specs'))
        except NoReverseMatch:
            pass
        help_menu.add_link_item(_('Django CMS User Guide'), url='https://vits.pro/info/django-cms/')

        for key, obj in self.toolbar.toolbars.items():
            if isinstance(obj, ExtensionToolbar):
                page_menu = self.toolbar.get_or_create_menu(PAGE_MENU_IDENTIFIER, _('Page'))
                page_menu.add_break(PAGE_MENU_LAST_BREAK_BEFORE_DELETE_PAGE, len(page_menu.items)-1)
                break
