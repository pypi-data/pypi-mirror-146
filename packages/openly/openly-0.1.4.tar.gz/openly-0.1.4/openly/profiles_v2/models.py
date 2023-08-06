from django.db import models
from PIL import Image, ImageOps

from aims.models import Organisation


class ImageModel:
    """ Basic image handling mixin for models. Models should set the allowable image sizes
    via the image_size dict { 'field name'=> size } and then call resize_image for the
    field name on image upload. This will clean the image and resize to the appropriate
    dimensions.
    """

    QUALITY = 100
    image_size = {}

    def thumb_image(self, path, width, height):

        image = Image.open(path)

        # clean and resize image
        image = image.convert("RGBA")
        ImageOps.fit(image, (width, height), Image.ANTIALIAS).save(path, quality=self.QUALITY)

    def resize_image(self, image):

        if image not in self.image_size:
            return False

        image_property = getattr(self, image)
        size = self.image_size[image]

        self.thumb_image(image_property.path, size[0], size[1])


class OrganisationProfile(models.Model, ImageModel):

    image_size = {
        'logo': [200, 200],
        'banner_image': [1500, 350]
    }

    organisation = models.OneToOneField(Organisation, related_name='profile', on_delete=models.CASCADE)

    url = models.URLField(null=True, blank=True)
    logo = models.ImageField(upload_to="profiles/organisation_logo/", null=True, blank=True)
    banner_image = models.ImageField(upload_to="profiles/organisation_banner_image/", null=True, blank=True)
    banner_text = models.CharField(max_length=256, null=True, blank=True)
    background = models.TextField(max_length=100000, null=True, blank=True)

    def __str__(self,):
        return self.organisation.name


class OrganisationContactInfo(models.Model):
    profile = models.OneToOneField(OrganisationProfile, related_name='contact_info', on_delete=models.CASCADE)
    title = models.CharField(max_length=64, null=True, blank=True)
    address = models.CharField(max_length=1000, null=True, blank=True)
    phone_number = models.CharField(max_length=64, null=True, blank=True)
    email = models.CharField(max_length=128, null=True, blank=True)
    website = models.URLField(max_length=256, null=True, blank=True)
    facebook = models.CharField(max_length=256, null=True, blank=True)
    twitter = models.CharField(max_length=128, null=True, blank=True)
    fax = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):
        return self.profile.organisation.name


class Person(models.Model, ImageModel):
    image_size = {
        'photo': [120, 120],
    }

    organisation_profile = models.ForeignKey(OrganisationProfile, related_name='people', on_delete=models.CASCADE)

    name = models.CharField(max_length=128, blank=True)
    position = models.CharField(max_length=128, null=True, blank=True)
    background = models.CharField(max_length=500, null=True, blank=True)
    phone_number = models.CharField(max_length=128, null=True, blank=True)
    email = models.CharField(max_length=128, null=True, blank=True)
    photo = models.ImageField(upload_to='profiles/person_photo', null=True, blank=True)
    order = models.IntegerField(blank=True, null=True, default=0)


class Contact(models.Model):
    organisation_profile = models.ForeignKey(OrganisationProfile, related_name="contacts", null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=64, null=True, blank=True)
    address = models.CharField(max_length=1000, null=True, blank=True)
    phone_number = models.CharField(max_length=64, null=True, blank=True)
    email = models.CharField(max_length=128, null=True, blank=True)
    fax = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self,):
        return self.organisation_profile.organisation.name
