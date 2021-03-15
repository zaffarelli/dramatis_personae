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
    gm = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    rpgsystem = models.ForeignKey(RpgSystem, null=True, blank=True, on_delete=models.SET_NULL)
    is_active = models.BooleanField(default=False)
    smart_code = models.CharField(default='xxxxxx', max_length=6)
    current_drama = models.ForeignKey(Drama, null=True, blank=True, on_delete=models.SET_NULL)
    color_front = models.CharField(max_length=9, default='#00F0F0F0')
    color_back = models.CharField(max_length=9, default='#00101010')
    color_linkup = models.CharField(max_length=9, default='#00801080')
    color_linkdown = models.CharField(max_length=9, default='#00401040')
    color_counterback = models.CharField(max_length=9, default='#00404040')
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
            avatars = Character.objects
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

    def prepare_colorset(self, size=16, color_scale=False):
        colorset = []
        hcolorset = []
        colval = '1234567894ABCDE'
        idx = 0
        if color_scale:
            colval = 'ABCDE'
            prev_com_arr = []
            while idx < size:
                if idx==0:
                    com_arr = []
                    com_arr.append(random.sample(colval, 1)[0])
                    com_arr.append(random.sample(colval, 1)[0])
                    com_arr.append(random.sample(colval, 1)[0])
                    com_arr.append(random.sample(colval, 1)[0])
                    prev_com_arr = com_arr
                    com = '%s%s%s%s' % (com_arr[0],com_arr[1],com_arr[2],com_arr[3])
                else:
                    com_arr = prev_com_arr
                    red = f'0x{com_arr[0]}{com_arr[1]}'
                    green = f'0x{com_arr[2]}{com_arr[3]}'
                    new_red = f'{hex(int(red,16) - 17)}'
                    new_green = f'{hex(int(green, 16) - 9)}'
                    com_arr[0] = new_red[2]
                    com_arr[1] = new_red[3]
                    com_arr[2] = new_green[2]
                    com_arr[3] = new_green[3]
                    com = '%s%s%s%s' % (com_arr[0], com_arr[1], com_arr[2], com_arr[3])
                    prev_com_arr = com_arr
                col = '#' + com + 'A0'
                hcol = '#' + com + 'C0'
                colorset.append(col)
                hcolorset.append(hcol)
                idx += 1
        else:
            while idx < size:
                com = '%s%s%s%s' % (
                    random.sample(colval, 1)[0],
                    random.sample(colval, 1)[0], random.sample(colval, 1)[0], random.sample(colval, 1)[0])
                col = '#' + com + 'A0'
                hcol = '#' + com + 'C0'
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
        from cartograph.models.system import System
        # from django.db.models import Count
        if pattern == '':
            all = Character.objects.order_by(order_by + bar_property) #.filter(epic=self.epic)
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


    def get_specific_chart(self, name=''):
        from collector.models.character import Character
        color_scale = False
        skip_zero = False
        if name== 'population_per_current_system':
            title = 'Population per current fief'
            bar_property = 'current_fief'
            ref = 'name'
            type = 'horizontalBar'
            legend_display = False
        elif name== 'population_per_native_system':
            title = 'Population per native fief'
            bar_property = 'fief'
            ref = 'name'
            type = 'horizontalBar'
            legend_display = False
        elif name== 'population_per_alliance':
            title = 'Population per Alliance'
            bar_property = 'alliance_ref'
            ref = 'reference'
            type = 'horizontalBar'
            legend_display = False
        elif name== 'population_per_team':
            title = 'Population per Team'
            bar_property = 'team'
            ref = ''
            type = 'horizontalBar'
            legend_display = False
            color_scale = True
        elif name== 'population_per_occult':
            title = 'Population with Occult powers'
            bar_property = 'OCC_LVL'
            ref = ''
            type = 'polarArea'
            legend_display = True
            color_scale = True
            skip_zero = True
        elif name== 'population_per_ranking':
            title = 'Population per Rank'
            bar_property = 'ranking'
            ref = ''
            type = 'polarArea'
            legend_display = True
            color_scale = True
            skip_zero = True

        ticks = False
        all = Character.objects.order_by(bar_property)
        inside_labels = []
        final_data = []
        border = []
        data_stack = {}
        for c in all:
            value = getattr(c,bar_property)
            if skip_zero and value == 0:
                pass
            else:
                if not value is None:
                    if ref == '':
                        if data_stack.get(value) is None:
                            data_stack[value] = 1
                        else:
                            data_stack[value] += 1
                    else:
                        if data_stack.get(getattr(value,ref)) is None:
                            data_stack[getattr(value,ref)] = 1
                        else:
                            data_stack[getattr(value,ref)] += 1
        for item in data_stack:
            inside_labels.append(item)
            final_data.append(data_stack[item])
            border.append('#222')
        colors, hoverColors = self.prepare_colorset(len(border),color_scale=color_scale)
        inside_datasets = [{
            'data': final_data,
            'backgroundColor': colors,
            'hoverBackgroundColor': hoverColors,
            'borderColor': border,
            'hoverBorderColor': hoverColors,
            'borderWidth': 1,
            'minBarLength': 10
        }]
        data = {
            'labels': inside_labels,
            'datasets': inside_datasets
        }
        full_data = {
            'name': name,
            'data': {
                'type': type,
                'data': data,
                'options': {
                    'title': {
                        'display': True,
                        'text': title.upper(),
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
                                'afterFit': 'function(scaleInstance){scaleInstance.width = 100;}',
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
