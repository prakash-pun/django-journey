import random
import string
from django.utils.text import slugify


def random_string_generator(size=5, chars=string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=4)
        )
        return unique_slug_generator(instance, new_slug=new_slug)

    return slug


# def get_unique_slug(sender, instance, **kwargs):
#     num = 1
#     slug = slugify(instance.title)
#     unique_slug = slug
#     while Post.objects.filter(slug=unique_slug).exists():
#         unique_slug = '{}-{}'.format(slug, num)
#         num += 1
#     instance.slug=unique_slug

# pre_save.connect(get_unique_slug,sender=Post)
