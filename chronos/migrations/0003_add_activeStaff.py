
from south.db import db
from django.db import models
from labgeeksrpg.chronos.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding ManyToManyField 'Location.active_staff'
        db.create_table('chronos_location_active_staff', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('location', models.ForeignKey(orm.Location, null=False)),
            ('player', models.ForeignKey(orm['player.Player'], null=False))
        ))
        
    
    
    def backwards(self, orm):
        
        # Dropping ManyToManyField 'Location.active_staff'
        db.delete_table('chronos_location_active_staff')
        
    
    
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
            'active_staff': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['player.Player']", 'null': 'True', 'blank': 'True'}),
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
            'outtime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
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
        },
        'player.player': {
            'about_me': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'aim_iChat': ('django.db.models.fields.CharField', [], {'max_length': '75', 'blank': 'True'}),
            'alt_phone': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'currency': ('django.db.models.fields.IntegerField', [], {}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'gmail': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'grad_date': ('django.db.models.fields.DateField', [], {}),
            'hp': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'irc_network': ('django.db.models.fields.CharField', [], {'max_length': '75', 'blank': 'True'}),
            'irc_nick': ('django.db.models.fields.CharField', [], {'max_length': '75', 'blank': 'True'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'middlename': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'office': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'skype': ('django.db.models.fields.CharField', [], {'max_length': '75', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'uw_gmail': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'uw_windows_live': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'uwnetid': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'windows_live': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'xp': ('django.db.models.fields.IntegerField', [], {}),
            'yahoo': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'})
        }
    }
    
    complete_apps = ['chronos']
