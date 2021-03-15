from django.db import models
from django.contrib.auth.models import User
from collector.models.character import Character
from scenarist.models.epics import Epic
from collector.models.campaign import Campaign
from django.contrib import admin


class Profile(models.Model):
    class Meta:
        ordering = ['main_epic', '-main_character' ]
        verbose_name = "References: User Profile"
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    main_character = models.ForeignKey(Character, on_delete=models.SET_NULL, null=True, blank=True)
    main_epic = models.ForeignKey(Epic, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def masterize(self):

        all = Campaign.objects.filter(gm=self.user)
        list = []
        for x in all:
            list.append(f'{x.smart_code}')
        return ", ".join(list)

    @property
    def is_gamemaster(self):
        from collector.utils.basic import get_current_config
        campaign = get_current_config()
        is_gm = False
        is_gm = campaign.gm == self.user
        return is_gm


    def __str__(self):
        return f'{self.user.username.title()} Profile'

    @property
    def name(self):
        return self.__str__()


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'masterize', 'main_character', 'main_epic']
    order_by = ['main_epic', '-main_character']
    list_filter = ['main_epic']
