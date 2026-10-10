#!/usr/bin/env python3
"""Hanzi Matrix: falling Chinese characters with a vocabulary key.

Run:
  python3 hanzi-matrix.py
  python3 hanzi-matrix.py --vocab

During animation: V opens vocabulary, P toggles red-word meanings, Q or Esc quits.
"""
import argparse
import curses
import random
import time

VOCAB = [
    ("Desktop & navigation", [
        ("桌面", "zhuōmiàn", "desktop"), ("窗口", "chuāngkǒu", "window"),
        ("任务栏", "rènwùlán", "taskbar"), ("菜单", "càidān", "menu"),
        ("图标", "túbiāo", "icon"), ("文件", "wénjiàn", "file"),
        ("文件夹", "wénjiànjiā", "folder"), ("回收站", "huíshōuzhàn", "recycle bin"),
        ("快捷方式", "kuàijié fāngshì", "shortcut"), ("搜索", "sōusuǒ", "search"),
        ("帮助", "bāngzhù", "help"),
    ]),
    ("Settings & display", [
        ("设置", "shèzhì", "settings"), ("系统", "xìtǒng", "system"),
        ("个性化", "gèxìnghuà", "personalization"), ("显示", "xiǎnshì", "display"),
        ("显示设置", "xiǎnshì shèzhì", "display settings"),
        ("分辨率", "fēnbiànlǜ", "resolution"), ("亮度", "liàngdù", "brightness"),
        ("字体", "zìtǐ", "font"), ("字体大小", "zìtǐ dàxiǎo", "font size"),
        ("背景", "bèijǐng", "background"), ("本地图片", "běndì túpiàn", "local pictures"),
        ("选择", "xuǎnzé", "select / choose"), ("应用", "yìngyòng", "apply / application"),
    ]),
    ("Network & wireless", [
        ("网络", "wǎngluò", "network"), ("无线网络", "wúxiàn wǎngluò", "wireless network"),
        ("无线", "wúxiàn", "wireless"), ("连接", "liánjiē", "connect / connection"),
        ("已连接", "yǐ liánjiē", "connected"), ("断开连接", "duànkāi liánjiē", "disconnect"),
        ("蓝牙", "lányá", "Bluetooth"), ("服务器", "fúwùqì", "server"),
        ("密码", "mìmǎ", "password"),
    ]),
    ("Files & software", [
        ("打开", "dǎkāi", "open"), ("关闭", "guānbì", "close"), ("保存", "bǎocún", "save"),
        ("删除", "shānchú", "delete"), ("复制", "fùzhì", "copy"), ("粘贴", "zhāntiē", "paste"),
        ("安装", "ānzhuāng", "install"), ("卸载", "xièzài", "uninstall"),
        ("更新", "gēngxīn", "update"), ("软件", "ruǎnjiàn", "software"),
        ("文件名", "wénjiànmíng", "filename"), ("下载", "xiàzài", "download"),
        ("上传", "shàngchuán", "upload"),
    ]),
    ("Terminal & system messages", [
        ("终端", "zhōngduān", "terminal"), ("命令", "mìnglìng", "command"),
        ("输入", "shūrù", "input / enter"), ("输出", "shūchū", "output"),
        ("回车", "huíchē", "Enter key"), ("请输入密码", "qǐng shūrù mìmǎ", "please enter your password"),
        ("密码错误", "mìmǎ cuòwù", "incorrect password"), ("错误", "cuòwù", "error"),
        ("正常", "zhèngcháng", "normal / working"), ("无法访问", "wúfǎ fǎngwèn", "cannot access"),
        ("没有那个文件或目录", "méiyǒu nàge wénjiàn huò mùlù", "no such file or directory"),
        ("重启", "chóngqǐ", "restart"), ("关机", "guānjī", "shut down"),
    ]),
    ("Everyday expressions", [
        ("你好", "nǐ hǎo", "hello"), ("你好吗？", "nǐ hǎo ma?", "how are you?"),
        ("我很好", "wǒ hěn hǎo", "I'm doing well"), ("谢谢", "xièxie", "thank you"),
        ("不客气", "bú kèqi", "you're welcome"), ("再见", "zàijiàn", "goodbye"),
        ("请", "qǐng", "please"), ("没问题", "méi wèntí", "no problem"),
        ("我明白了", "wǒ míngbai le", "I understand"), ("请再说一遍", "qǐng zài shuō yí biàn", "please say that again"),
        ("看这个！", "kàn zhège!", "look at this!"), ("看这里！", "kàn zhèlǐ!", "look here!"),
        ("小心脚下", "xiǎoxīn jiǎoxià", "watch your step"),
        ("小心站台间隙", "xiǎoxīn zhàntái jiànxì", "mind the platform gap"),
        ("怎么了？", "zěnme le?", "what's wrong?"), ("我不知道", "wǒ bù zhīdào", "I don't know"),
        ("真的？", "zhēn de?", "really?"), ("当然", "dāngrán", "of course"),
    ]),
]
POOL = list("设置系统网络无线连接密码显示字体背景图片本地文件文件夹桌面窗口菜单图标任务栏搜索帮助打开关闭保存删除复制粘贴安装更新软件下载上传终端命令输入输出回车错误正常重启关机你好谢谢再见请看这里注意小心间隙服务器蓝牙个性化分辨率亮度选择应用请输入账户用户安全数据电脑信息权限语言中文简体，。！？；：、（）《》「」『』…—·0123456789")

