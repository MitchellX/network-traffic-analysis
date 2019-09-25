from django.shortcuts import render

from django.contrib.auth import logout
from django.shortcuts import render_to_response
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json
import time
import paramiko


# Create your views here.

# @login_required(login_url='/login/')
def log(request):
    return render_to_response('log.html')

def show_image(request):
    return render_to_response("show_image.html")

def show_feature(request):
    return render_to_response("show_feature.html")

def getlog(request):
    hostname = '192.168.238.175'
    username = 'root'
    password = '19970930'

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostname, username=username, password=password)

    command='tail -f /home/chenmanjing/desktop/Prog_cmj/log/runtimelog.2019-04-17'

    # 加上get_pty=True 执行命令才有权限
    stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)
    # 循环发送消息给前段页面

    while True:
        nextline = stdout.readline().strip()  # 读取脚本输出内容
        print(nextline)
        if not nextline:
            break

    return render_to_response('log.html')

def log_http(request):
    return render(request,'log_http.html')

def log_tcp(request):
    return render(request,'log_tcp.html')

def log_udp(request):
    return render(request,'log_udp.html')

def log_ip(request):
    return render(request,'log_ip.html')
