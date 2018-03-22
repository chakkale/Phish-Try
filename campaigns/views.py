import os
from datetime import datetime
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Case, When
from django.core.mail import send_mail
from django_tables2 import RequestConfig

from .forms import CreateContact, UploadForm, CampaignForm, NewEmail
from .models import Contact, Campaign, ContactUpload, EmailLog
from .tables import ContactTable, CampaignTable

def click_page(request, slug):
    contact = Contact.objects.get(link_id=slug)
    contact.clicked = True
    contact.date_clicked = datetime.now()
    contact.save()
    return render(request, 'campaigns/click_page.html', {'contact':contact})

@login_required(login_url="/accounts/login/")
def campaigns(request):
    campaigns_contacts = Campaign.objects.all() \
        .filter(author=request.user).annotate(contact_count=Count('contacts', distinct=True)) \
        .annotate(sent_mails=Count(Case(When(contacts__email_sent=True, then='contacts')))) \
        .annotate(click_count=Count(Case(When(contacts__clicked=True, then='contacts'))))
    table = CampaignTable(campaigns_contacts)
    RequestConfig(request).configure(table)
    return render(request, 'campaigns/campaign_list.html', {'table':table})

@login_required(login_url="/accounts/login/")
def new_campaign(request):
    template_name = 'campaigns/new_campaign.html'
    if request.method == 'POST':
        form = CampaignForm(request.POST)
        if form.is_valid():
            campaign = form.save(commit=False)
            campaign.author = request.user
            campaign.save()
            return redirect('main:new_email')
    else:
        form = CampaignForm()
    return render(request, template_name, {'form':form})

@login_required(login_url="/accounts/login/")
def contacts(request):
    contacts_count = Contact.objects.all() \
        .filter(added_by=request.user)
    table = ContactTable(contacts_count)
    RequestConfig(request).configure(table)
    return render(request, 'campaigns/contact_list.html', {'table':table})

@login_required(login_url="/accounts/login/")
def new_contact(request):
    template_name = 'campaigns/new_contact.html'
    if request.method == 'POST':
        form = CreateContact(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.added_by = request.user
            contact.save()
            return redirect('main:contact_list')
    else:
        form = CreateContact()
    return render(request, template_name, {'form':form})

@login_required(login_url="/accounts/login/")
def uploadcontacts(request):
    template_name = 'campaigns/upload_contacts.html'
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            newfile = ContactUpload(textfile=request.FILES['textfile'])
            newfile.save()
            uploaded = ContactUpload.objects.first()
            uploaded.textfile.open()
            lines = uploaded.textfile.readlines()
            for line in lines:
                line = line.decode('utf-8') \
                    .replace('\n', '')[:-1].split(' <', 1)
                name = line[0]
                email = line[1]
                Contact.objects.create(name=name, email=email, added_by=request.user)
            newfile.delete()
            os.remove(os.path.join(settings.MEDIA_ROOT, uploaded.textfile.name))
            return redirect('main:contact_list')
    else:
        form = UploadForm()
    return render(request, template_name, {'form':form})

@login_required(login_url="/accounts/login/")
def new_email(request):
    template_name = 'campaigns/start_email.html'
    if request.method == 'POST':
        form = NewEmail(request.user, request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.campaign = Campaign.objects.first()
            post.save()
            form.save_m2m()
            linkbase = 'http://' + request.META['HTTP_HOST']  \
                + '/main/authorize/'
            from_email = settings.DEFAULT_FROM_EMAIL
            subject = 'Test Phish-Try'
            contacts_form = EmailLog.objects.first()
            for contact in contacts_form.contacts.all():
                person = Contact.objects.get(name=contact)
                recipient_list = []
                recipient_list.append(contact.email)
                link = linkbase + contact.link_id + '/'
                message = post.body + '\n\n' + link
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                person.campaign = post.campaign
                person.email_sent = True
                person.date_sent = datetime.now()
                person.save()
            return redirect('main:campaign_list')
    else:
        form = NewEmail(request.user)
    return render(request, template_name, {'form':form})
