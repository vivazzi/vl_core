import decimal


def replace_comma_to_point(value):
    return str(value).replace(',', '.')


def separate_thousand(value, char=' '):
    result = ''
    parts = str(value).split()
    for part in parts:
        try:
            n = '{0:,} '.format(decimal.Decimal(part))
            if char != ',':
                n = n.replace(',', char)

            result += n
        except decimal.InvalidOperation:
            result += '{} '.format(part)
    return result.replace('  ', ' ').strip()
