"""
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
"""
from django.db import models
from django.contrib import admin
import random
import math
import logging

logger = logging.getLogger(__name__)

RPG_SYSTEMS = (
    ('0', 'Undefined'),
    ('1', 'Fading Suns 2nd Edition'),
    ('2', 'Fading Suns FICS'),
    ('3', 'Pathfinder'),
    ('4', 'World of Darkness'),
    ('5', 'Call of Cthulhu 7E'),
    ('6', 'Polaris'),
)


class Campaign(models.Model):
    class Meta:
        ordering = ['title', 'epic']
        verbose_name = "References: Campaign Config"
    from scenarist.models.epics import Epic
    from scenarist.models.dramas import Drama
    from django.contrib.auth.models import User
    from collector.models.rpg_system import RpgSystem
    title = models.CharField(default='aaa', max_length=128, )
    epic = models.ForeignKey(Epic, null=True, blank=True, on_delete=models.SET_NULL)
    description = models.TextField(max_length=128, default='')
    #gamemaster = models.CharField(default='zaffarelli@gmail.com', max_length=128, blank=True)
    gm = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    rpgsystem = models.ForeignKey(RpgSystem, null=True, blank=True, on_delete=models.SET_NULL)
    is_active = models.BooleanField(default=False)
    smart_code = models.CharField(default='xxxxxx', max_length=6)
    current_drama = models.ForeignKey(Drama, null=True, blank=True, on_delete=models.SET_NULL)
    #rpg_system = models.CharField(max_length=32, choices=RPG_SYSTEMS, default="2")
    color_front = models.CharField(max_length=9, default='#00F0F0F0')
    color_back = models.CharField(max_length=9, default='#00101010')
    color_linkup = models.CharField(max_length=9, default='#00801080')
    color_linkdown = models.CharField(max_length=9, default='#00401040')
    color_counterback = models.CharField(max_length=9, default='#00404040')
    #logo = models.CharField(max_length=128, default='nologo.png')
    #back = models.CharField(max_length=128, default='back.png')
    black_text = models.BooleanField(default=True)
    hidden = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.title} [{self.rpgsystem}]'

    def get_full_cast(self):
        if self.epic:
            return self.epic.get_full_cast()
        else:
            return []

    @property
    def avatars(self):
        avatars = []
        if self.is_coc7:
            from collector.models.investigator import Investigator
            avatars = Investigator.objects
        else:
            from collector.models.character import Character
            avatars = Character.objects.filter(epic=self.epic)
        return avatars

    @property
    def open_avatars(self):
        avatars = []
        if self.is_coc7:
            from collector.models.investigator import Investigator
            avatars = Investigator.objects
        else:
            from collector.models.character import Character
            avatars = Character.objects
        return avatars

    @property
    def is_coc7(self):
        return self.rpgsystem.smart_code == "COC7"

    @property
    def is_fics(self):
        return self.rpgsystem.smart_code == "FICS"

    @property
    def is_wawwod(self):
        return self.rpgsystem.smart_code == "WaWWoD"

    @property
    def is_prpg(self):
        return self.rpgsystem.smart_code == "PRPG"


    def parse_details(self):
        """ Return details from the config epic, dramas and acts
        """
        from scenarist.models.epics import Epic
        from scenarist.models.dramas import Drama
        from scenarist.models.acts import Act
        from scenarist.models.events import Event
        from collector.utils.fs_fics7 import get_keywords

        epic = Epic.objects.get(title=self.epic.title)
        dramas = Drama.objects.filter(epic=epic).order_by('chapter', 'date')
        context_dramas = []
        for drama in dramas:
            context_acts = []
            acts = Act.objects.filter(drama=drama).order_by('chapter', 'date')
            for act in acts:
                context_events = []
                events = Event.objects.filter(act=act).order_by('chapter', 'date')
                for event in events:
                    context_event = {'title': event.title, 'data': event}
                    context_events.append(context_event)
                context_act = {'title': act.title, 'data': act, 'events': context_events}
                context_acts.append(context_act)
            context_drama = {'title': drama.title, 'data': drama, 'acts': context_acts}
            context_dramas.append(context_drama)
        context = {'title': epic.title, 'data': epic, 'dramas': context_dramas}
        context['keywords'] = get_keywords()
        return context

    def prepare_colorset(self, size=16):
        colorset = []
        hcolorset = []
        colval = '456789AB'
        idx = 0
        while idx < size:
            com = '%s%s%s%s%s%s' % (
            random.sample(colval, 1)[0], random.sample(colval, 1)[0], random.sample(colval, 1)[0],
            random.sample(colval, 1)[0], random.sample(colval, 1)[0], random.sample(colval, 1)[0])
            col = '#' + com + '88'
            hcol = '#' + com + 'FF'
            colorset.append(col)
            hcolorset.append(hcol)
            idx += 1
        return colorset, hcolorset

    def get_chart(self, field='', filter='', pattern='', type='bar', bar_property='full_name', order_by='', legend_display=False, limit=10, ticks=True):
        """ Makes the data dictionary ChartJS needs to build the relevant chart. Note that those charts
            are all built from the Character model; that justifies the choice for default values
            that might not be relevant to other model tables.
            Among the important parameters:
                - "field" is the main parameter used to sort the data.
                - "filter" is a model compliant filter, like "name__contains"
                - "pattern" is the value that we put on the other side of the filter after the equal sign, like "joe".
                    It can be of any type as long as it fits the content of "filter".
                - "type" is the type of chart in among the ChartJS options.
                - "bar_property" is the field that is supposed to be displayed on the left hand on the char.
                - "order_by" is the sort criteria. Set to the characters "full_name" by default.
        """
        from collector.models.character import Character
        # from django.db.models import Count
        if pattern == '':
            all = Character.objects.order_by(order_by + bar_property).filter(epic=self.epic)
        else:
            all = Character.objects.filter(**{filter: pattern}).order_by(order_by + bar_property)[:20]
        # if limit:
        #     all = all[:limit]
            # .values('epic').annotate(dcount=Count('epic'))
        # else:
        #     all = Character.objects.filter(epic=self.epic, is_visible=True).order_by(order_by)[:10]
        inside_labels = []
        dat = []
        border = []
        arrfetch = {}
        for c in all:
            value = c.__dict__[field]
            if pattern == '':
                if arrfetch.get(value) is None:
                    arrfetch[value] = 1
                else:
                    arrfetch[value] += 1
            else:
                if arrfetch.get(value) is None:
                    arrfetch[value] = c.__dict__[bar_property]
        for item in arrfetch:
            inside_labels.append(item)
            dat.append(arrfetch[item])
            border.append('#C0C0C0C0')
        colors, hoverColors = self.prepare_colorset(len(border))
        inside_datasets = [{
            'data': dat,
            'backgroundColor': colors,
            'hoverBackgroundColor': hoverColors,
            'borderColor': border,
            'hoverBorderColor': hoverColors,
            'borderWidth': 1,
            'minBarLength': 30
        }]
        data = {
            'labels': inside_labels,
            'datasets': inside_datasets
        }
        full_data = {
            'name': field,
            'data': {
                'type': type,
                'data': data,
                'options': {
                    'title': {
                        'display': True,
                        'text': bar_property.upper(),
                        'fontColor': '#fff',
                    },
                    'legend': {
                        'display': legend_display,
                        'position': 'right',
                        'labels': {
                            'fontColor': '#fff',
                        }
                    },
                    'scales': {
                        'yAxes': [
                            {
                                'ticks': {'mirror': ticks},
                                'afterFit': 'function(scaleInstance){scaleInstance.width = 400;}',
                                'fontStyle': 'bold'
                            }
                        ]
                    },
                    'circumference': 2 * math.pi,
                    'rotation': -math.pi,
                    'cutoutPercentage': 40,
                }
            }
        }
        return full_data


class CampaignAdmin(admin.ModelAdmin):
    ordering = ['title']
    list_display = ['__str__','title', 'epic', 'is_active', 'smart_code', 'rpgsystem', 'hidden', 'gm']
