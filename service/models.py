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
    slug = models.SlugField(null=False, unique=True,
                            blank=True, max_length=200)
    description = models.CharField(max_length=5000, null=True, blank=True)
    website = models.URLField(blank=True, max_length=200)
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
            while (True):
                test = slugify(val)
                if (self.__class__.objects.filter(slug=test).count() == 0):
                    break
                val = self.team_name + str(random.randint(1, 500))
            self.slug = test
        return super().save(*args, **kwargs)


class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE,
                             blank=True, null=True, related_name="team_member")
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

    def delete_avatar(self):
        img_file = self.avatar
        if not img_file.name == DEFAULT_AVATAR:
            img_file.delete()


class Countdown(models.Model):
    owner = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, blank=True, null=True, related_name="owner"
    )
    countdown_name = models.CharField(max_length=255, null=False)
    slug = models.SlugField(null=False, unique=True,
                            blank=True, max_length=200)
    description = models.CharField(max_length=5000, null=True, blank=True)
    emoji = models.CharField(max_length=100, null=True, blank=True)
    date_time = models.DateTimeField(null=False)
    countdown_timezone = models.CharField(max_length=50, null=True)
    position = models.PositiveIntegerField(null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.countdown_name

    def save(self, *args, **kwargs):
        if not self.slug:
            val = self.countdown_name
            while (True):
                test = slugify(val)
                if (self.__class__.objects.filter(slug=test).count() == 0):
                    break
                val = self.countdown_name + str(random.randint(1, 500))
            self.slug = test
        return super().save(*args, **kwargs)


class ProjectShowcase(models.Model):
    project_name = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=1000, null=True, blank=True)
    slug = models.SlugField(null=False, blank=True,
                            unique=True, max_length=200)
    project_url = models.URLField(max_length=200, blank=False)
    cover_image = models.ImageField(
        upload_to='projects/', default=DEFAULT_AVATAR, blank=True)
    completition_date = models.DateField(blank=True, null=True)
    tech_stack = models.CharField(max_length=400, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.project_name

    def save(self, *args, **kwargs):
        if not self.slug:
            val = self.project_name
            while (True):
                unique_name = slugify(val)
                if (self.__class__.objects.filter(slug=unique_name).count() == 0):
                    break
                val = self.project_name + str(random.randint(1, 500))
            self.slug = unique_name
        return super().save(*args, **kwargs)


# [
# 	{
# 		"id": 1,
# 		"project_name": "Courier Delivery (Fast Drop)",
# 		"description": "A courier delivery project for picking and droping courier from one place to another.",
# 		"slug": "courier-delivery-fast-drop",
# 		"project_url": "https://fastdroppro.herokuapp.com/",
# 		"cover_image": "http://localhost:8000/media/default/defaultAvatar.png",
# 		"completition_date": "2021-11-10",
# 		"tech_stack": "django,django_channels,celery,HTML,CSS,JavaScript",
# 		"created_at": "2022-12-16T21:49:02.004880+05:45",
# 		"updated_at": "2022-12-16T21:49:02.004880+05:45"
# 	}
# ]
