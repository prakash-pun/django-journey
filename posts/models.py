from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from authentication.constants import DEFAULT_AVATAR, DEFAULT_COVER_IMAGE
from authentication.models import CustomUser
from .utils import unique_slug_generator


def upload_to(instance, filename):
    return 'posts/{filename}'.format(filename=filename)


class Post(models.Model):
    name = models.CharField(max_length=200, null=False)
    slug = models.SlugField(null=False, blank=True,
                            unique=True, max_length=300)
    description = models.CharField(null=True, blank=True, max_length=500)
    cover_image = models.ImageField(
        upload_to='posts/', default=DEFAULT_COVER_IMAGE, blank=True)
    icon = models.CharField(max_length=200, null=True, blank=True)
    content = models.CharField(max_length=40000, null=True, blank=True)
    created_by = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, blank=True, null=True, related_name="post_created_by")
    public = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    @property
    def created_by(self):
        if self.created_by:
            return self.created_by.avatar
        return DEFAULT_AVATAR

    @property
    def owner_name(self):
        if self.created_by:
            return self.created_by.first_name
        return "Unknown"

    class Meta:
        verbose_name_plural = "Posts"


class SubPost(models.Model):
    title = models.CharField(max_length=500, null=False, default="Untitled")
    slug = models.SlugField(
        null=False, blank=True, unique=True, max_length=255
    )
    sub_title = models.CharField(max_length=500, blank=True, null=True)
    description = models.CharField(null=True, blank=True, max_length=500)
    cover_image = models.ImageField(
        upload_to='posts/', default=DEFAULT_COVER_IMAGE, blank=True)
    icon = models.CharField(max_length=200, null=True, blank=True)
    tags = models.CharField(max_length=400, blank=True, null=True)
    content = models.TextField(max_length=40000, blank=True)
    public = models.BooleanField(default=False)
    access_key = models.CharField(
        null=True, blank=True, unique=True, max_length=100)
    is_draft = models.BooleanField(default=True)
    public_link = models.URLField(max_length=400, null=True, blank=True)
    created_by = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, blank=True, null=True, related_name="subpost_created_by"
    )
    post = models.ForeignKey(
        Post, on_delete=models.SET_NULL, blank=True, null=True, related_name="post")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    @property
    def avatar(self):
        if self.created_by:
            return self.created_by.avatar
        return DEFAULT_AVATAR

    @property
    def owner_name(self):
        if self.created_by:
            return self.created_by.first_name
        return "Unknown"

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Sub Posts"


class Images(models.Model):
    sub_post = models.ForeignKey(
        SubPost, related_name="subpost_images", on_delete=models.CASCADE, blank=True, null=True,
    )
    post_image = models.ImageField(
        _("Post_Images"), upload_to="posts/", null=False, default=DEFAULT_COVER_IMAGE)
    tags = models.CharField(max_length=350, blank=True, null=True)
    caption = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.sub_post.title + "_image"

    class Meta:
        verbose_name_plural = "Images"

    def delete_image(self):
        image_file = self.post_image
        if image_file and not image_file.name == "posts/default.jpg":
            image_file.delete()

    def delete(self):
        image_file = self.post_image
        if (image_file and not image_file.name == "posts/default.jpg"):
            image_file.delete()
        super().delete()


def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(slug_generator, sender=Post)
pre_save.connect(slug_generator, sender=SubPost)
