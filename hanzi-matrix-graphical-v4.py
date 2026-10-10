#!/usr/bin/env python3
"""Hanzi Matrix - graphical version 4 with longer red vocabulary highlights and a soft text halo.
Run with: python3 hanzi-matrix-graphical-v4.py
Keys: V vocabulary, P red-word meaning on/off, Q or Esc quit.
Requires Python 3 with Tkinter (usually included with desktop Python).
"""
import random
import time
import tkinter as tk
from tkinter import font as tkfont

VOCAB = [
    ("Desktop & navigation", [("桌面", "zhuōmiàn", "desktop"), ("窗口", "chuāngkǒu", "window"), ("任务栏", "rènwùlán", "taskbar"), ("菜单", "càidān", "menu"), ("图标", "túbiāo", "icon"), ("文件", "wénjiàn", "file"), ("文件夹", "wénjiànjiā", "folder"), ("回收站", "huíshōuzhàn", "recycle bin"), ("快捷方式", "kuàijié fāngshì", "shortcut"), ("搜索", "sōusuǒ", "search"), ("帮助", "bāngzhù", "help")]),
    ("Settings & display", [("设置", "shèzhì", "settings"), ("系统", "xìtǒng", "system"), ("个性化", "gèxìnghuà", "personalization"), ("显示", "xiǎnshì", "display"), ("显示设置", "xiǎnshì shèzhì", "display settings"), ("分辨率", "fēnbiànlǜ", "resolution"), ("亮度", "liàngdù", "brightness"), ("字体", "zìtǐ", "font"), ("字体大小", "zìtǐ dàxiǎo", "font size"), ("背景", "bèijǐng", "background"), ("本地图片", "běndì túpiàn", "local pictures"), ("选择", "xuǎnzé", "select / choose"), ("应用", "yìngyòng", "apply / application")]),
    ("Network & wireless", [("网络", "wǎngluò", "network"), ("无线网络", "wúxiàn wǎngluò", "wireless network"), ("无线", "wúxiàn", "wireless"), ("连接", "liánjiē", "connect / connection"), ("已连接", "yǐ liánjiē", "connected"), ("断开连接", "duànkāi liánjiē", "disconnect"), ("蓝牙", "lányá", "Bluetooth"), ("服务器", "fúwùqì", "server"), ("密码", "mìmǎ", "password")]),
    ("Files & software", [("打开", "dǎkāi", "open"), ("关闭", "guānbì", "close"), ("保存", "bǎocún", "save"), ("删除", "shānchú", "delete"), ("复制", "fùzhì", "copy"), ("粘贴", "zhāntiē", "paste"), ("安装", "ānzhuāng", "install"), ("卸载", "xièzài", "uninstall"), ("更新", "gēngxīn", "update"), ("软件", "ruǎnjiàn", "software"), ("文件名", "wénjiànmíng", "filename"), ("下载", "xiàzài", "download"), ("上传", "shàngchuán", "upload")]),
    ("Terminal & system messages", [("终端", "zhōngduān", "terminal"), ("命令", "mìnglìng", "command"), ("输入", "shūrù", "input / enter"), ("输出", "shūchū", "output"), ("回车", "huíchē", "Enter key"), ("请输入密码", "qǐng shūrù mìmǎ", "please enter your password"), ("密码错误", "mìmǎ cuòwù", "incorrect password"), ("错误", "cuòwù", "error"), ("正常", "zhèngcháng", "normal / working"), ("无法访问", "wúfǎ fǎngwèn", "cannot access"), ("没有那个文件或目录", "méiyǒu nàge wénjiàn huò mùlù", "no such file or directory"), ("重启", "chóngqǐ", "restart"), ("关机", "guānjī", "shut down")]),
    ("Everyday expressions", [("你好", "nǐ hǎo", "hello"), ("你好吗？", "nǐ hǎo ma?", "how are you?"), ("我很好", "wǒ hěn hǎo", "I'm doing well"), ("谢谢", "xièxie", "thank you"), ("不客气", "bú kèqi", "you're welcome"), ("再见", "zàijiàn", "goodbye"), ("请", "qǐng", "please"), ("没问题", "méi wèntí", "no problem"), ("我明白了", "wǒ míngbai le", "I understand"), ("请再说一遍", "qǐng zài shuō yí biàn", "please say that again"), ("看这个！", "kàn zhège!", "look at this!"), ("看这里！", "kàn zhèlǐ!", "look here!"), ("小心脚下", "xiǎoxīn jiǎoxià", "watch your step"), ("小心站台间隙", "xiǎoxīn zhàntái jiànxì", "mind the platform gap"), ("怎么了？", "zěnme le?", "what's wrong?"), ("我不知道", "wǒ bù zhīdào", "I don't know"), ("真的？", "zhēn de?", "really?"), ("当然", "dāngrán", "of course")]),
]
POOL = list("设置系统网络无线连接密码显示字体背景图片本地文件文件夹桌面窗口菜单图标任务栏搜索帮助打开关闭保存删除复制粘贴安装更新软件下载上传终端命令输入输出回车错误正常重启关机你好谢谢再见请看这里注意小心间隙服务器蓝牙个性化分辨率亮度选择应用请输入账户用户安全数据电脑信息权限语言中文简体，。！？；：、（）《》「」『』…—·0123456789")