def safe_add(stdscr, y, x, text, attr=0):
    h, w = stdscr.getmaxyx()
    if y < 0 or y >= h or x < 0 or x >= w - 1:
        return
    try:
        stdscr.addnstr(y, x, text, max(0, w - x - 1), attr)
    except curses.error:
        pass

def vocab_lines():
    result = []
    for category, entries in VOCAB:
        result.append((f"── {category} ──", True))
        result.extend((f"  {hanzi:<8} {pinyin:<32} {english}", False)
                      for hanzi, pinyin, english in entries)
        result.append(("", False))
    return result

def show_vocab(stdscr, return_to_animation=False):
    curses.curs_set(0)
    offset = 0
    lines = vocab_lines()
    while True:
        stdscr.erase()
        h, w = stdscr.getmaxyx()
        safe_add(stdscr, 0, 1, "汉字词汇 KEY | Hanzi vocabulary", curses.A_BOLD | curses.color_pair(2))
        safe_add(stdscr, 1, 1, "Chinese characters     Pinyin (tones)                     English", curses.A_DIM)
        available = max(1, h - 4)
        for row, (content, heading) in enumerate(lines[offset:offset + available], 2):
            safe_add(stdscr, row, 1, content,
                     curses.A_BOLD | curses.color_pair(2) if heading else curses.color_pair(1))
        safe_add(stdscr, h - 1, 1, "↑/↓ or PgUp/PgDn: scroll   V: back   Q/Esc: quit", curses.A_DIM)
        stdscr.refresh()
        key = stdscr.getch()
        if key in (ord("q"), ord("Q"), 27):
            return False
        if key in (ord("v"), ord("V")) and return_to_animation:
            return True
        if key == curses.KEY_DOWN:
            offset = min(max(0, len(lines) - available), offset + 1)
        elif key == curses.KEY_UP:
            offset = max(0, offset - 1)
        elif key == curses.KEY_NPAGE:
            offset = min(max(0, len(lines) - available), offset + available)
        elif key == curses.KEY_PPAGE:
            offset = max(0, offset - available)

