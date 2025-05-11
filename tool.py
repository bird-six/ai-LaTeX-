import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import pyperclip
import re

# 正则表达式匹配 LaTeX 数学公式
inline_formula = re.compile(r"(?<!\\)\\\((.+?)(?<!\\)\\\)")
display_formula = re.compile(r"(?<!\\)\\\[(.+?)(?<!\\)\\\]", re.DOTALL)

# 处理公式，转换为 markdown 或 Word 兼容格式
def process_text(text, doc_type):
    if doc_type == 'md':
        # 替换 \( ... \) 为 $...$
        text = inline_formula.sub(r'$$\1$$', text)
        # 替换 \[ ... \] 为 $$...$$，多行公式
        text = display_formula.sub(lambda m: f'$$\n{m.group(1)}\n$$', text)
    elif doc_type == 'word':
        # 对于 Word，可以保留 LaTeX 或者转成数学域代码，但此处简单保留原始格式
        text = text  # 不处理
    return text

# 创建主窗口
root = tk.Tk()
root.title("ai公式（LaTeX）公式转换工具")
root.geometry("800x600")

# 输入区域
input_label = ttk.Label(root, text="请输入原始文案（建议直接点击复制后再粘贴到此处）：")
input_label.pack(anchor='w', padx=10, pady=5)
input_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=12)
input_text.pack(fill='both', expand=False, padx=10, pady=5)

# 文档类型选择
doc_type_label = ttk.Label(root, text="选择导出格式：")
doc_type_label.pack(anchor='w', padx=10, pady=5)
doc_type_var = tk.StringVar(value='md')
doc_type_combo = ttk.Combobox(root, textvariable=doc_type_var, values=['md', 'word'], state='readonly')
doc_type_combo.pack(anchor='w', padx=10, pady=5)

# 输出区域
output_label = ttk.Label(root, text="处理后的文案：")
output_label.pack(anchor='w', padx=10, pady=5)
output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=14)
output_text.pack(fill='both', expand=True, padx=10, pady=5)

# 处理按钮

def handle_convert():
    raw_text = input_text.get("1.0", tk.END)
    doc_type = doc_type_var.get()
    processed = process_text(raw_text, doc_type)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, processed)

def handle_copy():
    content = output_text.get("1.0", tk.END).strip()
    pyperclip.copy(content)
    messagebox.showinfo("复制成功", "内容已复制到剪贴板！")

convert_button = ttk.Button(root, text="转换", command=handle_convert)
convert_button.pack(pady=5)

copy_button = ttk.Button(root, text="复制结果", command=handle_copy)
copy_button.pack(pady=5)


root.mainloop()
