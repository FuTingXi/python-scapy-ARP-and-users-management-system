import tkinter as tk
from tkinter import messagebox
from tkinter.simpledialog import askstring  # Import askstring from simpledialog
import re
from scapy.all import *
from scapy.layers.inet import IP, TCP
import threading


def port_scan():
    target = entry_ip.get()

    # Check if the IP address is valid
    ip_pattern = re.compile(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$')
    if not ip_pattern.match(target):
        messagebox.showerror("错误", "请输入有效的IP地址。")
        return

    port_range = (1, 81)  # Default port range

    # Prompt the user to input port range
    while True:
        port_range_input = askstring("端口范围", "请输入要扫描的端口范围（1-65535），用逗号分隔:")
        if port_range_input:
            ports = port_range_input.split(',')
            if len(ports) != 2:
                messagebox.showerror("错误", "请输入正确的端口范围。")
                continue
            try:
                start, end = int(ports[0]), int(ports[1])
                if 1 <= start <= end <= 65535:
                    port_range = (start, end)
                    break
                else:
                    messagebox.showerror("错误", "请输入正确的端口范围（1-65535）。")
            except ValueError:
                messagebox.showerror("错误", "请输入正确的端口范围。")
        else:
            return  # User canceled input

    open_ports = []
    closed_ports = []

    def scan_port(port):
        nonlocal open_ports, closed_ports
        response = sr1(IP(dst=target) / TCP(dport=port), timeout=1, verbose=False)
        if response is None:
            closed_ports.append(port)
        elif response.haslayer(TCP) and response.getlayer(TCP).flags == 0x12:
            open_ports.append(port)
            send_rst = sr(IP(dst=target) / TCP(dport=port, flags='R'), timeout=1, verbose=False)
        else:
            closed_ports.append(port)

    threads = []
    for port in range(port_range[0], port_range[1] + 1):
        thread = threading.Thread(target=scan_port, args=(port,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    messagebox.showinfo("扫描结果", f"开放端口: {open_ports}")


def validate_ip(ip):
    # Check if the IP address format is valid
    ip_pattern = re.compile(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$')
    return ip_pattern.match(ip)


def start_scan():
    ip = entry_ip.get()
    if not validate_ip(ip):
        messagebox.showerror("错误", "请输入有效的IP地址。")
    else:
        port_scan()


root = tk.Tk()
root.title("端口扫描")

label_ip = tk.Label(root, text="请输入要扫描的IP地址:")
label_ip.pack()

entry_ip = tk.Entry(root, width=30)
entry_ip.pack()

button_style = {"padx": 50, "pady": 10, "bg": "skyblue", "fg": "black"}
scan_button = tk.Button(root, text="开始扫描", command=start_scan, **button_style)
scan_button.pack()

root.mainloop()
