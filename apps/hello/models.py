from django.db import models

# Create your models here.


class Profile(models.Model):
    name = models.CharField(blank=False, max_length=50)
    last_name = models.CharField(blank=False, max_length=50)
    date_of_birth = models.DateField()
    bio = models.TextField()
    email = models.EmailField(blank=False, unique=True)
    jabber = models.CharField(blank=True, max_length=30, unique=True)
    skype = models.CharField(blank=True, max_length=30, unique=True)
    other_contacts = models.TextField()

    def __unicode__(self):
        return self.name


class RequestHistory(models.Model):
    path = models.CharField(max_length=2000)
    host = models.CharField(max_length=100)
    method = models.CharField(max_length=20)
    ip = models.GenericIPAddressField()
    date = models.DateTimeField(auto_now_add=True)
    is_viewed = models.BooleanField(default=False)

    def __unicode__(self):
        return self.path

    def as_json(self):
        return dict(
            id=self.id,
            path=self.path,
            host=self.host,
            method=self.method,
            ip=self.ip,
            date=self.date.strftime('%Y-%m-%d %H:%M:%S'))
