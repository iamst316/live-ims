from django.urls import path
from .views import *

urlpatterns=[
    path("",Transactions.as_view(),name='transactions'),
    path("sell/", CreateTransaction,name="sell"),
    path("sell/<id>", TransactSpecific,name="sell-specific"),
]
