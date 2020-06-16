from django.conf.urls import url
from userapp import views
app_name='userapp'
urlpatterns = [
    url(r'^index/$',views.userindex),
    url(r'^gallery/$',views.usergallery),

  ]