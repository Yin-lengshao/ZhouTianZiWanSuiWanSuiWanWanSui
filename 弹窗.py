import tkinter as tk
import random
import threading
import time
from tkinter import font
import tkinter.messagebox as messagebox
import webbrowser
import os
import subprocess
import sys

try:
    import pygame
    pygame_available = True
except ImportError:
    pygame_available = False
    print("警告: pygame 库未安装，无法播放音乐。请运行: pip install pygame")

# -------------------- 新增：资源路径动态获取函数 --------------------
def get_resource_path(relative_path):
    """获取打包后资源文件的正确路径（适配开发环境和打包环境）"""
    try:
        # 打包后的临时资源路径
        base_path = sys._MEIPASS
    except Exception:
        # 开发环境下的当前路径
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class BlessingPopup:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()

        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(family=["SimHei", "Microsoft YaHei", "WenQuanYi Micro Hei", "Heiti TC"])

        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.popup_count = 0
        self.max_popups = 200

        self.music_playing = False
        # -------------------- 修改：音乐文件路径用资源函数获取 --------------------
        self.music_file = get_resource_path("resources/young_folks.mp3")

        self.init_music()

        self.blessings = [
            "周天子万岁万岁万万岁！",
            "周武王大人其实以后可以不用那么勇猛的！",
            "这嘉定周公真帅吧！",
            "祝你永葆少年心气，也祝你更坚定、更勇敢的走在自己的路上。",
            "不要让不同路的人和事挡道！",
            "让那些乱臣贼子都见鬼去吧！",
            "他们就欺负老周你是个知识分子！别总委屈自己！",
            "别太累着自己！保研不在于一城一地的得失。",
            "大雪深埋！",
            "小周肯定没问题！",
            "预祝转专业成功！保研成功！以后的一切都顺利！",
            "我们都有光明的未来！",
            "遇到不开心的事或许可以跟我讲讲呢？",
            "不要背叛自己口牙！",
            "小周是一个敏锐又丰盈的、特别特别好的人！",
            "小周值得所有美好的东西！"
        ]

        self.color_schemes = [
            {"bg": "#FF6B6B", "fg": "white"},
            {"bg": "#4ECDC4", "fg": "white"},
            {"bg": "#45B7D1", "fg": "white"},
            {"bg": "#FFA07A", "fg": "white"},
            {"bg": "#98D8C8", "fg": "#2E7D32"},
            {"bg": "#F7DC6F", "fg": "#5D4037"},
            {"bg": "#D7BDE2", "fg": "#4A148C"},
            {"bg": "#A3E4D7", "fg": "#00695C"},
            {"bg": "#F8C471", "fg": "#E65100"},
            {"bg": "#85C1E9", "fg": "#0D47A1"},
        ]

        self.root.bind("<Escape>", self.close_all)

        self.confession_message = "要多保重自己好吗？"

        self.show_confession = True
        # -------------------- 修改：HTML文件路径用资源函数获取 --------------------
        self.html_path = get_resource_path("html/letter.html")

    def init_music(self):
        if not pygame_available:
            print("pygame 不可用，跳过音乐初始化")
            return

        try:
            pygame.mixer.init()
            pygame.mixer.music.load(self.music_file)
            self.music_playing = True

        except Exception as e:
            self.music_playing = False

    def play_music(self):
        if not self.music_playing:
            return

        try:
            pygame.mixer.music.play(-1)
        except Exception as e:
            pass

    def stop_music(self):
        if pygame_available and self.music_playing:
            try:
                pygame.mixer.music.stop()
                pygame.mixer.quit()
            except Exception as e:
                pass

    def create_popup(self, text=None):
        if self.popup_count >= self.max_popups:
            return

        popup = tk.Toplevel(self.root)
        popup.overrideredirect(True)
        popup.attributes("-topmost", True)

        x = random.randint(50, self.screen_width - 300)
        y = random.randint(50, self.screen_height - 200)
        popup.geometry(f"250x120+{x}+{y}")

        color_scheme = random.choice(self.color_schemes)

        main_frame = tk.Frame(
            popup,
            bg=color_scheme["bg"],
            relief="solid",
            bd=2,
            highlightbackground=color_scheme["bg"],
            highlightthickness=2
        )
        main_frame.pack(fill="both", expand=True, padx=5, pady=5)

        title_frame = tk.Frame(
            main_frame,
            bg=color_scheme["bg"],
            height=3
        )
        title_frame.pack(fill="x", padx=2, pady=(2, 5))

        if text is None:
            text = random.choice(self.blessings)

        label = tk.Label(
            main_frame,
            text=text,
            font=("Microsoft YaHei", 12, "bold"),
            bg=color_scheme["bg"],
            fg=color_scheme["fg"],
            wraplength=220,
            justify="center",
            padx=10,
            pady=15
        )
        label.pack(expand=True, fill="both")

        bottom_frame = tk.Frame(
            main_frame,
            bg=color_scheme["bg"],
            height=3
        )
        bottom_frame.pack(fill="x", padx=2, pady=(5, 2))

        close_btn = tk.Label(
            main_frame,
            text="✕",
            font=("Arial", 10, "bold"),
            bg=color_scheme["bg"],
            fg=color_scheme["fg"],
            cursor="hand2"
        )
        close_btn.place(relx=0.95, rely=0.05, anchor="ne")
        close_btn.bind("<Button-1>", lambda e: self.close_popup(popup))

        def on_enter(e):
            close_btn.configure(fg="#FFFFFF")

        def on_leave(e):
            close_btn.configure(fg=color_scheme["fg"])

        main_frame.bind("<Enter>", on_enter)
        main_frame.bind("<Leave>", on_leave)
        close_btn.bind("<Enter>", lambda e: close_btn.configure(fg="#FF5252"))
        close_btn.bind("<Leave>", lambda e: close_btn.configure(fg=color_scheme["fg"]))

        self.popup_count += 1

        self.fade_in(popup)

        fade_delay = random.randint(6000, 12000)
        popup.after(fade_delay, lambda: self.fade_out(popup))

    def create_confession_popup(self):
        if not self.show_confession:
            return

        popup = tk.Toplevel(self.root)
        popup.overrideredirect(True)
        popup.attributes("-topmost", True)

        x = random.randint(50, self.screen_width - 300)
        y = random.randint(50, self.screen_height - 200)
        popup.geometry(f"250x150+{x}+{y}")

        color_scheme = {"bg": "#FFB6C1", "fg": "#8B0000"}

        main_frame = tk.Frame(
            popup,
            bg=color_scheme["bg"],
            relief="solid",
            bd=2,
            highlightbackground=color_scheme["bg"],
            highlightthickness=2
        )
        main_frame.pack(fill="both", expand=True, padx=5, pady=5)

        title_frame = tk.Frame(
            main_frame,
            bg=color_scheme["bg"],
            height=3
        )
        title_frame.pack(fill="x", padx=2, pady=(2, 5))

        label = tk.Label(
            main_frame,
            text=self.confession_message,
            font=("Microsoft YaHei", 12, "bold"),
            bg=color_scheme["bg"],
            fg=color_scheme["fg"],
            wraplength=220,
            justify="center",
            padx=10,
            pady=10
        )
        label.pack(expand=True, fill="both")

        button_frame = tk.Frame(
            main_frame,
            bg=color_scheme["bg"]
        )
        button_frame.pack(pady=5)

        agree_button = tk.Button(
            button_frame,
            text="好的！",
            font=("Microsoft YaHei", 10, "bold"),
            bg="#FF69B4",
            fg="white",
            relief="raised",
            command=lambda: self.on_agree(popup)
        )
        agree_button.pack(side="left", padx=10)

        refuse_button = tk.Button(
            button_frame,
            text="不要！",
            font=("Microsoft YaHei", 10, "bold"),
            bg="#D3D3D3",
            fg="black",
            relief="raised",
            command=lambda: self.on_refuse(popup)
        )
        refuse_button.pack(side="left", padx=10)

        bottom_frame = tk.Frame(
            main_frame,
            bg=color_scheme["bg"],
            height=3
        )
        bottom_frame.pack(fill="x", padx=2, pady=(5, 2))

        close_btn = tk.Label(
            main_frame,
            text="✕",
            font=("Arial", 10, "bold"),
            bg=color_scheme["bg"],
            fg=color_scheme["fg"],
            cursor="hand2"
        )
        close_btn.place(relx=0.95, rely=0.05, anchor="ne")
        close_btn.bind("<Button-1>", lambda e: self.on_close(popup))

        close_btn.bind("<Enter>", lambda e: close_btn.configure(fg="#FF5252"))
        close_btn.bind("<Leave>", lambda e: close_btn.configure(fg=color_scheme["fg"]))

        self.fade_in(popup)

    def fade_in(self, popup):
        def fade(alpha=0.0):
            if alpha < 1.0:
                popup.attributes("-alpha", alpha)
                popup.after(15, fade, alpha + 0.1)
            else:
                popup.attributes("-alpha", 1.0)

        fade()

    def fade_out(self, popup):
        def fade(alpha=1.0):
            if alpha > 0:
                popup.attributes("-alpha", alpha)
                popup.after(15, fade, alpha - 0.1)
            else:
                self.close_popup(popup)

        fade()

    def close_popup(self, popup):
        if popup.winfo_exists():
            self.popup_count -= 1
            popup.destroy()

    def close_all(self, event=None):
        self.stop_music()
        self.root.destroy()

    def batch_create(self, num=10):
        def create_task():
            for _ in range(num):
                if self.popup_count < self.max_popups:
                    self.root.after(0, self.create_popup)
                    time.sleep(random.uniform(0.1, 0.3))

        for _ in range(4):
            t = threading.Thread(target=create_task, daemon=True)
            t.start()

    def create_test_popup(self):
        x = random.randint(50, self.screen_width - 400)
        y = random.randint(50, self.screen_height - 200)

        popup = tk.Toplevel(self.root)
        popup.overrideredirect(True)
        popup.attributes("-topmost", True)
        popup.geometry(f"380x180+{x}+{y}")

        color_scheme = random.choice(self.color_schemes)

        main_frame = tk.Frame(
            popup,
            bg=color_scheme["bg"],
            relief="solid",
            bd=2,
            highlightbackground=color_scheme["bg"],
            highlightthickness=2
        )
        main_frame.pack(fill="both", expand=True, padx=5, pady=5)

        title_frame = tk.Frame(
            main_frame,
            bg=color_scheme["bg"],
            height=3
        )
        title_frame.pack(fill="x", padx=2, pady=(2, 5))

        label = tk.Label(
            main_frame,
            text="有点肉麻呢，不过这条消息你不一定会看到。不管啦！祝小殷和小周会一直是好朋友！",
            font=("Microsoft YaHei", 14, "bold"),
            bg=color_scheme["bg"],
            fg=color_scheme["fg"],
            justify="center",
            padx=15,
            pady=20,
            wraplength=360
        )
        label.pack(expand=True, fill="both")

        bottom_frame = tk.Frame(
            main_frame,
            bg=color_scheme["bg"],
            height=3
        )
        bottom_frame.pack(fill="x", padx=2, pady=(5, 2))

        close_btn = tk.Label(
            main_frame,
            text="✕",
            font=("Arial", 10, "bold"),
            bg=color_scheme["bg"],
            fg=color_scheme["fg"],
            cursor="hand2"
        )
        close_btn.place(relx=0.95, rely=0.05, anchor="ne")
        close_btn.bind("<Button-1>", lambda e: popup.destroy())

        close_btn.bind("<Enter>", lambda e: close_btn.configure(fg="#FF5252"))
        close_btn.bind("<Leave>", lambda e: close_btn.configure(fg=color_scheme["fg"]))

        self.fade_in(popup)

        popup.after(5000, lambda: self.fade_out(popup))

    def on_agree(self, popup):
        popup.destroy()
        self.show_confession = False

        if not os.path.exists(self.html_path):
            messagebox.showerror("错误", f"文件不存在: {self.html_path}\n请确认'html'文件夹与代码文件在同一目录")
            self.root.after(1000, self.close_all)
            return

        abs_path = os.path.abspath(self.html_path)
        success = False

        browsers = []
        if sys.platform == "win32":
            browsers = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
                r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                r"C:\Program Files\Mozilla Firefox\firefox.exe"
            ]
        elif sys.platform == "darwin":
            browsers = [
                "/Applications/Safari.app/Contents/MacOS/Safari",
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"
            ]
        else:
            browsers = ["chrome", "google-chrome", "chromium", "firefox", "xdg-open"]

        for browser in browsers:
            try:
                subprocess.Popen(
                    [browser, abs_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
                )
                success = True
                break
            except FileNotFoundError:
                continue
            except Exception as e:
                continue

        if not success:
            try:
                if sys.platform == "win32":
                    os.system(f'start "" /d "." "htmlfile" "{abs_path}"')
                    success = True
                elif sys.platform == "darwin":
                    subprocess.call(["open", "-a", "Safari", abs_path])
                    success = True
                else:
                    subprocess.call(["xdg-open", abs_path])
                    success = True
            except Exception as e:
                pass
        time.sleep(0.1)
        if not success:
            messagebox.showerror("错误", "未找到可用浏览器！\n可手动打开以下文件：\n" + abs_path)
        else:
            messagebox.showinfo("求求了求求了", "冷少没考上的话，别对他太苛刻好吗？哪怕他拧巴。")

        self.stop_music()
        self.root.after(1000, self.close_all)

    def on_refuse(self, popup):
        popup.destroy()
        delay = random.randint(1000, 3000)
        self.root.after(delay, self.create_confession_popup)

    def on_close(self, popup):
        popup.destroy()
        delay = random.randint(1000, 3000)
        self.root.after(delay, self.create_confession_popup)

    def run(self):
        self.play_music()

        test_delay = random.randint(2000, 4000)
        self.root.after(test_delay, self.create_test_popup)

        confession_delay = random.randint(5000, 8000)
        self.root.after(confession_delay, self.create_confession_popup)

        self.batch_create(40)
        self.root.mainloop()

if __name__ == "__main__":
    app = BlessingPopup()
    app.run()