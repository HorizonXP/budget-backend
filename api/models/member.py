from django.db import models
from django.conf import settings

class Member(models.Model):
    dependent = models.BooleanField(default=False)
    provider = models.BooleanField(default=False)
    user = models.OneToOneField(
             settings.AUTH_USER_MODEL,
             on_delete=models.CASCADE
           )
    family = models.ForeignKey(
               'Family',
               related_name='members'
             )
