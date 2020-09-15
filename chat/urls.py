from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views


urlpatterns = [
    path('api/messages/<int:sender>/<int:receiver>', views.message_list, name='message-detail'),
    path('api/messages', views.message_list, name='message-list'),
    path('api/users/', views.user_list, name='user-list'),
    path('api/setonline/', views.set_online, name='set-online'),
    path('api/userdetails', views.user_details, name='user-details')
]
