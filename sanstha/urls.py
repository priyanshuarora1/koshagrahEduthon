from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
	path("",views.login,name="login"),
	path("login",views.adminlogin,name="login"),
    path("logout",views.adminlogout,name="logout"),
	path("dashboard",views.dashboard,name="dashboard"),
	path("pending",views.pending,name="pending"),
    path("adminregister",views.adminregister,name="adminregister"),
	path("search",views.searchbar,name="searchbar"),
	path("emp/search",views.empsearchbar,name="empsearchbar"),
	path("status/<str:id>",views.status,name="status"),
	path("empdelete/<str:id>",views.empdelete,name="empdelete"),
	path("feed",views.posts,name="allpost"),
	path("delete",views.delpost,name="deletepost"),

]
