from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from PIL import Image
from crispy_forms import helper
from profiles_v2 import models


class FormHelper(helper.FormHelper):

    def __init__(self, *args, **kwargs):
        super(FormHelper, self).__init__(*args, **kwargs)
        self.form_tag = False
        self.form_class = 'form-horizontal'
        self.label_class = 'col-lg-3 col-md-3'
        self.field_class = 'col-lg-8 col-md-8'


class ContactForm(forms.ModelForm):

    class Meta:
        model = models.Contact
        exclude = []
        widgets = {
            'organisation_profile': forms.HiddenInput(),
            'address': forms.Textarea(attrs={'rows': 3})
        }

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields.get('title').required = True
        self.fields.get('address').required = True


class PersonForm(forms.ModelForm):

    class Meta:
        model = models.Person
        exclude = []
        widgets = {
            'organisation_profile': forms.HiddenInput(),
            'background': forms.Textarea(attrs={'rows': 3})
        }

    def __init__(self, *args, **kwargs):
        super(PersonForm, self).__init__(*args, **kwargs)

        self.fields['background'].label = _("Brief biography (limit 500 characters)")

        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field:
                field.widget.attrs.update({
                    'placeholder': field.label,
                    'class': 'form-control'
                })
                field.label = ''

        self.fields.get('name').required = True


class ImageUploadForm(forms.Form):
    """ Basic image upload form that raises a ValidationError if the image is not
    a formatted as a jpeg or png file.
    """
    image = forms.ImageField()

    def clean_image(self):
        path = self.cleaned_data['image']
        image = Image.open(path)
        if image.format not in ['JPEG', 'PNG']:
            raise ValidationError('Image must be formatted as a JPEG or PNG file!')

        return path
