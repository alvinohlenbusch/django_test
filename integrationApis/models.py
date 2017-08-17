# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class SynapseFIUser(models.Model):
    """
    Note Model
    Defines the attributest of a user note
    """
    user_id = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    oauth_key = models.CharField(max_length=200)
    refresh_token = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return '%s' % (self.user_id)
    
