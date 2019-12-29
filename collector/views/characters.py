'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.views.generic.edit import UpdateView
from extra_views import UpdateWithInlinesView
from django.views.generic.detail import DetailView
from django.contrib import messages
from collector.forms.basic import CharacterForm, SkillFormSet, TalentFormSet, BlessingCurseFormSet, BeneficeAfflictionFormSet, ArmorFormSet, WeaponFormSet, ShieldFormSet, TourOfDutyFormSet
from collector.models.character import Character
from scenarist.mixins.ajaxfromresponse import AjaxFromResponseMixin
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.template.loader import get_template

class CharacterDetailView(DetailView):
    model = Character
    context_object_name = 'c'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['no_skill_edit'] = True
        #print(context['c'].full_name)
        messages.info(self.request, 'Display avatar %s'%(context['c'].full_name))
        return context


class CharacterUpdateView(AjaxFromResponseMixin,UpdateView):
    model = Character
    form_class = CharacterForm
    context_object_name = 'c'
    template_name_suffix = '_update_form'
    #success_url=reverse_lazy('collector:view_character')

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        skills_formset = context['skills']
        talents_formset = context['talents']
        blessingcurses_formset = context['blessingcurses']
        beneficeafflictions_formset = context['beneficeafflictions']
        armors_formset = context['armors']
        weapons_formset = context['weapons']
        shields_formset = context['shields']
        tourofdutys_formset = context['tourofdutys']
        if skills_formset.is_valid() and talents_formset.is_valid() and blessingcurses_formset.is_valid() and beneficeafflictions_formset.is_valid() and armors_formset.is_valid() and weapons_formset.is_valid() and shields_formset.is_valid() and tourofdutys_formset.is_valid():
            response = super().form_valid(form)
            skills_formset.instance = self.object
            talents_formset.instance = self.object
            blessingcurses_formset.instance = self.object
            beneficeafflictions_formset.instance = self.object
            armors_formset.instance = self.object
            weapons_formset.instance = self.object
            shields_formset.instance = self.object
            tourofdutys_formset.instance = self.object
            skills_formset.save()
            talents_formset.save()
            blessingcurses_formset.save()
            beneficeafflictions_formset.save()
            armors_formset.save()
            weapons_formset.save()
            shields_formset.save()
            tourofdutys_formset.save()
            return response
        else:
            messages.info(self.request, 'Avatar %s has errors. unable to save.'%(context['c'].full_name))
            return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(CharacterUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['form'] = CharacterForm(self.request.POST, instance=self.object)
            context['skills'] = SkillFormSet(self.request.POST, instance=self.object)
            context['talents'] = TalentFormSet(self.request.POST, instance=self.object)
            context['blessingcurses'] = BlessingCurseFormSet(self.request.POST, instance=self.object)
            context['beneficeafflictions'] = BeneficeAfflictionFormSet(self.request.POST, instance=self.object)
            context['armors'] = ArmorFormSet(self.request.POST, instance=self.object)
            context['weapons'] = WeaponFormSet(self.request.POST, instance=self.object)
            context['shields'] = ShieldFormSet(self.request.POST, instance=self.object)
            context['tourofdutys'] = TourOfDutyFormSet(self.request.POST, instance=self.object)
            context['skills'].full_clean()
            context['talents'].full_clean()
            context['blessingcurses'].full_clean()
            context['beneficeafflictions'].full_clean()
            context['armors'].full_clean()
            context['weapons'].full_clean()
            context['shields'].full_clean()
            context['tourofdutys'].full_clean()
            messages.success(self.request, 'Updating avatar %s'%(context['form']['full_name'].value()))
        else:
            context['form'] = CharacterForm(instance=self.object)
            context['skills'] = SkillFormSet(instance=self.object)
            context['talents'] = TalentFormSet(instance=self.object)
            context['blessingcurses'] = BlessingCurseFormSet(instance=self.object)
            context['beneficeafflictions'] = BeneficeAfflictionFormSet(instance=self.object)
            context['armors'] = ArmorFormSet(instance=self.object)
            context['weapons'] = WeaponFormSet(instance=self.object)
            context['shields'] = ShieldFormSet(instance=self.object)
            context['tourofdutys'] = TourOfDutyFormSet(instance=self.object)
            messages.info(self.request, 'Form display for avatar %s'%(context['form']['full_name'].value()))
        return context

@csrf_exempt
def skill_pick(request, avatar, item, offset):
    """ Touching skills to edit them in the view """
    from collector.models.skill_ref import SkillRef
    context = {}
    offset = int(offset) -50;
    ch = Character.objects.get(pk=avatar)
    skillref = SkillRef.objects.get(pk=item)
    ch.charactercusto.add_or_update_skill(skillref.id,offset)
    ch.fix()
    ch.save()
    skill = ch.skill_set.all().filter(skill_ref__id=item).first()
    context["c"] = model_to_dict(ch)
    template = get_template('collector/character/character_skill.html')
    context["block"] = template.render({'c':ch, 'skill': skill})
    template = get_template('collector/custo/summary_block.html')
    context["summary"] = template.render({'c':ch})
    return JsonResponse(context)

@csrf_exempt
def attr_pick(request, avatar, item, offset):
    """ Touching skills to edit them in the view """
    context = {}
    offset = int(offset) -50;
    ch = Character.objects.get(pk=avatar)
    x = getattr(ch.charactercusto,item,-100)
    if x==-100:
        setattr(ch.charactercusto,item,offset)
    else:
        setattr(ch.charactercusto,item,x+offset)
    print(item)
    info = ("info_"+item.split("_")[1]).lower()
    ch.fix()
    ch.save()
    context["c"] = model_to_dict(ch)
    template = get_template('collector/character/character_pa.html')
    context["block"] = template.render({'c':getattr(ch,info)})
    template = get_template('collector/custo/summary_block.html')
    context["summary"] = template.render({'c':ch})
    return JsonResponse(context)



@csrf_exempt
def customize_skill(request,avatar,item):
    from collector.models.skill_ref import SkillRef
    from collector.models.character_custo import CharacterCusto
    from collector.models.skill_custo import SkillCusto
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
    context["block"] = template.render({'c':ch})
    template = get_template('collector/custo/skill_custo_block.html')
    context["custo_block"] = template.render({'c':ch})
    template = get_template('collector/custo/summary_block.html')
    context["summary"] = template.render({'c':ch})
    messages.info(request, 'Avatar %s customized with skill %s at +1.'%(ch.full_name,new_item.skill_ref.reference))
    return JsonResponse(context)

@csrf_exempt
def customize_bc(request,avatar,item):
    from collector.models.blessing_curse_ref import BlessingCurseRef
    from collector.models.character_custo import CharacterCusto
    from collector.models.blessing_curse_custo import BlessingCurseCusto
    context = {}
    ch = Character.objects.get(pk=avatar)
    bcr = BlessingCurseRef.objects.get(pk=item)
    bcc = BlessingCurseCusto()
    bcc.character_custo = ch.charactercusto
    bcc.blessing_curse_ref = bcr
    bcc.save()
    ch.fix()
    ch.save()
    context["c"] = model_to_dict(ch)
    template = get_template('collector/character/character_bc.html')
    context["block"] = template.render({'c':ch})
    template = get_template('collector/custo/bc_custo_block.html')
    context["custo_block"] = template.render({'c':ch})
    template = get_template('collector/custo/summary_block.html')
    context["summary"] = template.render({'c':ch})
    messages.info(request, 'Avatar %s customized with B/C %s.'%(ch.full_name,bcc.blessing_curse_ref.reference))
    return JsonResponse(context)

@csrf_exempt
def customize_bc_del(request,avatar,item):
    from collector.models.blessing_curse_ref import BlessingCurseRef
    from collector.models.character_custo import CharacterCusto
    from collector.models.blessing_curse_custo import BlessingCurseCusto
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
        ch.fix()
        ch.save()
        context["c"] = model_to_dict(ch)
        template = get_template('collector/character/character_bc.html')
        context["block"] = template.render({'c':ch})
        template = get_template('collector/custo/bc_custo_block.html')
        context["custo_block"] = template.render({'c':ch})
        messages.info(request, 'Avatar %s customized with B/C %s.'%(ch.full_name,txt))
        template = get_template('collector/custo/summary_block.html')
        context["summary"] = template.render({'c':ch})
    else:
        context["c"] = model_to_dict(ch)
        messages.info(request, 'B/C not found for %s.'%(ch.full_name))
    return JsonResponse(context)

@csrf_exempt
def customize_ba(request,avatar,item):
    from collector.models.benefice_affliction_ref import BeneficeAfflictionRef
    from collector.models.character_custo import CharacterCusto
    from collector.models.benefice_affliction_custo import BeneficeAfflictionCusto
    context = {}
    ch = Character.objects.get(pk=avatar)
    bar = BeneficeAfflictionRef.objects.get(pk=item)
    bac = BeneficeAfflictionCusto()
    bac.character_custo = ch.charactercusto
    bac.benefice_affliction_ref = bar
    bac.save()
    ch.fix()
    ch.save()
    context["c"] = model_to_dict(ch)
    template = get_template('collector/character/character_ba.html')
    context["block"] = template.render({'c':ch})
    template = get_template('collector/custo/ba_custo_block.html')
    context["custo_block"] = template.render({'c':ch})
    template = get_template('collector/custo/summary_block.html')
    context["summary"] = template.render({'c':ch})
    messages.info(request, 'Avatar %s customized with B/A %s.'%(ch.full_name,bac.benefice_affliction_ref.reference))
    return JsonResponse(context)

@csrf_exempt
def customize_ba_del(request,avatar,item):
    from collector.models.benefice_affliction_ref import BeneficeAfflictionRef
    from collector.models.character_custo import CharacterCusto
    from collector.models.benefice_affliction_custo import BeneficeAfflictionCusto
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
        ch.fix()
        ch.save()
        context["c"] = model_to_dict(ch)
        template = get_template('collector/character/character_ba.html')
        context["block"] = template.render({'c':ch})
        template = get_template('collector/custo/ba_custo_block.html')
        context["custo_block"] = template.render({'c':ch})
        template = get_template('collector/custo/summary_block.html')
        context["summary"] = template.render({'c':ch})
        messages.info(request, 'Avatar %s customized with B/A %s.'%(ch.full_name,txt))
    else:
        context["c"] = model_to_dict(ch)
        messages.info(request, 'B/A not found for %s.'%(ch.full_name))
    return JsonResponse(context)
