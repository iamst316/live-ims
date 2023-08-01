from django.urls import path

from management.views import ManagementHome


urlpatterns=[
    path("",ManagementHome,name='management-home')
]