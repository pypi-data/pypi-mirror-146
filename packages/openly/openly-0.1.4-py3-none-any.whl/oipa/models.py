from django.db import models
from django.contrib.postgres.fields import ArrayField


class OipaActivityLink(models.Model):
    oipa_field_choices = (
        ("B", u"Budgets"),
        ("C", u"Commitments"),
        ("OF", u"Outgoing Funds"),
        ("IF", u"Incoming Funds"),
    )

    activity = models.OneToOneField(
        "aims.Activity",
        null=False,
        blank=False,
        primary_key=True,
        on_delete=models.CASCADE,
        max_length=150,
    )
    oipa_fields = ArrayField(
        choices=oipa_field_choices,
        base_field=models.CharField(max_length=100),
        default=list,
        null=True,
    )

    class Meta:
        app_label = "oipa"

    def __init__(self, *args, **kwargs):
        super(OipaActivityLink, self).__init__(*args, **kwargs)


class OipaSyncRecord(models.Model):
    id = models.AutoField(primary_key=True)
    activity = models.ForeignKey(
        "aims.Activity",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        max_length=150,
    )
    b_added = models.IntegerField(default=0)
    c_added = models.IntegerField(default=0)
    of_added = models.IntegerField(default=0)
    if_added = models.IntegerField(default=0)
    sync_datetime = models.DateTimeField(default=None, null=True)

    class Meta:
        app_label = "oipa"

    def __init__(self, *args, **kwargs):
        super(OipaSyncRecord, self).__init__(*args, **kwargs)
