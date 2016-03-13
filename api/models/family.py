from django.db import models

class Family(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return '%s Family' % (self.name,)

    class Meta:
        app_label = 'api'
        verbose_name_plural = "Families"
        permissions = (
            ('view_family', 'Can view family'),
        )
