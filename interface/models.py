from django.db import models
from django.contrib.auth.models import User


class Contact(models.Model):
    subject = models.CharField(max_length=200)
    message = models.TextField(max_length=1000)
    user = models.ForeignKey(User)
    date_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
