# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):
    """
    Note Model
    Defines the attributest of a user note
    """
    title = models.CharField(max_length=200)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return '%s - %s' % (self.title, self.body)
    
class Account(models.Model):
    """
    Account Model
    Defines the attributes of a bank account
    """
    note = models.ForeignKey(Note, related_name='account')
    title = models.CharField(max_length=255)
    accountNumber = models.CharField(max_length=255)
    created_by = models.ForeignKey(User)
    
class SynapseUser(models.Model):
    """
    SynapseUser Model
    Defines the attributes of a Synapse user
    """
    covered_user = models.ForeignKey(User)
    synapse_id = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    

