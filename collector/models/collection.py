"""
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
"""
from django.db import models
from collector.models.character import Character
from django.contrib import admin
import math
import json

ORPHANS_COLLECTION = "Orphans"


class Collection(models.Model):
    class Meta:
        ordering = ['reference']
        verbose_name = "FICS: Collection"

    reference = models.CharField(max_length=64, default='', unique=True)
    description = models.TextField(max_length=1024, default='', blank=True)
    members = models.ManyToManyField(Character, blank=True)
    census = models.PositiveIntegerField(default=0, blank=True)
    category = models.PositiveIntegerField(default=1, blank=True)
    balanced_ratio = models.PositiveIntegerField(default=0, blank=True)
    published = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return f'{self.reference:20s}'

    @property
    def all_members(self):
        return self.members.all()

    @property
    def members_as_str(self):
        lst = []
        max = 100
        for item in self.all_members:
            if max > 0:
                lst.append(item.aka)
                max -= 1

        return ", ".join(lst)

    def fix(self):
        self.census = 0
        if self.reference == ORPHANS_COLLECTION:
            for c in Character.objects.all():
                if len(c.collection_set.exclude(reference=ORPHANS_COLLECTION, archived=True)) == 0:
                    self.members.add(c)
        self.census = self.members.all().count()
        # print('balanced ratio computation')
        if self.census > 0:
            cnt = self.members.filter(balanced=True).count()
            # print(cnt)
            # print(self.census)
            self.balanced_ratio = int(math.floor(float(cnt) / float(self.census) * 100))
        else:
            self.balanced_ratio = 0

    def fill_from_casting(self, rid_list=[]):
        mine = self.members.all()
        for c in Character.objects.filter(rid__in=rid_list):
            if not c in mine:
                self.members.add(c)
        self.census = self.members.all().count()
        print('Filled from casting :')
        print(rid_list)


    @classmethod
    def create_orphans_collection(klass):
        matches = klass.objects.filter(reference=ORPHANS_COLLECTION)
        if len(matches) != 1:
            orphans = Collection()
            orphans.reference = ORPHANS_COLLECTION
            orphans.save()
        else:
            orphans = matches.first()
        orphans.reference = ORPHANS_COLLECTION
        orphans.category = 0
        orphans.description = 'List of characters not included in any collection.'
        orphans.save()

    @property
    def to_json(self):
        """ Returns JSON of object """
        from datetime import datetime
        from scenarist.utils.tools import json_default
        jst = json.dumps(self, default=json_default, sort_keys=True, indent=4)
        job = json.loads(jst)
        members = ""
        for m in self.all_members:
            members += f"¤{m.rid}¤ "
        job['members'] = members
        return job


class CollectionAdmin(admin.ModelAdmin):
    ordering = ['reference']
    list_display = ['reference', 'category', 'description', 'members_as_str', 'census', 'balanced_ratio']
    list_filter = ['category']
    search_filter = ['description', 'reference']
