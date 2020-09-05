from django.db import models
from django.contrib.auth.models import User
import os
# Create your models here.

def path_rename(instance, filename):
    upload_to = 'admin'
    ext = "jpg"
    if instance.pk:
        filename = '{}.{}'.format(instance.adminid, ext)
    else:
        filename = '{}.{}'.format(uuid4().hex, ext)
    return os.path.join(upload_to, filename)


class admindetails(models.Model):
    adminid=models.OneToOneField(User, on_delete=models.CASCADE)
    pic=models.ImageField(upload_to=path_rename, max_length=255, default='admin/default.jpg')
    phone=models.IntegerField(null=False)
