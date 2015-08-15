import StringIO
from PIL import Image as Img
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models


class Profile(models.Model):
    name = models.CharField(blank=False, max_length=50)
    last_name = models.CharField(blank=False, max_length=50)
    date_of_birth = models.DateField()
    bio = models.TextField()
    email = models.EmailField(blank=False, unique=True)
    jabber = models.CharField(blank=True, max_length=30, unique=True)
    skype = models.CharField(blank=True, max_length=30, unique=True)
    other_contacts = models.TextField()
    photo = models.ImageField(upload_to='hello', null=True)
    photo_preview = models.ImageField(upload_to='hello/preview', null=True)

    def __unicode__(self):
        return self.name

    def as_json(self):
        return dict(
            id=self.id,
            name=self.name,
            last_name=self.last_name,
            date_of_birth=self.date_of_birth.strftime('%Y-%m-%d %H:%M:%S'),
            bio=self.bio,
            email=self.email,
            jabber=self.jabber,
            skype=self.skype,
            other_contacts=self.other_contacts,
            photo=self.photo.url if self.photo else '',
            photo_preview=self.photo_preview.url if self.photo_preview else '')

    def save(self, *args, **kwargs):
        if self.photo:
            image = Img.open(StringIO.StringIO(self.photo.read()))
            image.thumbnail((200, 200), Img.ANTIALIAS)
            output = StringIO.StringIO()
            image.save(output, format='JPEG', quality=75)
            output.seek(0)
            self.photo_preview = InMemoryUploadedFile(output,
                                                      'ImageField',
                                                      self.photo.name,
                                                      'image/jpeg',
                                                      output.len,
                                                      None)
        super(Profile, self).save(*args, **kwargs)

    def admin_preview(self):
        return '<a href="/uploads/{0}"><img src="/uploads/{0}"></a>'.\
            format(self.photo_preview)
    admin_preview.allow_tags = True


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
