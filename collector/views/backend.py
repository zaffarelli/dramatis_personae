"""
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
"""
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from collector.models.character import Character
from django.template.loader import get_template, render_to_string
from collector.utils import fs_fics7
from django.contrib import messages
from collector.utils.xls_collector import export_to_xls, update_from_xls
from collector.utils.basic import get_current_config, extract_rules, make_audit_report, make_deck
from collector.utils.gs_export import update_gss, summary_gss
from collector.models.sequence import Sequence
from collector.utils.helper import is_ajax
import os
import json
import logging

logger = logging.getLogger(__name__)


def pdf_character(request, id=None):
    """ Create and show a character as PDF """
    item = get_object_or_404(Character, pk=id)
    if item.backup() == True:
        answer = '<a class="pdflink" target="_blank" href="pdf/results/avatars/%s.pdf">%s</a>' % (item.rid, item.rid)
    else:
        answer = '<span class="pdflink">no character found</span>'
    messages.info(request, 'PDF created.')
    return HttpResponse(status=204)


def run_audit(request):
    campaign = get_current_config(request)
    # Let's consider only the current epic characters for the audit
    character_items = campaign.dramatis_personae.all()
    # character_items = Character.objects.all()
    x = 1
    for c in character_items:
        if len(c.player) > 0:
            c.need_fix = True
        x += 1
        messages.info(request, f'Recalculating {c.full_name}')
        c.save()
    messages.info(request, f'Launched {x} actions...')
    make_audit_report(campaign)
    return HttpResponse(status=204)


def export(request):
    export_to_xls()
    messages.info(request, 'Exported to XLS spreadsheet...')
    return HttpResponse(status=204)


def xls_update(request):
    update_from_xls()
    return HttpResponse(status=204)


def gss_update(request):
    update_gss()
    messages.info(request, 'Exported to Google spreadsheet...')
    return HttpResponse(status=204)


def gss_summary(request):
    summary_gss()
    messages.info(request, 'Extracting PCs to Google spreadsheet...')
    return HttpResponse(status=204)


def pdf_rules(request):
    messages.info(request, 'Rebuilding Rules reference...')
    extract_rules()
    messages.info(request, 'Done!')
    return HttpResponse(status=204)


def roll_dice(request, slug):
    context = {}
    contstant = 0
    formula = slug.replace("i", "!").replace("_", " ").replace("x", "+")
    # print(formula)
    actions = formula.split("+")
    dice = formula[0].split("d")
    if len(actions) > 1:
        constant = int(actions[1])
    # print(dice[0])
    total = 0
    for x in range(1, int(dice[0])):
        r, d = fs_fics7.d12x()
        total += r
    # print(r)
    # print(d)
    context = {
        'rolls': d,
        'mods': constant,
        'total': total,
    }
    return JsonResponse(context)


def bloke_selector(request):
    if request.method == "POST":
        return HttpResponse(status=204)
    else:
        from collector.models.bloke import Bloke, BLOKE_LEVELS
        levels = []
        for x in BLOKE_LEVELS:
            levels.append({'value': x[0], 'text': x[1]})
        other_characters = []
        players = ['Delphine', 'Chninkel', 'Marie', 'Lustus', 'Taz']
        for player in players:
            main_characters = Character.objects.filter(player=player)
            blokes = Bloke.objects.filter(character__in=main_characters)
            active_blokes = []
            for b in blokes:
                active_blokes.append({'character': b.npc, 'intimacy': b.level})
            npc = Character.objects.filter(player='')
            for c in npc:
                c.intimacy = 'none'
                for a in active_blokes:
                    if c.rid == a['character'].rid:
                        c.intimacy = a['intimacy']
            other_characters.append({'player': player, 'blokes': npc})
        context = {'blokes': other_characters, 'choices': levels}
        template = get_template('collector/blokes.html')
        html = template.render(context, request)
        messages.info(request, f'Blokes selector loaded.')
        response = {'mosaic': html}
        return JsonResponse(response)


def load_sequence(request):
    context = {'status': 'not ajax'}
    if is_ajax(request):
        reference = request.POST["reference"]
        order = request.POST["order"]
        sequences = Sequence.objects.filter(reference=reference, order=order)
        if len(sequences) == 0:
            context = {'status': 'not found'}
        else:
            sequence = sequences.first()
            data = json.loads(sequence.data)
            context['status'] = 'data found'
            context['data'] = data
    return JsonResponse(context)


def save_sequence(request):
    context = {'status': 'not ajax'}
    if is_ajax(request):
        reference = request.POST["reference"]
        order = request.POST["order"]
        data = request.POST["data"]
        sequences = Sequence.objects.filter(reference=reference, order=order)
        if len(sequences) == 0:
            sequence = Sequence()
        else:
            sequence = sequences.first()
        sequence.reference = reference
        sequence.order = 0
        sequence.data = json.dumps(data, indent=4, sort_keys=True)
        sequence.save()
        context['status'] = 'saved'
    return JsonResponse(context)


