from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('get_recs/', views.get_recs, name='get_recs'),
    path('send_tele/', views.send_tele, name='send_tele'),
]
