import cx_Oracle
import datetime,time
import configparser
import os
import paramiko
import uuid

def now():
    return str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))
