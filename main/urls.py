from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('download', views.download),
    path('oauth', views.oauth),
    path('reg', views.reg),
    path('list', views.list)
]
