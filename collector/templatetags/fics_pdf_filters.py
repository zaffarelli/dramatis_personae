"""
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
"""
from django import template
from collector.models.character import Character
from collector.models.spacecraft import Spaceship
from collector.models.loot import Loot
import re
import string
from django.template.defaultfilters import dictsort

register = template.Library()


@register.filter(name='parse_avatars_pdf')
def parse_avatars_pdf(value):
    value = "<br/>".join(value.split("\n"))
    """ Replace avatars rids by html links in a text """
    sym = '¤'
    search = '(\w+)'
    seeker = re.compile('\%s%s\%s' % (sym, search, sym))
    changes = []
    txt = str(value)
    iter = seeker.finditer(txt)
    for item in iter:
        rid = ''.join(item.group().split(sym))
        ch = Character.objects.filter(rid=rid).first()
        if ch:
            repstr = '<span class="embedded_link">%s%s</span>' % (ch.full_name, "" if ch.balanced == True else "*")
        else:
            repstr = '<span class="embedded_link broken">[%s was not found]</span>' % (rid)
        changes.append({'src': item.group(), 'dst': repstr})

    """ Ships """

    sym = '^'
    seeker = re.compile('\^(\w+)\^')
    res = str(value)
    iter = seeker.finditer(res)
    for item in iter:
        rid = ''.join(item.group().split('^'))
        try:
            ch = Spaceship.objects.get(full_name=rid)
        except Spaceship.DoesNotExist:
            ch = None
        if ch is not None:
            repstr = '<span id="%d" class="character_link embedded_link" title="%s">%s [%s | %s] %s</span>' % (
                ch.id, ch.ship_ref, ch.full_name, ch.flag, ch.ship_ref.ship_class,
                "" if ch.ship_ref.ship_status == "combat_ready" else "&dagger;")
        else:
            repstr = '<span class="embedded_link broken">[%s was not found]</span>' % (rid)
        changes.append({'src': item.group(), 'dst': repstr})

    """ Replace µ by subsection titles """
    sym = 'µ'
    search = "[A-Za-z0-9\é\è\ô\ö\à\s\.\'\;\-\(\)\&\:\,]+"
    myregex = "\%s%s\%s" % (sym, search, sym)
    seeker = re.compile(myregex)
    # changes = []
    iter = seeker.finditer(txt)
    for item in iter:
        occ = ''.join(item.group().split(sym))
        repstr = '</p><h6 class="subsection">%s</h6><p>' % (occ)
        changes.append({'src': item.group(), 'dst': repstr})
    for change in changes:
        txt = txt.replace(change['src'], change['dst'])
    """ Replace § by em"""
    sym = '§'
    search = "[A-Za-z0-9\é\è\ô\ö\à\s\.\'\;\-\(\)\&\:\,]+"
    myregex = "\%s%s\%s" % (sym, search, sym)
    seeker = re.compile(myregex)
    changes = []
    iter = seeker.finditer(txt)
    for item in iter:
        occ = ''.join(item.group().split(sym))
        repstr = '<em>%s</em>' % (occ)
        changes.append({'src': item.group(), 'dst': repstr})
    for change in changes:
        txt = txt.replace(change['src'], change['dst'])
    """ Replace ° by custom data"""
    sym = '°'
    search = "[A-Za-z0-9\é\è\ô\ö\à\s\.\'\;\-\(\)\&\:\,\_]+"
    myregex = "\%s%s\%s" % (sym, search, sym)
    seeker = re.compile(myregex)
    changes = []
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
    for change in changes:
        txt = txt.replace(change['src'], change['dst'])
    return txt


@register.filter(name='high_skill_check_pdf')
def high_skill_check_pdf(value):
    res = value
    if value >= 5:
        res = "<em>%d</em>" % (value)
    return value


@register.filter(name='as_ritual_category')
def as_ritual_category(value):
    cat = ['Psi', 'Theurgy', 'Symbiosis', 'Runecasting']
    return cat[int(value)]


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


@register.filter(name='is_melee')
def is_melee(value):
    return value == 'MELEE'
