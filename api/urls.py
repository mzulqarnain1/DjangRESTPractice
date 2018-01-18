"""RealEstate_API URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin
from rest_framework.schemas import get_schema_view

from api import views

schema_view = get_schema_view(title='Real Estate API')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^property/(?P<pk>[0-9]+)/', views.PropertyDetail.as_view(), name="property-details"),
    url(r'^property/(?P<pk>[0-9]+)', views.PropertyDetail.as_view(), name="property-details"),
    url(r'^property', views.PropertyList.as_view(), name='property-list'),
    url(r'^status/(?P<pk>[0-9]+)/', views.StatusDetail.as_view(), name="status-details"),
    url(r'^status/(?P<pk>[0-9]+)', views.StatusDetail.as_view(), name="status-details"),
    url(r'^status/', views.StatusList.as_view(), name='status-list'),
    url(r'^status', views.StatusList.as_view(), name='status-list'),
    url(r'^type/(?P<pk>[0-9]+)/', views.PropertyTypeDetail.as_view(), name="type-details"),
    url(r'^type/(?P<pk>[0-9]+)', views.PropertyTypeDetail.as_view(), name="type-details"),
    url(r'^type', views.PropertyTypeList.as_view(), name='type-list'),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name='users-details'),
    url(r'^users/$', views.UserList.as_view(), name='users-list'),
    url(r'^schema/$', schema_view),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls')),
]
