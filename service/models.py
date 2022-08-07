import random
from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify
from authentication.constants import DEFAULT_AVATAR
from authentication.models import CustomUser


class Team(models.Model):
    team_name = models.CharField(max_length=255, null=False)
    owner = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, blank=True, null=True, related_name="team_owner"
    )
    slug = models.SlugField(null=False, unique=True, blank=True, max_length=200)
    description = models.CharField(max_length=5000, null=True, blank=True)
    status = models.BooleanField(default=True)  # Public status
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    @property
    def avatar(self):
        if self.owner:
            return self.owner.avatar
        return DEFAULT_AVATAR

    @property
    def owner_name(self):
        if self.owner:
            return self.owner.username
        return "Unknown"

    def __str__(self):
        return self.team_name

    def save(self, *args, **kwargs):
        if not self.slug:
            val = self.team_name
            while(True):
                test = slugify(val)
                if(self.__class__.objects.filter(slug=test).count() == 0):
                    break
                val = self.team_name + str(random.randint(1, 500))
            self.slug = test
        return super().save(*args, **kwargs)


class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True, null=True, related_name="team_member")
    member_name = models.CharField(max_length=255, null=False)
    avatar = models.ImageField(
        upload_to='team/avatar/', default=DEFAULT_AVATAR, blank=True)
    position = models.CharField(max_length=255, null=False)
    website = models.CharField(max_length=100, null=True, blank=True)
    github_username = models.CharField(max_length=100, null=True, blank=True)
    linkedln_username = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    
    @property
    def team_name(self):
        "Returns the team name."
        if self.team:
            return self.team.team_name

    def __str__(self):
        return f"{self.member_name} of team"


class Countdown(models.Model):
    owner = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, blank=True, null=True, related_name="owner"
    )
    countdown_name = models.CharField(max_length=255, null=False)
    slug = models.SlugField(null=False, unique=True, blank=True, max_length=200)
    date = models.DateField(null=False)
    time = models.TimeField(null=False)
    countdown_timezone = models.CharField(max_length=50, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.countdown_name

    def save(self, *args, **kwargs):
        if not self.slug:
            val = self.countdown_name
            while(True):
                test = slugify(val)
                if(self.__class__.objects.filter(slug=test).count() == 0):
                    break
                val = self.countdown_name + str(random.randint(1, 500))
            self.slug = test
        return super().save(*args, **kwargs)