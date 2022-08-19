from os.path import exists, splitext

from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.template.loader import render_to_string

from vl_core.contrib.media_utils.utils import default_compress_settings


def get_thumb_size(orig_w, orig_h, w=None, h=None):
    if not w and not h:
        raise Exception('You need set width or height size')

    if w and h:
        return w, h

    ratio = orig_w / orig_h

    if not w:
        return ratio * h, h

    return w, w / ratio


def _get_thumb_path(path: str, w: int, h: int):
    """
    :param path: path, url or name only
    :param w: width
    :param h: height
    :return: thumb path
    """
    filename, file_extension = splitext(path)
    return f'{filename}_{w or 0}x{h or 0}{file_extension}'


def thumb(path: str, w: int, h: int, coordinates=None):
    thumb_path = _get_thumb_path(path, w, h)
    if exists(thumb_path):
        with Image.open(thumb_path) as pic:
            w, h = pic.size
    elif exists(path):
        with Image.open(path) as new_pic:
            if coordinates:
                if any(coordinates) != all(coordinates):
                    raise Exception('You need specify all coordinates: x1, y1, x2, y2')

                new_pic = new_pic.crop(coordinates)

            # check aspect
            if h:
                thumb_ratio = w / h
                new_pic_ratio = new_pic.width / new_pic.height
                if thumb_ratio != new_pic_ratio:
                    th_dimension_w = new_pic.width
                    th_dimension_h = new_pic.width / thumb_ratio

                    if th_dimension_h > new_pic.height:
                        th_dimension_w = new_pic.height * thumb_ratio
                        th_dimension_h = new_pic.height

                    new_pic = new_pic.crop((0, 0, th_dimension_w, th_dimension_h))

            new_pic.thumbnail((w or 10000, h or 10000), resample=Image.ANTIALIAS)
            new_pic.save(thumb_path, **default_compress_settings(new_pic))
            w, h = new_pic.size

    return thumb_path, w, h


def thumb_from_field(pic_field, w, h, coordinates):
    if isinstance(pic_field, InMemoryUploadedFile):
        return '', w, h

    if exists(pic_field.path) and pic_field.is_svg():
        thumb_w, thumb_h = get_thumb_size(pic_field.width, pic_field.height, w, h)
        return pic_field.url, thumb_w, thumb_h

    thumb_path, thumb_w, thumb_h = thumb(pic_field.path, w, h, coordinates)
    thumb_url = _get_thumb_path(pic_field.url, w, h)

    return thumb_url, thumb_w, thumb_h


def thumb_data(field, width=None, height=None, coordinates=None):
    ctx = {'is_exists': True}

    if not field:  # if field is empty (file did not load in admin)
        url = None
        width = 0
        height = 0
        ctx['is_exists'] = False

    elif not exists(field.path):  # if field is missing (file loaded in admin, but missing on the disk)
        url = field.url
        if not width: width = 0
        if not height: height = 0
        ctx['is_exists'] = False

    elif not width and not height:  # it means display orig image
        url = field.url
        width = field.width
        height = field.height

    else:
        url, width, height = thumb_from_field(field, width, height, coordinates)

    ctx.update({'url': url,
                'width': width, 'height': height,
                'ratio': height / width if width else 0})

    return ctx


def thumb_html(field, width=None, height=None, coordinates=None, th_type='cover', tag='img', silent=False):
    """
    Get thumb as html

    :param field:
    :param width:
    :param height:
    :param coordinates: (x1, y1, x2, y2)
    :param th_type: cover or contain
    :param tag: html tag
    :param silent: silent for empty. If True, no display anything
    :return:
    """
    ctx = thumb_data(field, width, height, coordinates)

    ctx.update({
        'th_type': th_type,
        'ratio_percent': ctx['ratio'] * 100,
    })

    if not ctx['is_exists'] and not silent:
        return render_to_string('vl_media_utils/no_img.html', ctx)

    if not ctx['is_exists'] and silent:
        return ''

    return render_to_string(f'vl_media_utils/adaptive_th_{tag}.html', ctx)
