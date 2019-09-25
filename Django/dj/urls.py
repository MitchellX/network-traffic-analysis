"""dj URL configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
#from django.urls import path
from django.conf.urls import url
from login import views as login
from frame import views as frame
from websocket import views as websocket
from log import views as log


urlpatterns = [
    url(r'^admin/',admin.site.urls),
    url(r'^login/',login.login_in),
    url(r'^$', login.login_in),             # 访问主页，跳到登录页面
    url(r'^dashboard/',frame.show_all),
    url(r'^my_tools/',frame.my_tools),
    url(r'^echo_once/',websocket.echo_once),
    url(r'^index/',websocket.echo_once),
    url(r'^my_task/',frame.my_task),
    url(r'^show_alarm/',frame.show_alarm), #流量捕获
    url(r'^my_scheduler/',frame.my_scheduler),
    url(r'^plugin_exec/$',frame.plugin_exec),
    url(r'^plugin_ctl/',frame.plugin_ctl),
    url(r'^sys_setting/',frame.sys_setting),
    url(r'^plugin_test/',websocket.plugin_test),
    url(r'^plugin_exelog$',frame.plugin_exelog),
    url(r'^gdb_command',websocket.gdb_command),
    url(r'^haha/',websocket.haha),
    url(r'^show_all/',frame.show_all),
    url(r'^log/',log.log),
    url(r'^getlog/',log.getlog),
    url(r'^home/',frame.home),
    url(r'^show_xx/$', log.show_image),

    url(r'^upload/$', frame.upload_file),
    url(r'^feature_test/$', websocket.feature_test),
    url(r'^show_image/$',frame.show_image),

]