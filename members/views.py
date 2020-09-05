import os
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from passlib.hash import pbkdf2_sha256
from .models import teachermodel,studentmodel,studentdetails,teacherdetails
from django.core.mail import send_mail
import math, random
from django.shortcuts import redirect
from django.views.decorators.clickjacking import xframe_options_sameorigin
from datetime import datetime
from .models import upload_posts,upload_achievements,upload_achievements_emp,chat_message,latestmessage,viewthread
import base64
from django.core.files.base import ContentFile
from datetime import datetime
from pytz import timezone


def register_member(request):
    if request.method=="POST":
        adminid=request.POST.get('adminid')
        print(adminid)
        a,adminid=adminid.split('*')
        adminid,a=adminid.split('$')
        print(adminid)
        admin=User.objects.get(id=adminid)
        membername = request.POST.get("type")
        if(membername=="teacher"):
            flag = 1
        else:
            flag = 0
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        uniqueid=request.POST.get('uniqueid')
        name=request.POST.get('name')
        password=request.POST.get('password')
        password=pbkdf2_sha256.hash(password,rounds=12000,salt_size=32)
        if flag:
            try:
                s=teachermodel.objects.create(name=name,phone=phone,password=password,empid=uniqueid,email=email,admin_id=adminid)
                s1 = teacherdetails.objects.create(admin=s)
            except:
                return HttpResponse("emplyeeId id already taken")
            return redirect("/login")
        else:
            try:
                s=studentmodel.objects.create(name=name,phone=phone,password=password,stuid=uniqueid,email=email,admin_id=adminid)
                s1 = studentdetails.objects.create(admin=s)
            except:
                return HttpResponse("studentId id already taken")
            return redirect("/login")
    
def signup(request,admin):
    # print(admin)
    return render(request,'general/usersignup.html',{'id':admin})

def login(request):
    if(request.session.has_key('logged') and request.session["logged"]==True):
        return redirect("/dashboard")
    else:
        if request.method=='POST':
            username=request.POST.get('userid')
            password=request.POST.get('password')
            flag = request.POST.get('type')
            if flag=="teacher":
                try:
                    user=teachermodel.objects.get(empid=username)
                except:
                    return render(request,'general/userlogin.html',{'error1':"Invalid teacher ID"})
                if(pbkdf2_sha256.verify(password,user.password)):
                    if user.is_active:
                        request.session['logged'] = True
                        request.session['teacher'] = username
                        return redirect("/dashboard")
                    else:
                        return HttpResponse("Contact Admin To Confirm Your Account.")
                else:
                    error1="Invalid login details supplied!"
                    return render(request,'general/userlogin.html',{'error1':error1})
            else:
                try:
                    user=studentmodel.objects.get(stuid=username)
                except:
                    return render(request,'general/userlogin.html',{'error1':"Invalid details"})
                if(pbkdf2_sha256.verify(password,user.password)):
                    if user.is_active:
                        request.session['logged'] = True
                        request.session['student'] = username
                        return redirect("/dashboard")
                    else:
                        return HttpResponse("Contact Admin To Confirm Your Account.")
                else:
                    error1="Invalid login details supplied!"
                    return render(request,'general/userlogin.html',{'error1':error1})
        # else: 
        #     return render(request,"general/userlogin.html")
        else:    
            return render(request,'general/userlogin.html')

@xframe_options_sameorigin
def userdashboard(request):
    if(request.session.has_key("logged") and request.session["logged"]==True):
        try:
            user=teachermodel.objects.get(empid=request.session["teacher"])
        except:
            user = studentmodel.objects.get(stuid=request.session["student"])
        return render(request,"general/userdashboard.html",{"user":user})
    else:
        return redirect("/login")




def userlogout(request):
    try:
        del request.session['teacher']
        request.session["logged"] = False
    except:
        del request.session['student']
    request.session["logged"] = False
    return redirect("/login")


