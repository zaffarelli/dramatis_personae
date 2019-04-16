'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.views.generic.edit import UpdateView
from extra_views import UpdateWithInlinesView
from django.views.generic.detail import DetailView
from django.contrib import messages
from collector.forms.basic import CharacterForm, SkillFormSet, TalentFormSet, BlessingCurseFormSet, BeneficeAfflictionFormSet, ArmorFormSet, WeaponFormSet, ShieldFormSet
from collector.models.characters import Character
from scenarist.mixins.ajaxfromresponse import AjaxFromResponseMixin
from django.urls import reverse_lazy

class CharacterDetailView(DetailView):
  model = Character
  context_object_name = 'c'  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    return context

class CharacterUpdateView(AjaxFromResponseMixin,UpdateView):
  model = Character
  form_class = CharacterForm
  context_object_name = 'c'
  template_name_suffix = '_update_form'  
  
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
      messages.add_message(self.request, messages.INFO, 'Updating character %s'%(context['form']['full_name']['value']))
    else:
      context['form'] = CharacterForm(instance=self.object)
      context['skills'] = SkillFormSet(instance=self.object)
      context['talents'] = TalentFormSet(instance=self.object)
      context['blessingcurses'] = BlessingCurseFormSet(instance=self.object)
      context['beneficeafflictions'] = BeneficeAfflictionFormSet(instance=self.object)
      context['armors'] = ArmorFormSet(instance=self.object)
      context['weapons'] = WeaponFormSet(instance=self.object)
      context['shields'] = ShieldFormSet(instance=self.object)
      messages.add_message(self.request, messages.INFO, 'Editing character %s'%(context['form']['full_name'].value()))
    return context
