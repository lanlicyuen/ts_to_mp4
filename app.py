import os
import sys
import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import locale
import threading

class App(tk.Tk):  # 改回使用基础 Tk
    def __init__(self):
        super().__init__()
        self.lang = locale.getdefaultlocale()[0]
        self.texts = self.get_localized_texts()
        
        self.title(self.texts['title'])
        self.geometry("600x300")
        
        self.save_path = ""
        self.load_settings()
        
        self.create_menu()
        self.create_widgets()

    def get_localized_texts(self):
        texts = {
            'zh_CN': {
                'title': 'TS 转 MP4 转换器',
                'file': '文件',
                'set_path': '设置保存路径',
                'exit': '退出',
                'select_file': '选择文件',
                'select_hint': '点击下方按钮选择 TS 文件转换为 MP4',
                'drag_hint': '拖放 TS 文件到此处或点击下方按钮选择文件',
                'converting': '转换中...',
                'error': '错误',
                'success': '完成',
                'set_path_first': '请先设置保存路径！',
                'path_set': '路径已设置',
                'path_set_to': '保存路径设置为：',
                'convert_complete': '转换完成',
                'convert_failed': '转换失败',
                'about': '关于',
                'about_title': '关于 TS 转 MP4 转换器',
                'about_message': '版本: v1.0\n\n乐趣开发，免费使用\n\n如有问题请联系：\nlanlic@hotmail.com'
            },
            'default': {
                'title': 'TS to MP4 Converter',
                'file': 'File',
                'set_path': 'Set Save Path',
                'exit': 'Exit',
                'select_file': 'Select File',
                'select_hint': 'Click the button below to select TS files',
                'drag_hint': 'Drag TS files here or click button below',
                'converting': 'Converting...',
                'error': 'Error',
                'success': 'Success',
                'set_path_first': 'Please set save path first!',
                'path_set': 'Path Set',
                'path_set_to': 'Save path set to:',
                'convert_complete': 'Conversion Complete',
                'convert_failed': 'Conversion Failed',
                'about': 'About',
                'about_title': 'About TS to MP4 Converter',
                'about_message': 'Version: v1.0\n\nDeveloped for fun, free to use\n\nContact:\nlanlic@hotmail.com'
            }
        }
        return texts.get(self.lang, texts['default'])

    def create_menu(self):
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)
        
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label=self.texts['file'], menu=file_menu)
        file_menu.add_command(label=self.texts['set_path'], command=self.set_save_path)
        file_menu.add_separator()
        file_menu.add_command(label=self.texts['exit'], command=self.quit)

        # 添加帮助菜单
        help_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label=self.texts['about'], menu=help_menu)
        help_menu.add_command(label=self.texts['about'], command=self.show_about)

    def show_about(self):
        messagebox.showinfo(
            self.texts['about_title'],
            self.texts['about_message']
        )

    def set_save_path(self):
        path = filedialog.askdirectory()
        if path:
            self.save_path = path
            self.save_settings()
            messagebox.showinfo(self.texts['path_set'], f"{self.texts['path_set_to']}: {self.save_path}")

    def save_settings(self):
        settings = {"save_path": self.save_path}
        with open("settings.json", "w") as f:
            json.dump(settings, f)

    def load_settings(self):
        if os.path.exists("settings.json"):
            with open("settings.json", "r") as f:
                settings = json.load(f)
                self.save_path = settings.get("save_path", "")

    def create_widgets(self):
        main_frame = tk.Frame(self)
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        self.label = tk.Label(main_frame, text=self.texts['select_hint'])
        self.label.pack(pady=20)

        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        
        self.open_button = tk.Button(
            main_frame, 
            text=self.texts['select_file'], 
            command=self.open_file, 
            width=20, height=2
        )
        self.open_button.pack(pady=10)

    def open_file(self):
        files = filedialog.askopenfilenames(
            title=self.texts['select_file'],
            filetypes=[("TS files", "*.ts"), ("All files", "*.*")]
        )
        for file in files:
            if file.lower().endswith('.ts'):
                self.convert_to_mp4(file)

    def convert_to_mp4(self, ts_file):
        if not self.save_path:
            messagebox.showerror(self.texts['error'], 
                               self.texts['set_path_first'])
            return

        # 显示进度条
        self.progress.pack(pady=10)
        self.progress.start()
        self.update()

        def convert():
            try:
                mp4_file = os.path.join(self.save_path, 
                                      os.path.basename(ts_file).replace(".ts", ".mp4"))
                command = [
                    "C:\\ffmpeg\\bin\\ffmpeg",
                    "-y",
                    "-i", ts_file,
                    "-c:v", "copy",
                    "-c:a", "copy",
                    mp4_file
                ]
                
                subprocess.run(command, check=True, 
                             encoding='utf-8', errors='replace')
                
                # 在主线程中更新UI
                self.after(0, lambda: self.conversion_complete(ts_file))
                
            except subprocess.CalledProcessError as e:
                self.after(0, lambda: self.conversion_failed(str(e)))

        # 在新线程中运行转换
        threading.Thread(target=convert, daemon=True).start()

    def conversion_complete(self, ts_file):
        self.progress.stop()
        self.progress.pack_forget()
        messagebox.showinfo(self.texts['success'], 
                          f"{os.path.basename(ts_file)} {self.texts['convert_complete']}")

    def conversion_failed(self, error):
        self.progress.stop()
        self.progress.pack_forget()
        messagebox.showerror(self.texts['error'], 
                           f"{self.texts['convert_failed']}: {error}")

if __name__ == "__main__":
    try:
        app = App()
        app.mainloop()
    except Exception as e:
        messagebox.showerror("Error", str(e))
