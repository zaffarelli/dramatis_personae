'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django import template
from collector.models.character import Character
from collector.models.spacecraft import Spaceship
from collector.models.loot import Loot
import re
import string
from django.template.defaultfilters import dictsort

register = template.Library()


@register.filter(name='modulo')
def modulo(num, val):
    return num % val


@register.filter(name='as_bullets')
def as_bullets(value):
    """ Change int value to list of bullet (in the "Mark Rein*Hagen" style)
    """
    one = '<i class="fas fa-circle fa-xs" title="%d toto"></i>' % (value)
    blank = '<i class="fas fa-circle fa-xs blank" title="%d"></i>' % (value)
    x = 0
    res = ''
    while x < 10:
        if x < int(value):
            res += one
        else:
            res += blank
        if (x + 1) % 5 == 0:
            res += '<br/>'
        x += 1
    return res


@register.filter(name='as_bullets_short')
def as_bullets_short(value):
    """ 
        Change int value to list of bullet (in the "Mark Rein*Hagen" style). 
        Do it with a width limit of 10
    """
    if isinstance(value, int):
        one_very_high = '<i class="fas fa-circle fa-xs veryhigh" title="%d bullet_short"></i>' % (int(value))
        one_high = '<i class="fas fa-circle fa-xs high" title="%d bullet_short"></i>' % (int(value))
        one_medium = '<i class="fas fa-circle fa-xs medium" title="%d bullet_short"></i>' % (int(value))
        one_low = '<i class="fas fa-circle fa-xs low" title="%d bullet_short"></i>' % (int(value))
        blank = '<i class="fas fa-circle fa-xs blank" title="%d bullet_short"></i>' % (int(value))
        special_blank = '<i class="fas fa-circle fa-xs special_blank" title="%d bullet_short"></i>' % (int(value))
        x = 0
        res = ''
        while x < 20:
            if x < int(value):
                if x > 6:
                    res += one_very_high
                elif x > 4:
                    res += one_high
                elif x > 2:
                    res += one_medium
                else:
                    res += one_low
            else:
                if (x + 1) % 5 == 0:
                    res += special_blank
                else:
                    res += blank
            if (x + 1) % 10 == 0:
                res += '<br/>'
            x += 1
        return res
    else:
        return "ERROR!"


@register.filter(name='as_bullets_short_wildcard')
def as_bullets_short_wildcard(value):
    """ Change int value to list of bullet (Mark Rein*Hagen like)
    """
    if isinstance(value, int):
        one_low = '<i class="fas fa-circle fa-xs wildcard" title="%d" name="bullet_short_wildcard"></i>' % (int(value))
        blank = '<i class="fas fa-circle fa-xs blank" title="%d" name="bullet_short_wildcard"></i>' % (int(value))
        x = 0
        res = ''
        while x < 10:
            if x < int(value):
                res += one_low
            else:
                res += blank
            if (x + 1) % 10 == 0:
                res += '<br/>'
            x += 1
        return res
    else:
        return "ERROR!"


def char_to_tag(sym, tag, src_txt, changes, prefix='', paragraph=False):
    search = "[A-Za-z0-9\é\è\ô\ö\à\s\.\'\;\-\(\)\&\:\,]+"
    pattern = f'\{sym}{search}\{sym}'
    seeker = re.compile(pattern)
    iter = seeker.finditer(src_txt)
    for item in iter:
        occ = ''.join(item.group().split(sym))
        if paragraph:
            replacement_str = f'<{tag}>{prefix}{occ}</{tag}>'
        else:
            replacement_str = f'<{tag}>{prefix}{occ}</{tag}>'
        changes.append({'src': item.group(), 'dst': replacement_str})
        # print(f'(C2T:{sym}) --> {replacement_str}')
    return


