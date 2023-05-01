from django.db import models
from django.contrib.auth.models import User
from collector.models.character import Character
# from collector.models.campaign import Campaign
from django.contrib import admin


class Profile(models.Model):
    class Meta:
        ordering = ['user']
        verbose_name = "References: User Profile"
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    # main_character = models.ForeignKey(Character, on_delete=models.SET_NULL, null=True, blank=True)
    # campaign = models.ForeignKey(Campaign, on_delete=models.SET_NULL, null=True, blank=True)

    option_display_as_list = models.BooleanField(default=False)
    option_display_count = models.PositiveIntegerField(default=10)


    @property
    def masterize(self):
        from scenarist.models.cards import Card
        all = Card.objects.filter(gamemaster=self.user.email, card_type__in=['EP']).order_by('era')
        list = []
        for x in all:
            list.append(f'{x.full_id} {x.name}')
        # return ", ".join(list)
        return list


    @property
    def is_gamemaster(self):
        from scenarist.models.cards import Card
        all = Card.objects.filter(gamemaster=self.user.email, card_type__in=['EP']).order_by('era')
        list = []
        for x in all:
            list.append(f'{x.full_id}')
        return len(list)>0

    @property
    def current_epic(self):
        from scenarist.models.cards import Card
        epic = None
        epics = Card.objects.filter(gamemaster=self.user.email, card_type__in=['EP'], is_ongoing=True)
        if len(epics)==1:
            epic = epics.first()
        return epic


    @property
    def plays(self):
        from scenarist.models.cards import Card
        if self.main_character is None:
            return None
        else:
            mine = f'{self.main_character.rid}__{self.main_character.id}'
            # print(mine)
        all = Card.objects.filter(card_type__in=['BK'], name__startswith='Players').order_by('era')
        list = []
        for x in all:
            if x.parent.card_type == 'EP':
                e = x.parent
                # print(e.name)
                # print(e.dramatis_personae)
                if mine in e.dramatis_personae:
                    list.append(f'{e.full_id} {e.name}')
        # return ", ".join(list)
        return list

    def __str__(self):
        return f'{self.user.username.title()} Profile'

    @property
    def main_character(self):
        result = None
        from collector.models.character import Character
        players = Character.objects.filter(player=self.user)
        if len(players)>0:
            result = players.first()
        return result


    @property
    def name(self):
        return self.__str__()


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'is_gamemaster', 'masterize', 'plays', 'main_character']
    order_by = ['-main_character']
    list_filter = []
