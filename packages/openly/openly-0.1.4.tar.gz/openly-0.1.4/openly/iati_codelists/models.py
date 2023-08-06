from django.db import models


class ResultType(models.Model):
    code = models.CharField(primary_key=True, max_length=40)
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True, null=True)

    def __str__(self,):
        return "%s - %s" % (self.code, self.name)


class IndicatorMeasure(models.Model):
    code = models.CharField(primary_key=True, max_length=40)
    name = models.CharField(max_length=40)
    description = models.TextField(blank=True, null=True)

    def __str__(self,):
        return "%s - %s" % (self.code, self.name)