def teacher_logout(request):
    del request.session['teacher']
    return render(request,'/general/userlogin')


def generateOTP() :
    digits = "0123456789"
    OTP = ""
    for i in range(4) :
        OTP += digits[math.floor(random.random() * 10)]
    return OTP

def send_otp(request):
    email=request.POST.get("email")
    o=generateOTP()
    htmlgen = '<p>Your OTP is <strong>'+o+'</strong></p>'
    send_mail('OTP request for Smart Menu',o,'noreply.jumblejuggle@gmail.com',[email],fail_silently=False,html_message=htmlgen)
    print(o)
    return HttpResponse(o)

@xframe_options_sameorigin
def home(request):
    try:
        username = request.session['teacher']
        log = teachermodel.objects.get(empid=username)
    except:
        username = request.session['student']
        log=studentmodel.objects.get(stuid=username)
    posts=upload_posts.objects.filter(admin=log.admin).order_by("id")[::-1]
    return render(request,"general/home.html",{'posts':posts})

@xframe_options_sameorigin
def vault(request):
    try:
        u=teachermodel.objects.get(empid=request.session["teacher"])
        details = upload_achievements_emp.objects.filter(user=u)
    except:
        u = studentmodel.objects.get(stuid=request.session["student"])
        details = upload_achievements.objects.filter(user=u)
        print(details)
    return render(request,"general/vault.html",{"cert":details})

@xframe_options_sameorigin
def profile(request):
    if(request.session.has_key("logged") and request.session["logged"]==True):
        try:
            user=teachermodel.objects.get(empid=request.session["teacher"])
            details = teacherdetails.objects.get(admin_id=user.id)
            username=user.empid
            detail = upload_achievements_emp.objects.filter(user=user)
        except:
            user = studentmodel.objects.get(stuid=request.session["student"])
            details = studentdetails.objects.get(admin_id=user.id)
            username=user.stuid
            detail = upload_achievements.objects.filter(user=user)
        posts=upload_posts.objects.filter(admin=user.admin,username=username ).order_by("id")[::-1]
        return render(request,"general/profile.html",{"user":user,"details":details,"posts":posts,"cert":detail})
    else:
        return redirect("/login ")
def teacher_accept(request):
    if request.method=="POST":
        id=request.POST.get('id')
        user=teachermodel.objects.get(id=id)
        user.is_active=True
        user.save()
        return HttpResponse("Accepted")
def student_accept(request):
    if request.method=="POST":
        id=request.POST.get('id')
        user=studentmodel.objects.get(id=id)
        user.is_active=True
        user.save()
        return HttpResponse("Accepted")
def teacher_decline(request):
    if request.method=="POST":
        id=request.POST.get('id')
        user=teachermodel.objects.get(id=id)
        user.delete()       
        return HttpResponse("Accepted")
def student_decline(request):
    if request.method=="POST":
        id=request.POST.get('id')
        user=studentmodel.objects.get(id=id)
        user.delete()
        return HttpResponse("Deleted")



@xframe_options_sameorigin
def threads(request):
    try:
        user=teachermodel.objects.get(empid=request.session["teacher"])
        username = user.empid
    except:
        user = studentmodel.objects.get(stuid=request.session["student"])
        username = user.stuid

    thread = latestmessage.objects.filter(myid=username)
    chatlog = []
    for i in thread:
        try:
            person=teachermodel.objects.get(empid=i.fid)
        except:
            person = studentmodel.objects.get(stuid=i.fid)
        temp = viewthread()
        temp.name = person.name
        temp.photo = person.photo
        temp.chatid = i.chatid
        chatlog.append(temp)
    return render(request,"general/messages.html",{"threads":chatlog})

@xframe_options_sameorigin
def chatroom(request):
    return render(request,"general/chatroom.html")

@xframe_options_sameorigin
def generalsetting(request):
    return render(request,"general/generalsetting.html")

@xframe_options_sameorigin
def contactsetting(request):
    return render(request,"general/contactsetting.html")

