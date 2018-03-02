# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'DiplomaticLetter.sourcename20'
        db.delete_column(u'dasa_diplomaticletter', 'sourcename20')

        # Deleting field 'DiplomaticLetter.rulername_original'
        db.delete_column(u'dasa_diplomaticletter', 'rulername_original')

        # Deleting field 'DiplomaticLetter.sourcename9'
        db.delete_column(u'dasa_diplomaticletter', 'sourcename9')

        # Deleting field 'DiplomaticLetter.sourcename8'
        db.delete_column(u'dasa_diplomaticletter', 'sourcename8')

        # Deleting field 'DiplomaticLetter.sourcename5'
        db.delete_column(u'dasa_diplomaticletter', 'sourcename5')

        # Deleting field 'DiplomaticLetter.sourcename4'
        db.delete_column(u'dasa_diplomaticletter', 'sourcename4')

        # Deleting field 'DiplomaticLetter.sourcename7'
        db.delete_column(u'dasa_diplomaticletter', 'sourcename7')

        # Deleting field 'DiplomaticLetter.sourcename1'
        db.delete_column(u'dasa_diplomaticletter', 'sourcename1')

        # Deleting field 'DiplomaticLetter.sourcename3'
        db.delete_column(u'dasa_diplomaticletter', 'sourcename3')

        # Deleting field 'DiplomaticLetter.sourcename6'
        db.delete_column(u'dasa_diplomaticletter', 'sourcename6')

        # Deleting field 'DiplomaticLetter.rulername3'
        db.delete_column(u'dasa_diplomaticletter', 'rulername3')

        # Deleting field 'DiplomaticLetter.sourcename19'
        db.delete_column(u'dasa_diplomaticletter', 'sourcename19')

        # Deleting field 'DiplomaticLetter.sourcename18'
        db.delete_column(u'dasa_diplomaticletter', 'sourcename18')

        # Deleting field 'DiplomaticLetter.destinationname14'
        db.delete_column(u'dasa_diplomaticletter', 'destinationname14')

        # Deleting field 'DiplomaticLetter.sourcename11'
        db.delete_column(u'dasa_diplomaticletter', 'sourcename11')

        # Deleting field 'DiplomaticLetter.sourcename10'
        db.delete_column(u'dasa_diplomaticletter', 'sourcename10')

        # Deleting field 'DiplomaticLetter.sourcename13'
        db.delete_column(u'dasa_diplomaticletter', 'sourcename13')

        # Deleting field 'DiplomaticLetter.sourcename15'
        db.delete_column(u'dasa_diplomaticletter', 'sourcename15')

        # Deleting field 'DiplomaticLetter.sourcename14'
        db.delete_column(u'dasa_diplomaticletter', 'sourcename14')

        # Deleting field 'DiplomaticLetter.sourcename17'
        db.delete_column(u'dasa_diplomaticletter', 'sourcename17')

        # Deleting field 'DiplomaticLetter.sourcename16'
        db.delete_column(u'dasa_diplomaticletter', 'sourcename16')

        # Deleting field 'DiplomaticLetter.rulername5'
        db.delete_column(u'dasa_diplomaticletter', 'rulername5')

        # Deleting field 'DiplomaticLetter.rulername4'
        db.delete_column(u'dasa_diplomaticletter', 'rulername4')

        # Deleting field 'DiplomaticLetter.rulername7'
        db.delete_column(u'dasa_diplomaticletter', 'rulername7')

        # Deleting field 'DiplomaticLetter.rulername6'
        db.delete_column(u'dasa_diplomaticletter', 'rulername6')

        # Deleting field 'DiplomaticLetter.rulername1'
        db.delete_column(u'dasa_diplomaticletter', 'rulername1')

        # Deleting field 'DiplomaticLetter.rulername2'
        db.delete_column(u'dasa_diplomaticletter', 'rulername2')

        # Deleting field 'DiplomaticLetter.rulername9'
        db.delete_column(u'dasa_diplomaticletter', 'rulername9')

        # Deleting field 'DiplomaticLetter.rulername8'
        db.delete_column(u'dasa_diplomaticletter', 'rulername8')

        # Deleting field 'DiplomaticLetter.rulername12'
        db.delete_column(u'dasa_diplomaticletter', 'rulername12')

        # Deleting field 'DiplomaticLetter.rulername11'
        db.delete_column(u'dasa_diplomaticletter', 'rulername11')

        # Deleting field 'DiplomaticLetter.rulername10'
        db.delete_column(u'dasa_diplomaticletter', 'rulername10')

        # Deleting field 'DiplomaticLetter.rulername13'
        db.delete_column(u'dasa_diplomaticletter', 'rulername13')

        # Deleting field 'DiplomaticLetter.rulername15'
        db.delete_column(u'dasa_diplomaticletter', 'rulername15')

        # Deleting field 'DiplomaticLetter.rulername14'
        db.delete_column(u'dasa_diplomaticletter', 'rulername14')

        # Deleting field 'DiplomaticLetter.rulername16'
        db.delete_column(u'dasa_diplomaticletter', 'rulername16')

        # Deleting field 'DiplomaticLetter.destinationname3'
        db.delete_column(u'dasa_diplomaticletter', 'destinationname3')

        # Deleting field 'DiplomaticLetter.destinationname2'
        db.delete_column(u'dasa_diplomaticletter', 'destinationname2')

        # Deleting field 'DiplomaticLetter.destinationname1'
        db.delete_column(u'dasa_diplomaticletter', 'destinationname1')

        # Deleting field 'DiplomaticLetter.sourcename12'
        db.delete_column(u'dasa_diplomaticletter', 'sourcename12')

        # Deleting field 'DiplomaticLetter.destinationname7'
        db.delete_column(u'dasa_diplomaticletter', 'destinationname7')

        # Deleting field 'DiplomaticLetter.destinationname6'
        db.delete_column(u'dasa_diplomaticletter', 'destinationname6')

        # Deleting field 'DiplomaticLetter.destinationname5'
        db.delete_column(u'dasa_diplomaticletter', 'destinationname5')

        # Deleting field 'DiplomaticLetter.destinationname4'
        db.delete_column(u'dasa_diplomaticletter', 'destinationname4')

        # Deleting field 'DiplomaticLetter.destinationname9'
        db.delete_column(u'dasa_diplomaticletter', 'destinationname9')

        # Deleting field 'DiplomaticLetter.destinationname8'
        db.delete_column(u'dasa_diplomaticletter', 'destinationname8')

        # Deleting field 'DiplomaticLetter.destinationname17'
        db.delete_column(u'dasa_diplomaticletter', 'destinationname17')

        # Deleting field 'DiplomaticLetter.destinationname16'
        db.delete_column(u'dasa_diplomaticletter', 'destinationname16')

        # Deleting field 'DiplomaticLetter.destinationname15'
        db.delete_column(u'dasa_diplomaticletter', 'destinationname15')

        # Deleting field 'DiplomaticLetter.destinationname13'
        db.delete_column(u'dasa_diplomaticletter', 'destinationname13')

        # Deleting field 'DiplomaticLetter.destinationname12'
        db.delete_column(u'dasa_diplomaticletter', 'destinationname12')

        # Deleting field 'DiplomaticLetter.destinationname11'
        db.delete_column(u'dasa_diplomaticletter', 'destinationname11')

        # Deleting field 'DiplomaticLetter.destinationname10'
        db.delete_column(u'dasa_diplomaticletter', 'destinationname10')

        # Deleting field 'DiplomaticLetter.sourcename21'
        db.delete_column(u'dasa_diplomaticletter', 'sourcename21')

        # Deleting field 'DiplomaticLetter.sourcename2'
        db.delete_column(u'dasa_diplomaticletter', 'sourcename2')

        # Deleting field 'DiplomaticLetter.destinationname19'
        db.delete_column(u'dasa_diplomaticletter', 'destinationname19')

        # Deleting field 'DiplomaticLetter.destinationname18'
        db.delete_column(u'dasa_diplomaticletter', 'destinationname18')


    def backwards(self, orm):
        # Adding field 'DiplomaticLetter.sourcename20'
        db.add_column(u'dasa_diplomaticletter', 'sourcename20',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DiplomaticLetter.rulername_original'
        db.add_column(u'dasa_diplomaticletter', 'rulername_original',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DiplomaticLetter.sourcename9'
        db.add_column(u'dasa_diplomaticletter', 'sourcename9',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DiplomaticLetter.sourcename8'
        db.add_column(u'dasa_diplomaticletter', 'sourcename8',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DiplomaticLetter.sourcename5'
        db.add_column(u'dasa_diplomaticletter', 'sourcename5',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DiplomaticLetter.sourcename4'
        db.add_column(u'dasa_diplomaticletter', 'sourcename4',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DiplomaticLetter.sourcename7'
        db.add_column(u'dasa_diplomaticletter', 'sourcename7',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DiplomaticLetter.sourcename1'
        db.add_column(u'dasa_diplomaticletter', 'sourcename1',
                      self.gf('django.db.models.fields.TextField')(null=True),
                      keep_default=False)

        # Adding field 'DiplomaticLetter.sourcename3'
        db.add_column(u'dasa_diplomaticletter', 'sourcename3',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DiplomaticLetter.sourcename6'
        db.add_column(u'dasa_diplomaticletter', 'sourcename6',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DiplomaticLetter.rulername3'
        db.add_column(u'dasa_diplomaticletter', 'rulername3',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DiplomaticLetter.sourcename19'
        db.add_column(u'dasa_diplomaticletter', 'sourcename19',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DiplomaticLetter.sourcename18'
        db.add_column(u'dasa_diplomaticletter', 'sourcename18',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DiplomaticLetter.destinationname14'
        db.add_column(u'dasa_diplomaticletter', 'destinationname14',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DiplomaticLetter.sourcename11'
        db.add_column(u'dasa_diplomaticletter', 'sourcename11',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DiplomaticLetter.sourcename10'
        db.add_column(u'dasa_diplomaticletter', 'sourcename10',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DiplomaticLetter.sourcename13'
        db.add_column(u'dasa_diplomaticletter', 'sourcename13',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DiplomaticLetter.sourcename15'
        db.add_column(u'dasa_diplomaticletter', 'sourcename15',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DiplomaticLetter.sourcename14'
        db.add_column(u'dasa_diplomaticletter', 'sourcename14',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DiplomaticLetter.sourcename17'
        db.add_column(u'dasa_diplomaticletter', 'sourcename17',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DiplomaticLetter.sourcename16'
        db.add_column(u'dasa_diplomaticletter', 'sourcename16',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DiplomaticLetter.rulername5'
        db.add_column(u'dasa_diplomaticletter', 'rulername5',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DiplomaticLetter.rulername4'
        db.add_column(u'dasa_diplomaticletter', 'rulername4',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DiplomaticLetter.rulername7'
        db.add_column(u'dasa_diplomaticletter', 'rulername7',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DiplomaticLetter.rulername6'
        db.add_column(u'dasa_diplomaticletter', 'rulername6',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DiplomaticLetter.rulername1'
        db.add_column(u'dasa_diplomaticletter', 'rulername1',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DiplomaticLetter.rulername2'
        db.add_column(u'dasa_diplomaticletter', 'rulername2',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DiplomaticLetter.rulername9'
        db.add_column(u'dasa_diplomaticletter', 'rulername9',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DiplomaticLetter.rulername8'
        db.add_column(u'dasa_diplomaticletter', 'rulername8',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DiplomaticLetter.rulername12'
        db.add_column(u'dasa_diplomaticletter', 'rulername12',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DiplomaticLetter.rulername11'
        db.add_column(u'dasa_diplomaticletter', 'rulername11',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DiplomaticLetter.rulername10'
        db.add_column(u'dasa_diplomaticletter', 'rulername10',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DiplomaticLetter.rulername13'
        db.add_column(u'dasa_diplomaticletter', 'rulername13',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DiplomaticLetter.rulername15'
        db.add_column(u'dasa_diplomaticletter', 'rulername15',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DiplomaticLetter.rulername14'
        db.add_column(u'dasa_diplomaticletter', 'rulername14',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DiplomaticLetter.rulername16'
        db.add_column(u'dasa_diplomaticletter', 'rulername16',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DiplomaticLetter.destinationname3'
        db.add_column(u'dasa_diplomaticletter', 'destinationname3',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DiplomaticLetter.destinationname2'
        db.add_column(u'dasa_diplomaticletter', 'destinationname2',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DiplomaticLetter.destinationname1'
        db.add_column(u'dasa_diplomaticletter', 'destinationname1',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DiplomaticLetter.sourcename12'
        db.add_column(u'dasa_diplomaticletter', 'sourcename12',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DiplomaticLetter.destinationname7'
        db.add_column(u'dasa_diplomaticletter', 'destinationname7',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DiplomaticLetter.destinationname6'
        db.add_column(u'dasa_diplomaticletter', 'destinationname6',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DiplomaticLetter.destinationname5'
        db.add_column(u'dasa_diplomaticletter', 'destinationname5',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DiplomaticLetter.destinationname4'
        db.add_column(u'dasa_diplomaticletter', 'destinationname4',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DiplomaticLetter.destinationname9'
        db.add_column(u'dasa_diplomaticletter', 'destinationname9',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DiplomaticLetter.destinationname8'
        db.add_column(u'dasa_diplomaticletter', 'destinationname8',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DiplomaticLetter.destinationname17'
        db.add_column(u'dasa_diplomaticletter', 'destinationname17',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DiplomaticLetter.destinationname16'
        db.add_column(u'dasa_diplomaticletter', 'destinationname16',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DiplomaticLetter.destinationname15'
        db.add_column(u'dasa_diplomaticletter', 'destinationname15',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DiplomaticLetter.destinationname13'
        db.add_column(u'dasa_diplomaticletter', 'destinationname13',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DiplomaticLetter.destinationname12'
        db.add_column(u'dasa_diplomaticletter', 'destinationname12',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DiplomaticLetter.destinationname11'
        db.add_column(u'dasa_diplomaticletter', 'destinationname11',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DiplomaticLetter.destinationname10'
        db.add_column(u'dasa_diplomaticletter', 'destinationname10',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DiplomaticLetter.sourcename21'
        db.add_column(u'dasa_diplomaticletter', 'sourcename21',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DiplomaticLetter.sourcename2'
        db.add_column(u'dasa_diplomaticletter', 'sourcename2',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DiplomaticLetter.destinationname19'
        db.add_column(u'dasa_diplomaticletter', 'destinationname19',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DiplomaticLetter.destinationname18'
        db.add_column(u'dasa_diplomaticletter', 'destinationname18',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'dasa.basicpage': {
            'Meta': {'ordering': "['title', 'slug']", 'object_name': 'BasicPage'},
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'content_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'content_id': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'description_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_id': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('dasa.models.ImageFieldMainText', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'image_caption': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'image_caption_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'image_caption_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'image_description': ('dasa.models.ImageFieldIntro', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'image_description_caption': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'image_description_caption_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'image_description_caption_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'meta_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'meta_description_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'meta_description_id': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'meta_keywords': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'meta_keywords_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'meta_keywords_id': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'dasa.diplomaticletter': {
            'Meta': {'ordering': "['insertion_date']", 'object_name': 'DiplomaticLetter'},
            'archiveFile': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'destinations': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'letters_to'", 'symmetrical': 'False', 'to': u"orm['dasa.DiplomaticLetterLocation']"}),
            'folio_number_from': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'folio_number_to': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'insertion_d': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'insertion_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'insertion_m': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'insertion_y': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'next': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'previous'", 'null': 'True', 'to': u"orm['dasa.DiplomaticLetter']"}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'originalLanguage': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'originalLetterAvailableYN': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'original_d': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'original_m': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'original_y': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pagePubFirst': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'pagePubLast': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'rulers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'letters'", 'symmetrical': 'False', 'to': u"orm['dasa.DiplomaticLetterRuler']"}),
            'sealedYN': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'sources': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'letters_from'", 'symmetrical': 'False', 'to': u"orm['dasa.DiplomaticLetterLocation']"}),
            'translatedInto': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'volume': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'dasa.diplomaticletterlocation': {
            'Meta': {'object_name': 'DiplomaticLetterLocation'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'city_alternative_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'city_alternative_name2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'city_alternative_name3': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'continent': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'exact': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'place': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'reference': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'region_altenative_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'})
        },
        u'dasa.diplomaticletterruler': {
            'Meta': {'object_name': 'DiplomaticLetterRuler'},
            'alternative_name1': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'alternative_name2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'alternative_name3': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'alternative_name4': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'alternative_name5': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'alternative_name6': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'alternative_name7': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'alternative_name8': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'name_modern': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'period_end': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'period_start': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'reference': ('django.db.models.fields.TextField', [], {'null': 'True'})
        },
        u'dasa.hartakaruncategory': {
            'Meta': {'ordering': "['name']", 'object_name': 'HartaKarunCategory'},
            'hartakarun_main_category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subcategories'", 'null': 'True', 'to': u"orm['dasa.HartaKarunMainCategory']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('dasa.models.ImageFieldMainText', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'image_caption': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'image_caption_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'image_caption_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'image_description_caption': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'image_description_caption_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'image_description_caption_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'image_intro': ('dasa.models.ImageFieldIntro', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'longIntroText': ('tinymce.models.HTMLField', [], {'blank': 'True'}),
            'longIntroText_en': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'longIntroText_id': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'shortIntroText': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'shortIntroText_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'shortIntroText_id': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'dasa.hartakarunitem': {
            'ISBN': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'Meta': {'object_name': 'HartaKarunItem'},
            'archivalSourceReference': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'citation': ('tinymce.models.HTMLField', [], {'blank': 'True'}),
            'citation_en': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'citation_id': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'comment_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'comment_id': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'date_on_timeline': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'edited_by': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'hartakaruncategory': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'hartakarun_items'", 'to': u"orm['dasa.HartaKarunCategory']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('dasa.models.ImageFieldIntro', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'image_caption': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'image_caption_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'image_caption_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'introduced_by': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'introduction': ('tinymce.models.HTMLField', [], {'blank': 'True'}),
            'introduction_en': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'introduction_id': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'long_title': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'long_title_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'long_title_id': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '50', 'unique': 'True', 'null': 'True'}),
            'pdf': ('dasa.models.FileBrowseField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'pdf_id': ('dasa.models.FileBrowseField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'release_date': ('django.db.models.fields.DateField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'selected_by': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'short_title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'short_title_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'short_title_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title_nl': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'transcribed_by': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'transcription': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'translated_en_by': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'translated_id_by': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'translation_en': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'translation_id': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'})
        },
        u'dasa.hartakarunmaincategory': {
            'Meta': {'ordering': "['position']", 'object_name': 'HartaKarunMainCategory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('dasa.models.ImageFieldMainText', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'image_caption': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'image_caption_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'image_caption_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'image_description_caption': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'image_description_caption_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'image_description_caption_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'image_intro': ('dasa.models.ImageFieldIntro', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'longIntroText': ('tinymce.models.HTMLField', [], {'blank': 'True'}),
            'longIntroText_en': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'longIntroText_id': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'shortIntroText': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'shortIntroText_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'shortIntroText_id': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'dasa.journalentry': {
            'Meta': {'object_name': 'JournalEntry'},
            'annotation': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'archiveFile': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'folio_number_from': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'folio_number_to': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'next': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'previous'", 'null': 'True', 'to': u"orm['dasa.JournalEntry']"}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'priority': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'vessel_names': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'dasa.lightboxitem': {
            'Meta': {'object_name': 'LightBoxItem'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('dasa.models.FileBrowseField', [], {'max_length': '255', 'null': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'url_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'url_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'dasa.menuitem': {
            'Meta': {'ordering': "['order']", 'object_name': 'MenuItem'},
            'function_call': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dasa.BasicPage']", 'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dasa.MenuItem']", 'null': 'True', 'blank': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {'blank': 'True'})
        },
        u'dasa.metatags': {
            'Meta': {'object_name': 'MetaTags'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_id': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'keywords_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'keywords_id': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'object_type': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'dasa.news': {
            'Meta': {'ordering': "['-date']", 'object_name': 'News'},
            'content': ('tinymce.models.HTMLField', [], {'blank': 'True'}),
            'content_en': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'content_id': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2015, 11, 13, 0, 0)'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'description_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_id': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('dasa.models.ImageFieldMainText', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'image_caption': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'image_caption_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'image_caption_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'image_description': ('dasa.models.ImageFieldIntro', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'image_description_caption': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'image_description_caption_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'image_description_caption_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'dasa.placard': {
            'Meta': {'object_name': 'Placard'},
            'governor': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issued_date_d': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'issued_date_m': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'issued_date_y': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'next': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'previous'", 'null': 'True', 'to': u"orm['dasa.Placard']"}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'page_number_from': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'page_number_to': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'published_date_d': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'published_date_m': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'published_date_y': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'volume_number': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'dasa.resolution': {
            'Meta': {'ordering': "('order',)", 'object_name': 'Resolution'},
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'fonds': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'next_resolution': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'_previous_resolution'", 'null': 'True', 'to': u"orm['dasa.Resolution']"}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True'}),
            'priority': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'register_folionumber': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'resolution_folionumber': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'dasa.scan': {
            'Meta': {'ordering': "['position']", 'object_name': 'Scan'},
            'file_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'fonds': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'hartakarun_item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'scans'", 'null': 'True', 'to': u"orm['dasa.HartaKarunItem']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('dasa.models.FileBrowseField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'image_caption': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'image_caption_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'image_caption_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'institution': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'dasa.timelineitem': {
            'Meta': {'object_name': 'TimeLineItem'},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'caption_en': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'caption_id': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'day': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'month': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        },
        u'dasa.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'country': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mugshot': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'privacy': ('django.db.models.fields.CharField', [], {'default': "'registered'", 'max_length': '15'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'userprofile'", 'unique': 'True', 'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['dasa']