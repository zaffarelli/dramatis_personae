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


def customize_skill(slug):
  print(slug)

def customize_bc(slug):
  print(slug)

def customize_ba(slug):
  print(slug)