@xframe_options_sameorigin
def securitysetting(request):
    return render(request,"general/securitysetting.html")

@xframe_options_sameorigin
def setting(request):
    return render(request,"general/setting.html")

@xframe_options_sameorigin
def contacts(request):
    try:
        user = teachermodel.objects.get(empid=request.session['teacher'])
    except:
        user = studentmodel.objects.get(stuid=request.session['student'])
    teachers = teachermodel.objects.filter(admin_id=user.admin_id)
    students = studentmodel.objects.filter(admin_id=user.admin_id)
    return render(request,"general/contacts.html",{"teachers":teachers,"students":students})

def editprofile(request):
    if request.method=="POST":
        email = request.POST["email"]
        phone = request.POST["phone"]
        about = request.POST["bio"]
        dob=request.POST["dob"]
        if(dob=="" or dob=="none"):
            dob="none"
        print("dob",dob)
        websiteurl = request.POST["website"]
        fblink = request.POST["fb"]
        if(fblink!=""):
                fblink = "https://www.facebook.com/"+fblink
        githublink = request.POST["github"]
        if(githublink!=""):
                githublink = "https://www.github.com/"+githublink
        linkedinlink = request.POST["linkedin"]
        if(linkedinlink!=""):
                linkedinlink = "https://www.linkedin.com/"+linkedinlink
        instalink = request.POST["insta"]
        if(instalink!=""):
                instalink = "https://www.instagram.com/"+instalink
        try:
            user=teachermodel.objects.get(empid=request.session["teacher"])
            details=teacherdetails.objects.get(admin_id=user.id)
            user.email = email
            user.phone = phone
            details.about = about
            if(dob!="none"):
                details.dob=dob
            details.websiteurl = websiteurl
            details.fblink = fblink
            details.githublink=githublink
            details.linkedinlink=linkedinlink
            details.instalink=instalink
        except:
            user = studentmodel.objects.get(stuid=request.session["student"])
            details=studentdetails.objects.get(admin_id=user.id)
            user.email = email
            user.phone = phone
            details.about = about
            if(dob!="none"):
                details.dob=dob
            details.websiteurl = websiteurl
            details.fblink = fblink
            details.githublink=githublink
            details.linkedinlink=linkedinlink
            details.instalink=instalink
        user.save()
        details.save()
        return redirect("profile")

def editcover(request):
    if(request.session.has_key('logged') and request.session['logged']==True):
        image=request.FILES["file"]
        try:
            user=teachermodel.objects.get(empid=request.session["teacher"])
            temp = "media/teacher/"+request.session["teacher"]+"cover"+".jpg"
            print(temp)
            try:
                os.remove(temp)
            except:
                pass
            image.name = request.session["teacher"]+"cover"+".jpg"
            print("image name",image.name)
        except:
            user = studentmodel.objects.get(stuid=request.session["student"])
            temp = "media/student/"+request.session["student"]+"cover"+".jpg"
            try:
                os.remove(temp)
            except:
                pass
            image.name = request.session["student"]+"cover"+".jpg"
        user.coverphoto=image
        user.save()
        return redirect("/profile")
    else:
        return redirect("/login")

def editdp(request):
    if(request.session.has_key('logged') and request.session['logged']==True):
        image=request.FILES["file"]
        try:
            user=teachermodel.objects.get(empid=request.session["teacher"])
            temp = "media/teacher/"+user.empid+"dp"+".jpg"
            try:
                os.remove(temp)
            except:
                pass
            image.name = user.empid+"dp"+".jpg"
        except:
            user = studentmodel.objects.get(stuid=request.session["student"])
            temp = "media/student/"+user.stuid+"dp"+".jpg"
            try:
                os.remove(temp)
            except:
                pass
            image.name = user.stuid+"dp"+".jpg"
        user.photo=image
        user.save()
        return redirect("profile")
    else:
        return redirect("/login")
        
