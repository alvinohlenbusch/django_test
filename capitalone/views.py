# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views import generic
from capitalone.services import CapitalOne, SynapseFI

from django.shortcuts import render

class AccountsPage(generic.TemplateView):
    def get(self, request):
        co = CapitalOne()
        account_applications_list = co.get_account_applications()
        return render(request, 'capitalone.html', 
                      {'accountNumber': '12345',
                       'bankABANumber': account_applications_list['bankABANumber'],
                       'applicationStatus': account_applications_list['applicationStatus']})
    # Create your views here.
class SynapseUsers(generic.TemplateView):
    def get(self, request):
        syn = SynapseFI()
        users_list = syn.get_users()
        return render(request, 'synapseusers.html', {'users_list': users_list })
