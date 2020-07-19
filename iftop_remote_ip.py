#!/usr/bin/python
#coding=utf-8
#针对业务监听的端口流量进行统计，忽略对随机端口流量统计
#若针对突然流量增大，找到其进程进行告警，可以不做统计，获取到流量进行判断，若大于多少阀值，则输出
import os
def change_unit(unit):
    if "Mb" in unit:
        flow = float(unit.strip("Mb")) * 1024
        return flow
    elif "Kb" in unit:
        flow = float(unit.strip("Kb"))
        return flow
    elif "b" in unit:
        flow = float(unit.strip("b")) / 1024
        return flow

def get_flow():
    #iftop参数：-t 使用不带ncurses的文本界面,-P显示主机以及端口信息,-N只显示连接端口号，不显示端口对应的服务名称,-n 将输出的主机信息都通过IP显示，不进行DNS解析,-s num  num秒后打印一次文本输出然后退出
    mes = os.popen("iftop -t -P -N -n -L 500 -s 5  2>/dev/null |grep -E '=>|<=' ").read()
    #以换行符进行分割
    iftop_list = mes.split("\n")
    count = len(iftop_list)
    #定义字典 存放主机信息和进出流量
    flow_dict = {}
    #定义列表，存放主机信息
    remote_ips = []

    #这里的 count/2 是iftop获取到的数据，是进出流量为一组，则有count/2 个流量连接，可执行os.popen 里面的iftop命令即可明白
    for i in range(count/2):
        flow_msg = ""
        #获取发送的ip地址(本地ip地址)，端口(本地端口)，发送的流量,以换行符分割后，数据偶数位为本地发送流量信息
        location_li_s = iftop_list[i*2]
        send_flow_lists = location_li_s.split(" ")
        #去空元素
        while '' in send_flow_lists:
            send_flow_lists.remove('')
        local_host_ip = send_flow_lists[1]
        send_flow = send_flow_lists[3]
        send_flow_float = change_unit(send_flow)
        #print send_flow_lists
        #获取接收的流量
        location_li_r = iftop_list[i*2+1]
        rec_flow_lists = location_li_r.split(" ")
        while '' in rec_flow_lists:
            rec_flow_lists.remove('')
        remote_host_ip = rec_flow_lists[0]
        rec_flow = rec_flow_lists[3]
        rec_flow_float = change_unit(rec_flow)
        sp_local_host_ip = local_host_ip.split(':')
        if len(sp_local_host_ip) < 2:
            continue
        local_ip   = sp_local_host_ip[0]
        local_port = sp_local_host_ip[1]

        # only consider http or https port
        if int(local_port) != 80 and int(local_port) != 443:
            continue

        sp_remote_host_ip = remote_host_ip.split(':')
        if len(sp_remote_host_ip) < 2:
            continue
        remote_ip   = sp_remote_host_ip[0]
        remote_port = sp_remote_host_ip[1]

        #remote 主机信息若不存在列表则加入host_ips，若存在，则字典取值，对进出流量进行相加
        if remote_ip not in remote_ips:
                remote_ips.append(remote_ip)
                flow_msg = {
                        'send': int(send_flow_float),
                        'recv': int(rec_flow_float),
                        }
                flow_dict[remote_ip] = flow_msg
        else:
            flow_dict_msg = flow_dict[remote_ip]
            flow_dict_msg_send =  flow_dict_msg.get('send')
            flow_dict_msg_rec  =  flow_dict_msg.get('recv')
            #字典里面的发送接收流量和获取到的新流量相加
            flow_add_send = flow_dict_msg_send + int(send_flow_float)
            flow_add_rec  = flow_dict_msg_rec  + int(rec_flow_float)
            #把新得出的结果，更新到字典
            flow_dict_msg['send'] = flow_add_send
            flow_dict_msg['recv'] = flow_add_rec
            flow_dict[remote_ip] = flow_dict_msg

    for k,v in flow_dict.items():
        # 单位是Kb
        print('remote_ip:{0} send:{1} Kb/s recv:{2} Kb/s'.format(k, v.get('send'), v.get('recv')))

if __name__ == '__main__':
    while True:
        get_flow()