def animate(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(35)
    if curses.has_colors():
        curses.start_color()
        try:
            curses.use_default_colors()
            if curses.COLORS >= 256:
                curses.init_pair(1, 37, -1)   # teal trail
                curses.init_pair(2, 157, -1)  # mint highlight
                curses.init_pair(3, 202, -1)  # blood orange
            else:
                curses.init_pair(1, curses.COLOR_CYAN, -1)
                curses.init_pair(2, curses.COLOR_GREEN, -1)
                curses.init_pair(3, curses.COLOR_RED, -1)
        except curses.error:
            curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
            curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
            curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

    def make_stream(x, height):
        length = random.randint(7, max(8, min(18, height)))
        return {
            "x": x, "y": random.randint(-height, 0), "speed": 1,
            "chars": [random.choice(POOL) for _ in range(length)],
            "length": length, "active": random.random() < 0.84,
        }

    streams = []
    last_size = (0, 0)
    next_red_time = time.monotonic() + 5
    red_until = 0.0
    red_position = None
    red_entry = None
    show_red_meaning = True

    while True:
        height, width = stdscr.getmaxyx()
        if (height, width) != last_size:
            streams = [make_stream(x, height) for x in range(0, max(1, width - 1), 2)]
            last_size = (height, width)

        now = time.monotonic()
        if now >= next_red_time and now >= red_until:
            candidates = [(i, j) for i, stream in enumerate(streams) if stream["active"]
                          for j in range(stream["length"])
                          if 0 <= stream["y"] - j < height - 2]
            if candidates:
                red_position = random.choice(candidates)
                red_entry = random.choice([entry for _, entries in VOCAB for entry in entries])
                red_until = now + 2.8
                next_red_time = now + random.uniform(9, 15)

        stdscr.erase()
        for i, stream in enumerate(streams):
            if not stream["active"]:
                if random.random() < 0.025:
                    stream.update(make_stream(stream["x"], height))
                continue

            for tail in range(stream["length"]):
                y = stream["y"] - tail
                if not 0 <= y < height - 1:
                    continue
                char = stream["chars"][tail]

                if red_position == (i, tail) and now < red_until and red_entry:
                    # Highlight an actual vocabulary term so its reading and
                    # meaning shown in the footer match the red text.
                    red_text = red_entry[0]
                    try:
                        stdscr.addstr(y, stream["x"], red_text, curses.color_pair(3) | curses.A_BOLD)
                    except curses.error:
                        pass
                    continue
                elif tail == 0:
                    attr = curses.color_pair(2) | curses.A_BOLD
                elif tail < 3:
                    attr = curses.color_pair(2) if tail == 1 else curses.color_pair(1)
                else:
                    attr = curses.color_pair(1) | curses.A_DIM
                try:
                    stdscr.addstr(y, stream["x"], char, attr)
                except curses.error:
                    pass

            stream["y"] += 1
            if stream["y"] - stream["length"] > height:
                stream.update(make_stream(stream["x"], height))
                stream["active"] = random.random() < 0.72

        if height >= 3 and show_red_meaning and red_entry and now < red_until:
            safe_add(stdscr, height - 2, 1,
                     f"红字 {red_entry[0]}  {red_entry[1]}  —  {red_entry[2]}",
                     curses.color_pair(3) | curses.A_DIM)
        safe_add(stdscr, height - 1, 1,
                 "汉字矩阵 | V: vocabulary key   P: red-word meaning on/off   Q/Esc: quit", curses.A_DIM)
        stdscr.refresh()
        key = stdscr.getch()
        if key in (ord("q"), ord("Q"), 27):
            break
        if key in (ord("p"), ord("P")):
            show_red_meaning = not show_red_meaning
        if key in (ord("v"), ord("V")):
            stdscr.nodelay(False)
            back = show_vocab(stdscr, return_to_animation=True)
            if not back:
                break
            stdscr.nodelay(True)
            stdscr.timeout(35)
            last_size = (0, 0)
        # Moderate refresh cadence: smoother than the original, but not excessively fast.
        time.sleep(0.075)

def main():
    parser = argparse.ArgumentParser(description="Chinese character cascade with vocabulary review")
    parser.add_argument("--vocab", action="store_true", help="show vocabulary key only")
    args = parser.parse_args()
    try:
        if args.vocab:
            curses.wrapper(lambda scr: show_vocab(scr, return_to_animation=False))
        else:
            curses.wrapper(animate)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
