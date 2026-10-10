#!/usr/bin/env python3
"""hanzi-matrix: a green Chinese-character cascade with a built-in vocabulary key.

Usage:
  python3 hanzi-matrix.py          # animated cascade
  python3 hanzi-matrix.py --vocab  # vocabulary key only

During animation: V = vocabulary key, Q or Esc = quit.
In vocabulary mode: Q or Esc = return/quit, arrows or PgUp/PgDn = scroll.
"""
import argparse
import curses
import locale
import random
import sys
import time

VOCAB = [
    ("Desktop & navigation", [
        ("桌面", "zhuōmiàn", "desktop"),
        ("窗口", "chuāngkǒu", "window"),
        ("任务栏", "rènwùlán", "taskbar"),
        ("菜单", "càidān", "menu"),
        ("图标", "túbiāo", "icon"),
        ("文件", "wénjiàn", "file"),
        ("文件夹", "wénjiànjiā", "folder"),
        ("回收站", "huíshōuzhàn", "trash / recycle bin"),
        ("快捷方式", "kuàijié fāngshì", "shortcut"),
        ("搜索", "sōusuǒ", "search"),
        ("帮助", "bāngzhù", "help"),
    ]),
    ("Settings & display", [
        ("设置", "shèzhì", "settings"),
        ("系统", "xìtǒng", "system"),
        ("个性化", "gèxìnghuà", "personalization"),
        ("显示", "xiǎnshì", "display / show"),
        ("显示设置", "xiǎnshì shèzhì", "display settings"),
        ("分辨率", "fēnbiànlǜ", "resolution"),
        ("亮度", "liàngdù", "brightness"),
        ("字体", "zìtǐ", "font"),
        ("字体大小", "zìtǐ dàxiǎo", "font size"),
        ("背景", "bèijǐng", "background"),
        ("本地图片", "běndì túpiàn", "local pictures"),
        ("选择", "xuǎnzé", "select / choose"),
        ("应用", "yìngyòng", "apply; application (context-dependent)"),
    ]),
    ("Network & wireless", [
        ("网络", "wǎngluò", "network"),
        ("无线网络", "wúxiàn wǎngluò", "wireless network"),
        ("无线", "wúxiàn", "wireless"),
        ("Wi-Fi", "wài fài", "Wi-Fi (often written Wi-Fi)"),
        ("连接", "liánjiē", "connect / connection"),
        ("已连接", "yǐ liánjiē", "connected"),
        ("断开连接", "duànkāi liánjiē", "disconnect"),
        ("蓝牙", "lányá", "Bluetooth"),
        ("服务器", "fúwùqì", "server"),
        ("密码", "mìmǎ", "password"),
    ]),
    ("Files & software", [
        ("打开", "dǎkāi", "open"),
        ("关闭", "guānbì", "close"),
        ("保存", "bǎocún", "save"),
        ("删除", "shānchú", "delete"),
        ("复制", "fùzhì", "copy"),
        ("粘贴", "zhāntiē", "paste"),
        ("安装", "ānzhuāng", "install"),
        ("卸载", "xièzài", "uninstall"),
        ("更新", "gēngxīn", "update"),
        ("软件", "ruǎnjiàn", "software"),
        ("文件名", "wénjiànmíng", "filename"),
        ("下载", "xiàzài", "download"),
        ("上传", "shàngchuán", "upload"),
    ]),
    ("Terminal & system messages", [
        ("终端", "zhōngduān", "terminal"),
        ("命令", "mìnglìng", "command"),
        ("输入", "shūrù", "input / enter"),
        ("输出", "shūchū", "output"),
        ("回车", "huíchē", "Enter key"),
        ("请输入密码", "qǐng shūrù mìmǎ", "please enter your password"),
        ("密码错误", "mìmǎ cuòwù", "incorrect password"),
        ("错误", "cuòwù", "error"),
        ("正常", "zhèngcháng", "normal / working properly"),
        ("无法访问", "wúfǎ fǎngwèn", "cannot access"),
        ("没有那个文件或目录", "méiyǒu nàge wénjiàn huò mùlù", "no such file or directory"),
        ("重启", "chóngqǐ", "restart / reboot"),
        ("关机", "guānjī", "shut down"),
    ]),
    ("Everyday expressions", [
        ("你好", "nǐ hǎo", "hello"),
        ("你好吗？", "nǐ hǎo ma?", "how are you?"),
        ("我很好", "wǒ hěn hǎo", "I'm doing well"),
        ("谢谢", "xièxie", "thank you"),
        ("不客气", "bú kèqi", "you're welcome"),
        ("再见", "zàijiàn", "goodbye"),
        ("请", "qǐng", "please"),
        ("没问题", "méi wèntí", "no problem"),
        ("我明白了", "wǒ míngbai le", "I understand now"),
        ("请再说一遍", "qǐng zài shuō yí biàn", "please say that again"),
        ("看这个！", "kàn zhège!", "look at this!"),
        ("看这里！", "kàn zhèlǐ!", "look here!"),
        ("小心脚下", "xiǎoxīn jiǎoxià", "watch your step / mind your step"),
        ("小心站台间隙", "xiǎoxīn zhàntái jiànxì", "mind the platform gap"),
        ("怎么了？", "zěnme le?", "what's wrong? / what's up?"),
        ("我不知道", "wǒ bù zhīdào", "I don't know"),
        ("真的？", "zhēn de?", "really?"),
        ("当然", "dāngrán", "of course"),
    ]),
]

