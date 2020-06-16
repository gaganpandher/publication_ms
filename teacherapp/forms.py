from django import forms
from teacherapp.models import UserRole, FacultyInfo,PaperUpload

class UserRoleForm(forms.ModelForm):
    class Meta():
        model=UserRole
        exclude=["role_id","role_name"]
class FacultyInfoForm(forms.ModelForm):
    class Meta():
        model=FacultyInfo
        exclude=["teacher_name", "role_id"
                 "email","mobile","isActive","otp","token","time","password","user_image1","area_of_int"]

class PaperUploadForm(forms.ModelForm):
    class Meta():
        model=PaperUpload
        exclude=["role_id","paper_upload","paper_description","author_name","email"]