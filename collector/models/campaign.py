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
from colour import Color

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
    description = models.TextField(max_length=128, default='', blank=True)
    gm = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    rpgsystem = models.ForeignKey(RpgSystem, null=True, blank=True, on_delete=models.SET_NULL)
    irl_year_start = models.PositiveIntegerField(default=1990, blank=True)
    is_active = models.BooleanField(default=False)
    is_available = models.BooleanField(default=False)
    smart_code = models.CharField(default='xxxxxx', max_length=6)
    current_drama = models.ForeignKey(Drama, null=True, blank=True, on_delete=models.SET_NULL)
    color_front = models.CharField(max_length=9, default='#00F0F0F0')
    color_back = models.CharField(max_length=9, default='#00101010')
    color_linkup = models.CharField(max_length=9, default='#00801080')
    color_linkdown = models.CharField(max_length=9, default='#00401040')
    color_counterback = models.CharField(max_length=9, default='#00404040')
    black_text = models.BooleanField(default=True)
    hidden = models.BooleanField(default=False)
    known_systems = models.TextField(max_length=1024, default='', blank=True)
    new_narrative = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.title} [{self.rpgsystem}]'

    def get_full_cast(self):
        if self.epic:
            return self.epic.get_full_cast()
        else:
            return []

    @property
    def avatars(self):
        from collector.models.character import Character
        avatars = Character.objects
        return avatars

    @property
    def open_avatars(self):
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
        # epic_json = self.epic.to_json()
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
        context_adventures = []
        for adventure in self.epic.adventure_set.all():
            context_adventures.append({'title': adventure.title, 'data': adventure})
            context_adventures.append(context_adventures)
            context = {'title': epic.title, 'data': epic, 'dramas': context_dramas}
            context['keywords'] = get_keywords()
        return context

    def prepare_colorset(self, size=16, color_scale=False):
        colorset = []
        hcolorset = []
        start = Color("#F0C040")
        stop = Color("#901090")
        c_colorset = list(start.range_to(stop, size))
        # c_hcolorset = list(start.range_to(Color('white'), size))
        for c in c_colorset:
            colorset.append(Color(c.hex, luminance=c.luminance * 0.75).hex)
        for c in c_colorset:
            hcolorset.append(Color(c.hex, luminance=c.luminance * 1.25).hex)
        return colorset, hcolorset

    def get_chart(self, field='', filter='', pattern='', type='bar', bar_property='full_name', order_by='',
                  legend_display=False, limit=10, ticks=True):
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
            all = self.dramatis_personae.order_by(order_by + bar_property)  # .filter(epic=self.epic)
        else:
            all = self.dramatis_personae.filter(**{filter: pattern}).order_by(order_by + bar_property)[:20]
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
                    'plugins': {
                        'title': {
                            'display': True,
                            'text': bar_property.upper(),
                            'fontColor': '#fff',
                        },
                        'legend': {
                            'display': True,
                            'position': 'top',
                            'labels': {
                                'fontColor': '#fff',
                            }
                        },
                        'scales': {
                            'yAxes': [
                                {
                                    'ticks': {'mirror': ticks},
                                    'afterFit': 'function(scaleInstance){scaleInstance.width = 300;}',
                                    'fontStyle': 'bold'
                                }
                            ]
                        },
                    },

                    # 'circumference': 2 * math.pi,
                    # 'rotation': -math.pi,
                    # 'cutoutPercentage': 40,
                }
            }
        }
        return full_data

    def get_specific_chart(self, name=''):
        from collector.models.character import Character
        color_scale = False
        skip_zero = False
        per_item = False
        if name == 'population_per_current_system':
            bar_property = 'current_fief'
            ref = 'name'
            type = 'doughnut'
            title = "Population per current system"
            legend_display = True
            skip_zero = False
        elif name == 'population_per_native_system':
            bar_property = 'fief'
            ref = 'name'
            type = 'doughnut'
            legend_display = True
            skip_zero = False
            title = "Population per native System"
        elif name == 'population_per_keyword':
            title = 'Population per Keyword'
            bar_property = 'keyword'
            ref = ''
            type = 'doughnut'
            legend_display = True
            skip_zero = True
        elif name == 'population_per_OP':
            bar_property = 'OP'
            ref = ''
            type = 'doughnut'
            legend_display = True
            skip_zero = False
            title = "Population per Freebies"
        elif name == 'population_per_alliance':
            title = 'Population per Alliance'
            bar_property = 'alliance_ref'
            ref = 'reference'
            type = 'doughnut'
            legend_display = True
            skip_zero = True
        elif name == 'population_per_team':
            title = 'Population per Team'
            bar_property = 'team'
            ref = ''
            type = 'doughnut'
            legend_display = True
            skip_zero = False
        elif name == 'population_per_ranking':
            title = 'Population per Rank'
            bar_property = 'ranking'
            ref = ''
            type = 'doughnut'
            legend_display = True
            # color_scale = True
            skip_zero = True
        elif name == 'population_per_species':
            title = 'Population per Species'
            bar_property = 'specie'
            ref = 'species'
            type = 'doughnut'
            legend_display = False
            # color_scale = True
        ticks = False
        if not per_item:
            all = self.dramatis_personae.order_by(bar_property).exclude(historical_figure=True)
        else:
            all = self.dramatis_personae.filter(occult_fire_power__gt=0).exclude(historical_figure=True)
        inside_labels = []
        final_data = []
        border = []
        data_stack = {}
        for c in all:
            value = getattr(c, bar_property)
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
                        if data_stack.get(getattr(value, ref)) is None:
                            data_stack[getattr(value, ref)] = 1
                        else:
                            data_stack[getattr(value, ref)] += 1
        for item in data_stack:
            inside_labels.append(item)
            final_data.append(data_stack[item])
            border.append('#222')
        colors, hoverColors = self.prepare_colorset(len(border), color_scale=color_scale)
        inside_datasets = [{
            'data': final_data,
            'backgroundColor': colors,
            'hoverBackgroundColor': hoverColors,
            'borderColor': border,
            'hoverBorderColor': hoverColors,
            'borderWidth': 1,
            'minBarLength': 10,
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
                    'indexAxis': 'y',
                    'responsive': True,
                    'plugins': {
                        'title': {
                            'display': True,
                            'text': title,
                            'fontColor': '#fff',
                        },
                        'legend': {
                            'display': legend_display,
                            'position': 'top',
                            'labels': {
                                'fontColor': '#FFFFFF',
                            }
                        }
                        # 'scales': {
                        #     'yAxes': [
                        #         {
                        #             'ticks': {'mirror': ticks},
                        #             'afterFit': 'function(scaleInstance){scaleInstance.width = 50;}',
                        #             'fontStyle': 'bold'
                        #         }
                        #     ]
                        # }
                        # 'circumference': 2 * math.pi,
                        # 'rotation': -math.pi,
                        # 'cutoutPercentage': 40,
                    }
                }
            }
        }
        # if name == 'population_per_occult':
        #     print(full_data)
        return full_data

    def get_occult_chart(self, occult='Psi'):
        from collector.models.character import Character
        title = 'Population with Occult powers'
        type = 'radar'
        legend_display = True
        all = self.dramatis_personae.filter(OCC_LVL__gt=0).filter(is_dead=False, occult=occult)
        inside_labels = []
        border = []
        firepowers = []
        darksides = []
        levels = []
        for c in all:
            inside_labels.append(getattr(c, 'full_name'))
            firepowers.append(getattr(c, 'occult_fire_power') / 2)
            levels.append(getattr(c, 'OCC_LVL'))
            darksides.append(getattr(c, 'OCC_DRK') * 2)
            border.append('#CCC')
        inside_datasets = [{
            'label': 'Occult Level',
            'data': levels,
            'borderWidth': 2,
            'fill': False,
            'backgroundColor': 'transparent',
            'borderColor': '#1070C0',
            'tension': 0.15,

            'pointRadius': 4,
            'pointHoverRadius': 12,
            'spanGaps': True,
        }, {
            'label': 'Darkside Level',
            'data': darksides,
            'borderWidth': 2,
            'fill': False,
            'backgroundColor': 'transparent',
            'borderColor': '#C01010',
            'tension': 0.10,
            'pointStyle': 'Cross',
            'pointRadius': 6,
            'pointHoverRadius': 12,
            'spanGaps': True,
        }, {
            'label': 'Occult firepower',
            'data': firepowers,
            'borderWidth': 2,
            'fill': False,
            'backgroundColor': 'transparent',
            'borderColor': '#10C010',
            'tension': 0.25,
            'pointRadius': 3,
            'pointHoverRadius': 12,
            'spanGaps': True,
            'clip': -5
        }
        ]
        data = {
            'labels': inside_labels,
            'datasets': inside_datasets
        }
        full_data = {
            'name': 'Occult Arts',
            'data': {
                'type': type,
                'data': data,
                'options': {
                    'plugins': {
                        'title': {
                            'display': True,
                            'text': title.upper(),
                            'fontColor': '#fff',
                        },
                        'legend': {
                            'display': legend_display,
                            'position': 'bottom',
                            'labels': {
                                'fontColor': '#fff',
                            }
                        },
                        'scales': {
                            'r': {
                                'angleLines': {
                                    'display': True,
                                    'color': '#11F',
                                    'backgroundColor': 'transparent',
                                },
                                'grid': {
                                    'display': True,
                                    'color': '#E0E',

                                },
                                'ticks': {
                                    'display': True,
                                    'color': '#F00',
                                    'backgroundColor': 'transparent',

                                },
                                'pointLabels': {
                                    'display': True,
                                    'color': '#F00',
                                    'backgroundColor': 'transparent',

                                },
                                'suggestedMin': 0,
                                'suggestedMax': 11
                            }
                        }
                    }
                }
            }
        }
        return full_data

    def to_json(self):
        from collector.utils.basic import json_default
        import json
        jstr = json.dumps(self, default=json_default, sort_keys=True, indent=4)
        return jstr

    @property
    def dramatis_personae(self):
        result = []
        if self.epic:
            rids = self.epic.get_full_cast()
            all_cast = self.avatars.filter(rid__in=rids)
            all_sup = self.avatars.filter(keyword=self.epic.shortcut)
            result = all_cast | all_sup
        return result

    @property
    def population(self):
        result = 0
        if self.epic:
            rids = self.epic.get_full_cast()
            result = len(rids)
        return result

    def get_adventures(self):
        list = []
        for a in self.epic.adventure_set.all():
            list.append({'title': a.title})
        return list

    def grab(self, id):
        if self.epic:
            characters = self.avatars.filter(pk=id)
            if len(characters) == 1:
                character = characters.first()
                if character.rid in self.epic.get_full_cast():
                    logger.warning(f"Character {character.full_name} already casted in {self.epic.name}")
                else:
                    logger.info(f"Character {character.full_name} added to cast in {self.epic.name}")
                    self.epic.description += f" ¤{character.rid}¤ "
                    self.epic.save()
            else:
                logger.error(f"Character id {id} gets multiple instances!!!")
        else:
            logger.error(f"Campaign has no epic !!!")


class CampaignAdmin(admin.ModelAdmin):
    ordering = ['irl_year_start', 'epic__era', 'title']
    list_display = ['title', 'irl_year_start', 'epic', 'is_active', 'is_available', 'new_narrative', 'smart_code',
                    'rpgsystem', 'hidden', 'gm', 'population']
