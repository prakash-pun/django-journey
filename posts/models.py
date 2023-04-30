import random
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify
from authentication.constants import DEFAULT_AVATAR, DEFAULT_COVER_IMAGE
from authentication.models import CustomUser


def upload_to(instance, filename):
    return 'posts/{filename}'.format(filename=filename)


class Folder(models.Model):
    name = models.CharField(max_length=100, null=False)
    slug = models.SlugField(null=False, blank=True,
                            unique=True, max_length=300)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name="parent_folder")
    created_by = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, blank=True, null=True)
    description = models.CharField(max_length=600, null=True, blank=True)
    icon = models.CharField(max_length=200, blank=True, null=True)
    cover_image = models.ImageField(
        upload_to='folders/', default=DEFAULT_COVER_IMAGE, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    @property
    def owner_name(self):
        if self.created_by:
            return self.created_by.full_name
        return "Unknown"

    class Meta:
        verbose_name_plural = "Folders"

    def save(self, *args, **kwargs):
        if not self.slug:
            value = self.name
            while (True):
                slug = slugify(value)
                if (self.__class__.objects.filter(slug=slug).count() == 0):
                    break
                value = self.name + str(random.randint(1, 500))
            self.slug = slug
        return super().save(*args, **kwargs)


class Post(models.Model):
    title = models.CharField(max_length=200, null=False)
    slug = models.SlugField(null=False, blank=True,
                            unique=True, max_length=300)
    sub_title = models.CharField(max_length=500, blank=True, null=True)
    description = models.CharField(null=True, blank=True, max_length=500)
    cover_image = models.ImageField(
        upload_to='posts/', default=DEFAULT_COVER_IMAGE, blank=True)
    icon = models.CharField(max_length=200, null=True, blank=True)
    tags = models.CharField(max_length=400, blank=True, null=True)
    content = models.CharField(max_length=40000, null=True, blank=True)
    public = models.BooleanField(default=False)
    access_key = models.CharField(
        null=True, blank=True, unique=True, max_length=100)
    is_draft = models.BooleanField(default=True)
    public_link = models.URLField(max_length=400, null=True, blank=True)
    created_by = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, blank=True, null=True)
    folder = models.ForeignKey(
        Folder, on_delete=models.SET_NULL, blank=True, null=True, related_name="post_folder")
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    @property
    def avatar(self):
        if self.created_by:
            return self.created_by.avatar
        return DEFAULT_AVATAR

    @property
    def owner_name(self):
        if self.created_by:
            return self.created_by.full_name
        return "Unknown"

    class Meta:
        verbose_name_plural = "Posts"

    def save(self, *args, **kwargs):
        if not self.slug:
            value = self.title
            while (True):
                slug = slugify(value)
                if (self.__class__.objects.filter(slug=slug).count() == 0):
                    break
                value = self.title + str(random.randint(1, 500))
            self.slug = slug
        return super().save(*args, **kwargs)


class Images(models.Model):
    post = models.ForeignKey(
        Post, related_name="post_images", on_delete=models.CASCADE, blank=True, null=True,
    )
    post_image = models.ImageField(
        _("Post_Images"), upload_to="posts/", null=False, default=DEFAULT_COVER_IMAGE)
    tags = models.CharField(max_length=350, blank=True, null=True)
    caption = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.post.title + "_image"

    class Meta:
        verbose_name_plural = "Post Images"

    def delete_image(self):
        image_file = self.post_image
        if image_file and not image_file.name == "posts/default.jpg":
            image_file.delete()

    def delete(self):
        image_file = self.post_image
        if (image_file and not image_file.name == "posts/default.jpg"):
            image_file.delete()
        super().delete()
