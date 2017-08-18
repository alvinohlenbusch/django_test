# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views import generic
from integrationApis.services import CapitalOne, SynapseFI
from django.http import JsonResponse
from django.shortcuts import render
import filter

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
    """ a rendered view is served of the users from the SynapseFI.get_users API call """
    def get(self, request, query=''):
        syn = SynapseFI()
        users_list = syn.get_users(query)
        
        return render(request, 'synapseusers.html', {'users_list': users_list})

class SynapseUsersAPI(generic.TemplateView):
    """ a rendered view is served of the users from the SynapseFI.get_users API call """
    def get(self, request, query=''):
        syn = SynapseFI()
        users_list = syn.get_users(query)
        
        return JsonResponse(users_list)

class SynapseGetAccountsAPI(generic.TemplateView):
    """ a call to test getting a user's account information """
    def get(selfself, request, user_id):
        syn = SynapseFI()
        account_list = syn.get_accounts(user_id)
        return JsonResponse(account_list)

class SynapseGetAccounts(generic.TemplateView):
    """ a call to test getting a user's account information """
    def get(selfself, request, user_id):
        syn = SynapseFI()
        account_list = syn.get_accounts(user_id)
        return render(request, 'synapseaccounts.html', {'account_list': account_list})