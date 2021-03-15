"""
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
"""
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.conf import settings
from PyPDF2 import PdfFileMerger
import os
import logging
from collector.models.tourofduty import TourOfDutyRef
from django.contrib import messages

logger = logging.getLogger(__name__)


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('utf-8')), result)
    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        filename = 'avatar_%s.pdf' % context_dict['filename']
        content = "inline; filename='%s'"% filename
        response['content-disposition'] = content
        return response
    return HttpResponse(pdf.err, content_type='text/plain')


def write_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    uri = '%s.pdf'%(context_dict['filename'])
    filename = os.path.join(settings.MEDIA_ROOT, 'pdf/results/avatars/' + uri)
    result = open(filename, 'wb')
    pdf = pisa.pisaDocument(BytesIO(html.encode('utf-8')), dest=result, encoding='utf-8')
    result.close()


def get_current_config():
    from collector.models.campaign import Campaign
    item = Campaign.objects.get(is_active=True)
    if item is None:
        item = Campaign.objects.first()
    return item


def make_avatar_appendix(campaign):
    res = []
    media_resources = os.path.join(settings.MEDIA_ROOT, 'pdf/resources/')
    media_results = os.path.join(settings.MEDIA_ROOT, 'pdf/results/')
    media_avatars = os.path.join(settings.MEDIA_ROOT, 'pdf/results/avatars/')
    onlyfiles = [f for f in os.listdir(media_avatars) if os.path.isfile(os.path.join(media_avatars, f))]
    pdfs = onlyfiles
    merger = PdfFileMerger()
    # merger.append(open('%s__aa_header.pdf'%(media_resources), 'rb'))
    pdfs.sort()
    ep = campaign.epic
    cast = ep.get_full_cast()
    i = 0
    for pdf in pdfs:
        # if 'avatar_' in pdf:
        #     arid = pdf.split('avatar_')
        #     if arid[1].split('.')[0] in cast:
        if pdf.split('.')[0] in cast:
            i += 1
            merger.append(open(media_avatars+pdf, 'rb'))
    if i>0:
        des = '%sappendix_%s.pdf'%(media_results, campaign.epic.shortcut)
        with open(des, 'wb') as fout:
            merger.write(fout)
    return res


def make_epic_corpus(campaign):
    res = []
    mypath = os.path.join(settings.MEDIA_ROOT, 'pdf/')
    media_resources = os.path.join(settings.MEDIA_ROOT, 'pdf/resources/')
    media_results = os.path.join(settings.MEDIA_ROOT, 'pdf/results/')
    mystaticpath = os.path.join(settings.STATIC_ROOT, 'pdf/')
    merger = PdfFileMerger()
    # merger.append(open('%sresources/__es_header.pdf'%(mystaticpath), 'rb'))
    template = get_template('collector/conf_pdf.html')
    context = {'epic':campaign.parse_details()}
    html = template.render(context)
    uri = 'c_%s.pdf'%(campaign.epic.shortcut)
    filename = os.path.join(settings.MEDIA_ROOT, 'pdf/results/' + uri)
    es_pdf = open(filename, 'wb')
    # import pdb; pdb.set_trace()
    pdf = pisa.pisaDocument(BytesIO(html.encode('utf-8')), es_pdf)
    # print(pdf)
    es_pdf.close()
    merger.append(open(filename, 'rb'))
    des = '%scorpus_%s.pdf'%(media_results,campaign.epic.shortcut)
    with open(des, 'wb') as fout:
      merger.write(fout)
    return res


def export_epic(request,campaign):
    res = {'epic':campaign.epic.title}
    comments = []
    comments += make_avatar_appendix(campaign)
    comments += make_epic_corpus(campaign)
    com = '<br/>'.join(comments)
    res['comment'] = '<div class="classyview"><p>'+com+'</p></div>'
    media_results = os.path.join(settings.MEDIA_ROOT, 'pdf/results/')
    merger = PdfFileMerger()
    merger.append(open('%scorpus_%s.pdf'%(media_results,campaign.epic.shortcut), 'rb'))
    merger.append(open('%sappendix_%s.pdf'%(media_results,campaign.epic.shortcut), 'rb'))
    des = '%s%s.pdf'%(media_results,campaign.epic.shortcut)
    with open(des, 'wb') as fout:
        merger.write(fout)
    messages.info(request,'Epic [%s] exported to PDF: [%s]'%(campaign.epic.title,des))
    return res


