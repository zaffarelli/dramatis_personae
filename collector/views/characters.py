'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView
from collector.forms.basic import CharacterForm, SkillFormSet, TalentFormSet, BlessingCurseFormSet, BeneficeAfflictionFormSet, ArmorFormSet, WeaponFormSet, ShieldFormSet
from collector.models.characters import Character
from scenarist.mixins.ajaxfromresponse import AjaxFromResponseMixin

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
  template_name_suffix = '_form'

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
    else:
      context['form'] = CharacterForm(instance=self.object)
      context['skills'] = SkillFormSet(instance=self.object)
      context['talents'] = TalentFormSet(instance=self.object)
      context['blessingcurses'] = BlessingCurseFormSet(instance=self.object)
      context['beneficeafflictions'] = BeneficeAfflictionFormSet(instance=self.object)
      context['armors'] = ArmorFormSet(instance=self.object)
      context['weapons'] = WeaponFormSet(instance=self.object)
      context['shields'] = ShieldFormSet(instance=self.object)      
    return context
