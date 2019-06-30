"""course_specifications URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.auth import logout, login
from django.urls import path, include

urlpatterns = i18n_patterns(
    path('', include('main_app.urls', namespace='main_app')),
    path('admin/', admin.site.urls),
    path('login/', login, name='login'),  # The base django login view
    path('logout/', logout, name='logout'),  # The base django logout view
)