@register.filter(name='parse_avatars')
def parse_avatars(value):
    """ Replace avatars rids by html links in a text """
    value = "<br/>".join(value.split("\n"))
    txt = str(value)
    changes = []
    # Simple replacements
    char_to_tag('§', 'strong', txt, changes)
    char_to_tag('£', 'em', txt, changes)
    char_to_tag('=', 'h5', txt, changes, prefix='<i class="fa fa-square"></i> ')
    char_to_tag('µ', 'h6', txt, changes, prefix='<i class="fa fa-minus"></i> ')
    # RollCheck
    sym = '%'
    search = "[A-Za-z0-9\é\è\ô\ö\à\s\.\'\;\-\(\)\&\:\,\_]+"
    pattern = "\%s%s\%s" % (sym, search, sym)
    seeker = re.compile(pattern)
    iter = seeker.finditer(txt)
    for item in iter:
        occ = ''.join(item.group().split(sym))
        from optimizer.utils.gaming import rollcheck
        txt, title = rollcheck(occ)
        replacement_string = f'<div class="embedded_link" title="{title}">{txt}</div>'
        print(replacement_string)
        changes.append({'src': item.group(), 'dst': replacement_string})

    # Characters
    seeker = re.compile('\¤(\w+)\¤')
    iter = seeker.finditer(txt)
    for item in iter:
        rid = ''.join(item.group().split('¤'))
        try:
            ch = Character.objects.get(rid=rid)
        except Character.DoesNotExist:
            ch = None
        if ch is not None:
            str_name = ch.full_name
            if ch.alias:
                str_name = f'{ch.alias} ({ch.full_name})'
            replacement_string = '<span id="%d" class="character_link embedded_link" title="%s:\n%s">%s %s</span>' % (
                ch.id, ch.full_name, ch.entrance, str_name,
                "<i class='fa fa-angle-double-up'></i>" if ch.balanced == True else "<i class='fa fa-angle-double-down'></i>")
        else:
            replacement_string = '<span class="embedded_link broken">[%s&dagger;]</span>' % (rid)
        changes.append({'src': item.group(), 'dst': replacement_string})
        # print(replacement_string)
    # Ships
    sym = '^'
    seeker = re.compile(f'\^(\w+)\^')
    iter = seeker.finditer(txt)
    for item in iter:
        rid = ''.join(item.group().split('^'))
        try:
            ch = Spaceship.objects.get(full_name=rid)
        except Spaceship.DoesNotExist:
            ch = None
        if ch is not None:
            replacement_string = '<span id="%d" class="character_link embedded_link" title="%s">%s %s</span>' % (
                ch.id, ch.ship_ref, ch.full_name,
                "(<i class='fa fa-anchor'></i>)" if ch.ship_ref.ship_status == "combat_ready" else "&dagger;")
        else:
            replacement_string = '<span class="embedded_link broken">[%s&dagger;]</span>' % (rid)
        changes.append({'src': item.group(), 'dst': replacement_string})

    # Sleeve article
    sym = '°'
    search = "[A-Za-z0-9\é\è\ô\ö\à\s\.\'\;\-\(\)\&\:\,\_]+"
    pattern = "\%s%s\%s" % (sym, search, sym)
    seeker = re.compile(pattern)
    iter = seeker.finditer(txt)
    for item in iter:
        occ = ''.join(item.group().split(sym))
        loot = Loot.objects.filter(code=occ).first()
        repstr = "<div class='loot'>"
        repstr += "<strong>%s (%d)</strong><ul>" % (loot.name, loot.id)
        repstr += "<ul>"
        repstr += "<li>Response DV: <em>%d</em></li>" % (10 + loot.sleeves_fame * loot.sleeves_gossip)
        repstr += "<li>Number of people participating to the auction: %d</li>" % (
                loot.sleeves_authenticity * loot.sleeves_fame)
        repstr += "<li>Highest auction: <em>£%d</em></li>" % (
                loot.sleeves_gossip * loot.sleeves_fame * loot.sleeves_minimum_increment + loot.price + loot.sleeves_auction * 3)
        repstr += "<li>Group: %s</li>" % (loot.group)
        repstr += "<li>Estimated value: <em>£%d</em></li>" % (loot.price)
        repstr += "</ul><ul>"
        repstr += "<li>Fame: %d</li>" % (loot.sleeves_fame)
        repstr += "<li>Gossip: %d</li>" % (loot.sleeves_gossip)
        repstr += "<li>Authenticity: %d</li>" % (loot.sleeves_authenticity)
        repstr += "<li>Base auction: <em>£%d</em></li>" % (loot.sleeves_auction)
        repstr += "<li>Step: +£%d</li>" % (loot.sleeves_minimum_increment)
        repstr += "</ul>"
        repstr += "<p><strong>Procurrer:</strong> %s of %s</p>" % (loot.owner.full_name, loot.owner.alliance)
        if loot.description:
            repstr += "<strong>Description:</strong>"
            repstr += "<p>%s</p>" % (loot.description)
        if loot.secret:
            repstr += "<strong>Notes:</strong>"
            repstr += "<p>%s</p>" % (loot.secret)
        repstr += "</div>"
        changes.append({'src': item.group(), 'dst': repstr})
    # Apply all changes
    for change in changes:
        txt = txt.replace(change['src'], change['dst'])
    return txt


