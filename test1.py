import baostock as bs
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime
import os
from PIL import Image, ImageTk  # 需要安装 Pillow 库
import tkinter.ttk as ttk       # 明确导入 ttk

# 定义爬取数据的函数
def fetch_data():
    # 获取用户输入
    code_num = code_entry.get().strip()
    start_date = start_date_entry.get().strip()
    end_date = end_date_entry.get().strip()
    selected_frequency = frequency_var.get().strip()  # 获取用户选择的频率
    folder_path = folder_path_entry.get().strip()

    # 检查输入的有效性
    if not code_num or not start_date or not end_date or not folder_path:
        messagebox.showerror("错误", "请输入所有必要的信息！")
        return

    try:
        # 将日期字符串转换为日期对象进行验证
        datetime.strptime(start_date, "%Y-%m-%d")
        datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("错误", "日期格式不正确，请使用 YYYY-MM-DD 格式！")
        return

    # 根据用户选择的频率，转换为对应的缩写
    frequency_map = {
        "day": "d",
        "week": "w",
        "month": "m"
    }
    frequency = frequency_map.get(selected_frequency, "d")

    # 生成文件名
    file_name = f"{code_num.replace('.', '')}.csv"
    res_path = os.path.join(folder_path, file_name)

    # 登录BaoStock
    lg = bs.login()
    if lg.error_code != '0':
        messagebox.showerror("错误", f"登录失败: {lg.error_msg}")
        return

    # 动态选择字段
    if frequency in ['w', 'm']:  # 根据频率选择对应的字段
        fields = "date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg"
    else:
        fields = "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM,isST"

    # 查询历史数据
    rs = bs.query_history_k_data_plus(code_num, fields,
        start_date, end_date,
        frequency, adjustflag="3")

    if rs.error_code != '0':
        messagebox.showerror("错误", f"数据查询失败: {rs.error_msg}")
        bs.logout()
        return

    # 处理查询结果
    data_list = []
    while (rs.error_code == '0') & rs.next():
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)

    # 保存到文件
    try:
        result.to_csv(res_path, encoding="utf-8", index=False)
        messagebox.showinfo("成功", f"数据已成功保存到 {res_path}")
    except Exception as e:
        messagebox.showerror("错误", f"保存文件失败: {e}")

    # 登出
    bs.logout()

# 创建主窗口
root = tk.Tk()
root.title("股票数据爬虫工具")
root.geometry("600x500")  # 设置窗口大小
root.resizable(False, False)  # 禁用窗口大小调整

# 设置背景图片
try:
    background_image = Image.open("abc.png")  # 加载背景图片
    background_image = background_image.resize((600, 500), Image.LANCZOS)  # 调整图片尺寸以适应窗口
    background_photo = ImageTk.PhotoImage(background_image)
    background_label = ttk.Label(root, image=background_photo)
    background_label.place(relx=0, rely=0, relwidth=1, relheight=1)
except Exception as e:
    messagebox.showerror("错误", f"加载背景图片失败: {e}")

# 创建输入框和标签的现代样式
style = ttk.Style()
style.configure('TLabel', font=('Arial', 12))
style.configure('TEntry', font=('Arial', 12))
style.configure('TButton', font=('Arial', 12), background='#4CAF50', foreground='blue')

# 股票代码
code_label = ttk.Label(root, text="请输入正确的股票代码:")
code_label.grid(row=0, column=0, padx=10, pady=10)
code_entry = ttk.Entry(root)
code_entry.insert(0, "sz.002039")  # 默认值
code_entry.config(width=20)  # 调整输入框宽度
code_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

# 开始日期
start_date_label = ttk.Label(root, text="开始日期 (YYYY-MM-DD):")
start_date_label.grid(row=1, column=0, padx=10, pady=10)
start_date_entry = ttk.Entry(root)
start_date_entry.insert(0, "2016-01-01")  # 默认值
start_date_entry.config(width=20)  # 调整输入框宽度
start_date_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

# 结束日期
end_date_label = ttk.Label(root, text="结束日期 (YYYY-MM-DD):")
end_date_label.grid(row=2, column=0, padx=10, pady=10)
end_date_entry = ttk.Entry(root)
end_date_entry.insert(0, "2025-01-01")  # 默认值
end_date_entry.config(width=20)  # 调整输入框宽度
end_date_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

# 爬取频率
frequency_label = ttk.Label(root, text="请选择您的爬取频率:")
frequency_label.grid(row=3, column=0, padx=10, pady=10)
frequency_var = tk.StringVar(root)
#frequency_var.set("day")  # 默认值为天
frequency_options = ["day", "week", "month"]  # 修正了频率选项
frequency_menu = ttk.OptionMenu(root, frequency_var, *frequency_options)
frequency_menu.config(width=10)  # 增大下拉框宽度
frequency_menu.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

# 保存路径
folder_path_label = ttk.Label(root, text="请选择您的保存路径:")
folder_path_label.grid(row=4, column=0, padx=10, pady=10)
folder_path_entry = ttk.Entry(root, width=30)  # 调整输入框宽度
folder_path_entry.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

# 添加选择文件夹路径的按钮
def select_folder_path():
    folder_path = filedialog.askdirectory(title="选择保存文件夹")
    if folder_path:
        folder_path_entry.delete(0, tk.END)
        folder_path_entry.insert(0, folder_path)

# 调整按钮布局，使其不被挤出界面
folder_path_button = ttk.Button(root, text="浏览", command=select_folder_path)
folder_path_button.grid(row=4, column=2, padx=10, pady=10)  # 调整按钮所在列

# 添加开始按钮
start_button = ttk.Button(root, text="点击此处开始爬取", command=fetch_data)
start_button.grid(row=5, column=0, columnspan=3, pady=20,sticky="ew")

# 启动主循环
root.mainloop()