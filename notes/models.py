from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save 
from authentication.constants import DEFAULT_AVATAR
from authentication.models import CustomUser
from .utils import unique_slug_generator


def upload_to(instance, filename):
    return 'notes/{filename}'.format(filename=filename)


class Notes(models.Model):
    title = models.CharField(max_length=500, null=False)
    slug = models.SlugField(
        null=False, blank=True, unique=True, max_length=255
    )
    sub_title = models.CharField(max_length=500)
    note_image = models.ImageField(
        _("Image"), upload_to='notes/', default='notes/default.jpg'
    )
    tags = models.CharField(max_length=350, blank=True, null=True)
    content = models.TextField(max_length=10000, blank=True)
    is_public = models.BooleanField(default=True)
    is_draft = models.BooleanField(default=True)
    owner = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, blank=True, null=True, related_name="note_owner"
    )
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
            return self.owner.first_name
        return "Unknown"

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Notes"


class Images(models.Model):
    notes = models.ForeignKey(
        Notes, related_name="note_images", on_delete=models.CASCADE
    )
    note_images = models.ImageField(_("Note_Images"), upload_to="notes/")
    tags = models.CharField(max_length=350, blank=True, null=True)
    description = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.notes.title + "_image"

    class Meta:
        verbose_name_plural = "Images"

    def delete(self):
        image_file = self.note_images
        if(image_file and not image_file.name == "notes/default.jpg"):
            image_file.delete()
        super().delete()


def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(slug_generator, sender=Notes)

# def get_unique_slug(sender, instance, **kwargs):
#     num = 1
#     slug = slugify(instance.title)
#     unique_slug = slug
#     while Notes.objects.filter(slug=unique_slug).exists():
#         unique_slug = '{}-{}'.format(slug, num)
#         num += 1
#     instance.slug=unique_slug

# pre_save.connect(get_unique_slug,sender=Notes)