# Character pool is drawn from the vocabulary above, emphasizing common desktop terms.
POOL = list("设置系统网络无线连接密码显示字体背景图片本地文件文件夹桌面窗口菜单图标任务栏搜索帮助打开关闭保存删除复制粘贴安装更新软件下载上传终端命令输入输出回车错误正常重启关机你好谢谢再见请看这里注意小心间隙服务器蓝牙个性化分辨率亮度选择应用请输入账户用户安全数据电脑信息权限语言中文简体")


def draw_text(stdscr, y, x, text, attr=0, max_x=None):
    """Safely draw text, avoiding curses errors at screen edges."""
    h, w = stdscr.getmaxyx()
    if y < 0 or y >= h or x < 0 or x >= w:
        return
    if max_x is None:
        max_x = w - x
    try:
        stdscr.addnstr(y, x, text, max(0, min(max_x, w - x - 1)), attr)
    except curses.error:
        pass


def vocab_lines():
    lines = []
    for title, entries in VOCAB:
        lines.append((title, None))
        for hanzi, pinyin, english in entries:
            lines.append((f"  {hanzi:<8} {pinyin:<34} {english}", "entry"))
        lines.append(("", None))
    return lines


def show_vocab(stdscr, return_to_animation=False):
    curses.curs_set(0)
    offset = 0
    lines = vocab_lines()
    while True:
        stdscr.erase()
        h, w = stdscr.getmaxyx()
        draw_text(stdscr, 0, 1, "汉字词汇 KEY  |  Hanzi vocabulary", curses.A_BOLD | curses.color_pair(2))
        draw_text(stdscr, 1, 1, "Chinese characters     Pinyin (tones)                         English", curses.A_DIM)
        available = max(1, h - 4)
        for row, item in enumerate(lines[offset:offset + available], start=2):
            content, kind = item
            if kind is None and content:
                draw_text(stdscr, row, 1, f"── {content} ──", curses.A_BOLD | curses.color_pair(2))
            else:
                draw_text(stdscr, row, 1, content, curses.color_pair(1))
        footer = "↑/↓ or PgUp/PgDn: scroll   V: back to animation   Q/Esc: " + ("return" if return_to_animation else "quit")
        draw_text(stdscr, h - 1, 1, footer, curses.A_DIM)
        stdscr.refresh()
        key = stdscr.getch()
        if key in (ord('q'), ord('Q'), 27):
            return False
        if key in (ord('v'), ord('V')) and return_to_animation:
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
    stdscr.timeout(60)
    if curses.has_colors():
        curses.start_color()
        try:
            curses.use_default_colors()
            curses.init_pair(1, curses.COLOR_GREEN, -1)
            curses.init_pair(2, curses.COLOR_GREEN, -1)
            curses.init_pair(3, curses.COLOR_GREEN, -1)
        except curses.error:
            curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
            curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
            curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    streams = []
    last_size = (0, 0)
    frame = 0
    while True:
        h, w = stdscr.getmaxyx()
        if (h, w) != last_size:
            streams = []
            # Use every other column: most Han characters occupy two terminal cells.
            for x in range(0, max(1, w - 1), 2):
                streams.append({"x": x, "y": random.randint(-h, 0), "speed": random.choice([1, 1, 1, 2]), "length": random.randint(4, max(5, min(16, h))), "active": random.random() < 0.55})
            last_size = (h, w)
        stdscr.erase()
        for s in streams:
            if not s["active"] and random.random() < 0.025:
                s["active"] = True
                s["y"] = random.randint(-h, 0)
            if not s["active"]:
                continue
            y = s["y"]
            for tail in range(s["length"]):
                yy = y - tail
                if 0 <= yy < h - 1:
                    ch = random.choice(POOL)
                    if tail == 0:
                        attr = curses.color_pair(1) | curses.A_BOLD
                    elif tail < 3:
                        attr = curses.color_pair(1)
                    else:
                        attr = curses.color_pair(1) | curses.A_DIM
                    try:
                        stdscr.addstr(yy, s["x"], ch, attr)
                    except curses.error:
                        pass
            s["y"] += s["speed"]
            if s["y"] - s["length"] > h:
                s["y"] = random.randint(-h, -1)
                s["active"] = random.random() < 0.7
        draw_text(stdscr, h - 1, 1, "汉字矩阵  |  V: vocabulary key   Q/Esc: quit", curses.A_DIM)
        stdscr.refresh()
        frame += 1
        key = stdscr.getch()
        if key in (ord('q'), ord('Q'), 27):
            break
        if key in (ord('v'), ord('V')):
            stdscr.nodelay(False)
            back = show_vocab(stdscr, return_to_animation=True)
            if not back:
                break
            stdscr.nodelay(True)
            stdscr.timeout(60)
            last_size = (0, 0)
        time.sleep(0.015)


def main():
    parser = argparse.ArgumentParser(description="Green Chinese-character cascade with a desktop vocabulary key")
    parser.add_argument("--vocab", action="store_true", help="show vocabulary key without animation")
    args = parser.parse_args()
    try:
        locale.setlocale(locale.LC_ALL, "")
    except locale.Error:
        pass
    if not sys.stdout.isatty():
        print("Please run hanzi-matrix inside a UTF-8 terminal.")
        return 1
    def app(stdscr):
        if curses.has_colors():
            curses.start_color()
            try:
                curses.use_default_colors()
                curses.init_pair(1, curses.COLOR_GREEN, -1)
                curses.init_pair(2, curses.COLOR_GREEN, -1)
            except curses.error:
                curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
                curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        if args.vocab:
            show_vocab(stdscr, return_to_animation=False)
        else:
            animate(stdscr)
    try:
        curses.wrapper(app)
    except KeyboardInterrupt:
        pass
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
