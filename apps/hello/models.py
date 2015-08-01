from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(blank=False, max_length=50)
    last_name = models.CharField(blank=False, max_length=50)
    date_of_birth = models.DateField()
    bio = models.TextField()
    email = models.EmailField(blank=False, unique=True)
    jabber = models.CharField(blank=True, max_length=30, unique=True)
    skype =models.CharField(blank=True, max_length=30, unique=True)
    other_contacts = models.TextField()

    def __unicode__(self):
        return self.name