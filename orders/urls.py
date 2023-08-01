from django.urls import path
# from django.conf.urls import url

from . import views
urlpatterns = [
    path("", views.Orders.as_view(),name="orders"),
    path("order/", views.CreateOrder,name="order"),
    path("received/", views.ReceivedList.as_view(),name="orders-received"),
    path("cancelled/", views.CancelledList.as_view(),name="orders-cancelled"),
    path("order/<id>", views.OrderSpecific,name="order-specific"),
    path("receive-confirmation/<id>",views.MarkReceived,name="receive-confirmation"),
    path("cancel-confirmation/<id>",views.MarkCancelled,name="cancel-confirmation"),
]