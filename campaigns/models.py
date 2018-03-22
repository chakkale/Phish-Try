import uuid
from datetime import timedelta

from django.db import models
from django.contrib.auth.models import User


class Campaign(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return self.title

#Not implemented yet
class Group(models.Model):
    name = models.CharField(max_length=50)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    campaign = models.ForeignKey(Campaign, default=None, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return self.name

class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    link_id = models.SlugField(default=uuid.uuid4)
    campaign = models.ForeignKey(Campaign, default=None, related_name='contacts', \
        on_delete=models.CASCADE, blank=True, null=True)
    group = models.ForeignKey(Group, default=None, \
        on_delete=models.CASCADE, blank=True, null=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    clicked = models.BooleanField(default=False)
    email_sent = models.BooleanField(default=False)
    date_sent = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    date_clicked = models.DateTimeField(auto_now_add=False, blank=True, null=True)

    def passed_time(self):
        sent = self.date_sent
        clickdate = self.date_clicked
        result = clickdate - sent
        return timedelta(seconds=result.seconds)

    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return self.name

class ContactUpload(models.Model):
    textfile = models.FileField()

class EmailLog(models.Model):
    campaign = models.ForeignKey(Campaign, default=None, on_delete=models.CASCADE)
    contacts = models.ManyToManyField(Contact)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
