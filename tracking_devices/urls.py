from django.urls import path
from .api import views

urlpatterns = [

    # module api
    path('module', views.ModuleView.as_view(), name='module'),
    # meter api
    path('meter', views.MeterView.as_view(), name='meter'),
]
