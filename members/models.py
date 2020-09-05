from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone
import os

def path_rename(instance, filename):
    upload_to = 'teacher'
    ext = "jpg"
    if instance.pk:
        filename = '{}.{}'.format(instance.empid, ext)
    else:
        filename = '{}.{}'.format(uuid4().hex, ext)
    return os.path.join(upload_to, filename)


class teachermodel(models.Model):
    admin=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(null=False,max_length=100)
    email=models.EmailField(null=False,max_length=50)
    empid=models.CharField(null=False,max_length=100,unique=True)
    password=models.CharField(null=False,max_length=100)
    phone=models.IntegerField(null=False)
    is_active=models.BooleanField(default=False)
    photo = models.ImageField(upload_to=path_rename, max_length=255, default='teacher/default.jpg')
    coverphoto = models.ImageField(upload_to=path_rename,default='teacher/coverphoto.jpg')


def path_rename_student(instance, filename):
    upload_to = 'student'
    ext = "jpg"
    if instance.pk:
        filename = '{}.{}'.format(instance.stuid, ext)
    else:
        filename = '{}.{}'.format(uuid4().hex, ext)
    return os.path.join(upload_to, filename)

class studentmodel(models.Model):
    admin=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(null=False,max_length=100)
    email=models.EmailField(null=False,max_length=50)
    stuid=models.CharField(null=False,max_length=100,unique=True)
    password=models.CharField(null=False,max_length=100)
    phone=models.IntegerField(null=False)
    is_active=models.BooleanField(default=False)
    photo = models.ImageField(upload_to=path_rename_student, max_length=255, default='student/default.jpg')
    coverphoto = models.ImageField(upload_to=path_rename_student,default='student/coverphoto.jpg')


class teacherdetails(models.Model):
    admin=models.OneToOneField(teachermodel,on_delete=models.CASCADE)
    about=models.CharField(null=False,max_length=500,default="Hello! I am a Teacher.")
    dob=models.DateField(null=True)
    websiteurl=models.CharField(null=True,max_length=200)
    fblink=models.CharField(null=True,max_length=200)
    githublink=models.CharField(null=True,max_length=200)
    linkedinlink=models.CharField(null=True,max_length=200)
    instalink=models.CharField(null=True,max_length=200)

class studentdetails(models.Model):
    admin=models.OneToOneField(studentmodel,on_delete=models.CASCADE)
    about=models.CharField(null=False,max_length=500,default="Hello! I am a student.")
    dob=models.DateField(null=True)
    websiteurl=models.CharField(null=True,max_length=200)
    fblink=models.CharField(null=True,max_length=200)
    githublink=models.CharField(null=True,max_length=200)
    linkedinlink=models.CharField(null=True,max_length=200)
    instalink=models.CharField(null=True,max_length=200)

class upload_posts(models.Model):
    admin=models.ForeignKey(User,on_delete=models.CASCADE)
    username=models.CharField(null=False,max_length=100)
    photolink=models.CharField(null=False,max_length=100,default='student/default.jpg')
    profilelink=models.CharField(null=False,max_length=100)
    designation=models.BooleanField()
    name=models.CharField(null=True,max_length=100)
    desc=models.TextField()
    time = models.CharField(max_length=200,null=True)
    link=models.URLField(null=True,max_length=200)
    image=models.ImageField(upload_to='post/images',null=True)

class upload_achievements(models.Model):
    user=models.ForeignKey(studentmodel,on_delete=models.CASCADE)
    name=models.CharField(null=True,max_length=100)
    desc=models.CharField(null=False,max_length=200)
    link=models.URLField(null=True,max_length=200)
    image=models.ImageField(upload_to='achievements/student',null=True)
class upload_achievements_emp(models.Model):
    user=models.ForeignKey(teachermodel,on_delete=models.CASCADE)
    name=models.CharField(null=True,max_length=100)
    desc=models.CharField(null=False,max_length=200)
    link=models.URLField(null=True,max_length=200)
    image=models.ImageField(upload_to='achievements/student',null=True)
class chat_message(models.Model):
    chatid=models.CharField(null=False,max_length=200)
    desc=models.TextField()
    sender=models.CharField(null=False,max_length=100)
    reciever=models.CharField(null=False,max_length=200)
    time = models.CharField(max_length=200,null=True)
class latestmessage(models.Model):
    chatid=models.CharField(null=False,max_length=200)
    myid=models.CharField(null=False,max_length=100)
    fid=models.CharField(null=False,max_length=200)
    flag=models.BooleanField()

class viewthread:
    pic:str
    name:str
    chatroom:str
    
class upload_reviews(models.Model):
    stuid=models.CharField(null=False,max_length=100)
    empphoto=models.CharField(null=False,max_length=100)
    emplink=models.CharField(null=False,max_length=100)
    empname=models.CharField(null=True,max_length=100)
    review=models.TextField()
    time = models.CharField(max_length=200,null=True)