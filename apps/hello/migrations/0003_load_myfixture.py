# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        from django.core.management import call_command
        call_command("loaddata", "initial_data.json")

    def backwards(self, orm):
        pass

    models = {
        u'hello.profile': {
            'Meta': {'object_name': 'Profile'},
            'bio': ('django.db.models.fields.TextField', [], {}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jabber': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'other_contacts': ('django.db.models.fields.TextField', [], {}),
            'skype': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30', 'blank': 'True'})
        }
    }

    complete_apps = ['hello']