from django.db import models

from aims.models import Activity
from profiles_v2.models import ImageModel


class ActivityProfile(models.Model, ImageModel):
    image_size = {
        'banner': [1500, 350]
    }

    activity = models.OneToOneField(Activity, related_name='profile', on_delete=models.CASCADE)
    banner_image = models.ImageField(upload_to="profiles/activity_banner_image/", null=True, blank=True)

    def __str__(self):
        return str(self.activity.title)
