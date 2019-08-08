from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from gatepass_approve import views

app_name = 'gatepass_approve'

urlpatterns = [
                  path('', views.index, name='index'),
                  path('pending_list/', views.pending_list, name='pending_list'),
                  path('approved_list/', views.approved_list, name='approved_list'),
                  path('rejected_list/', views.rejected_list, name='rejected_list'),
                  path('detail/<id>/', views.gatepass_detail, name='gatepass_detail'),
                  path('print/<pk>/', views.GeneratePdf.as_view(), name='print'),
                  path('approved-supervisor/<id>/', views.approve_gatepass_hostel_supervisor,
                       name='approve_gatepass_hostel_supervisor'),
                  path('approved-warden/<id>/', views.approve_gatepass_hostel_warden,
                       name='approve_gatepass_hostel_warden'),
                  path('approved-assistant-warden/<id>/', views.approve_gatepass_hostel_assistant_warden,
                       name='approve_gatepass_hostel_assistant_warden'),
                  path('approved-controlroom/<id>/', views.approve_gatepass_control_room,
                       name='approve_gatepass_control_room'),
                  path('reject-controlroom/<id>/', views.reject_gatepass_control_room,
                       name='reject_gatepass_control_room'),
                  path('reject-hostel-supervisor/<id>/', views.reject_gatepass_hostel_supervisor,
                       name='reject_gatepass_hostel_supervisor'),
                  path('reject-hostel-warden/<id>/', views.reject_gatepass_hostel_warden,
                       name='reject_gatepass_hostel_warden'),
                  path('reject-hostel-assistant-warden/<id>/', views.reject_gatepass_hostel_assistant_warden,
                       name='reject_gatepass_hostel_assistant_warden'),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