@xframe_options_sameorigin
def post(request):
      if(request.session.has_key("logged") and request.session["logged"]==True):
        fmt = "%d-%m-%Y %H:%M"
        zone = 'Asia/Kolkata'
        now_time = datetime.now(timezone(zone))
        time = now_time.strftime(fmt)
        print(time)
        try:
            user=teachermodel.objects.get(empid=request.session["teacher"])
            try:
                desc=request.POST.get('desc')
            except:
                desc="."
            try:
                link=request.POST.get('link')
            except:
                link="#"
            try:
                base64_string = request.POST["outputimg"]
                image = request.FILES["file"]
                data = ContentFile(base64.b64decode(base64_string), name=image.name)
                r=upload_posts.objects.create(desc=desc,image=data,link=link,admin=user.admin,name=user.name,username=user.empid,profilelink="T/"+str(user.id),photolink=user.photo,designation=1,time=time)
            except:
                r=upload_posts.objects.create(desc=desc,link=link,admin=user.admin,name=user.name,username=user.empid,profilelink="T/"+str(user.id),photolink=user.photo,designation=1,time=time)
        except:
            user = studentmodel.objects.get(stuid=request.session["student"])
            try:
                desc=request.POST.get('desc')
                print(desc)
            except:
                desc="."
            try:
                link=request.POST.get('link')
            except:
                link="#"
            try:
                base64_string = request.POST["outputimg"]
                image = request.FILES["file"]
                data = ContentFile(base64.b64decode(base64_string), name=image.name)
                r=upload_posts.objects.create(time=time,desc=desc,image=data,link=link,admin=user.admin,name=user.name,username=user.stuid,profilelink="S/"+str(user.id),photolink=user.photo,designation=0)    
            except:
                r=upload_posts.objects.create(time=time,desc=desc,link=link,admin=user.admin,name=user.name,username=user.stuid,profilelink="S/"+str(user.id),photolink=user.photo,designation=0)
        return redirect("/home")

def achievements(request):
    if(request.session.has_key("logged") and request.session["logged"]==True):
        try:
            u=teachermodel.objects.get(empid=request.session["teacher"])
            desc=request.POST.get('desc')
            name=request.POST.get('name')
            try:
                link=request.POST.get('link')
            except:
                link="#"
            photo=request.FILES['cert']
            upload_achievements_emp.objects.create(user=u,desc=desc,name=name,link=link,image=photo)
            return redirect('/home')
        except:
            u=studentmodel.objects.get(stuid=request.session["student"])
            desc=request.POST.get('desc')
            name=request.POST.get('name')
            try:
                link=request.POST.get('link')
            except:
                link="#"
            photo=request.FILES['cert']
            upload_achievements.objects.create(user=u,desc=desc,name=name,link=link,image=photo)
            return redirect('/home')



def deleteachievements(request,id):
    if(request.session.has_key("logged") and request.session["logged"]==True):
        try:
            u=teachermodel.objects.get(empid=request.session["teacher"])
            r=upload_achievements_emp.objects.get(id=id)
            if r.user==u:
                r.delete()
                return redirect('/home')
            else:
                return HttpResponse("You can't access this request!")
        except:
            u=studentmodel.objects.get(stuid=request.session["student"])
            r=upload_achievements.objects.get(id=id)
            if r.user==u:
                r.delete()
                return redirect('/home')
            else:
                return HttpResponse("You can't access this request!")

def evaluate(a,b):
    l=[]
    l.append(a)
    l.append(b)
    chatid=max(l)+'*$*'+min(l)
    return chatid

