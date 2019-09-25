from django.shortcuts import render
from frame.models import PluginList

# Create your views here.
import os
import json

from django.shortcuts import render,render_to_response
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.contrib import messages
from django.utils import timezone

import datetime
#from frame import tools
# 配置文件
import configparser
import base64
import frame.models as models_frame
import time
import paramiko

import subprocess

def upload(request):
    return render(request,'upload.html')

def show_image(request):
    return render(request,'show_image.html')

def upload_file(request):
    # 请求方法为POST时，进行处理
    if request.method == "POST":
        # 获取上传的文件，如果没有文件，则默认为None
        File = request.FILES.get("myfile", None)
        if File is None:
            return HttpResponse("没有需要上传的文件")
        else:
            # 打开特定的文件进行二进制的写操作
            # print(os.path.exists('/temp_file/'))
#            with open("./test01app/temp_file/%s" % File.name, 'wb+') as f:
            with open("/home/mingcanxiang/pyCode/code_intern/temp_file/uploaded_file.json", 'wb+') as f:
                # 分块写入文件
                for chunk in File.chunks():
                    f.write(chunk)
            return HttpResponse("UPload over!")
    else:
        # 不用加其他前缀路径，直接就能检索到 templates 下的
        return render(request, "upload.html")


# @login_required(login_url='/login')
def show_all(request):
    return render_to_response('dashboard.html')

# @login_required(login_url='/login')
def my_tools(request):
    return render_to_response('my_tools.html')

# @login_required(login_url='/login')
def my_task(request):
    return render(request,'my_task.html')

# @login_required(login_url='/login')
def show_alarm(request):
    return render_to_response('show_alarm.html')

# @login_required(login_url='/login')
def my_scheduler(request):
    return render_to_response('my_scheduler.html')

# @login_required(login_url='/login')
def plugin_exec(request):
    if request.method=='POST':
        # 获取上传的文件，如果没有则默认为NONE
        File=request.FILES.get("myfile",None)
        type=request.POST.get("plugin_type")


        if File is None:
            return HttpResponse("没有选择文件")
        else:
            # 打开特定的文件进行二进制的写操作
            with open("/home/chenmanjing/desktop/Prog_cmj/ctplugin/%s_ct_plugin/%s"%(type,File.name),'wb+') as f:
                # 分块写入文件
                for chunk in File.chunks():
                    f.write(chunk)

        plugin = PluginList(plugin_no=1, plugin_info='udp2290', plugin_name=File.name)
        plugin.save()

    plugin_list=PluginList.objects.all()


    return render(request,'plugin_exec.html',{'plugin_list':plugin_list})


@login_required(login_url='/login')
def plugin_ctl(request):
    return render(request,'plugin_ctl.html')

@login_required(login_url='/login')
def sys_setting(request):
    host='192.168.238.145'
    port='22'
    user='root'
    password_mysql='12345678'
    dbname='mesa'
    now='2019.03'
    password_email='12345678'
    username='admin'
    reciever='milleryo@126.com'
    msg_form='DB_MONITOR<milleryo@126.com>'
    check_sleep_time='100'
    alarm_sleep_time='500'
    next_send_email_time='50'
    return render_to_response('sys_setting.html',{'username':username,'password_email':password_email,'reciever':reciever,'msg_form':msg_form,'check_sleep_time':check_sleep_time,'alarm_sleep_time':alarm_sleep_time,'next_send_email_time':next_send_email_time,'host':host,'port':port,'user':user,'password_mysql':password_mysql,'dbname':dbname,'now':now})

# @login_required(login_url='/login')
def plugin_exelog(request):
    log_name=request.GET.get('log_name')
    log_name = log_name.split('.')[0]
    # 打开文件
    fo = open('/home/chenmanjing/PycharmProjects/dj/log/log_%s'%log_name, 'r')
    # 保存变量
    list = fo.readlines()
    # 返回list列表，传递给前端
    return render(request, 'plugin_exelog.html', {'alist': list,'log_name':log_name})

# @login_required(login_url='/login')
def home(request):
    return render(request,'home.html')

# home页面点击执行系统启动
def system_on(request):
    command = 'cd /home/chenmanjing/desktop/Prog_cmj && echo "19970930" | sudo ./start'
    # command='uptime'

    # 远程连接服务器
    hostname = '192.168.238.187'
    username = 'root'
    password = '19970930'

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostname, username=username, password=password)

    # 加上get_pty=True 执行命令才有权限

    stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)
    # 循环发送消息给前段页面

    ssh.close()

    # 利用runtimelog判断是否运行成功
    time_now = datetime.datetime.now() + datetime.timedelta(seconds=-3)

    content = time_now.strftime("%b %d %H:%M:%S %Y")
    date = now().date() + timedelta(days=0)
    DateName = date.strftime("%Y-%m-%d")

    log_out_str = "/home/chenmanjing/desktop/Prog_cmj/log/runtimelog." + DateName
    log_content = open(log_out_str, "r")

    s = log_content.read()
    result = s.count(content + ',  FATAL, plugin, ./ctplugin/ct_control_plug/ct_control.so init error,don\'t load it')
    if result > 0:
        state = 'success'
    else:
        state = 'danger'





