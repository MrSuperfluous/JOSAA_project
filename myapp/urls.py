from django.urls import path
from django.urls import include
from django.views.static import serve
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('graph/', views.graph_view, name='graph'),
    path('choice/',views.front_choice,name ='front_choice'),
    path('populate/',views.populate,name ='populate'),
    path('branch_list/',views.branch_list,name = 'branch_list'),
    path('get_academic_programs', views.get_academic_programs, name='get_academic_programs'),
    path('get_branch', views.get_branch, name='get_branch'),
    # path('myapp/', include('myapp.urls')),
    url(r'^media/(?P<path>.*)$', serve,{'document_root':       settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
]
