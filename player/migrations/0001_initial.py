
from south.db import db
from django.db import models
from labgeeksrpg.player.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'PlayerWageHistory'
        db.create_table('player_playerwagehistory', (
            ('id', orm['player.PlayerWageHistory:id']),
        ))
        db.send_create_signal('player', ['PlayerWageHistory'])
        
        # Adding model 'Player'
        db.create_table('player_player', (
            ('id', orm['player.Player:id']),
            ('firstname', orm['player.Player:firstname']),
            ('lastname', orm['player.Player:lastname']),
            ('uwnetid', orm['player.Player:uwnetid']),
            ('hp', orm['player.Player:hp']),
            ('xp', orm['player.Player:xp']),
            ('currency', orm['player.Player:currency']),
            ('status', orm['player.Player:status']),
            ('start_date', orm['player.Player:start_date']),
            ('end_date', orm['player.Player:end_date']),
            ('grad_date', orm['player.Player:grad_date']),
            ('phone', orm['player.Player:phone']),
            ('alt_phone', orm['player.Player:alt_phone']),
            ('uw_gmail', orm['player.Player:uw_gmail']),
            ('uw_windows_live', orm['player.Player:uw_windows_live']),
            ('gmail', orm['player.Player:gmail']),
            ('windows_live', orm['player.Player:windows_live']),
            ('aim_iChat', orm['player.Player:aim_iChat']),
            ('irc_nick', orm['player.Player:irc_nick']),
            ('irc_network', orm['player.Player:irc_network']),
            ('skype', orm['player.Player:skype']),
            ('yahoo', orm['player.Player:yahoo']),
        ))
        db.send_create_signal('player', ['Player'])
        
        # Adding model 'PlayerReview'
        db.create_table('player_playerreview', (
            ('id', orm['player.PlayerReview:id']),
        ))
        db.send_create_signal('player', ['PlayerReview'])
        
        # Adding model 'Skills'
        db.create_table('player_skills', (
            ('id', orm['player.Skills:id']),
        ))
        db.send_create_signal('player', ['Skills'])
        
        # Adding model 'Position'
        db.create_table('player_position', (
            ('id', orm['player.Position:id']),
        ))
        db.send_create_signal('player', ['Position'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'PlayerWageHistory'
        db.delete_table('player_playerwagehistory')
        
        # Deleting model 'Player'
        db.delete_table('player_player')
        
        # Deleting model 'PlayerReview'
        db.delete_table('player_playerreview')
        
        # Deleting model 'Skills'
        db.delete_table('player_skills')
        
        # Deleting model 'Position'
        db.delete_table('player_position')
        
    
    
    models = {
        'player.player': {
            'aim_iChat': ('django.db.models.fields.CharField', [], {'max_length': '75', 'blank': 'True'}),
            'alt_phone': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'currency': ('django.db.models.fields.IntegerField', [], {}),
            'end_date': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'gmail': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'grad_date': ('django.db.models.fields.DateField', [], {}),
            'hp': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'irc_network': ('django.db.models.fields.CharField', [], {'max_length': '75', 'blank': 'True'}),
            'irc_nick': ('django.db.models.fields.CharField', [], {'max_length': '75', 'blank': 'True'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
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
        },
        'player.playerreview': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'player.playerwagehistory': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'player.position': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'player.skills': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }
    
    complete_apps = ['player']
