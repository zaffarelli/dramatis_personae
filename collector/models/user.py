from django.db import models
from django.contrib.auth.models import User
from collector.models.character import Character
from scenarist.models.epics import Epic
from django.contrib import admin


class Profile(models.Model):
    class Meta:
        ordering = ['main_epic', '-main_character' ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    main_character = models.ForeignKey(Character, on_delete=models.SET_NULL, null=True, blank=True)
    main_epic = models.ForeignKey(Epic, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_gamemaster(self):
        return self.main_character is None

    def __str__(self):
        return f'{self.user.username.title()} Profile'

    @property
    def name(self):
        return self.__str__()


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'is_gamemaster', 'main_character', 'main_epic']
    order_by = ['main_epic', '-main_character']
    list_filter = ['main_epic']
