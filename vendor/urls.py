from django.urls import path, include

from . import views

from accounts import views as AccountViews


urlpatterns = [
    path('', AccountViews.vendorDashboard, name='vendor'),
    path('profile/', views.vprofile, name='vprofile'),
    path('menu-builder/', views.menu_builder, name='menu_builder'),
    path('menu-builder/category/<int:pk>/', views.online_item_by_category, name='online_item_by_category'),

    # Category CRUD
    path('menu-builder/category/add/', views.add_category, name='add_category'),
    path('menu-builder/category/edit/<int:pk>/', views.edit_category, name='edit_category'),
    path('menu-builder/category/delete/<int:pk>/', views.delete_category, name='delete_category'),

    # Onlineitems crude
    path('menu-builder/item/add/', views.add_item, name='add_item'),
    path('menu-builder/food/edit/<int:pk>/', views.edit_item, name='edit_item'),
    path('menu-builder/item/delete/<int:pk>/', views.delete_item, name='delete_item'),
]