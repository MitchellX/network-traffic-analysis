from django.db import models
import datetime
from datetime import date

# Create your models here.

class PluginList(models.Model):
    id=models.AutoField(primary_key=True)
    plugin_no=models.IntegerField()   #插件返回的ID
    plugin_info=models.TextField() #插件功能描述
    plugin_name=models.CharField(max_length=255)  #插件名
    plugin_state=models.CharField(max_length=255)  #是否已上线 1-上线 0-没上线 如果操作是加入 则就是上线了
    color=models.IntegerField(null=True)   #颜色
    exec_time=models.DateTimeField(null=True)  #上线的时间(取最后一次加入操作的时间)
    oper_type=models.IntegerField(null=True)  #操作类型-1 加入 2 删除
