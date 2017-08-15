import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Note, Account
from myproject.serializers import NoteSerializer, AccountSerializer


# initialize the APIClient app
client = Client()

class GetAllNotesTest(TestCase):
    """ Test module for GET all notes API """
    
    def setUp(self):
        Note.objects.create(title='Test title 1', body='Test body 1')
        Note.objects.create(title='Test title 2', body='Test body 2')
        
    def test_get_all_notes(self):
        # get API response
        response = client.get(reverse('get_notes'))
        # get data from db
        notes = Note.objects.all()
        serializer = NoteSerializer(notes, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
class GetSingleNoteTest(TestCase):
    """ Test module for GET all notes API """
    
    def setUp(self):
        self.note1 = Note.objects.create(title='Test title 1', body='Test body 1')
        self.note2 = Note.objects.create(title='Test title 2', body='Test body 2')
        
    def test_get_valid_single_note(self):
        # get API response
        response = client.get(reverse('get_note', kwargs={'note_id': self.note1.id}))
        # get data from db
        note = Note.objects.get(pk=self.note1.id)
        serializer = NoteSerializer(note)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_invalid_single_note(self):
        response = client.get(reverse('get_note', kwargs={'note_id': 30})) # shouldn't have a 30
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class CreateNewNoteTest(TestCase):
    """ Test for inserting a new note """
    
    def setUp(self):
        
        self.note1 = Note.objects.create(title='Test title 0', body='Test body 0')
        self.valid_payload= {
            'title': 'test title 1',
            'body': 'test body 1',
            'username': 'alvin',
            'password': '12345'
        }
        
        self.invalid_payload = {
            'title': '',
            'body': 'test body 2',
            'username': 'alvin',
            'password': '12345'
        }
    
    def test_create_valid_note(self):
        self.user = User.objects.create_superuser('alvin', 'myemail@test.com', '12345')
        res = client.login(username='alvin', password='12345')
        self.assertEqual(res, True)
        
        response = client.post(
            reverse('get_notes'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
            )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_create_invalid_note(self):
        client.login(username='alvin', password='12345')
        response = client.post(
            reverse('get_notes'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
            )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)