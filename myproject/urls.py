"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from api import views
import integrationApis.views

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #url(r'^api/', include(note_resource.urls))
    url(r'^api/notes/$', views.NoteList.as_view(), name='get_notes'),
    url(r'^api/notes/(?P<note_id>[0-9]+)/$', views.NoteDetail.as_view(), name='get_note'),
    url(r'^api/notes/(?P<note_id>[0-9]+)/accounts/$', views.AccountList.as_view(), name='get_accounts'),
    url(r'^api/notes/(?P<note_id>[0-9]+)/accounts/(?P<account_id>[0-9]+)/$', views.AccountDetail.as_view(), name='get_account'),
    url(r'^api-token-auth/', obtain_auth_token),
    url(r'^capitalone/$', integrationApis.views.AccountsPage.as_view()),
    url(r'^synapseusers/(?P<query>\w+)/$', integrationApis.views.SynapseUsers.as_view()),
    url(r'^synapseusers/$', integrationApis.views.SynapseUsers.as_view())
]

#Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    url(r'^accounts/', include('django.contrib.auth.urls')),
]