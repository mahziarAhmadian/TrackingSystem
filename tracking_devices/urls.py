from django.urls import path
from .api import views

urlpatterns = [

    # module api
    path('module', views.ModuleView.as_view(), name='module'),
    # meter api
    path('meter', views.MeterView.as_view(), name='meter'),
    # truck api
    path('truck', views.TruckView.as_view(), name='truck'),
    # truck_record api
    path('truckRecord', views.TruckRecordView.as_view(), name='truck_record'),
    # meter_site api
    path('meterSite', views.MeterSiteView.as_view(), name='meter_site'),

]
