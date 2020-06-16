from django.db import models

# Create your models here.
class UserRole(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=200, default="", unique=True)
class FacultyInfo(models.Model):
    role_id = models.ForeignKey(UserRole, on_delete=models.CASCADE)
    teacher_name = models.CharField(max_length=200, default="")
    email = models.CharField(max_length=200, default="", primary_key=True)
    mobile = models.BigIntegerField(null=True)
    isActive = models.BooleanField(default=False)
    otp = models.CharField(max_length=200, default="", null=True)
    token = models.CharField(max_length=200, default="", null=True)
    time = models.CharField(max_length=200, default="", null=True)
    password = models.CharField(max_length=200, default="")
    user_image1 = models.CharField(max_length=500, null=True)
    area_of_int=models.CharField(max_length=500,default="",null=True)
class PaperUpload(models.Model):
    email=models.ForeignKey(FacultyInfo,on_delete=models.CASCADE)
    role_id=models.ForeignKey(UserRole,on_delete=models.CASCADE,default="1")
    paper_id=models.CharField(max_length=200,default="", primary_key=True)
    paper_upload=models.FileField()
    paper_description=models.CharField(max_length=500,default="")
    author_name=models.CharField(max_length=200,default="")
