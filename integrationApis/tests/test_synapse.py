import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from ..services import SynapseFI
from curses.ascii import SYN


# initialize the APIClient app
client = Client()

class GetUsers(TestCase):
    """ Test module for GET all notes API """
    
    def test_get_users(self):
        syn = SynapseFI()
        answer = syn.get_users('Calvin Knight')
        
        self.assertEqual(answer['users'][0]['_id'], '593209d416772e00261678f7')

