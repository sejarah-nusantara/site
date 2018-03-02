# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'RetroBook'
        db.delete_table('dasa_retrobook')

        # Deleting model 'RetroBookScan'
        db.delete_table('dasa_retrobookscan')

        # Adding unique constraint on 'HartaKarunItem', fields ['number']
        db.create_unique('dasa_hartakarunitem', ['number'])

    def backwards(self, orm):
        # Removing unique constraint on 'HartaKarunItem', fields ['number']
        db.delete_unique('dasa_hartakarunitem', ['number'])

        # Adding model 'RetroBook'
        db.create_table('dasa_retrobook', (
            ('comments_en', self.gf('django.db.models.fields.TextField')(max_length=255, null=True, blank=True)),
            ('short_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('image', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100, null=True, blank=True)),
            ('citation', self.gf('django.db.models.fields.CharField')(max_length=1000, blank=True)),
            ('full_title_en', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('comments', self.gf('django.db.models.fields.TextField')(max_length=255, blank=True)),
            ('fonds', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('citation_id', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('full_title_dutch', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('original_language', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('short_title_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('citation_en', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('full_title', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('short_summary_en', self.gf('django.db.models.fields.TextField')(max_length=255, null=True, blank=True)),
            ('file_id', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('short_summary', self.gf('django.db.models.fields.TextField')(max_length=255, blank=True)),
            ('institution', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('comments_id', self.gf('django.db.models.fields.TextField')(max_length=255, null=True, blank=True)),
            ('full_title_id', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('publication_year', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('original_language_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('original_language_en', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('short_title_dutch', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('publication_place', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('short_summary_id', self.gf('django.db.models.fields.TextField')(max_length=255, null=True, blank=True)),
            ('short_title_en', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('dasa', ['RetroBook'])

        # Adding model 'RetroBookScan'
        db.create_table('dasa_retrobookscan', (
            ('folio_number', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('type_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('image', self.gf('sorl.thumbnail.fields.ImageField')(max_length=255, null=True, blank=True)),
            ('time_frame_from', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('translation_id', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('relation', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('contributor', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('translation_author_english', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('time_frame_to', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('type_en', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('institution', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('keywords_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('format', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('URI', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('translation', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('keywords_en', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('rights', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('retrobook', self.gf('django.db.models.fields.related.ForeignKey')(related_name='scans', null=True, to=orm['dasa.RetroBook'], blank=True)),
            ('journalentry', self.gf('django.db.models.fields.related.ForeignKey')(related_name='scans', null=True, to=orm['dasa.JournalEntry'], blank=True)),
            ('creator', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('keywords', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('pagenumber', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('fonds', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('transcription', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('subject_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('language_en', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('language_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('translation_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('subject_en', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('source_en', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('title_en', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('transcription_author', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('file_id', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('publisher', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('title_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('translation_author_bahassa', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('source_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('position', self.gf('django.db.models.fields.PositiveSmallIntegerField')(blank=True)),
            ('resolution', self.gf('django.db.models.fields.related.ForeignKey')(related_name='scans', null=True, to=orm['dasa.Resolution'], blank=True)),
            ('transcription_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('dasa', ['RetroBookScan'])

    models = {
        'dasa.basicpage': {
            'Meta': {'object_name': 'BasicPage'},
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'content_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'content_id': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'description_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_id': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('dasa.models.ImageFieldMainText', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'image_description': ('dasa.models.ImageFieldIntro', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'dasa.hartakaruncategory': {
            'Meta': {'ordering': "['position']", 'object_name': 'HartaKarunCategory'},
            'hartakarun_main_category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subcategories'", 'null': 'True', 'to': "orm['dasa.HartaKarunMainCategory']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('dasa.models.ImageFieldMainText', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'image_intro': ('dasa.models.ImageFieldIntro', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
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
        'dasa.hartakarunitem': {
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
            'hartakaruncategory': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'hartakarun_items'", 'to': "orm['dasa.HartaKarunCategory']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('dasa.models.ImageFieldIntro', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'introduced_by': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'introduction': ('tinymce.models.HTMLField', [], {'blank': 'True'}),
            'introduction_en': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'introduction_id': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'long_title': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'long_title_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'long_title_id': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '50', 'unique': 'True', 'null': 'True'}),
            'pdf': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
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
        'dasa.hartakarunmaincategory': {
            'Meta': {'ordering': "['position']", 'object_name': 'HartaKarunMainCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('dasa.models.ImageFieldMainText', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'image_intro': ('dasa.models.ImageFieldIntro', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
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
        'dasa.journalentry': {
            'Meta': {'object_name': 'JournalEntry'},
            'annotation': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'archiveFile': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'folio_number_from': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'folio_number_to': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'next': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'previous'", 'null': 'True', 'to': "orm['dasa.JournalEntry']"}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'priority': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'vessel_names': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'dasa.lightboxitem': {
            'Meta': {'object_name': 'LightBoxItem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'dasa.news': {
            'Meta': {'ordering': "['-date']", 'object_name': 'News'},
            'content': ('tinymce.models.HTMLField', [], {'blank': 'True'}),
            'content_en': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'content_id': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 4, 26, 0, 0)'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'description_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_id': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('dasa.models.ImageFieldMainText', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'image_description': ('dasa.models.ImageFieldIntro', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'dasa.resolution': {
            'Meta': {'ordering': "('order',)", 'object_name': 'Resolution'},
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'fonds': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'next_resolution': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'_previous_resolution'", 'null': 'True', 'to': "orm['dasa.Resolution']"}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True'}),
            'priority': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'register_folionumber': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'resolution_folionumber': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'dasa.resolutionclass': {
            'Meta': {'object_name': 'ResolutionClass'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'authorized': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'authorized_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'authorized_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'colofon': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'colofon_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'colofon_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'contents': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'contents_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'contents_id': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'digital': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'digital_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'digital_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'explanation': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'explanation_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'explanation_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'filegroup': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'full_name_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'full_name_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'history_archive': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'history_archive_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'history_archive_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'history_institute': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'history_institute_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'history_institute_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'period_end': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'period_start': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'public': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'public_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'public_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'short_name_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'short_name_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'summary_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'summary_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'usage': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'usage_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'usage_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'year_created': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'dasa.scan': {
            'Meta': {'ordering': "['position']", 'object_name': 'Scan'},
            'file_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'fonds': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'hartakarun_item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'scans'", 'null': 'True', 'to': "orm['dasa.HartaKarunItem']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'institution': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'dasa.timelineitem': {
            'Meta': {'object_name': 'TimeLineItem'},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'caption_en': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'caption_id': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'day': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'month': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['dasa']