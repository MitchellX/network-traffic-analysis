from django.shortcuts import render,HttpResponseRedirect,redirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate,login,logout

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

import os
import subprocess

# Create your views here.

@csrf_exempt
def login_in(request):
    err_msg=''
    if request.method=='POST':
        username = request.POST.get('username',None)
        password = request.POST.get('password',None)
#        user=authenticate(username=username,password=password)

#        if user is not None and user.is_active:
#
#           login(request,user)
        if username == 'admin' and password == 'admin' :
            return render(request,'home.html')

        else:
            err_msg='登陆失败'
            messages.add_message(request,messages.ERROR,'请输入正确的用户名密码')

    elif request.method=='GET':
        return render(request,'login.html',{err_msg:err_msg})

def page_not_found(request):
    return render(request,'404.html')


