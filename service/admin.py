from django.contrib import admin
from .models import Team, TeamMember, Countdown, ProjectShowcase

admin.site.register(Team)
admin.site.register(TeamMember)
admin.site.register(Countdown)
admin.site.register(ProjectShowcase)
