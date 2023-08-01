from django.urls import path
from . import views

urlpatterns = [
    path("", views.Home,name="home"),
    # path('pie-chart/', views.pie_chart, name='pie-chart'),
    path("items/", views.Items.as_view(),name="items"),
    path("items/edit", views.ItemEditList.as_view(),name="items-edit-list"),
    path("items/view", views.ItemViewList.as_view(),name="items-view-list"),
    path("add-item/",views.AddItem,name="add-item"),
    path("items/<int:pk>/",views.ItemDetailsView.as_view(), name="item-details"),
    path("items/<int:pk>/edit/",views.EditItemDetailsView.as_view(), name="edit-item-details"),
    path("items/<id>/orders",views.ItemSpecificOrders,name='items-specific-orders'),
    path("items/<id>/received-orders",views.ItemSpecificReceivedOrders,name='items-specific-received-orders'),
    path("items/<id>/cancelled-orders",views.ItemSpecificCancelledOrders,name='items-specific-cancelled-orders')
]