@register.filter(name='dictsort_3cols')
def dictsort_3cols(value, ref):
    mylist = dictsort(value, ref)
    count = len(mylist)
    rowcount = int(count / 3)
    if count % 3 != 0:
        rowcount += 1
    idx = 0
    cols = [[], [], []]
    for x in dictsort(value, ref):
        c = int(idx / rowcount)
        cols[c].append(x)
        idx += 1
    flat_cols = []
    for idx in range(rowcount):
        if len(cols[0]) > idx:
            flat_cols.append(cols[0][idx])
        if len(cols[1]) > idx:
            flat_cols.append(cols[1][idx])
        if len(cols[2]) > idx:
            flat_cols.append(cols[2][idx])
    return flat_cols


@register.filter(name='signed')
def signed(value):
    return "%+d" % (int(value))


@register.filter(name='as_root')
def as_root(value):
    return "<b>%s</b>" % (value)


@register.filter(name='as_specialty')
def as_specialty(value):
    x = value.split('(')[1]
    val = x.split(')')[0]
    return "&gt;&nbsp;<i>%s</i>" % (val)


@register.filter(name='as_lifepath')
def as_lifepath(value):
    lp = {'0': 'Race', '5': 'Race Balance', '10': 'Upbringing', '20': 'Apprenticeship', '30': 'Early Career',
          '40': 'Tour of Duty', '50': 'Worldly Benefits', '60': 'Nameless Kit'}
    return "%s" % (lp[value])


@register.filter(name='prettybool')
def prettybool(value):
    if value == True:
        res = '<i class="fas fa-check" style="color:green;"></i>'
    else:
        res = '<i class="fas fa-times" style="color:red;"></i>'
    return res


@register.filter(name='prettyhistory')
def prettyhistory(value):
    if value == True:
        res = '<i class="fas fa-monument" style="color:yellow;"></i>'
    else:
        res = '<i class="fas fa-times" style="color:red;"></i>'
    return res


@register.filter(name='as_height')
def as_height(value):
    res = value
    """ Display height in meters """
    if isinstance(value,int):
        res = "%2.2f m" % (value / 100)
    return res


@register.filter(name='as_weight')
def as_weight(value):
    res = value
    """ Display weight in kilograms """
    if isinstance(value, int):
        res = "%3d kg" % (value)
    return res


