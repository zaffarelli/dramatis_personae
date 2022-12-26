from django.template.loader import get_template


def json_default(value):
    import datetime, uuid
    if isinstance(value, datetime.datetime):
        return dict(year=value.year, month=value.month, day=value.day, hour=value.hour, minute=value.minute)
    elif isinstance(value, datetime.date):
        return dict(year=value.year, month=value.month, day=value.day)
    elif isinstance(value, uuid.UUID):
        return dict(hex=value.hex)
    else:
        return value.__dict__


def adventure_tag(label, value, front="#F0C040", back="transparent"):
    svg = ""
    if value:
        context = {'label': label, 'front': front, "back": back}
        template = get_template('scenarist/svg/adventure_tag.svg')
        svg = template.render(context)
        #print(svg)
    return svg
