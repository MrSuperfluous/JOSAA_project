from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('graph/', views.graph_view, name='graph'),
    path('choice/',views.front_choice,name ='front_choice')
]