def epic_deck(request):
    if is_ajax(request):
        campaign = get_current_config(request)
        characters = []
        all = campaign.dramatis_personae.filter(selected=True)
        for c in all:
            characters.append(json.loads(c.to_jsonDECK()))
        context = {'data': characters}
        return JsonResponse(context)
    else:
        return Http404


def svg_to_pdf(request, slug):
    import cairosvg
    print(">> SVG to PDF")
    response = {'status': 'error'}
    if is_ajax(request):
        pdf_name = os.path.join(settings.MEDIA_ROOT, 'pdf/results/' + request.POST["pdf_name"])
        svg_name = os.path.join(settings.MEDIA_ROOT, 'pdf/results/' + request.POST["svg_name"])
        svgtxt = request.POST["svg"]
        rid = request.POST["rid"]
        pagecount = int(request.POST["pagecount"])
        with open(svg_name, "w") as f:
            f.write(svgtxt)
            f.close()
        cairosvg.svg2pdf(url=svg_name, write_to=pdf_name, scale=1.0)
        message = all_in_one_pdf(rid,pagecount)
        if len(message)>0:
            messages.info(request,message)
        response['status'] = 'ok'
    return JsonResponse(response)


def all_in_one_pdf(rid,pagecount=4):
    print(f'>> All in One PDFing for [{rid}].')
    res = ""
    from PyPDF2 import PdfMerger
    media_results = os.path.join(settings.MEDIA_ROOT, 'pdf/results/')
    csheet_results = os.path.join(settings.MEDIA_ROOT, 'pdf/results/')
    onlyfiles = [f for f in os.listdir(media_results) if os.path.isfile(os.path.join(media_results, f))]
    previousfiles = [f for f in os.listdir(media_results) if os.path.isfile(os.path.join(media_results, f))]
    pdfs = onlyfiles
    merger = PdfMerger()
    pdfs.sort()
    i = 0
    perfect_set = []
    for x in range(0, pagecount):
        perfect_set.append(f'{rid}_p{x}.pdf')
    print(perfect_set)
    got_them_all = True
    for pdf in pdfs:
        if pdf.startswith(rid + "_p") and pdf.endswith(".pdf"):
            print(f"Checking PDF... {pdf}")
            with open(media_results + pdf, 'rb') as p:
                merger.append(p)
            i += 1
            print(f"Page {i} merged")
    for ps in perfect_set:
        if ps not in pdfs:
            got_them_all = False
    if got_them_all:
        des = f'{csheet_results}{rid}.pdf'
        with open(des, 'wb') as fout:
            merger.write(fout)
        cleanlist = previousfiles
        for f in cleanlist:
            if f.startswith(rid + "_p") and (f.endswith(".svg") or f.endswith(".pdf")):
                os.unlink(media_results + f)
        res = f'Successfully merged {i} page(s) as [{des}].'
    return res


# def osave_to_svg(request, slug):
#     response = {'status': 'error'}
#     if is_ajax(request):
#         svg_name = os.path.join(settings.MEDIA_ROOT, 'pdf/results/svg/' + request.POST["svg_name"])
#         svgtxt = request.POST["svg"]
#         with open(svg_name, "w") as f:
#             f.write(svgtxt)
#             f.close()
#         response['status'] = 'ok'
#     return JsonResponse(response)
#
#
# def xsvg_to_pdf(request, slug):
#     response = {'status': 'error'}
#     logger.info(f'Saving to PDF.')
#     if is_ajax(request):
#         import cairosvg
#         svg_name = os.path.join(settings.MEDIA_ROOT, 'pdf/results/' + request.POST["svg_name"])
#         svgtxt = request.POST["svg"]
#         # creature = request.POST["creature"]
#         with open(svg_name, "w") as f:
#             f.write(svgtxt)
#             f.close()
#         logger.info(f'--> Created --> {svg_name}.')
#
#         pdf_name = os.path.join(settings.MEDIA_ROOT, 'pdf/results/pdf/' + request.POST["pdf_name"])
#         if "rid" in request.POST:
#             rid = request.POST["rid"]
#         else:
#             rid = "adventure_sheet"
#         cairosvg.svg2pdf(url=svg_name, write_to=pdf_name, scale=1.0)
#         logger.info(f'--> Created --> {pdf_name}.')
#         print(f'--> Created --> {pdf_name}.')
#         response['status'] = 'ok'
#         # all_in_one_pdf(rid)
#         print(response)
#     return JsonResponse(response)
