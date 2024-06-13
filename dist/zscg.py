import subprocess
import tkinter as tk
from tkinter import messagebox
import pymysql

# 插入数据
def insert_data():
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        passwd='123456',
        port=3306,
        db='itcast',
        charset='utf8mb4'
    )
    cursor = conn.cursor()  # 创建游标对象用于执行数据库操作

    # 处理插入操作的函数
    def insert():
        username = username_entry.get()
        password = password_entry.get()

        # 检查用户名和密码是否为空
        if not username or not password:
            messagebox.showerror("错误", "用户名和密码不能为空！")
            return

        # 查询数据库是否已存在该用户名
        query = "SELECT * FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            messagebox.showerror("错误", "用户名已经存在！")
        else:
            query = "INSERT INTO users (username, password) VALUES (%s, %s)"
            cursor.execute(query, (username, password))
            conn.commit()
            messagebox.showinfo("插入成功", "数据插入成功！")

        conn.close()

    # 创建新窗口进行插入操作
    insert_window = tk.Toplevel(root)
    insert_window.title("插入数据")

    # 创建用户名和密码的输入字段
    username_label = tk.Label(insert_window, text="用户名:")
    username_label.pack()
    username_entry = tk.Entry(insert_window)
    username_entry.pack()

    password_label = tk.Label(insert_window, text="密码:")
    password_label.pack()
    password_entry = tk.Entry(insert_window, show="*")
    password_entry.pack()

    # 执行插入操作的按钮
    insert_button = tk.Button(insert_window, text="注册", command=insert)
    insert_button.pack()

# 删除数据
def delete_data():
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        passwd='123456',
        port=3306,
        db='itcast',
        charset='utf8mb4'
    )
    cursor = conn.cursor()  # 创建游标对象用于执行数据库操作
    # 处理删除操作的函数
    def delete():
        username = username_entry.get()
        query = "DELETE FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        conn.commit()
        conn.close()
        messagebox.showinfo("删除成功", "数据删除成功！")

    # 创建新窗口进行删除操作
    delete_window = tk.Toplevel(root)
    delete_window.title("删除数据")

    # 创建用户名输入字段
    username_label = tk.Label(delete_window, text="用户名:")
    username_label.pack()
    username_entry = tk.Entry(delete_window)
    username_entry.pack()

    # 执行删除操作的按钮
    delete_button = tk.Button(delete_window, text="删除", command=delete)
    delete_button.pack()

# 查找数据
def select_data():
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        passwd='123456',
        port=3306,
        db='itcast',
        charset='utf8mb4'
    )
    cursor = conn.cursor()  # 创建游标对象用于执行数据库操作
    # 处理查找操作的函数
    def select():
        username = username_entry.get()
        query = "SELECT * FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        conn.close()

        if result:
            messagebox.showinfo("查询结果", f"用户名：{result[0]}, 密码：{result[1]}")
        else:
            messagebox.showinfo("查询结果", "未找到相关用户！")

    # 创建新窗口进行查找操作
    select_window = tk.Toplevel(root)
    select_window.title("查询数据")

    # 创建用户名输入字段
    username_label = tk.Label(select_window, text="用户名:")
    username_label.pack()
    username_entry = tk.Entry(select_window)
    username_entry.pack()

    # 执行查找操作的按钮
    select_button = tk.Button(select_window, text="查询", command=select)
    select_button.pack()

# 更新数据
def update_data():
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        passwd='123456',
        port=3306,
        db='itcast',
        charset='utf8mb4'
    )
    cursor = conn.cursor()  # 创建游标对象用于执行数据库操作
    # 处理更新操作的函数
    def update():
        username = username_entry.get()
        new_password = password_entry.get()
        query = "UPDATE users SET password = %s WHERE username = %s"
        cursor.execute(query, (new_password, username))
        conn.commit()
        conn.close()
        messagebox.showinfo("更新成功", "数据更新成功！")

    # 创建新窗口进行更新操作
    update_window = tk.Toplevel(root)
    update_window.title("更新数据")

    # 创建用户名和新密码的输入字段
    username_label = tk.Label(update_window, text="用户名:")
    username_label.pack()
    username_entry = tk.Entry(update_window)
    username_entry.pack()

    password_label = tk.Label(update_window, text="新密码:")
    password_label.pack()
    password_entry = tk.Entry(update_window, show="*")
    password_entry.pack()

    # 执行更新操作的按钮
    update_button = tk.Button(update_window, text="更新", command=update)
    update_button.pack()

# 端口扫描
def ARP_scan():
    # 点击按钮后启动另一个Python脚本
    subprocess.run(["python", "scapy_scan.py"])

# ARP攻击
def ARP_attack():
    # 点击按钮后启动另一个Python脚本
    subprocess.run(["python", "scapy_ARP_attack.py"])




# 主窗口
root = tk.Tk()
root.title("酷派极客")

# 不同操作的按钮
button_style = {"padx": 100, "pady": 20, "bg": "skyblue", "fg": "black"}

insert_button = tk.Button(root, text="插入数据", command=insert_data, **button_style)
insert_button.pack()

delete_button = tk.Button(root, text="删除数据", command=delete_data, **button_style)
delete_button.pack()

select_button = tk.Button(root, text="查询数据", command=select_data, **button_style)
select_button.pack()

update_button = tk.Button(root, text="更新数据", command=update_data, **button_style)
update_button.pack()

ARP_scan_button = tk.Button(root, text="端口扫描", command=ARP_scan, **button_style)
ARP_scan_button.pack()

ARP_attack = tk.Button(root, text="ARP攻击", command=ARP_attack, **button_style)
ARP_attack.pack()

# 运行主循环
root.mainloop()