def extract_rules():
    from collector.models.weapon import WeaponRef
    from collector.models.skill import SkillRef
    from collector.models.benefice_affliction import BeneficeAfflictionRef
    from collector.models.blessing_curse import BlessingCurseRef
    from collector.models.ritual import RitualRef
    from collector.models.gear import Gear
    context = {}
    import datetime
    context['date'] = datetime.datetime.now()
    skills = SkillRef.objects.all().filter(is_wildcard=False).order_by('reference', 'is_root', 'is_speciality')
    context['skills'] = skills
    benefice_afflictions = BeneficeAfflictionRef.objects.order_by('-source')
    context['benefice_afflictions'] = benefice_afflictions
    blessing_curses = BlessingCurseRef.objects.order_by('-source')
    context['blessing_curses'] = blessing_curses
    melee_weapons = WeaponRef.objects.filter(category='MELEE')
    context['melee_weapons'] = melee_weapons
    ranged_weapons = WeaponRef.objects.exclude(category='MELEE')
    context['ranged_weapons'] = ranged_weapons
    rituals = RitualRef.objects.order_by('category', 'path', 'level')
    context['rituals'] = rituals
    racial = TourOfDutyRef.objects.filter(category='0').order_by('-source')
    context['racial'] = racial
    castes = ['Nobility', 'Freefolk', 'Church', 'Guild', 'Alien']
    castes_context = []
    for caste in castes:
        caste_context = {}
        caste_context['name'] = caste
        upbringing = TourOfDutyRef.objects.filter(category='10',caste=caste).order_by('-source')
        caste_context['upbringing'] = upbringing
        apprenticeship = TourOfDutyRef.objects.filter(category='20',caste=caste).order_by('-source')
        caste_context['apprenticeship'] = apprenticeship
        early_career = TourOfDutyRef.objects.filter(category='30',caste=caste).order_by('-source')
        caste_context['early_career'] = early_career
        castes_context.append(caste_context)
    context['castes'] = castes_context
    tour_of_duty = TourOfDutyRef.objects.filter(category='40').order_by('-source')
    context['tour_of_duty'] = tour_of_duty
    worldly_benefits = TourOfDutyRef.objects.filter(category='50').order_by('-source')
    context['worldly_benefits'] = worldly_benefits
    template = get_template('collector/references.html')
    html = template.render(context)
    fname = 'rules.pdf'
    filename = os.path.join(settings.MEDIA_ROOT, 'pdf/results/' + fname)
    es_pdf = open(filename, 'wb')
    pdf = pisa.pisaDocument(BytesIO(html.encode('utf-8')), es_pdf)
    if not pdf.err:
        es_pdf.close()
    else:
        print(pdf.err)
    extract_equipment()


def extract_equipment():
    from collector.models.gear import Gear
    from collector.models.weapon import WeaponRef
    from collector.models.armor import ArmorRef
    context = {}
    import datetime
    context['date'] = datetime.datetime.now()
    # Categorizing gear
    gears = Gear.objects.order_by('category', '-reference', 'name', 'variant')
    cat = ''
    context['gears'] = []
    current = dict(name='', data=[])
    for g in gears:
        if g.get_category_display() != cat:
            if cat:
                context['gears'].append(current)
            current = dict(name=g.get_category_display(), data=[])
            cat = g.get_category_display()
        current['data'].append(g)
    if cat:
        context['gears'].append(current)
    # Weapons
    weapons = WeaponRef.objects.filter(hidden=False).order_by('meta_type','cost')
    cat = ''
    context['weapons'] = []
    current = { 'name':'', 'data':[] }
    for w in weapons:
        if w.meta_type != cat:
            if cat:
                context['weapons'].append(current)
            current = { 'name':'', 'data':[] }
            current['name'] = w.meta_type
            current['data'] = []
            cat = w.meta_type
        current['data'].append(w)
    if cat:
        context['weapons'].append(current)
    # Armors
    armors = ArmorRef.objects.order_by('category','cost')
    cat = ''
    context['armors'] = []
    current = { 'name':'', 'data':[] }
    for a in armors:
        if a.get_category_display() != cat:
            if cat:
                context['armors'].append(current)
            current = { 'name':'', 'data':[] }
            current['name'] = a.get_category_display()
            current['data'] = []
            cat = a.get_category_display()
        current['data'].append(a)
    if cat:
        context['armors'].append(current)
    # Energy Shields
    template = get_template('collector/equipment.html')
    html = template.render(context)
    fname = 'fading_suns_shopping_guide.pdf'
    filename = os.path.join(settings.MEDIA_ROOT, 'pdf/results/' + fname)
    es_pdf = open(filename, 'wb')
    pdf = pisa.pisaDocument(BytesIO(html.encode('utf-8')), es_pdf)
    if not pdf.err:
        es_pdf.close()
    else:
        print(pdf.err)