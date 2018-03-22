#from django.contrib.auth.models import User
from django import forms
from . import models

class CreateContact(forms.ModelForm):
    class Meta:
        model = models.Contact
        fields = ['name', 'email']

class CampaignForm(forms.ModelForm):
    class Meta:
        model = models.Campaign
        fields = ['title']

class UploadForm(forms.Form):
    textfile = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )

class NewEmail(forms.ModelForm):

    class Meta:
        model = models.EmailLog
        fields = ['contacts', 'body']

    def __init__(self, user, *args, **kwargs):
        super(NewEmail, self).__init__(*args, **kwargs)
        self.fields['contacts'] = forms.ModelMultipleChoiceField( \
            widget=forms.CheckboxSelectMultiple, \
            queryset=models.Contact.objects.filter(added_by=user))
