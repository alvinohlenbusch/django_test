from django.test import TestCase

from ..models import Note, Account

class NoteTest(TestCase):
    """Test module for Note model """
    
    def setUp(self):
        Note.objects.create(title='auto test1', body='unit test 1')
    
    def test_note_body(self):
        note_body = Note.objects.get(title='auto test1')
        self.assertEqual(note_body.body, 'unit test 1')