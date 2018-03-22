from django.contrib import admin
from django.db import models
from django.forms import CheckboxSelectMultiple
from .models import Contact, Campaign, ContactUpload, EmailLog #, Group


class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'email_sent', \
        'clicked', 'date_added', 'campaign', 'group', 'added_by')

class CampaignAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date')

class EmailAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'author')
    formfield_overrides = {
        models.ManyToManyField : {'widget' : CheckboxSelectMultiple},
    }


admin.site.register(Campaign, CampaignAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(ContactUpload)
admin.site.register(EmailLog, EmailAdmin)
#admin.site.register(Group)