BG = "#020807"
TEAL = "#20cdbb"
MINT = "#b8ffe2"
RED = "#ff542e"
DIM = "#20aa9a"
HALO_OUTER = "#04201d"
HALO_MID = "#064038"
HALO_INNER = "#087060"

class HanziMatrix:
    def __init__(self, root):
        self.root = root
        root.title("Hanzi Matrix — 汉字矩阵")
        root.configure(bg=BG)
        root.geometry("1000x700")
        root.minsize(640, 420)
        self.canvas = tk.Canvas(root, bg=BG, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.font = tkfont.Font(family="Noto Sans CJK SC", size=17)
        self.small_font = tkfont.Font(family="Noto Sans CJK SC", size=11)
        self.streams = []
        self.last_size = (0, 0)
        self.last_t = time.monotonic()
        self.next_red = self.last_t + random.uniform(5, 9)
        self.red_until = 0
        self.red_entry = None
        self.show_meaning = True
        self.paused = False
        self.vocab_win = None
        root.bind("<KeyPress>", self.keypress)
        root.bind("<Escape>", lambda e: root.destroy())
        root.bind("<Configure>", self.on_resize)
        self.frame()

    def on_resize(self, _event=None):
        self.last_size = (0, 0)

    def make_stream(self, x, height):
        return {"x": x, "y": random.uniform(-height, 0), "speed": random.uniform(27, 49),
                "length": random.randint(7, 17), "chars": [random.choice(POOL) for _ in range(20)],
                "active": random.random() < .85}

    def keypress(self, event):
        k = event.keysym.lower()
        if k in ("q", "escape"):
            self.root.destroy()
        elif k == "p":
            self.show_meaning = not self.show_meaning
        elif k == "v":
            self.show_vocab()

    def show_vocab(self):
        if self.vocab_win and self.vocab_win.winfo_exists():
            self.vocab_win.lift(); return
        win = tk.Toplevel(self.root)
        self.vocab_win = win
        win.title("汉字词汇 — Hanzi vocabulary")
        win.geometry("760x620")
        frame = tk.Frame(win, bg=BG); frame.pack(fill="both", expand=True)
        text = tk.Text(frame, bg=BG, fg=TEAL, insertbackground=MINT, wrap="none", font=("Noto Sans CJK SC", 12), padx=12, pady=12)
        sy = tk.Scrollbar(frame, orient="vertical", command=text.yview); sx = tk.Scrollbar(frame, orient="horizontal", command=text.xview)
        text.configure(yscrollcommand=sy.set, xscrollcommand=sx.set)
        text.grid(row=0, column=0, sticky="nsew"); sy.grid(row=0, column=1, sticky="ns"); sx.grid(row=1, column=0, sticky="ew")
        frame.rowconfigure(0, weight=1); frame.columnconfigure(0, weight=1)
        for category, entries in VOCAB:
            text.insert("end", f"\n── {category} ──\n", "head")
            for hanzi, pinyin, meaning in entries:
                text.insert("end", f"  {hanzi:<8}  {pinyin:<30}  {meaning}\n")
        text.tag_config("head", foreground=MINT, font=("Noto Sans CJK SC", 12, "bold"))
        text.configure(state="disabled")

    def draw_glow_text(self, x, y, char, color, is_red=False, tail_strength=1.0):
        # Layered halo behind the glyph; the foreground glyph is always drawn last
        # at full brightness so the glow never muddies the character itself.
        if is_red:
            outer, mid, inner = "#3b1915", "#733024", "#b13b29"
        else:
            outer, mid, inner = HALO_OUTER, HALO_MID, HALO_INNER
        # The surrounding layers are deliberately broad and faint, like a small
        # comet-like aura rather than separate dots beside each character.
        for dx, dy in [(-3,0),(3,0),(0,-3),(0,3),(-2,-2),(2,-2),(-2,2),(2,2)]:
            self.canvas.create_text(x+dx, y+dy, text=char, fill=outer, font=self.font)
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            self.canvas.create_text(x+dx, y+dy, text=char, fill=mid, font=self.font)
        self.canvas.create_text(x, y, text=char, fill=color, font=self.font)

    def frame(self):
        now = time.monotonic()
        dt = min(now - self.last_t, .08)
        self.last_t = now
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        if (w, h) != self.last_size and w > 20 and h > 20:
            self.last_size = (w, h)
            step = max(22, self.font.measure("中") + 2)
            self.streams = [self.make_stream(x, h) for x in range(12, w, step)]
        if now >= self.next_red and now >= self.red_until:
            self.red_entry = random.choice([entry for _, entries in VOCAB for entry in entries])
            self.red_column = random.choice(self.streams)["x"] if self.streams else 12
            self.red_until = now + 10.5
            self.next_red = now + random.uniform(9, 15)
        self.canvas.delete("all")
        if not self.paused:
            for stream in self.streams:
                if not stream["active"]:
                    if random.random() < .025:
                        stream.update(self.make_stream(stream["x"], h))
                    continue
                stream["y"] += stream["speed"] * dt
                for tail in range(stream["length"]):
                    y = stream["y"] - tail * 22
                    if y < -22 or y > h - 60:
                        continue
                    ch = stream["chars"][tail]
                    color = MINT if tail == 0 else (TEAL if tail < 3 else DIM)
                    # A red vocabulary highlight is a visible word, not an unrelated glyph.
                    if self.red_entry and now < self.red_until and int(stream["x"]) == int(self.red_column) and tail == 0:
                        ch, color = self.red_entry[0], RED
                    self.draw_glow_text(stream["x"], y, ch, color, color == RED, max(.35, 1 - tail / max(1, stream["length"])))
                if stream["y"] - stream["length"] * 22 > h:
                    stream.update(self.make_stream(stream["x"], h))
                    stream["active"] = random.random() < .82
        if self.red_entry and now < self.red_until and self.show_meaning:
            line = f"红字  {self.red_entry[0]}   {self.red_entry[1]}   —   {self.red_entry[2]}"
            self.canvas.create_text(16, h-42, anchor="w", text=line, fill="#a84a38", font=self.small_font)
        self.canvas.create_text(16, h-17, anchor="w", text="汉字矩阵   V: vocabulary key    P: red-word meaning on/off    Q/Esc: quit", fill="#527d73", font=self.small_font)
        self.root.after(40, self.frame)  # 25 fps, smooth fractional-pixel movement

def main():
    root = tk.Tk()
    HanziMatrix(root)
    root.mainloop()

if __name__ == "__main__":
    main()
