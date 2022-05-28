# vl_core

vl_core is core of Viva Library and contains some helpful functions (including functionality of VL plugins).

> [Viva Library](https://vits.pro/dev/) is helpful library for more fast creation of personal and corporate websites. This library
> can help to typical site task: content management (using django-cms plugin mechanism), seo, some utils and so on.

> **NOTE:** Documentation is writing and now here you can read description of some functionality only. 
> You can understand how it works by code comment in first time while documentation is not ready.


## Installation

There is no vl_core in PyPI, so you can install this package from repository only.

```shell
$ pip install git+https://github.com/vivazzi/vl_core.git
```

Also, you need install django-vite from repo: `https://github.com/vivazzi/django-vite/tree/multi-config` - this is fork
with extended functionality:

```shell
$ pip install git+https://github.com/vivazzi/django-vite.git@multi-config
```

## Configuration

Add "vl_core" to INSTALLED_APPS

```python
INSTALLED_APPS = (
    ...
    'vl_core',
    ...
)
```


## Base plugins

1. Snippet: https://github.com/vivazzi/vl_snippet

Other plugins with old version (first version was named SBL) are non-compatible, but you can look to these plugins
and take ideas for your project or help me upgrade old plugins to new version (please use pull request for it).

Plugins with old version:

1. Columns. sb_cols - https://bitbucket.org/vivazzi/sb_cols/
2. File. sb_file - https://bitbucket.org/vivazzi/sb_file/
3. Picture. sb_picture - https://bitbucket.org/vivazzi/sb_picture/
4. Gallery. sb_gallery - https://bitbucket.org/vivazzi/sb_gallery/
5. Slider. sb_slider - https://bitbucket.org/vivazzi/sb_slider/
6. Link/Button. sb_link - https://bitbucket.org/vivazzi/sb_link/
7. Forms. sb_form_base - https://bitbucket.org/vivazzi/sb_form_base/
8. Style. sb_style - https://bitbucket.org/vivazzi/sb_style/

## Documentation

vl_core contains many functions for different parts of site (admin utilities, handled images, shortcuts and other).

### vl_core

#### templatetags

- vl_admin

- vl_core

- vl_debug

- vl_math

- vl_url


#### utils

- core
- math
- os
- url - working with urls.


#### template_pool

Functionality that allows to include template field to model and work with template (for example, for rendering custom cms-plugins).


### admin_utils (vl_core.contrib.admin_utils)
Removes "application name" item from breadcrumbs. In most cases application name adds redundancy if django-admin-tools is used in admin interface.

#### Using:

Add `vl_core.contrib.admin_utils`, to `INSTALLED_APPS` before `django.contrib.admin`

```python
INSTALLED_APPS = (
    ...
    'vl_core.contrib.admin_utils',
    'django.contrib.admin',
    ...
)
```


### backup (vl_core.contrib.backup)

#### Management commands

1. `backup` (vl_core.contrib.admin_utils) - makes backup of database and media files and send it to backup server, if you have them. 
You should have setting like this

   ```python
   BACKUPS = [{'user': 'user_in_backup_server', 'host': '82.246.10.184'}, ...]
   ```

2. `generate_sitemap` (vl_core.contrib.seo) - generates sitemap.

Service commands:

1. `up_refs` - update commit id in Pipfile.lock for git packages (Those packages that install from git repository,
   for example, vl_snippet = {editable = true, git = "https://github.com/vivazzi/vl_snippet.git"}



### media_utils (vl_core.contrib.media_utils)

### seo (vl_core.contrib.seo)

### site_utils (vl_core.contrib.site_utils)


## Run tests

Run `python manage.py test vl_core`


# CONTRIBUTING

To reporting bugs or suggest improvements, please use the [issue tracker](https://github.com/vivazzi/vl_core/issues).

Thank you very much, that you would like to contribute to vl_core. Thanks to the [present, past and future contributors](https://github.com/vivazzi/vl_core/contributors).

If you think you have discovered a security issue in our code, please do not create issue or raise it in any public forum until we have had a chance to deal with it.
**For security issues use security@vuspace.pro**


# LINKS

- Project's home: https://github.com/vivazzi/vl_core
- Report bugs and suggest improvements: https://github.com/vivazzi/vl_core/issues
- Author's site, Artem Maltsev: https://vivazzi.pro

# LICENCE

Copyright © 2022 Artem Maltsev and contributors.

MIT licensed.
