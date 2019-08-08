from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from gatepass_apply import views

app_name = 'gatepass_apply'
urlpatterns = [
                  path('apply/', views.apply, name='apply'),
                  path('history/', views.history, name='history'),
                  path('add_item/<id>/', views.add_item, name='add_item'),
                  path('print/<pk>/', views.GeneratePdf.as_view(), name='print'),
                  path('delete/<id>/<gatepass_id>/', views.delete_item, name='delete_item'),
                  path('detail/<id>/', views.gatepass_detail, name='gatepass_detail'),
                  path('gatepass_delete/<id>/', views.gatepass_delete, name='gatepass_delete'),
                  path('gatepass_update/<id>/', views.gatepass_update, name='gatepass_update'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
