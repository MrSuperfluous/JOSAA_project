"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from . import view
from django.urls import include, path
from allauth.socialaccount import providers
from django.views.generic import RedirectView
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
   
)

urlpatterns = [
    path('myapp/', include('myapp.urls')),
    path('admin/', admin.site.urls),
    path('', view.home),
    # path('accounts/', include('allauth.urls')),
    # path('accounts/google/login/callback/', OAuth2CallbackView.as_view(adapter=OAuth2Adapter)),
    # path('accounts/google/login/', OAuth2LoginView.as_view(adapter=OAuth2Adapter)),
    # path('accounts/google/', RedirectView.as_view(url='/accounts/google/login/')),
    path('accounts/', include('allauth.urls')),
]
