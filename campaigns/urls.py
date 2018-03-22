from django.urls import path

from . import views


app_name = 'main'

urlpatterns = [
    path('campaigns/', views.campaigns, name="campaign_list"),
    path('contacts/', views.contacts, name="contact_list"),
    path('campaigns/new/', views.new_campaign, name="new_campaign"),
    path('campaigns/new/startemail/', views.new_email, name="new_email"),
    path('contacts/new/', views.new_contact, name="new_contact"),
    path('contacts/upload/', views.uploadcontacts, name="upload_contacts"),
    path('authorize/<slug>/', views.click_page, name="click_page"),
]
