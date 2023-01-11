from django.urls import path
from .api import views

urlpatterns = [
    # permissions
    path('add', views.PermissionAPI.as_view(), name='add permission'),
]
