from django.db import models


class IndicatorVocabulary(models.Model):
    code = models.CharField(primary_key=True, max_length=2)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)

    def __str__(self):
        return "%s - %s" % (self.code, self.name)
