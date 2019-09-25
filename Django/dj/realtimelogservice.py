#!/usr/bin/python
# coding: utf-8
import struct
import base64
import hashlib
import socket
import threading
import re
import sys,importlib
import json
import paramiko
import traceback

importlib.reload(sys)

connectionlist = {}  # 存放链接客户fd,元组
g_code_length = 0
g_header_length = 0  # websocket数据头部长度
PRINT_FLAG = True

def get_datalength(msg):
    global g_code_length
    global g_header_length
    g_code_length = msg[1] & 127
    if g_code_length == 126:
        g_code_length = struct.unpack('>H', msg[2:4])[0]
        g_header_length = 8
    elif g_code_length == 127:
        g_code_length = struct.unpack('>Q', msg[2:10])[0]
        g_header_length = 14
    else:
        g_header_length = 6
    g_code_length = int(g_code_length)
    return g_code_length

# 服务器解析浏览器发送的信息
def recv_data(conn):
    try:
        all_data = conn.recv(1024)
        print('msg len', len(all_data))
        if not len(all_data):
            return False
    except:
        pass
    else:
        #all_data=all_data.decode(encoding='unicode_escape')

        code_len = all_data[1] & 127
        print(code_len)
        if code_len == 126:
            print('126')
            masks = all_data[4:8]
            data = all_data[8:]
        elif code_len == 127:
            print('127')
            masks = all_data[10:14]
            data = all_data[14:]
        else:
            print('else')
            masks = all_data[2:6]
            data = all_data[6:]
        raw_str = ""
        i = 0
        for d in data:
            raw_str += chr(d ^ masks[i % 4])
            i += 1
        print(raw_str)
        return raw_str


# 服务器处理发送给浏览器的信息
def send_data(conn, data):
    # print('send_data')
    # if data:
    #     data = str(data)
    # else:
    #     return False
    # token = b"\x81"
    # length = len(data)
    # print(length)
    # if length < 126:
    #     token += struct.pack("B", length)
    # elif length <= 0xFFFF:
    #     token += struct.pack("!BH", 126, length)
    # else:
    #     token += struct.pack("!BQ", 127, length)
    # # struct为Python中处理二进制数的模块，二进制流为C，或网络流的形式。
    # print(token)
    # data = '%s%s' % (token, data)
    # print('data:')
    # print(data)
    # data=data.encode('utf-8')
    # #conn.send(data.encode(encoding='utf-8'))
    # conn.send(data)
    # return True
    send_msg = b""  # 使用bytes格式,避免后面拼接的时候出现异常
    send_msg += b"\x81"
    back_str = []
    back_str.append('\x81')
    data_length = len(data.encode())  # 可能有中文内容传入，因此计算长度的时候需要转为bytes信息
    if PRINT_FLAG:
        print("INFO: send message is %s and len is %d" % (data, len(data.encode('utf-8'))))
    # 数据长度的三种情况
    if data_length <= 125:  # 当消息内容长度小于等于125时，数据帧的第二个字节0xxxxxxx 低7位直接标示消息内容的长度
        send_msg += str.encode(chr(data_length))
    elif data_length <= 65535:  # 当消息内容长度需要两个字节来表示时,此字节低7位取值为126,由后两个字节标示信息内容的长度
        send_msg += struct.pack('b', 126)
        send_msg += struct.pack('>h', data_length)
    elif data_length <= (2 ^ 64 - 1):  # 当消息内容长度需要把个字节来表示时,此字节低7位取值为127,由后8个字节标示信息内容的长度
        send_msg += struct.pack('b', 127)
        send_msg += struct.pack('>q', data_length)
    else:
        print(u'太长了')
    send_message = send_msg + data.encode('utf-8')

    if send_message != None and len(send_message) > 0:
        print(send_message)
        conn.send(send_message)


# 握手
def handshake(conn, address, thread_name):
    print('handshake')
    headers = {}
    shake = conn.recv(1024)
    print("from client")
    if not len(shake):
        return False

    print ('%s : Socket start handshaken with %s:%s' % (thread_name, address[0], address[1]))

    #shake = shake.decode(encoding='utf-8')
    header, data = shake.split(b'\r\n\r\n', 1)
    for line in header.split(b'\r\n')[1:]:
        key, value = line.split(b': ', 1)
        key=key.decode(encoding='utf-8')
        headers[key] = value.decode(encoding='utf-8')

    if 'Sec-WebSocket-Key' not in headers:
        print ('%s : This socket is not websocket, client close.' % thread_name)
        conn.close()
        return False

    MAGIC_STRING = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
    HANDSHAKE_STRING = "HTTP/1.1 101 Switching Protocols\r\n" \
                       "Upgrade:WebSocket\r\n" \
                       "Connection: Upgrade\r\n" \
                       "Sec-WebSocket-Accept: {1}\r\n" \
                       "WebSocket-Location: ws://{2}/chat\r\n" \
                       "WebSocket-Protocol:chat\r\n\r\n"

    sec_key = headers['Sec-WebSocket-Key']
    res_key = base64.b64encode(hashlib.sha1(sec_key.encode(encoding='utf-8') + MAGIC_STRING.encode(encoding='utf-8')).digest())
    str_handshake = HANDSHAKE_STRING.replace('{1}', res_key.decode(encoding='utf-8')).replace('{2}', headers['Origin']).replace('{3}',
                                                                                                       headers['Host'])

    print(str_handshake) #看看发过去的是什么消息
    conn.send(str_handshake.encode(encoding='utf-8'))
    print ('%s : Socket handshaken with %s:%s success' % (thread_name, address[0], address[1]))
    print('Start transmitting data...')
    print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -')
    return True