@register.filter(name='as_pa_short')
def as_pa_short(value):
    """ Display weight in kilograms """
    PA = {
        "PA_STR": "STR",
        "PA_CON": "CON",
        "PA_BOD": "BOD",
        "PA_MOV": "MOV",
        "PA_INT": "INT",
        "PA_WIL": "WIL",
        "PA_TEM": "TEM",
        "PA_PRE": "PRE",
        "PA_TEC": "TEC",
        "PA_REF": "REF",
        "PA_AGI": "AGI",
        "PA_AWA": "AWA",
        "OCC_LVL": "Occult",
        "OCC_DRK": "Darkside",
        "": "Error!",
    }
    return PA[value]


@register.filter(name='as_roman')
def as_roman(value):
    if isinstance(int(value), int):
        value = int(value)
        ROMAN = [
            (1000, "M"),
            (900, "CM"),
            (500, "D"),
            (400, "CD"),
            (100, "C"),
            (90, "XC"),
            (50, "L"),
            (40, "XL"),
            (10, "X"),
            (9, "IX"),
            (5, "V"),
            (4, "IV"),
            (1, "I"),
        ]
        result = ""
        for (arabic, roman) in ROMAN:
            (factor, value) = divmod(value, arabic)
            result += roman * factor
    else:
        result = value
    return result


@register.filter(name='wound')
def wound(value):
    if value == '':
        value = 0
    res = int(value)
    if res > 0:
        res = "<span class='wounded'>%d</span>" % (value)
    return res


@register.filter(name='parse_stories')
def parse_stories(value):
    txt = ""
    arr = value.split('#')
    lst = list(filter(None, arr))
    new_lst = []
    for item in lst:
        x = item.split('_')
        new_lst.append(f'{x[0]}={x[1]}')
    txt += ", ".join(new_lst)
    txt += "."
    return txt


@register.filter(name='extract_id')
def extract_id(value):
    import json
    x = json.load(value)
    return x[id]


@register.filter(name='as_media_image')
def as_media_image(value):
    str = f'images/f_{value}.jpg'
    from django.core.files.storage import default_storage
    if default_storage.exists(str):
        str = f'media/images/f_{value}.jpg'
    else:
        str = 'media/images/f_blank.jpg'
    return str


@register.filter(name='as_media_video')
def as_media_video(value):
    str = f'images/{value}.jpg'
    from django.core.files.storage import default_storage
    if default_storage.exists(str):
        str = f'media/images/{value}.mp4'
    return str


@register.filter(name='media_check')
def media_check(value):
    str = f'images/f_{value}.jpg'
    from django.core.files.storage import default_storage
    if default_storage.exists(str):
        str = '<span class="golden"><i class="fas fa-portrait"></i></span>'
    else:
        str = '<span><i class="fas fa-times" style="color:red;"></i></span>'
    return str


@register.filter(name='is_not_blank')
def is_not_blank(value):
    return (value != '')


@register.filter(name='colorteam')
def colorteam(value):
    from collector.utils.fics_references import DRAMA_SEATS_COLORS
    color = DRAMA_SEATS_COLORS[value]
    return "<span style='color:%s;'>%s</span>" % (color, value)


@register.filter(name='parseclean')
def parseclean(value):
    res = value.replace("\n", "<br/>")
    return res


@register.filter(name='as_place')
def as_place(value):
    res = 'n/a'
    if isinstance(value, str):
        val = value.replace('|', '/')
        words = val.split('/')
        list = []
        for word in words:
            list.append(word.strip())
        res = " <i class='fa fa-arrow-right'></i> ".join(list)
    return res


@register.filter(name='zfill')
def zfill(value):
    res = str(value).rjust(5, '0')
    return res


@register.filter(name='as_date')
def as_date(value):
    res = 0
    from datetime import datetime
    year = value['year']
    month = value['month']
    day = value['day']
    # print(year, month, day)
    res = f"{year:04}-{month:02}-{day:02}"
    return res


@register.filter(name='format_date')
def format_date(date_string):
    import datetime
    return datetime.datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S %Z')
