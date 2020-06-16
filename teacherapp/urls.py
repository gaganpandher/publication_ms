from django.conf.urls import url
from teacherapp import views
app_name='teacherapp'
urlpatterns = [
    url(r'^index/',views.index),
    url(r'^usermaster/$',views.usmaster),
    url(r'^login/$',views.login),
    url(r'^signup/$',views.signup),
    url(r'^updatepass/$',views.passwordUpdate),
    url(r'^verification/$',views.verifyuser),
    url(r'^logout/$',views.logout),
    url(r'^forget/$',views.forget),
    url(r'^gallery/$',views.gallery),
    url(r'^useraccount/$',views.useraccount),
    url(r'^profile/$',views.profile),
    url(r'^document/$',views.documentupload),
    url(r'^documentlist/$',views.documentList),
    url(r'^delete/$',views.delete),
    url(r'^logout/$',views.logout),
    url(r'^edit/$',views.edit),
    ]