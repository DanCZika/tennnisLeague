from django.contrib import admin
from .models import PlayerData, Round, Entry, Match, MatchEntry

admin.site.register(PlayerData)
admin.site.register(Round)
admin.site.register(Entry)
admin.site.register(Match)
admin.site.register(MatchEntry)