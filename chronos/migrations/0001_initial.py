
from south.db import db
from django.db import models
from labgeeksrpg.chronos.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Shift'
        db.create_table('chronos_shift', (
            ('id', orm['chronos.Shift:id']),
            ('person', orm['chronos.Shift:person']),
            ('intime', orm['chronos.Shift:intime']),
            ('outtime', orm['chronos.Shift:outtime']),
            ('punchclock', orm['chronos.Shift:punchclock']),
            ('shiftnote', orm['chronos.Shift:shiftnote']),
        ))
        db.send_create_signal('chronos', ['Shift'])
        
        # Adding model 'Punchclock'
        db.create_table('chronos_punchclock', (
            ('id', orm['chronos.Punchclock:id']),
            ('name', orm['chronos.Punchclock:name']),
            ('location', orm['chronos.Punchclock:location']),
            ('ip_address', orm['chronos.Punchclock:ip_address']),
        ))
        db.send_create_signal('chronos', ['Punchclock'])
        
        # Adding model 'Location'
        db.create_table('chronos_location', (
            ('id', orm['chronos.Location:id']),
            ('name', orm['chronos.Location:name']),
        ))
        db.send_create_signal('chronos', ['Location'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Shift'
        db.delete_table('chronos_shift')
        
        # Deleting model 'Punchclock'
        db.delete_table('chronos_punchclock')
        
        # Deleting model 'Location'
        db.delete_table('chronos_location')
        
    
    
    models = {
        'auth.group': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'chronos.location': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'chronos.punchclock': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['chronos.Location']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'chronos.shift': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intime': ('django.db.models.fields.DateTimeField', [], {}),
            'outtime': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'punchclock': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['chronos.Punchclock']"}),
            'shiftnote': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }
    
    complete_apps = ['chronos']
