from django.shortcuts import render,HttpResponse,redirect
from teacherapp.models import UserRole,FacultyInfo,PaperUpload
from teacherapp.forms import UserRoleForm,FacultyInfoForm,PaperUploadForm


# Create your views here.
def userindex(request):
    return render(request,"userindex.html")
def usergallery(request):
    return render(request,"usergallery.html")
