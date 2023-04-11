'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView
from django.contrib import messages
from collector.forms.basic import CharacterForm, TourOfDutyFormSet, CoreTourOfDutyFormSet
from collector.models.character import Character
from scenarist.mixins.ajaxfromresponse import AjaxFromResponseMixin
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.template.loader import get_template
from django.shortcuts import redirect, reverse
from collector.models.bloke import Bloke


class CharacterDetailView(DetailView):
    model = Character
    context_object_name = 'c'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['no_skill_edit'] = False
        # self.object.fix()
        # context['blokes'] = BlokesFormSet(instance=self.object)
        context['data'] = self.object.to_json()
        x =self.object.to_json_customizer()
        mobile_form = get_template('collector/mobile_form.html')
        mf = mobile_form.render({'c': x}, self.request)


        context['mobile_form'] = mf
        # print(x)

        messages.success(self.request, 'Displaying character [%s].' % (context['object'].full_name))
        return context


class CharacterUpdateView(AjaxFromResponseMixin, UpdateView):
    model = Character
    form_class = CharacterForm
    context_object_name = 'c'
    template_name_suffix = '_update_form'

    # success_url = 'view_character'

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

    def get_context_data(self, **kwargs):
        context = super(CharacterUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['form'] = CharacterForm(self.request.POST, instance=self.object)
            context['tourofdutys'] = TourOfDutyFormSet(self.request.POST, instance=self.object)
            context['tourofdutys'].full_clean()
            messages.success(self.request, 'Avatar updated: %s' % (context['form']['full_name'].value()))
        else:
            context['form'] = CharacterForm(instance=self.object)
            print(context['form']['is_core'].value())
            if context['form']['is_core'].value():
                context['tourofdutys'] = CoreTourOfDutyFormSet(instance=self.object)
            else:
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
    # from collector.utils.basic import get_current_config
    import time
    st = time.time()
    # campaign = get_current_config(request)
    context = {}
    offset = int(offset) - 50;
    ch = Character.objects.get(pk=avatar)
    skillref = SkillRef.objects.get(pk=item)
    ch.charactercusto.add_or_update_skill(skillref.id, offset)
    ch.fix(conf=None, focus_on="SKILLS")
    ch.save()
    skill = ch.skill_set.all().filter(skill_ref__id=item).first()
    context["c"] = model_to_dict(ch)
    template = get_template('collector/character/character_skill.html')
    context["block"] = template.render({'c': ch, 'skill': skill})
    template_challenge = get_template('collector/character/character_challenge.html')
    context["challenge"] = template_challenge.render({'c': ch})
    context = respawn_summary(ch, context, request)
    context = respawn_avatar_link(ch, context, request)
    et = time.time()
    elapsed_time = et-st
    print(f"TRACE SKILLS> Execution time: {elapsed_time:.2f} seconds.")
    return JsonResponse(context)


def attr_pick(request, avatar, item, offset):
    """ Touching skills to edit them in the view """
    # from collector.utils.basic import get_current_config
    # campaign = get_current_config(request)
    import time
    st = time.time()
    context = {}
    offset = int(offset) - 50;
    ch = Character.objects.get(pk=avatar)
    x = getattr(ch.charactercusto, item, -100)
    if x == -100:
        setattr(ch.charactercusto, item, offset)
    else:
        setattr(ch.charactercusto, item, x + offset)
    # print(item)
    info = ("info_" + item.split("_")[1]).lower()
    #ch.fix(conf=campaign)
    ch.fix(conf=None, focus_on="ATTR")
    ch.save()
    context["c"] = model_to_dict(ch)
    template = get_template('collector/character/character_pa.html')
    context["block"] = template.render({'c': getattr(ch, info)})
    template_challenge = get_template('collector/character/character_challenge.html')
    context["challenge"] = template_challenge.render({'c': ch})
    context = respawn_summary(ch, context, request)
    context = respawn_avatar_link(ch, context, request)
    et = time.time()
    elapsed_time = et-st
    print(f"TRACE ATTRIBUTES> Execution time: {elapsed_time:.2f} seconds.")
    return JsonResponse(context)


def customize_skill(request, avatar, item):
    from collector.models.skill import SkillRef, SkillCusto
    from collector.models.character_custo import CharacterCusto
    import time
    st = time.time()
    # from collector.utils.basic import get_current_config
    # campaign = get_current_config(request)
    context = {}
    ch = Character.objects.get(pk=avatar)
    ref = SkillRef.objects.get(pk=item)
    new_item = SkillCusto()
    new_item.character_custo = ch.charactercusto
    new_item.skill_ref = ref
    new_item.value = 1
    new_item.save()
    #ch.fix(conf=campaign)
    ch.fix(conf=None, focus_on="SKILL")
    ch.save()
    print("Fixed")
    context["c"] = model_to_dict(ch)
    template = get_template('collector/character/character_skills.html')
    context["block"] = template.render({'c': ch})
    template = get_template('collector/custo/skill_custo_block.html')
    context["custo_block"] = template.render({'c': ch})
    template_challenge = get_template('collector/character/character_challenge.html')
    context["challenge"] = template_challenge.render({'c': ch})
    context = respawn_summary(ch, context, request)
    context = respawn_avatar_link(ch, context, request)
    # messages.info(request, 'Avatar %s customized with skill %s at +1.' % (ch.full_name, new_item.skill_ref.reference))
    et = time.time()
    elapsed_time = et-st
    print(f"TRACE SKILLS> Execution time: {elapsed_time:.2f} seconds.")
    return JsonResponse(context)


def customize_bc(request, avatar, item):
    from collector.models.blessing_curse import BlessingCurseRef, BlessingCurseCusto
    from collector.models.character_custo import CharacterCusto
    from collector.utils.basic import get_current_config
    campaign = get_current_config(request)
    context = {}
    ch = Character.objects.get(pk=avatar)
    bcr = BlessingCurseRef.objects.get(pk=item)
    bcc = BlessingCurseCusto()
    bcc.character_custo = ch.charactercusto
    bcc.blessing_curse_ref = bcr
    bcc.save()
    ch.fix(campaign)
    ch.save()
    context["c"] = model_to_dict(ch)
    template = get_template('collector/character/character_bc.html')
    context["block"] = template.render({'c': ch})
    template = get_template('collector/custo/bc_custo_block.html')
    context["custo_block"] = template.render({'c': ch})
    template_challenge = get_template('collector/character/character_challenge.html')
    context["challenge"] = template_challenge.render({'c': ch})
    context = respawn_summary(ch, context, request)
    context = respawn_avatar_link(ch, context, request)
    messages.info(request, 'Avatar %s customized with B/C %s.' % (ch.full_name, bcc.blessing_curse_ref.reference))
    return JsonResponse(context)


def customize_bc_del(request, avatar, item):
    from collector.models.blessing_curse import BlessingCurseRef, BlessingCurseCusto
    from collector.models.character_custo import CharacterCusto
    from collector.utils.basic import get_current_config
    campaign = get_current_config(request)
    context = {}
    ch = Character.objects.get(pk=avatar)
    bcr = BlessingCurseRef.objects.get(pk=item)
    bcca = ch.charactercusto.blessingcursecusto_set.all()
    bcc = None
    for x in bcca:
        if x.blessing_curse_ref == bcr:
            bcc = x
    if bcc:
        txt = bcc.blessing_curse_ref.reference
        bcc.delete()
        ch.fix(conf=campaign)
        ch.save()
        context["c"] = model_to_dict(ch)
        template = get_template('collector/character/character_bc.html')
        context["block"] = template.render({'c': ch})
        template = get_template('collector/custo/bc_custo_block.html')
        context["custo_block"] = template.render({'c': ch})
        template_challenge = get_template('collector/character/character_challenge.html')
        context["challenge"] = template_challenge.render({'c': ch})
        context = respawn_summary(ch, context, request)
        context = respawn_avatar_link(ch, context, request)
        messages.info(request, 'Avatar %s customized with B/C %s.' % (ch.full_name, txt))
    else:
        context["c"] = model_to_dict(ch)
        messages.info(request, 'B/C not found for %s.' % (ch.full_name))
    return JsonResponse(context)


def customize_ba(request, avatar, item):
    from collector.models.benefice_affliction import BeneficeAfflictionRef
    from collector.models.character_custo import CharacterCusto
    from collector.models.benefice_affliction import BeneficeAfflictionCusto
    from collector.utils.basic import get_current_config
    campaign = get_current_config(request)
    context = {}
    ch = Character.objects.get(pk=avatar)
    bar = BeneficeAfflictionRef.objects.get(pk=item)
    bac = BeneficeAfflictionCusto()
    bac.character_custo = ch.charactercusto
    bac.benefice_affliction_ref = bar
    bac.description = request.POST["freefield"]
    bac.save()
    ch.fix(campaign)
    ch.save()
    context["c"] = model_to_dict(ch)
    template = get_template('collector/character/character_ba.html')
    context["block"] = template.render({'c': ch})
    template = get_template('collector/custo/ba_custo_block.html')
    context["custo_block"] = template.render({'c': ch})
    template_challenge = get_template('collector/character/character_challenge.html')
    context["challenge"] = template_challenge.render({'c': ch})
    context = respawn_summary(ch, context, request)
    context = respawn_avatar_link(ch, context, request)
    messages.info(request, 'Avatar %s customized with B/A %s.' % (ch.full_name, bac.benefice_affliction_ref.reference))
    return JsonResponse(context)


def customize_ba_del(request, avatar, item):
    from collector.models.benefice_affliction import BeneficeAfflictionRef
    from collector.models.character_custo import CharacterCusto
    from collector.models.benefice_affliction import BeneficeAfflictionCusto
    from collector.utils.basic import get_current_config
    campaign = get_current_config(request)
    context = {}
    ch = Character.objects.get(pk=avatar)
    bcr = BeneficeAfflictionRef.objects.get(pk=item)
    bcca = ch.charactercusto.beneficeafflictioncusto_set.all()
    bcc = None
    for x in bcca:
        if x.benefice_affliction_ref == bcr:
            bcc = x
    if bcc:
        txt = bcc.benefice_affliction_ref.reference
        bcc.delete()
        ch.fix(campaign)
        ch.save()
        context["c"] = model_to_dict(ch)
        template = get_template('collector/character/character_ba.html')
        context["block"] = template.render({'c': ch})
        template = get_template('collector/custo/ba_custo_block.html')
        context["custo_block"] = template.render({'c': ch})
        template_challenge = get_template('collector/character/character_challenge.html')
        context["challenge"] = template_challenge.render({'c': ch})
        context = respawn_summary(ch, context, request)
        context = respawn_avatar_link(ch, context, request)
        messages.info(request, 'Avatar %s customized with B/A %s.' % (ch.full_name, txt))
    else:
        context["c"] = model_to_dict(ch)
        messages.info(request, 'B/A not found for %s.' % (ch.full_name))
    return JsonResponse(context)


def customize_weapon(request, avatar, item):
    from collector.models.weapon import WeaponRef, WeaponCusto
    from collector.models.character_custo import CharacterCusto
    from collector.utils.basic import get_current_config
    campaign = get_current_config(request)
    context = {}
    ch = Character.objects.get(pk=avatar)
    item_ref = WeaponRef.objects.get(pk=item)
    item_custo = WeaponCusto()
    item_custo.character_custo = ch.charactercusto
    item_custo.weapon_ref = item_ref
    item_custo.save()
    ch.fix(campaign)
    ch.save()
    context["c"] = model_to_dict(ch)
    template = get_template('collector/character/character_weapon.html')
    context["block"] = template.render({'c': ch})
    template = get_template('collector/custo/weapon_custo_block.html')
    context["custo_block"] = template.render({'c': ch})
    template_challenge = get_template('collector/character/character_challenge.html')
    context["challenge"] = template_challenge.render({'c': ch})
    context = respawn_summary(ch, context, request)
    context = respawn_avatar_link(ch, context, request)
    messages.info(request, 'Avatar %s customized with weapon %s.' % (ch.full_name, item_custo.weapon_ref.reference))
    return JsonResponse(context)


def customize_weapon_del(request, avatar, item):
    from collector.models.weapon import WeaponRef, WeaponCusto
    from collector.models.character_custo import CharacterCusto
    from collector.utils.basic import get_current_config
    campaign = get_current_config(request)
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
        ch.fix(campaign)
        ch.save()
        context["c"] = model_to_dict(ch)
        template = get_template('collector/character/character_weapon.html')
        context["block"] = template.render({'c': ch})
        template = get_template('collector/custo/weapon_custo_block.html')
        context["custo_block"] = template.render({'c': ch})
        template_challenge = get_template('collector/character/character_challenge.html')
        context["challenge"] = template_challenge.render({'c': ch})
        context = respawn_summary(ch, context, request)
        context = respawn_avatar_link(ch, context, request)
        messages.info(request, 'Avatar %s customized with weapon %s.' % (ch.full_name, txt))
    else:
        context["c"] = model_to_dict(ch)
        messages.info(request, 'Weapon not found for %s.' % (ch.full_name))
    return JsonResponse(context)


def customize_armor(request, avatar, item):
    from collector.models.armor import ArmorRef
    from collector.models.character_custo import CharacterCusto
    from collector.utils.basic import get_current_config
    campaign = get_current_config(request)
    from collector.models.armor import ArmorCusto
    context = {}
    ch = Character.objects.get(pk=avatar)
    item_ref = ArmorRef.objects.get(pk=item)
    item_custo = ArmorCusto()
    item_custo.character_custo = ch.charactercusto
    item_custo.armor_ref = item_ref
    item_custo.save()
    ch.fix(campaign)
    ch.save()
    context["c"] = model_to_dict(ch)
    template = get_template('collector/character/character_armor.html')
    context["block"] = template.render({'c': ch})
    template = get_template('collector/custo/armor_custo_block.html')
    context["custo_block"] = template.render({'c': ch})
    template_challenge = get_template('collector/character/character_challenge.html')
    context["challenge"] = template_challenge.render({'c': ch})
    context = respawn_summary(ch, context, request)
    context = respawn_avatar_link(ch, context, request)
    messages.info(request, 'Avatar %s customized with armor %s.' % (ch.full_name, item_custo.armor_ref.reference))
    return JsonResponse(context)


def customize_armor_del(request, avatar, item):
    from collector.models.armor import ArmorRef
    from collector.models.character_custo import CharacterCusto
    from collector.models.armor import ArmorCusto
    from collector.utils.basic import get_current_config
    campaign = get_current_config(request)
    context = {}
    ch = Character.objects.get(pk=avatar)
    item_ref = ArmorRef.objects.get(pk=item)
    custo_items = ch.charactercusto.armorcusto_set.all()
    item_found = None
    for item in custo_items:
        if item.armor_ref == item_ref:
            item_found = item
            break
    if item_found:
        txt = item_found.armor_ref.reference
        item_found.delete()
        ch.fix(campaign)
        ch.save()
        context["c"] = model_to_dict(ch)
        template = get_template('collector/character/character_armor.html')
        context["block"] = template.render({'c': ch})
        template = get_template('collector/custo/armor_custo_block.html')
        context["custo_block"] = template.render({'c': ch})
        template_challenge = get_template('collector/character/character_challenge.html')
        context["challenge"] = template_challenge.render({'c': ch})
        context = respawn_summary(ch, context, request)
        context = respawn_avatar_link(ch, context, request)
        messages.info(request, 'Avatar %s customized with armor %s.' % (ch.full_name, txt))
    else:
        context["c"] = model_to_dict(ch)
        messages.info(request, 'Armor not found for %s.' % (ch.full_name))
    return JsonResponse(context)


def customize_shield(request, avatar, item):
    from collector.models.shield import ShieldRef
    from collector.models.character_custo import CharacterCusto
    from collector.models.shield import ShieldCusto
    from collector.utils.basic import get_current_config
    campaign = get_current_config(request)
    context = {}
    ch = Character.objects.get(pk=avatar)
    item_ref = ShieldRef.objects.get(pk=item)
    item_custo = ShieldCusto()
    item_custo.character_custo = ch.charactercusto
    item_custo.shield_ref = item_ref
    item_custo.save()
    ch.fix(campaign)
    ch.save()
    context["c"] = model_to_dict(ch)
    template = get_template('collector/character/character_shield.html')
    context["block"] = template.render({'c': ch})
    template = get_template('collector/custo/shield_custo_block.html')
    context["custo_block"] = template.render({'c': ch})
    template_challenge = get_template('collector/character/character_challenge.html')
    context["challenge"] = template_challenge.render({'c': ch})
    context = respawn_summary(ch, context, request)
    context = respawn_avatar_link(ch, context, request)
    messages.info(request, 'Avatar %s customized with shield %s.' % (ch.full_name, item_custo.shield_ref.reference))
    return JsonResponse(context)


def customize_shield_del(request, avatar, item):
    from collector.models.shield import ShieldRef
    from collector.models.character_custo import CharacterCusto
    from collector.models.shield import ShieldCusto
    from collector.utils.basic import get_current_config
    campaign = get_current_config(request)
    context = {}
    ch = Character.objects.get(pk=avatar)
    item_ref = ShieldRef.objects.get(pk=item)
    custo_items = ch.charactercusto.shieldcusto_set.all()
    item_found = None
    for item in custo_items:
        if item.shield_ref == item_ref:
            item_found = item
            break
    if item_found:
        txt = item_found.shield_ref.reference
        item_found.delete()
        ch.fix(campaign)
        ch.save()
        context["c"] = model_to_dict(ch)
        template = get_template('collector/character/character_shield.html')
        context["block"] = template.render({'c': ch})
        template = get_template('collector/custo/shield_custo_block.html')
        context["custo_block"] = template.render({'c': ch})
        template_challenge = get_template('collector/character/character_challenge.html')
        context["challenge"] = template_challenge.render({'c': ch})
        context = respawn_summary(ch, context, request)
        context = respawn_avatar_link(ch, context, request)
        messages.info(request, 'Avatar %s customized with shield %s.' % (ch.full_name, txt))
    else:
        context["c"] = model_to_dict(ch)
        messages.info(request, 'Shield not found for %s.' % (ch.full_name))
    return JsonResponse(context)


def customize_ritual(request, avatar, item):
    from collector.models.ritual import RitualRef, RitualCusto
    from collector.models.character_custo import CharacterCusto
    from collector.utils.basic import get_current_config
    campaign = get_current_config(request)
    context = {}
    ch = Character.objects.get(pk=avatar)
    item_ref = RitualRef.objects.get(pk=item)
    item_custo = RitualCusto()
    item_custo.character_custo = ch.charactercusto
    item_custo.ritual_ref = item_ref
    item_custo.save()
    ch.fix(campaign)
    ch.save()
    context["c"] = model_to_dict(ch)
    template = get_template('collector/character/character_ritual.html')
    context["block"] = template.render({'c': ch})
    template = get_template('collector/custo/ritual_custo_block.html')
    context["custo_block"] = template.render({'c': ch})
    template_challenge = get_template('collector/character/character_challenge.html')
    context["challenge"] = template_challenge.render({'c': ch})
    context = respawn_summary(ch, context, request)
    context = respawn_avatar_link(ch, context, request)
    messages.info(request, 'Avatar %s customized with weapon %s.' % (ch.full_name, item_custo.ritual_ref.reference))
    return JsonResponse(context)


def customize_ritual_del(request, avatar, item):
    from collector.models.ritual import RitualRef, RitualCusto
    from collector.models.character_custo import CharacterCusto
    from collector.utils.basic import get_current_config
    campaign = get_current_config(request)
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
        ch.fix(campaign)
        ch.save()
        context["c"] = model_to_dict(ch)
        template = get_template('collector/character/character_ritual.html')
        context["block"] = template.render({'c': ch})
        template = get_template('collector/custo/ritual_custo_block.html')
        context["custo_block"] = template.render({'c': ch})
        template_challenge = get_template('collector/character/character_challenge.html')
        context["challenge"] = template_challenge.render({'c': ch})
        context = respawn_summary(ch, context, request)
        context = respawn_avatar_link(ch, context, request)
        messages.info(request, 'Avatar %s customized with weapon %s.' % (ch.full_name, txt))
    else:
        context["c"] = model_to_dict(ch)
        messages.info(request, 'Ritual not found for %s.' % (ch.full_name))
    return JsonResponse(context)
