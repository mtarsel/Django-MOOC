from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from django.views.generic.detail import DetailView

class UserProfileView(DetailView):
    model = User
    slug_field = "username"
    template_name = "dashboard.html"	
