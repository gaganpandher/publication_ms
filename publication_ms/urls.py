"""publication_ms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from django.urls import path
from django.conf.urls import url,include
from teacherapp import views
from django.conf.urls.static import static
from django.conf import settings
from userapp import views
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^teacher/',include('teacherapp.urls')),
    url(r'^user/',include('userapp.urls')),
    url(r'^$',views.userindex),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
