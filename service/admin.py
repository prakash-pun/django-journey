from django.contrib import admin
from .models import Team, TeamMember, Countdown

admin.site.register(Team)
admin.site.register(TeamMember)
admin.site.register(Countdown)