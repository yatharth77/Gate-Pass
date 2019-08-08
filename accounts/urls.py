from django.urls import path
from accounts import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'accounts'

urlpatterns = [
                  path('login/', views.user_login, name='user_login'),
                  path('logout/', views.user_logout, name='user_logout'),
                  path('signup/', views.signup, name='user_signup'),
                  path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
                       views.activate, name='activate'),
                  path('password_change/', views.PasswordChangeView.as_view(), name='password_change'),
                  path('password_change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),
                  path('update-profile/', views.update_profile, name='update_profile'),
                  path('view-profile/', views.view_profile, name='view_profile'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
