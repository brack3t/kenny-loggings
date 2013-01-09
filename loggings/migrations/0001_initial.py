# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Log'
        db.create_table('loggings_log', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('action', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('app_name', self.gf('django.db.models.fields.CharField')(default='', max_length=255, db_index=True, blank=True)),
            ('model_name', self.gf('django.db.models.fields.CharField')(default='', max_length=255, db_index=True, blank=True)),
            ('model_instance_pk', self.gf('django.db.models.fields.CharField')(default='', max_length=255, db_index=True, blank=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('previous_json_blob', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('current_json_blob', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('user_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('loggings', ['Log'])

        # Adding model 'LogExtra'
        db.create_table('loggings_logextra', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('log', self.gf('django.db.models.fields.related.ForeignKey')(related_name='extras', to=orm['loggings.Log'])),
            ('field_name', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('field_value', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
        ))
        db.send_create_signal('loggings', ['LogExtra'])


    def backwards(self, orm):
        # Deleting model 'Log'
        db.delete_table('loggings_log')

        # Deleting model 'LogExtra'
        db.delete_table('loggings_logextra')


    models = {
        'loggings.log': {
            'Meta': {'ordering': "['-timestamp']", 'object_name': 'Log'},
            'action': ('django.db.models.fields.SmallIntegerField', [], {}),
            'app_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'db_index': 'True', 'blank': 'True'}),
            'current_json_blob': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model_instance_pk': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'db_index': 'True', 'blank': 'True'}),
            'model_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'db_index': 'True', 'blank': 'True'}),
            'previous_json_blob': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'loggings.logextra': {
            'Meta': {'ordering': "['-log__timestamp']", 'object_name': 'LogExtra'},
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'field_value': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'extras'", 'to': "orm['loggings.Log']"})
        }
    }

    complete_apps = ['loggings']