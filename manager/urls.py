from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from manager import views

app_name = 'manager'

urlpatterns = [
                  path('', views.index, name='index'),
                  path('list-users/', views.list_users, name='list_users'),
                  path('add-user/', views.add_user, name='add_user'),
                  path('update-user/<id>/', views.update_user, name='update_user'),
                  path('detail/<id>/', views.user_detail, name='user-detail'),
                  path('delete/<id>/', views.del_user, name='delete-user'),
                  path('pending-list/', views.pending_list, name='pending_list'),
                  path('rejected-list/', views.rejected_list, name='rejected_list'),
                  path('approved-list/', views.approved_list, name='approved_list'),
                  path('gatepass-detail/<id>/', views.gatepass_detail, name='gatepass_detail'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
