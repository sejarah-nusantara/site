# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BasicPage'
        db.create_table('dasa_basicpage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('title_en', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('title_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('description_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('description_id', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('image_description', self.gf('dasa.models.ImageFieldIntro')(max_length=100, null=True, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('content_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('content_id', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('image', self.gf('dasa.models.ImageFieldMainText')(max_length=100, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('dasa', ['BasicPage'])

        # Adding model 'News'
        db.create_table('dasa_news', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('title_en', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('title_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2012, 10, 26, 0, 0))),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('description_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('description_id', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('image_description', self.gf('dasa.models.ImageFieldIntro')(max_length=100, null=True, blank=True)),
            ('content', self.gf('tinymce.models.HTMLField')(blank=True)),
            ('content_en', self.gf('tinymce.models.HTMLField')(null=True, blank=True)),
            ('content_id', self.gf('tinymce.models.HTMLField')(null=True, blank=True)),
            ('image', self.gf('dasa.models.ImageFieldMainText')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('dasa', ['News'])

        # Adding model 'HartaKarunMainCategory'
        db.create_table('dasa_hartakarunmaincategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('name_en', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('name_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('shortIntroText', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('shortIntroText_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('shortIntroText_id', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('image_intro', self.gf('dasa.models.ImageFieldIntro')(max_length=100, null=True, blank=True)),
            ('longIntroText', self.gf('tinymce.models.HTMLField')(blank=True)),
            ('longIntroText_en', self.gf('tinymce.models.HTMLField')(null=True, blank=True)),
            ('longIntroText_id', self.gf('tinymce.models.HTMLField')(null=True, blank=True)),
            ('image', self.gf('dasa.models.ImageFieldMainText')(max_length=100, null=True, blank=True)),
            ('position', self.gf('django.db.models.fields.IntegerField')(blank=True)),
        ))
        db.send_create_signal('dasa', ['HartaKarunMainCategory'])

        # Adding model 'HartaKarunCategory'
        db.create_table('dasa_hartakaruncategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('name_en', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('name_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('shortIntroText', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('shortIntroText_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('shortIntroText_id', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('image_intro', self.gf('dasa.models.ImageFieldIntro')(max_length=100, null=True, blank=True)),
            ('longIntroText', self.gf('tinymce.models.HTMLField')(blank=True)),
            ('longIntroText_en', self.gf('tinymce.models.HTMLField')(null=True, blank=True)),
            ('longIntroText_id', self.gf('tinymce.models.HTMLField')(null=True, blank=True)),
            ('image', self.gf('dasa.models.ImageFieldMainText')(max_length=100, null=True, blank=True)),
            ('position', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('hartakarun_main_category', self.gf('django.db.models.fields.related.ForeignKey')(related_name='subcategories', null=True, to=orm['dasa.HartaKarunMainCategory'])),
        ))
        db.send_create_signal('dasa', ['HartaKarunCategory'])

        # Adding model 'HartaKarunItem'
        db.create_table('dasa_hartakarunitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hartakaruncategory', self.gf('django.db.models.fields.related.ForeignKey')(related_name='hartakarun_items', to=orm['dasa.HartaKarunCategory'])),
            ('short_title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('short_title_en', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('short_title_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('long_title', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('long_title_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('long_title_id', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('title_nl', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('citation', self.gf('tinymce.models.HTMLField')(blank=True)),
            ('citation_en', self.gf('tinymce.models.HTMLField')(null=True, blank=True)),
            ('citation_id', self.gf('tinymce.models.HTMLField')(null=True, blank=True)),
            ('edited_by', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('introduced_by', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('selected_by', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('transcription', self.gf('tinymce.models.HTMLField')(null=True, blank=True)),
            ('transcribed_by', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('translation_id', self.gf('tinymce.models.HTMLField')(null=True, blank=True)),
            ('translation_en', self.gf('tinymce.models.HTMLField')(null=True, blank=True)),
            ('translated_en_by', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('translated_id_by', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('release_date', self.gf('django.db.models.fields.DateField')(max_length=255, null=True, blank=True)),
            ('introduction', self.gf('tinymce.models.HTMLField')(blank=True)),
            ('introduction_en', self.gf('tinymce.models.HTMLField')(null=True, blank=True)),
            ('introduction_id', self.gf('tinymce.models.HTMLField')(null=True, blank=True)),
            ('image', self.gf('dasa.models.ImageFieldIntro')(max_length=100, null=True, blank=True)),
            ('date_on_timeline', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('ISBN', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('archivalSourceReference', self.gf('django.db.models.fields.CharField')(max_length=1000, blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('comment_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('comment_id', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('dasa', ['HartaKarunItem'])

        # Adding model 'Scan'
        db.create_table('dasa_scan', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('reference', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('hartakarun_item', self.gf('django.db.models.fields.related.ForeignKey')(related_name='scans', null=True, to=orm['dasa.HartaKarunItem'])),
            ('institution', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('fonds', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('file_id', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('position', self.gf('django.db.models.fields.PositiveSmallIntegerField')(blank=True)),
            ('image', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('dasa', ['Scan'])

        # Adding model 'RetroBook'
        db.create_table('dasa_retrobook', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('short_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('short_title_en', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('short_title_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('short_title_dutch', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('full_title', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('full_title_en', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('full_title_id', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('full_title_dutch', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('publication_place', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('publication_year', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('original_language', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('original_language_en', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('original_language_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('short_summary', self.gf('django.db.models.fields.TextField')(max_length=255, blank=True)),
            ('short_summary_en', self.gf('django.db.models.fields.TextField')(max_length=255, null=True, blank=True)),
            ('short_summary_id', self.gf('django.db.models.fields.TextField')(max_length=255, null=True, blank=True)),
            ('comments', self.gf('django.db.models.fields.TextField')(max_length=255, blank=True)),
            ('comments_en', self.gf('django.db.models.fields.TextField')(max_length=255, null=True, blank=True)),
            ('comments_id', self.gf('django.db.models.fields.TextField')(max_length=255, null=True, blank=True)),
            ('citation', self.gf('django.db.models.fields.CharField')(max_length=1000, blank=True)),
            ('citation_en', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('citation_id', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('image', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100, null=True, blank=True)),
            ('institution', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('fonds', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('file_id', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal('dasa', ['RetroBook'])

        # Adding model 'ResolutionClass'
        db.create_table('dasa_resolutionclass', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('full_name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('full_name_en', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('full_name_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('short_name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('short_name_en', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('short_name_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('period_start', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('period_end', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('summary', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('summary_en', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('summary_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('filegroup', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('public', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('public_en', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('public_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('digital', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('digital_en', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('digital_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('authorized', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('authorized_en', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('authorized_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('explanation', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('explanation_en', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('explanation_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('history_institute', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('history_institute_en', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('history_institute_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('history_archive', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('history_archive_en', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('history_archive_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('contents', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('contents_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('contents_id', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('usage', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('usage_en', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('usage_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('year_created', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('colofon', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('colofon_en', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('colofon_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('dasa', ['ResolutionClass'])

        # Adding model 'Resolution'
        db.create_table('dasa_resolution', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=255, null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=255, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('priority', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('source', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=255, null=True, blank=True)),
            ('register_folionumber', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('resolution_folionumber', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('institution', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('fonds', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('file', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('next_resolution', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='_previous_resolution', null=True, to=orm['dasa.Resolution'])),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')(blank=True)),
        ))
        db.send_create_signal('dasa', ['Resolution'])

        # Adding model 'JournalEntry'
        db.create_table('dasa_journalentry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')(blank=True)),
            ('priority', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('folio_number_from', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('folio_number_to', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('annotation', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('vessel_names', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('next', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='previous', null=True, to=orm['dasa.JournalEntry'])),
            ('institution', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('fonds', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('file_id', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal('dasa', ['JournalEntry'])

        # Adding model 'RetroBookScan'
        db.create_table('dasa_retrobookscan', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('URI', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('institution', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('fonds', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('file_id', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('position', self.gf('django.db.models.fields.PositiveSmallIntegerField')(blank=True)),
            ('retrobook', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='scans', null=True, to=orm['dasa.RetroBook'])),
            ('resolution', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='scans', null=True, to=orm['dasa.Resolution'])),
            ('journalentry', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='scans', null=True, to=orm['dasa.JournalEntry'])),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('subject_en', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('subject_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('pagenumber', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('image', self.gf('sorl.thumbnail.fields.ImageField')(max_length=255, null=True, blank=True)),
            ('format', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('creator', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('contributor', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('publisher', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('rights', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('language_en', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('language_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('type_en', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('type_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('source_en', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('source_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('title_en', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('title_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('time_frame_from', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('time_frame_to', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('keywords', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('keywords_en', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('keywords_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('transcription', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('transcription_author', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('transcription_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('translation', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('translation_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('translation_id', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('translation_author_english', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('translation_author_bahassa', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('relation', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('folio_number', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal('dasa', ['RetroBookScan'])

        # Adding model 'TimeLineItem'
        db.create_table('dasa_timelineitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('year', self.gf('django.db.models.fields.IntegerField')()),
            ('month', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('day', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('caption', self.gf('django.db.models.fields.CharField')(max_length=1000, blank=True)),
            ('caption_en', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('caption_id', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
        ))
        db.send_create_signal('dasa', ['TimeLineItem'])

        # Adding model 'LightBoxItem'
        db.create_table('dasa_lightboxitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('title_en', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('title_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('image', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100, null=True)),
            ('visible', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('dasa', ['LightBoxItem'])

    def backwards(self, orm):
        # Deleting model 'BasicPage'
        db.delete_table('dasa_basicpage')

        # Deleting model 'News'
        db.delete_table('dasa_news')

        # Deleting model 'HartaKarunMainCategory'
        db.delete_table('dasa_hartakarunmaincategory')

        # Deleting model 'HartaKarunCategory'
        db.delete_table('dasa_hartakaruncategory')

        # Deleting model 'HartaKarunItem'
        db.delete_table('dasa_hartakarunitem')

        # Deleting model 'Scan'
        db.delete_table('dasa_scan')

        # Deleting model 'RetroBook'
        db.delete_table('dasa_retrobook')

        # Deleting model 'ResolutionClass'
        db.delete_table('dasa_resolutionclass')

        # Deleting model 'Resolution'
        db.delete_table('dasa_resolution')

        # Deleting model 'JournalEntry'
        db.delete_table('dasa_journalentry')

        # Deleting model 'RetroBookScan'
        db.delete_table('dasa_retrobookscan')

        # Deleting model 'TimeLineItem'
        db.delete_table('dasa_timelineitem')

        # Deleting model 'LightBoxItem'
        db.delete_table('dasa_lightboxitem')

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
            'date': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'file_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'folio_number_from': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'folio_number_to': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'fonds': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
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
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 10, 26, 0, 0)'}),
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
            'Meta': {'ordering': "('type', 'order', 'subject', 'date')", 'object_name': 'Resolution'},
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
        'dasa.retrobook': {
            'Meta': {'object_name': 'RetroBook'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'citation': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'citation_en': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'citation_id': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'max_length': '255', 'blank': 'True'}),
            'comments_en': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'comments_id': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'file_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'fonds': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'full_title': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'full_title_dutch': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'full_title_en': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'full_title_id': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'institution': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'original_language': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'original_language_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'original_language_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'publication_place': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'publication_year': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'short_summary': ('django.db.models.fields.TextField', [], {'max_length': '255', 'blank': 'True'}),
            'short_summary_en': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'short_summary_id': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'short_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'short_title_dutch': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'short_title_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'short_title_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'dasa.retrobookscan': {
            'Meta': {'ordering': "['position', 'pagenumber', 'folio_number']", 'object_name': 'RetroBookScan'},
            'URI': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'contributor': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'creator': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'file_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'folio_number': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'fonds': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'format': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'institution': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'journalentry': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'scans'", 'null': 'True', 'to': "orm['dasa.JournalEntry']"}),
            'keywords': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'keywords_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'keywords_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'language_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'language_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'pagenumber': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'blank': 'True'}),
            'publisher': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'relation': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'resolution': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'scans'", 'null': 'True', 'to': "orm['dasa.Resolution']"}),
            'retrobook': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'scans'", 'null': 'True', 'to': "orm['dasa.RetroBook']"}),
            'rights': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'source_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'source_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'subject_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'subject_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'time_frame_from': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'time_frame_to': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'transcription': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'transcription_author': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'transcription_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'translation': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'translation_author_bahassa': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'translation_author_english': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'translation_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'translation_id': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'type_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'type_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'dasa.scan': {
            'Meta': {'ordering': "['position']", 'object_name': 'Scan'},
            'file_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'fonds': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'hartakarun_item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'scans'", 'null': 'True', 'to': "orm['dasa.HartaKarunItem']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'institution': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'blank': 'True'}),
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