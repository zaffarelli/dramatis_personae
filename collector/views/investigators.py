"""
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
"""
from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView
from django.contrib import messages
from collector.forms.coc7 import InvestigatorForm
from collector.models.investigator import Investigator
from scenarist.mixins.ajaxfromresponse import AjaxFromResponseMixin
#from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.template.loader import get_template
from django.shortcuts import redirect

class InvestigatorDetailView(DetailView):
    model = Investigator
    context_object_name = 'c'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['no_skill_edit'] = True
        messages.success(self.request, 'Display investigator %s' % (context['c'].full_name))
        return context


class InvestigatorUpdateView(AjaxFromResponseMixin, UpdateView):
    model = Investigator
    form_class = InvestigatorForm
    context_object_name = 'c'
    template_name_suffix = '_update_form'

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        tourofdutys_formset = context['tourofdutys']
        if tourofdutys_formset.is_valid():
            response = super().form_valid(form)
            tourofdutys_formset.instance = self.object
            tourofdutys_formset.save()
            return response
        else:
            messages.error(self.request, 'Avatar %s has errors. unable to save.' % (context['c'].full_name))
            return super().form_invalid(form)

    def get_success_url(self):
        return f'ajax/recalc/character/{self.object.id}/'

    def get_context_data(self, **kwargs):
        context = super(CharacterUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['form'] = CharacterForm(self.request.POST, instance=self.object)
            context['tourofdutys'] = TourOfDutyFormSet(self.request.POST, instance=self.object)
            context['tourofdutys'].full_clean()
            messages.success(self.request, 'Avatar updated: %s' % (context['form']['full_name'].value()))
        else:
            context['form'] = CharacterForm(instance=self.object)
            context['tourofdutys'] = TourOfDutyFormSet(instance=self.object)
            messages.info(self.request, 'Avatar displayed: %s' % (context['form']['full_name'].value()))
        return context


def respawn_avatar_link(avatar, context, request):
    template = get_template('collector/character_link.html')
    context["avatar_link"] = template.render({'c': avatar}, request)
    return context


def respawn_summary(avatar, context, request):
    template = get_template('collector/custo/summary_block.html')
    context["summary"] = template.render({'c': avatar}, request)
    return context


def skill_pick(request, avatar, item, offset):
    """ Touching skills to edit them in the view """
    from collector.models.skill import SkillRef
    context = {}
    offset = int(offset) - 50;
    ch = Character.objects.get(pk=avatar)
    skillref = SkillRef.objects.get(pk=item)
    ch.charactercusto.add_or_update_skill(skillref.id, offset)
    ch.fix()
    ch.save()
    skill = ch.skill_set.all().filter(skill_ref__id=item).first()
    context["c"] = model_to_dict(ch)
    template = get_template('collector/character/character_skill.html')
    context["block"] = template.render({'c': ch, 'skill': skill})
    context = respawn_summary(ch, context, request)
    context = respawn_avatar_link(ch, context, request)
    return JsonResponse(context)


def attr_pick(request, avatar, item, offset):
    """ Touching attributes to edit them in the view """
    context = {}
    offset = int(offset) - 50;
    ch = Character.objects.get(pk=avatar)
    x = getattr(ch.charactercusto, item, -100)
    if x == -100:
        setattr(ch.charactercusto, item, offset)
    else:
        setattr(ch.charactercusto, item, x + offset)
    print(item)
    info = ("info_" + item.split("_")[1]).lower()
    ch.fix()
    ch.save()
    context["c"] = model_to_dict(ch)
    template = get_template('collector/character/character_pa.html')
    context["block"] = template.render({'c': getattr(ch, info)})
    context = respawn_summary(ch, context, request)
    context = respawn_avatar_link(ch, context, request)
    return JsonResponse(context)



def customize_skill(request, avatar, item):
    from collector.models.skill import SkillRef, SkillCusto
    from collector.models.character_custo import CharacterCusto
    context = {}
    ch = Character.objects.get(pk=avatar)
    ref = SkillRef.objects.get(pk=item)
    new_item = SkillCusto()
    new_item.character_custo = ch.charactercusto
    new_item.skill_ref = ref
    new_item.value = 1
    new_item.save()
    ch.fix()
    ch.save()
    context["c"] = model_to_dict(ch)
    template = get_template('collector/character/character_skills.html')
    context["block"] = template.render({'c': ch})
    template = get_template('collector/custo/skill_custo_block.html')
    context["custo_block"] = template.render({'c': ch})
    context = respawn_summary(ch, context, request)
    context = respawn_avatar_link(ch, context, request)
    messages.info(request, 'Avatar %s customized with skill %s at +1.' % (ch.full_name, new_item.skill_ref.reference))
    return JsonResponse(context)

def customize_weapon(request, avatar, item):
    from collector.models.weapon import WeaponRef, WeaponCusto
    from collector.models.character_custo import CharacterCusto
    context = {}
    ch = Character.objects.get(pk=avatar)
    item_ref = WeaponRef.objects.get(pk=item)
    item_custo = WeaponCusto()
    item_custo.character_custo = ch.charactercusto
    item_custo.weapon_ref = item_ref
    item_custo.save()
    ch.fix()
    ch.save()
    context["c"] = model_to_dict(ch)
    template = get_template('collector/character/character_weapon.html')
    context["block"] = template.render({'c': ch})
    template = get_template('collector/custo/weapon_custo_block.html')
    context["custo_block"] = template.render({'c': ch})
    context = respawn_summary(ch, context, request)
    context = respawn_avatar_link(ch, context, request)
    messages.info(request, 'Avatar %s customized with weapon %s.' % (ch.full_name, item_custo.weapon_ref.reference))
    return JsonResponse(context)


def customize_weapon_del(request, avatar, item):
    from collector.models.weapon import WeaponRef, WeaponCusto
    from collector.models.character_custo import CharacterCusto
    context = {}
    ch = Character.objects.get(pk=avatar)
    item_ref = WeaponRef.objects.get(pk=item)
    custo_items = ch.charactercusto.weaponcusto_set.all()
    item_found = None
    for item in custo_items:
        if item.weapon_ref == item_ref:
            item_found = item
            break
    if item_found:
        txt = item_found.weapon_ref.reference
        item_found.delete()
        ch.fix()
        ch.save()
        context["c"] = model_to_dict(ch)
        template = get_template('collector/character/character_weapon.html')
        context["block"] = template.render({'c': ch})
        template = get_template('collector/custo/weapon_custo_block.html')
        context["custo_block"] = template.render({'c': ch})
        context = respawn_summary(ch, context, request)
        context = respawn_avatar_link(ch, context, request)
        messages.info(request, 'Avatar %s customized with weapon %s.' % (ch.full_name, txt))
    else:
        context["c"] = model_to_dict(ch)
        messages.info(request, 'Weapon not found for %s.' % (ch.full_name))
    return JsonResponse(context)





def customize_ritual(request, avatar, item):
    from collector.models.ritual import RitualRef, RitualCusto
    from collector.models.character_custo import CharacterCusto
    context = {}
    ch = Character.objects.get(pk=avatar)
    item_ref = RitualRef.objects.get(pk=item)
    item_custo = RitualCusto()
    item_custo.character_custo = ch.charactercusto
    item_custo.ritual_ref = item_ref
    item_custo.save()
    ch.fix()
    ch.save()
    context["c"] = model_to_dict(ch)
    template = get_template('collector/character/character_ritual.html')
    context["block"] = template.render({'c': ch})
    template = get_template('collector/custo/ritual_custo_block.html')
    context["custo_block"] = template.render({'c': ch})
    context = respawn_summary(ch, context, request)
    context = respawn_avatar_link(ch, context, request)
    messages.info(request, 'Avatar %s customized with weapon %s.' % (ch.full_name, item_custo.ritual_ref.reference))
    return JsonResponse(context)



def customize_ritual_del(request, avatar, item):
    from collector.models.ritual import RitualRef, WeaponCusto
    from collector.models.character_custo import CharacterCusto
    context = {}
    ch = Character.objects.get(pk=avatar)
    item_ref = RitualRef.objects.get(pk=item)
    custo_items = ch.charactercusto.ritualcusto_set.all()
    item_found = None
    for item in custo_items:
        if item.ritual_ref == item_ref:
            item_found = item
            break
    if item_found:
        txt = item_found.ritual_ref.reference
        item_found.delete()
        ch.fix()
        ch.save()
        context["c"] = model_to_dict(ch)
        template = get_template('collector/character/character_ritual.html')
        context["block"] = template.render({'c': ch})
        template = get_template('collector/custo/ritual_custo_block.html')
        context["custo_block"] = template.render({'c': ch})
        context = respawn_summary(ch, context, request)
        context = respawn_avatar_link(ch, context, request)
        messages.info(request, 'Avatar %s customized with weapon %s.' % (ch.full_name, txt))
    else:
        context["c"] = model_to_dict(ch)
        messages.info(request, 'Ritual not found for %s.' % (ch.full_name))
    return JsonResponse(context)
