from django.shortcuts import render ,redirect, HttpResponse
from teacherapp.models import UserRole, FacultyInfo,PaperUpload
from teacherapp.forms import UserRoleForm,FacultyInfoForm,PaperUploadForm
from mics import otpGen,author
from mics.emailsending import otpsend,linksend
from django.contrib.auth.hashers import make_password,check_password
import random
from django.conf import settings
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate, login


# Create your views here.
def index(request):
    return render(request,"index.html",)
def useraccount(request):
    auth = author.authorize(request.session['Authentication'], request.session["role"], 1)
    if auth == True:
        return render(request, "userAccount.html")
    else:
        auth, msg = auth
        if auth == False:
            return render(request,"login.html")#HttpResponse("WrongUser")
        elif auth == False:
            return render(request,"login.html")#HttpResponse('Login first')
def usmaster(request):
    return render(request, "masterlogin.html")
def signup(request):
    data = UserRole.objects.all()
    if request.method=="POST":
        form=FacultyInfoForm(request.POST)
        f=form.save(commit=False)
        f.role_id_id = request.POST['role_id']
        f.teacher_name=request.POST["teacher_name"]
        f.email = request.POST["email"]
        f.mobile = request.POST["mobile"]
        password = request.POST["password"]
        cpass=request.POST["cpass"]
        if password != "" and cpass != "":
            if password == cpass:
                f.password = make_password(request.POST["password"])
            else:
                return render(request, "signup.html", {"passworderror": False, 'roledata': data})

        number, numbertime = otpGen.otpfunc()
        token = request.POST["email"][0:5] + str(number) + str(request.POST["mobile"][0:3])
        link = "http//:127.0.0.1:8000/verifyuser/?email=" + request.POST["email"] + "&token=" + str(token)
        linksend(request.POST["email"], link)

        f.token = token
        f.save()
        return HttpResponse("<h1>Data Saved</h1>")
    return render(request, "signup.html", {'roledata':data})
def login(request):
    if request.method=="POST":
        email=request.POST["email"]
        password=request.POST["password"]
        try:
            data=FacultyInfo.objects.get(email=email)
        except:
            return render(request,"login.html",{"emailerror":True})
        dp=check_password(password,data.password)
        role=data.role_id_id
        chkactive=data.isActive
        if(chkactive==False):
            return render(request,"login.html",{"activeerror":True})
        else:
            if(dp==True):
                request.session["email"]=email
                request.session["Authentication"]=True
                request.session["role"] = role
                if role == 1:
                    return redirect("/teacher/index/")
                elif role == 2:
                    return redirect("/user/index/")
            else:
                return render(request,"login.html",{"passworderror":True})
    return render(request,"login.html")

def passwordUpdate(request):
    email = request.GET["email"]
    if request.method == "POST":

        otpvalue = request.POST["otp"]
        new_pass = request.POST["new_password"]
        con_pass = request.POST["conf_password"]
        data = FacultyInfo.objects.get(email=email)
        data_otp = data.otp

        if otpvalue != "":
            if data_otp == otpvalue:
                return render(request, "passwordUpdate.html", {'updatepassword': True})
            else:
                return render(request, "passwordUpdate.html", {'OTP': True, 'wrongotp': True})
        if new_pass != "" and con_pass != "":
            result = confirmation(new_pass, con_pass, email)
            if result == True:

                return redirect("/teacher/login")
            else:
                return redirect("<h1>Password is not updated,Your confirm password is wrong</h1>")

    return render(request, "passwordUpdate.html", {'OTP': True})
def confirmation(np,cp,email):
    new_pass=np
    con_pass=cp
    if new_pass == con_pass:
        db_pass=make_password(con_pass)
        update = FacultyInfo(
                    email=email,
                    password=db_pass
                )
        update.save(update_fields=["password"])
        return True
    else:
        return False
def forget(request):
    if request.method=="POST":
        email=request.POST["email"]
        data=FacultyInfo.objects.get(email= email)
        otp, otp_time = otpGen.otpfunc()
        update = FacultyInfo(
            email=email,
            otp=otp,
            time=otp_time
        )
        update.save(update_fields=["otp", "time"])
        request.session['email'] = email
        otpsend(email, otp)
        return redirect("/teacher/updatepass/?email="+email)
    return render(request,'forget.html')
def logout(request):
    request.session['Authentication']=False
    request.session['email']=None
    return redirect("/")
def gallery(request):
    return render(request,"gallery.html")
def verifyuser(request):
    token = request.GET["token"]
    email = request.GET["email"]
    data = UserInfo.objects.get(email=email)
    print(data)

    tokenvalue = data.token

    print(tokenvalue)

    if (token == tokenvalue):
        update = UserInfo(
            email=email,
            isActive=True
        )
        update.save(update_fields=["isActive"])

        return redirect("/user/login/")

    else:
        return HttpResponse("<h1>not verified </h1>")
