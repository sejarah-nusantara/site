# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'MarginaliaPersonNamesAsian'
        # try:
        #     db.delete_table(u'dasa_marginaliapersonnamesasian')
        # except:
        #     pass

        # Adding field 'Appendix.person_names_asian'
        db.add_column('dasa_appendix', 'person_names_asian',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'Appendix.person_names_european'
        db.add_column('dasa_appendix', 'person_names_european',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'Appendix.place_names'
        db.add_column('dasa_appendix', 'place_names',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'MarginaliaPersonNamesAsian'
        db.create_table(u'dasa_marginaliapersonnamesasian', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'dasa', ['MarginaliaPersonNamesAsian'])

        # Deleting field 'Appendix.person_names_asian'
        db.delete_column('dasa_appendix', 'person_names_asian')

        # Deleting field 'Appendix.person_names_european'
        db.delete_column('dasa_appendix', 'person_names_european')

        # Deleting field 'Appendix.place_names'
        db.delete_column('dasa_appendix', 'place_names')


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
        u'dasa.appendix': {
            'Meta': {'ordering': "('order',)", 'object_name': 'Appendix'},
            'archiveFile': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'doc_d': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'doc_m': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'doc_y': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'document_type_nl': ('django.db.models.fields.TextField', [], {'max_length': '255', 'blank': 'True'}),
            'folio_number_extra': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'folio_number_from': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'folio_number_to': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'person_names_asian': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'person_names_european': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'place_names': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'res_d': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'res_m': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'res_y': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'title_nl': ('django.db.models.fields.TextField', [], {'max_length': '255', 'blank': 'True'}),
            'vessel_names': ('django.db.models.fields.TextField', [], {'blank': 'True'})
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
        u'dasa.corpusdiplomaticumcontract': {
            'Meta': {'object_name': 'CorpusDiplomaticumContract'},
            'areaName': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'contractSourceDescription': ('django.db.models.fields.TextField', [], {}),
            'dayFrom': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_index': 'True'}),
            'dayTo': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kingdomName': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'monthFrom': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_index': 'True'}),
            'monthTo': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_index': 'True'}),
            'numberDigits': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'numberRoman': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'pageFrom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'pageSupp': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'pageTo': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'signedAsians': ('django.db.models.fields.TextField', [], {}),
            'signedEuropeans': ('django.db.models.fields.TextField', [], {}),
            'signedPlace': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'volumeNumber': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'yearFrom': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_index': 'True'}),
            'yearTo': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_index': 'True'})
        },
        u'dasa.corpusdiplomaticumpersoon': {
            'Meta': {'object_name': 'CorpusDiplomaticumPersoon'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ref': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'volumePage': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'dasa.corpusdiplomaticumplaats': {
            'Meta': {'object_name': 'CorpusDiplomaticumPlaats'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ref': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'volumePage': ('django.db.models.fields.TextField', [], {'blank': 'True'})
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
            'person_names_asian': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'person_names_european': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'place_names': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
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
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2017, 9, 22, 0, 0)'}),
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
