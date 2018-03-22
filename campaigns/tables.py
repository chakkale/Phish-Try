import django_tables2 as tables
from .models import Contact, Campaign


class ContactTable(tables.Table):
    time_passed = tables.Column(accessor='passed_time')

    class Meta:
        model = Contact
        exclude = ('added_by', 'group')
        template_name = 'django_tables2/bootstrap.html'

class CampaignTable(tables.Table):
    contact_count = tables.Column(accessor='contact_count')
    sent_mails = tables.Column(accessor='sent_mails')
    clicked = tables.Column(accessor='click_count')

    class Meta:
        model = Campaign
        exclude = ('author')
        template_name = 'django_tables2/bootstrap.html'