def profile(request):
    auth = author.authorize(request.session['Authentication'], request.session["role"], 1)
    if auth == True:
        email = request.session["email"]
        data1 = FacultyInfo.objects.get(email=email)

        roledata = UserRole.objects.all()

        if request.method == "POST":
            email = request.POST["email"]
            teacher_name = request.POST["name"]
            mobile = request.POST["mobile"]
            area_of_int=request.POST["area_of_int"]
            user_image1 = data1.user_image1
            if request.FILES:
                myfile = request.FILES["user_image1"]
                fs = FileSystemStorage()
                filename = fs.save(myfile.name, myfile)
                user_image1 = fs.url(filename)
                user_image1 = myfile.name
            update = FacultyInfo(
                email=email,
                teacher_name=teacher_name,
                mobile=mobile,
                user_image1=user_image1,
                area_of_int=area_of_int
            )
            update.save(update_fields=["teacher_name", "mobile", "user_image1","area_of_int" ])
            return redirect("/teacher/useraccount/")
        return render(request, "profile.html", {"profile": data1,'roledata':roledata})
    else:
        aut, msg = auth
        if msg == 'wrongUser':
            return HttpResponse("<h1>WrongUser</h1>")
        elif msg == 'notLogin':
            return HttpResponse('<h1>Login first</h1>')

def documentupload(request):
    auth = author.authorize(request.session['Authentication'], request.session["role"], 1)
    if auth == True:
        email = request.session["email"]
        data1 = FacultyInfo.objects.get(email=email)
        data2 = PaperUpload.objects.all()
        data = UserRole.objects.all()

        if request.method=="POST":
            form = PaperUploadForm(request.POST,request.FILES)
            f=form.save(commit=False)
            f.email_id=email
            f.paper_id=request.POST["paper_id"]
            f.author_name = request.POST["author_name"]
            f.paper_description = request.POST["paper_description"]
            f.paper_upload = request.FILES["paper_upload"]
            if request.FILES:
                paper_upload=request.FILES["paper_upload"]
                fs = FileSystemStorage()
                filename = fs.save(paper_upload.name, paper_upload)
                paper_upload = fs.url(filename)
                #paper_upload = paper_upload.name
            f.save()

            return redirect("/teacher/documentlist/")
        return render(request,"document.html",{'profile':data1,'documents':data2})
    else:
        auth, msg = auth
        if auth == False:
            return render(request,"login.html")#HttpResponse("WrongUser")
        elif auth == False:
            return render(request,"login.html")#HttpResponse('Login first')

def documentList(request):
    auth = author.authorize(request.session['Authentication'], request.session["role"], 1)
    if auth == True:
        email = request.session["email"]
        data1 = FacultyInfo.objects.get(email=email)
        data2 = PaperUpload.objects.filter(email=email)
        data = UserRole.objects.all()
        return render(request, "documentList.html", {'profile': data1, 'documents': data2})
    else:
        auth, msg = auth
        if auth == False:
            return render(request,"login.html")#HttpResponse("WrongUser")
        elif auth == False:
            return render(request,"login.html")#HttpResponse('Login first')


def delete(request):
    auth = author.authorize(request.session['Authentication'], request.session["role"], 1)
    if auth == True:
        email=request.session["email"]
        data1 = FacultyInfo.objects.get(email=email)
        data2=PaperUpload.objects.filter(email=email)
        data2.delete()
        return redirect("/teacher/documentlist/")
    else:
        auth, msg = auth
        if msg == 'wrongUser':
            return HttpResponse("WrongUser")
        elif msg == 'notLogin':
            return HttpResponse('Login first')
def edit(request):
    auth = author.authorize(request.session['Authentication'], request.session["role"], 1)
    if auth == True:
        #email = request.session["email"]
        #paper_id=request.session["paper_id"]
        #data1 = FacultyInfo.objects.get(email=email)
        data2 = PaperUpload.objects.filter(paper_id)
        data = UserRole.objects.all()
        if request.method == "POST":
            #form = PaperUploadForm(request.POST, request.FILES)
            #f = form.save(commit=False)
            email_id = email
            paper_id = request.POST["paper_id"]
            author_name = request.POST["author_name"]
            paper_description = request.POST["paper_description"]
            paper_upload = request.FILES["paper_upload"]
            if request.FILES:
                paper_upload = request.FILES["paper_upload"]
                fs = FileSystemStorage()
                filename = fs.save(paper_upload.name, paper_upload)
                paper_upload = fs.url(filename)
                # paper_upload = paper_upload.name
            update = PaperUpload(
                paper_id=paper_id,
                author_name=author_name,
                paper_description=paper_description,
                paper_upload=paper_upload,
            )
            update.save(update_fields=["author_name", "paper_description", "paper_upload"])
            return redirect("/teacher/documentlist/")
        return render(request, "edit.html", {'profile': data1, 'documents': data2})
    else:
        auth, msg = auth
        if auth == False:
            return render(request, "login.html")  # HttpResponse("WrongUser")
        elif auth == False:
            return render(request, "login.html")  # HttpResponse('Login first')


def logout(request):
    request.session['Authentication']=False
    request.session['email']=None
    return redirect("/")
