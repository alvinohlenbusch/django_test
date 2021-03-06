# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from api.models import Note, Account
from myproject.serializers import NoteSerializer, AccountSerializer
from myproject.permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly

class NoteList(generics.ListCreateAPIView):
    queryset = Note.objects.all()
    permission_classes = (IsAdminOrReadOnly, )
    serializer_class = NoteSerializer

class NoteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = (IsAdminOrReadOnly, )
    lookup_url_kwarg = 'note_id'
        
class AccountList(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    lookup_url_kwarg = 'note_id'
    
    def perform_create(self, serializer):
        serializer.save(
            created_by=self.request.user,
            note_id=self.kwargs['note_id'])
        
    def get_queryset(self):
        note = self.kwargs['note_id']
        return Account.objects.filter(note__id=note)
        
class AccountDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AccountSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    lookup_url_kwarg = 'account_id'
    
    def get_queryset(self):
        account = self.kwargs['account_id']
        return Account.objects.filter(id=account)