def getlog(conn, address, thread_name):
    print('getlog')
    handshake(conn, address, thread_name)  # 先进行握手连接
    server_name = recv_data(conn)  # 获得浏览器发来的信息 第一次是获得客户端传来的名字
    print('connect to ' + str(server_name))
    conn.setblocking(0)  # 设置socket为非阻塞

    hostname = '192.168.123.78'
    username = 'mingcanxiang'
    password = 'ww7727055'

    ssh = paramiko.SSHClient()

    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostname, username=username, password=password)

    # open channel pipeline
    transport = ssh.get_transport()
    channel = transport.open_session()
    channel.get_pty()

    print('test')

    # 执行命令
    command = 'tail -f /home/mingcanxiang/pyCode/cmj_dj/log.txt'


    # out command into pipeline
    channel.exec_command(command)

    while True:
        try:
            clientdata = recv_data(conn)
            if clientdata is not None and 'quit' in clientdata:  #客户端传来的一直都是空
                print('Not None %s : Socket close with %s:%s' % (thread_name, address[0], address[1]))
                send_data(conn, json.dumps('Bye'))
                ssh.close()
                channel.close()
                conn.close()
                break

            # 如果数据已经缓冲并准备从此通道读取，则返回true。如果返回的是false，也不一定代表通道关闭，可能需要等到更多的数据到来
            while channel.recv_ready():
                print('helloxmc')
                recvfromssh = channel.recv(16371)#传来的byte类型

                #b'[2019-04-21 12:04:19][Error],{this is content}\r\n
                # [2019-04-21 12:04:21][Error],{this is content}\r\n
                # [2019-04-21 12:04:23][Error],{this is content}\r\n
                # [2019-04-21 12:04:25][Error],{this is content}\r\n
                # [2019-04-21 12:04:27][Error],{this is content}\r\n
                # [2019-04-21 12:04:29][Error],{this is content}\r\n
                # [2019-04-21 12:04:31][Error],{this is content}\r\n
                # [2019-04-21 12:04:33][Error],{this is content}\r\n
                # [2019-04-21 12:04:35][Error],{this is content}\r\n
                # [2019-04-21 12:04:37][Error],{this is content}\r\n'

                # 这一段正则表达式是用来提取日志的时间、名字和内容
                print('h1')
                log = re.findall("\[(.*?)\]\[(.*?)\]\[(.*?)\]\[(.*?)\],({.*})", recvfromssh.decode(encoding='utf-8'))#传来的是字典类型
                print('h2')
                #[('2019-04-21 12:04:19', 'Error', '{this is content}'),
                # ('2019-04-21 12:04:21', 'Error', '{this is content}'),
                 #('2019-04-21 12:04:23', 'Error', '{this is content}'),
                 #('2019-04-21 12:04:25', 'Error', '{this is content}'),
                 #('2019-04-21 12:04:27', 'Error', '{this is content}'),
                 #('2019-04-21 12:04:29', 'Error', '{this is content}'),
                 #('2019-04-21 12:04:31', 'Error', '{this is content}'),
                 #('2019-04-21 12:04:33', 'Error', '{this is content}'),
                 #('2019-04-21 12:04:35', 'Error', '{this is content}'),
                 #('2019-04-21 12:04:37', 'Error', '{this is content}')]

                if len(log):
                    send_data(conn, json.dumps(log))
            if channel.exit_status_ready(): #如果远程状态已退出并返回了退出状态，则返回true
                print('chanel.exit')
                break
        except Exception as e:
            print('traceback.print_exc():');traceback.print_exc()
            print('traceback.format_exc(): %s' % traceback.format_exc())
            print('except %s : Socket close with %s:%s' % (thread_name, address[0], address[1]))
            ssh.close()
            channel.close()
            conn.close()
    channel.close()
    ssh.close()

def wbservice():
    print('webservice')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('0.0.0.0', 8080)) #监听地址
    sock.listen(100)
    index = 1
    print ('Websocket server start, wait for connect!')
    print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -')
    while True:
        connection, address = sock.accept()
        thread_name = 'thread_%s' % index
        print ('%s : Connection from %s:%s' % (thread_name, address[0], address[1]))
        t = threading.Thread(target=getlog, args=(connection, address, thread_name))
        t.start()
        index += 1


if __name__ == '__main__':
    wbservice()
