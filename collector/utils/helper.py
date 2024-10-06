from django.contrib import admin


def json_default(value):
    import datetime
    if isinstance(value, datetime.datetime):
        return dict(year=value.year, month=value.month, day=value.day, hour=value.hour, minute=value.minute)
    elif isinstance(value, datetime.date):
        return dict(year=value.year, month=value.month, day=value.day)
    else:
        return value.__dict__


def toRID(txt):
    if txt == '':
        return ''
    s = txt.lower()
    x = s.replace(' ', '_').replace("'", '').replace('é', 'e') \
        .replace('è', 'e').replace('ë', 'e').replace('â', 'a') \
        .replace('ô', 'o').replace('"', '').replace('ï', 'i') \
        .replace('à', 'a').replace('-', '').replace('ö', 'oe') \
        .replace('ä', 'ae').replace('ü', 'ue').replace('ß', 'ss').replace('ç', 'c')
    return f'_{x.lower()}'


# # Converting lat/long to cartesian
# def get_cartesian(lat=None, lon=None):
#     import numpy as np
#     lat, lon = np.deg2rad(lat), np.deg2rad(lon)
#     R = 6371  # radius of the earth
#     x = R * np.cos(lat) * np.cos(lon)
#     y = R * np.cos(lat) * np.sin(lon)
#     z = R * np.sin(lat)
#     return x, y, z


def is_ajax(request):
    return request.headers.get('x-requested-with') == 'XMLHttpRequest'


def refix(modeladmin, request, queryset):
    for item in queryset:
        item.fix()
        item.save()
    short_description = 'Refix'

