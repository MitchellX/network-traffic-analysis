from django.shortcuts import render,render_to_response,redirect
from dwebsocket.decorators import accept_websocket,require_websocket
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.utils import timezone
from django.utils.timezone import now,timedelta
from frame.models import PluginList
from pygdbmi.gdbcontroller import GdbController
from django.template import Context,Template
from django.urls import reverse
import datetime
import paramiko
import json
import psutil
import frame.views as Frame
import threading

# Create your views here.
global gdbmi

@accept_websocket
def echo_once(request):
#系统运行函数
    if not request.is_websocket():  #判断是不是websocket连接
        try: #普通的http方法的话
            message=request.GET['messsage']
            return HttpResponse(message)
        except:
            return render(request,'plugin_exec.html')
    else:
        for message in request.websocket:
            message=message.decode('utf-8') #接受前段的数据
            if message=='backup_all':
                command='cd /home/chenmanjing/desktop/Prog_cmj && echo "19970930" | sudo ./start'
                #command='uptime'

                #远程连接服务器
                hostname='192.168.238.187'
                username='root'
                password='19970930'

                ssh=paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname=hostname,username=username,password=password)

                #加上get_pty=True 执行命令才有权限

                stdin,stdout,stderr=ssh.exec_command(command,get_pty=True)
                #循环发送消息给前段页面

                while True:
                    nextline=stdout.readline().strip()  #读取脚本输出内容
                    print(nextline)
                    request.websocket.send(nextline) #发送消息到客户端
                    if not nextline:
                        break

                ssh.close()

                #利用runtimelog判断是否运行成功
                time_now=datetime.datetime.now()+datetime.timedelta(seconds=-3)

                content = time_now.strftime("%b %d %H:%M:%S %Y")
                date = now().date() + timedelta(days=0)
                DateName=date.strftime("%Y-%m-%d")

                log_out_str = "/home/chenmanjing/desktop/Prog_cmj/log/runtimelog."+DateName
                log_content = open(log_out_str, "r")

                s = log_content.read()
                result = s.count(content+',  FATAL, plugin, ./ctplugin/ct_control_plug/ct_control.so init error,don\'t load it')
                if result>0:
                    state='success'
                else:
                    state='danger'


                cpu_per=psutil.cpu_percent(1)
                # print(cpu_per)
                mem=psutil.virtual_memory()
                mem_per=mem.percent
                # print(mem_per)

                print('return')
                res = {
                    'state': state,
                    'host': hostname,
                    'cpu_per': cpu_per,
                    'mem_per': mem_per,
                    'tag': 1
                }
                res2str = json.dumps(res, ensure_ascii=False)
                request.websocket.send('finalres_' + res2str)
            else:
                request.websocket.send('没有权限！'.encode('utf-8'))




def haha(request):
    global gdbmi
    gdbmi=GdbController()
    return render_to_response('dashboard.html')

@accept_websocket
def gdb_command(request):
#gdb调试函数
    if not request.is_websocket():  #判断是不是websocket连接
        try: #普通的http方法的话
            message=request.GET['messsage']
            return HttpResponse(message)
        except:
            return render(request,'dashboard.html')
    else:
        for message in request.websocket:
            message=message.decode(encoding='utf-8') #接受前段的数据
            if message=='quit':
                result=gdbmi.exit()
            else:
                result = gdbmi.write(message)

            print(json.dumps(result,ensure_ascii=False,indent=4))

            if result==None:
                request.websocket.send("QUIT\n")
            else:
                for item in result:
                    if type(item["payload"])==dict:
                        continue
                    if item["payload"]==None:
                        request.websocket.send("None\n")
                        continue
                    request.websocket.send(item["payload"])
        return render_to_response('dashboard.html')



@accept_websocket
def feature_test_wrong(request):
    if not request.is_websocket():  #判断是不是websocket连接
        try: #普通的http方法的话
            message=request.GET['messsage']
            return HttpResponse(message)
        except:
            return render(request,'plugin_exec.html')
    else:
        for message in request.websocket:
            message=message.decode('utf-8') #接受前段的数据
            if message=='backup_all':