@xframe_options_sameorigin
def chat(request,id):
    a,b=id.split('*$*')
    chatid=evaluate(a,b)
    try:
        obj1 = teachermodel.objects.get(empid=b)
    except:
        obj1 = studentmodel.objects.get(stuid=b)
    try:
        obj2 = teachermodel.objects.get(empid=a)
    except:
        obj2 = studentmodel.objects.get(stuid=a)
    try:
        username=request.session["teacher"]
        
    except:
        username=request.session["student"]
    if a==username:
        friend=obj1
        me = obj2
        fname,myname = b,a

    else:
        friend = obj1
        me = obj2
        fname,myname = b,a
    try:
        messages=chat_message.objects.filter(chatid=chatid)
        return render(request,"general/chatroom.html",{"me":me,"friend":friend,'messages':messages,"roomcode":chatid,"fname":fname,"myname":myname})
    except:
        return render(request,"general/chatroom.html",{"me":me,"friend":friend,"roomcode":chatid,"fname":fname,"myname":myname})

def savechat(request):
    desc=request.POST.get('desc')
    sender=request.POST.get('sender')
    reciever=request.POST.get('reciever')
    chatid=request.POST.get('chatid')
    print(chatid,sender,reciever,desc)
    fmt = "%d-%m-%Y %H:%M"
    zone = 'Asia/Kolkata'
    now_time = datetime.now(timezone(zone))
    time = now_time.strftime(fmt)
    messages=chat_message.objects.create(chatid=chatid,desc=desc,sender=sender,reciever=reciever,time=time)
    lastmessage(chatid,sender,reciever)
    return HttpResponse('Send')

def lastmessage(id,sender,reciever):
    try:
        r=latestmessage.objects.get(myid=sender,fid=reciever,chatid=id)
        s=latestmessage.objects.get(myid=reciever,fid=sender,chatid=id)
        r.delete()
        s.delete()
        r=latestmessage.objects.create(myid=sender,fid=reciever,chatid=id,flag=0)
        s=latestmessage.objects.create(myid=reciever,fid=sender,chatid=id,flag=1)
    except:
        r=latestmessage.objects.create(myid=sender,fid=reciever,chatid=id,flag=0)
        s=latestmessage.objects.create(myid=reciever,fid=sender,chatid=id,flag=1)

def profileForOthers(request,id):
    user = studentmodel.objects.get(id=id)
    username = user.stuid
    posts=upload_posts.objects.filter(username=user.stuid ) 
    details = studentdetails.objects.get(admin_id=user.id)
    detail = upload_achievements.objects.filter(user=user)
    try:
        logged=teachermodel.objects.get(empid=request.session["teacher"])
        userid = logged.empid
    except:
        logged=studentmodel.objects.get(stuid=request.session["student"])
        userid = logged.stuid
    return render(request,"general/profileForOthers.html",{"username":username,"userid":userid,'user':user,'posts':posts,"details":details,"logged":logged,"cert":detail})

    # return render(request,"general/profileForOthers.html",{'user':user,'posts':posts,"details":details})
def empprofileForOthers(request,id):
    user = teachermodel.objects.get(id=id)
    username = user.empid
    posts=upload_posts.objects.filter(username=user.empid ) 
    detail = upload_achievements_emp.objects.filter(user=user)
    details = teacherdetails.objects.get(admin_id=user.id)
    try:
        logged=teachermodel.objects.get(empid=request.session["teacher"])
        userid = logged.empid
    except:
        logged=studentmodel.objects.get(stuid=request.session["student"])
        userid = logged.stuid
    return render(request,"general/profileForOthers.html",{"username":username,"userid":userid,'user':user,'posts':posts,"details":details,"logged":logged,"cert":detail})

@xframe_options_sameorigin
def review(request):
      if(request.session.has_key("logged") and request.session["logged"]==True):
        fmt = "%d-%m-%Y %H:%M"
        zone = 'Asia/Kolkata'
        now_time = datetime.now(timezone(zone))
        time = now_time.strftime(fmt)
        print(time)
        user=teachermodel.objects.get(empid=request.session["teacher"])
        review=request.POST.get('review')
        r=upload_review.objects.create(review=review,admin=user.admin,name=user.name,username=user.empid,profilelink="T/"+int(user.id),photolink=user.photo,designation=1,time=time)
        return redirect("/general/profileForOthers")


    
