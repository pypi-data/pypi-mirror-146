from django.db import models


class IATISourceRef(models.Model):
    ref = models.CharField(
        max_length=70)
    title = models.CharField(max_length=255, default="")
    type = models.IntegerField(
        choices=(
            (1, 'Activity Files'),
            (2, 'Organisation Files'),
        ),
        default=1)
    url = models.CharField(
        max_length=255,
        unique=True)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now_add=True, editable=False)
    last_found_in_registry = models.DateTimeField(default=None, null=True)
    activity_count = models.IntegerField(null=True, default=None)
    iati_standard_version = models.CharField(max_length=10, default="")
    is_parsed = models.BooleanField(null=False, default=False)

    class Meta:
        verbose_name_plural = "IATI XML sources"
        ordering = ["ref"]

    def __str__(self):
        return self.ref