#                command='cd /home/chenmanjing/desktop/Prog_cmj && echo "19970930" | sudo ./start'
                command = 'python /home/mingcanxiang/pyCode/cmj_dj/test.py'
                #command='uptime'

                #远程连接服务器
                hostname='192.168.1.192'
                username='root'
                password='ww7727055'

                ssh=paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname=hostname,username=username,password=password)

                #加上get_pty=True 执行命令才有权限
                stdin,stdout,stderr=ssh.exec_command(command,get_pty=True)

                #循环发送消息给前段页面

                while True:
                    nextline=stdout.readline().strip()  #读取脚本输出内容
                    print(nextline)
                    request.websocket.send(nextline) #发送消息到客户端
                    if not nextline:
                        break

                ssh.close()

                #利用runtimelog判断是否运行成功
                time_now=datetime.datetime.now()+datetime.timedelta(seconds=-3)

                content = time_now.strftime("%b %d %H:%M:%S %Y")
                date = now().date() + timedelta(days=0)
                DateName=date.strftime("%Y-%m-%d")

                log_out_str = "/home/chenmanjing/desktop/Prog_cmj/log/runtimelog."+DateName
                log_content = open(log_out_str, "r")

                s = log_content.read()
                result = s.count(content+',  FATAL, plugin, ./ctplugin/ct_control_plug/ct_control.so init error,don\'t load it')
                if result>0:
                    state='success'
                else:
                    state='danger'


                cpu_per=psutil.cpu_percent(1)
                # print(cpu_per)
                mem=psutil.virtual_memory()
                mem_per=mem.percent
                # print(mem_per)

                print('return')
                res = {
                    'state': state,
                    'host': hostname,
                    'cpu_per': cpu_per,
                    'mem_per': mem_per,
                    'tag': 1
                }
                res2str = json.dumps(res, ensure_ascii=False)
                request.websocket.send('finalres_' + res2str)
            else:
                request.websocket.send('没有权限！'.encode('utf-8'))
    return



@accept_websocket
def feature_test(request):
# if not request.is_websocket():  # 判断是不是websocket连接
#     try:  # 普通的http方法的话
#         print('no')
#         message = request.GET['messsage']
#         return HttpResponse(message)
#     except:
#         return render(request, 'plugin_exec.html')
# else:
   #     command0 = "conda activate"
        command = "/home/mingcanxiang/anaconda3/bin/python /home/mingcanxiang/pyCode/code_intern/test_getdata.py"
        # 前面的一行要根据自己的python环境，手动切换到。

        print('h1')

        # 远程连接服务器
        hostname = '192.168.123.78'
        username = 'mingcanxiang'
        password = 'ww7727055'

        print('h2')
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username=username, password=password)
        print('h3')

        # 务必要加上get_pty=True,否则执行命令会没有权限
 #       ssh.exec_command(command0, get_pty=True)
        print('h33')
        ssh.exec_command(command, get_pty=True)

#        request.websocket.send('ok')

    #    stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)
        print('h4')


        return render(request,'upload.html')



@accept_websocket
def plugin_test(request):
#插件测试函数

    log_name=request.GET['plugin_name']



    command = 'cd /home/chenmanjing/desktop/Prog_cmj && echo "19970930" | sudo ./start'  # 这里是要执行的命令或者脚本

    # 远程连接服务器
    hostname = '192.168.238.176'
    username = 'root'
    password = '19970930'

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostname, username=username, password=password)
    # 务必要加上get_pty=True,否则执行命令会没有权限
    stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)

    result = stdout.read().decode(encoding='utf-8')

    log_name=log_name.split('.')[0]
    fout = open('./log/log_%s'%log_name, 'w', encoding='utf8')

    # 写入文件内容
    fout.write(result)
    fout.close()


    ssh.close()  # 关闭ssh连接

    # time_now = datetime.datetime.now() + datetime.timedelta(seconds=-2)
    #
    # content = time_now.strftime("%b %d %H:%M:%S %Y")
    # print(content)

    date = now().date() + timedelta(days=0)
    DateName = date.strftime("%Y-%m-%d")

    log_out_str = "/home/chenmanjing/desktop/Prog_cmj/log/runtimelog." + DateName
    with open(log_out_str,"r") as f:
        txt = f.readlines()
    keys = [k for k in range(0, len(txt))]
    result = {k: v for k, v in zip(keys, txt[::-1])}
    state=''
    if result[1] == 'Tue Apr 2 10:32:04 2019, FATAL, plugin, load ct_control success!':
        PluginList.objects.filter(plugin_info='udp2290').update(plugin_state='success')
        state='success'
    else:
        PluginList.objects.filter(plugin_info='udp2290').update(plugin_state='danger')
        state='fail'

    plugin_list=PluginList.objects.all()
    #return render(request, 'plugin_exec.html',{'plugin_list':plugin_list})
    print("done")

    # return redirect('/plugin_exec/')


    return HttpResponse(state)




