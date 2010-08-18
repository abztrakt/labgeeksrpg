# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'EmploymentStatus'
        db.create_table('people_employmentstatus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('people', ['EmploymentStatus'])

        # Adding model 'TimePeriod'
        db.create_table('people_timeperiod', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('people', ['TimePeriod'])

        # Adding model 'WorkGroup'
        db.create_table('people_workgroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('manager', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('people', ['WorkGroup'])

        # Deleting field 'UserProfile.hp'
        db.delete_column('people_userprofile', 'hp')

        # Deleting field 'UserProfile.currency'
        db.delete_column('people_userprofile', 'currency')

        # Deleting field 'UserProfile.xp'
        db.delete_column('people_userprofile', 'xp')

        # Adding field 'UserProfile.call_me_by'
        db.add_column('people_userprofile', 'call_me_by', self.gf('django.db.models.fields.CharField')(default='', max_length=256, blank=True), keep_default=False)

        # Adding field 'UserProfile.status'
        db.add_column('people_userprofile', 'status', self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['people.EmploymentStatus']), keep_default=False)

        # Adding field 'UserProfile.supervisor'
        db.add_column('people_userprofile', 'supervisor', self.gf('django.db.models.fields.related.ForeignKey')(default='', related_name='supervisor', to=orm['auth.User']), keep_default=False)

        # Adding field 'UserProfile.title'
        db.add_column('people_userprofile', 'title', self.gf('django.db.models.fields.CharField')(default='', max_length=256, blank=True), keep_default=False)

        # Adding field 'UserProfile.working_periods'
        db.add_column('people_userprofile', 'working_periods', self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['people.TimePeriod']), keep_default=False)


    def backwards(self, orm):
        
        # Deleting model 'EmploymentStatus'
        db.delete_table('people_employmentstatus')

        # Deleting model 'TimePeriod'
        db.delete_table('people_timeperiod')

        # Deleting model 'WorkGroup'
        db.delete_table('people_workgroup')

        # Adding field 'UserProfile.hp'
        db.add_column('people_userprofile', 'hp', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Adding field 'UserProfile.currency'
        db.add_column('people_userprofile', 'currency', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Adding field 'UserProfile.xp'
        db.add_column('people_userprofile', 'xp', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Deleting field 'UserProfile.call_me_by'
        db.delete_column('people_userprofile', 'call_me_by')

        # Deleting field 'UserProfile.status'
        db.delete_column('people_userprofile', 'status_id')

        # Deleting field 'UserProfile.supervisor'
        db.delete_column('people_userprofile', 'supervisor_id')

        # Deleting field 'UserProfile.title'
        db.delete_column('people_userprofile', 'title')

        # Deleting field 'UserProfile.working_periods'
        db.delete_column('people_userprofile', 'working_periods_id')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'people.employmentstatus': {
            'Meta': {'object_name': 'EmploymentStatus'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'people.timeperiod': {
            'Meta': {'object_name': 'TimePeriod'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'people.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'about_me': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'alt_phone': ('django.db.models.fields.CharField', [], {'max_length': '12', 'blank': 'True'}),
            'call_me_by': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'grad_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'office': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '12', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.EmploymentStatus']"}),
            'supervisor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'supervisor'", 'to': "orm['auth.User']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'uwnetid'", 'unique': 'True', 'to': "orm['auth.User']"}),
            'working_periods': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.TimePeriod']"})
        },
        'people.workgroup': {
            'Meta': {'object_name': 'WorkGroup'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manager': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        }
    }

    complete_apps = ['people']
