from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from Qsystem import views

app_name = 'Qsystem'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('info/', views.info, name='info'),
    path('deposit/', views.deposit, name='deposit'),
    path('withdraw/', views.withdraw, name='withdraw'),
]
