from django.db import models

from django.conf import settings
from media.models import StatusPost

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(StatusPost, on_delete=models.CASCADE)
    text = models.TextField(max_length=250, null=False, blank=False)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user.username)