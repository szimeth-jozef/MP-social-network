from django.db import models

import uuid
from django.conf import settings
from django.utils.text import slugify
from django.dispatch import receiver
from django.db.models.signals import post_delete, pre_save


def upload_location(instance, filename):
    file_path = 'status_post_images/{author}/{post_id}-{filename}'.format(
        author = str(instance.author.username), post_id = str(instance.post_id), filename=filename
    )
    return file_path


class StatusPost(models.Model):
    author      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post_id     = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text        = models.TextField(max_length=250, null=False, blank=False)
    image       = models.ImageField(upload_to=upload_location, blank=True)
    date_posted = models.DateTimeField(verbose_name="date posted", auto_now_add=True)
    slug        = models.SlugField(blank=True, unique=True)
    likes       = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="likes", symmetrical=False, blank=True)

    def __str__(self):
        return f'{self.author.username} ({self.post_id})'

@receiver(post_delete, sender=StatusPost)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)


def pre_save_status_post_receiver(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.author.username + "-" + str(instance.post_id))

pre_save.connect(pre_save_status_post_receiver, sender=StatusPost)