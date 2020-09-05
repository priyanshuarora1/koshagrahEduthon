from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from passlib.hash import pbkdf2_sha256
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate,logout
from .models import admindetails
from members.models import studentmodel,teachermodel
import string 
import random 
# Create your views here.

# @login_required
# def adminregister(request):
#     username = request.session["session_key"]
#     p=User.objects.get(username=username)
#     if p.is_superuser:
#         if request.method=='POST':
#             name=request.POST.get("name")
#             username=request.POST.get("username")
#             email=request.POST.get("email")
#             phone=request.POST.get("phone")
#             password=request.POST.get("password")
#             u=User.objects.create_user(email=email,first_name=username,username=username,password=password)
#             u.save()
#             user=User.objects.get(username=username)
#             user.set_password(password)
#             user.save()
#             return redirect("/admin")
        
#         else:
#             return render(request,'general/adminlogin.html')
#     else:
#         return HttpResponse("Not Allowed.")
# @login_required
def adminregister(request):
    if request.user.is_superuser:
        if request.method=='POST':
            name=request.POST.get("name")
            username=request.POST.get("username")
            email=request.POST.get("email")
            phone=request.POST.get("phone")
            password=request.POST.get("password")
            u=User.objects.create_user(email=email,first_name=name,username=username,password=password)
            u.save()
            user=User.objects.get(username=username)
            user.set_password(password)
            user.save()
            r=admindetails.objects.create(adminid=user,phone=phone)
            r.save()
            return redirect("/sanstha/adminregister")
        else:
            return render(request,'adminregister.html')
    else:
        return HttpResponse("You are not allowed to access this page!")

def adminlogin(request):
    if(request.session.has_key('loged')==False or request.session['loged']==False):
    # print("yha ")
        if request.method=='POST':
            # print("yha aaya")
            username=request.POST.get('username')
            password=request.POST.get('password')
            user=authenticate(username=username,password=password)
            if user:
                if user.is_active:
                    login(request,user)
                    request.session['loged'] = True
                    request.session['username'] = username
                    # print("hogya")
                    return redirect("/sanstha/dashboard")
        return render(request,"sanstha/login.html")
    else:
        return redirect("/sanstha/dashboard")

# Create your views here.
def adminlogout(request):
    logout(request)
    request.session['loged'] = False
    request.session['username'] =""
    return redirect('/sanstha/login')

def dashboard(request):
    if(request.session.has_key('loged') and request.session['loged']==True):
        username = request.session["username"]
        logged=User.objects.get(username=username)
        n=random.randint(5, 9)
        res = ''.join(random.choices(string.ascii_uppercase + string.digits, k = n))
        res=res+"*"+str(logged.id)+"$"+res

        return render(request,"sanstha/dashboard.html",{"user":logged,"res":res})
    else:
        return redirect("/sanstha/login")

def pending(request):
    if(request.session.has_key('loged') and request.session['loged']==True):
        username = request.session["username"]
        logged=User.objects.get(username=username)
        # details = User.objects.filter(username=logged)
        req=studentmodel.objects.filter(admin=logged.id,is_active=False)
        t_req=teachermodel.objects.filter(admin=logged.id,is_active=False)
        return render(request,"sanstha/pending.html",{"user":logged,"stu_req":req,"teacher_req":t_req})
    else:
        return redirect("/sanstha/login")
def searchbar(request):
    if(request.session.has_key('loged') and request.session['loged']==True):
        if request.method=='POST':
            username=request.POST.get('username')
            r=studentmodel.objects.get(stuid=username)
            return render(request,"sanstha/search.html",{'r':r})

        else:
            return render(request,"sanstha/search.html")
def status(request,id):
    student=studentmodel.objects.get(id=id)
    if request.user.id==student.admin_id:
        if student.is_active:
            student.is_active=False
            student.save()
        else:
            student.is_active=True
            student.save()
        return redirect('/sanstha/search')
    else:
        return HttpResponse("You cannot access this request.")
def empsearchbar(request):
    if(request.session.has_key('loged') and request.session['loged']==True):
        if request.method=='POST':
            username=request.POST.get('username')
            r=teachermodel.objects.get(empid=str(username))
            return render(request,"sanstha/search.html",{'e':r})

        else:
            return render(request,"sanstha/search.html")
def empdelete(request,id):
    employee=teachermodel.objects.get(id=id)
    if request.user.id==employee.admin_id:
        employee.delete()
        return redirect('/sanstha/search')
    else:
        return HttpResponse("You cannot access this request.")

def posts(request):
    if(request.session.has_key('loged') and request.session['loged']==True):
        username = request.session["username"]
        logged=User.objects.get(username=username)
        return render(request,"sanstha/allpost.html")

def delpost(request):
    if(request.session.has_key('loged') and request.session['loged']==True):
        username = request.session["username"]
        logged=User.objects.get(username=username)
        postid = request.GET["id"]
        return HttpResponse("post deleted")
