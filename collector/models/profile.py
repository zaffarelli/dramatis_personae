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
    option_display_as_list = models.BooleanField(default=False, blank=True)
    option_display_count = models.PositiveIntegerField(default=10, blank=True)
    option_has_main_epic_access = models.BooleanField(default=False, blank=True)


    @property
    def masterize(self):
        all = Campaign.objects.filter(gm=self.user)
        list = []
        for x in all:
            list.append(f'{x.smart_code}')
        return ", ".join(list)

    @property
    def is_gamemaster(self):
        campaigns = Campaign.objects.filter(gm=self.user)
        return len(campaigns)>0

    def __str__(self):
        return f'{self.user.username.title()} Profile'

    @property
    def name(self):
        return self.__str__()


    @classmethod
    def update(cls):
        users = User.objects.all()
        for user in users:
            profiles = cls.objects.filter(user=user)
            if len(profiles) == 0:
                profile = Profile()
                profile.user = user
                profile.save()
            elif len(profiles) == 1:
                profile = profiles.first()
                if not profile.is_gamemaster:
                    profile.option_display_count = 20
                    profile.option_display_as_list = True
                    profile.save()


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'is_gamemaster','option_has_main_epic_access', 'masterize', 'main_character', 'main_epic', 'option_display_as_list', 'option_display_count']
    order_by = ['-main_epic', '-main_character']
    list_filter = ['main_epic']
    list_editable = ['option_display_as_list', 'option_display_count','main_epic', 'option_has_main_epic_access','main_character']
