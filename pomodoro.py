import argparse, time, os, sys, subprocess
from tomato_art import TOMATO

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base_path, relative_path)

RED = "\033[31m"
RESET = "\033[0m"

def print_tomato(color_on=True):
    if color_on:
        print(RED + TOMATO + RESET)
    else:
        print(TOMATO)

def parse_time(s):
    s = s.strip().lower()
    if not s:
        raise ValueError("Empty time value")

    if "h" in s:
        h, m = s.split("h", 1)
        hours = int(h) if h else 0
        minutes = int(m) if m else 0
        return float(hours * 60 + minutes)

    if s.endswith("m"):
        return float(s[:-1])

    return float(s)

def play_sound():
    return subprocess.Popen(
        ["mpg123", "-q", resource_path("tinker-ring.mp3")],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL,
    )

def start_timer(minutes, label, sound_on):
    total_seconds = int(minutes * 60)
    width = 20
    for remaining in range(total_seconds, 0, -1):
        elapsed = total_seconds - remaining
        filled = int(width * elapsed / total_seconds)
        bar = "-" * filled + " " * (width - filled)
        mins, secs = divmod(remaining, 60)
        print(f"\r[{bar}] {label}: {mins:02d}:{secs:02d}", end="", flush=True)
        time.sleep(1)
    bar = "-" * width
    print(f"\r[{bar}] {label}: 00:00", end="", flush=True)
    if sound_on:
        play_sound()
    input()

def build_parser():
    parser = argparse.ArgumentParser(
        prog="pomotimer",
        description="A simple CLI based pomodoro timer."
    )
    parser.add_argument("-w", "--work", default="25", help="work time, e.g. 0.5 or 25 or 1h45")
    parser.add_argument("-b", "--break-time", default="5", help="short break time, e.g. 0.15 or 15m")
    parser.add_argument("-l", "--long-break", default="15", help="long break time, e.g. 15")
    parser.add_argument("-s", "--sessions", type=int, default=4, help="number of work sessions before the long break")
    parser.add_argument("--no-color", action="store_true", help="disable colored output")
    parser.add_argument("--sound", choices=["on", "off"], default="on", help="enable or disable sound")
    parser.add_argument("-v", "--version", action="version", version="pomotimer 1.0.0") 
    return parser

def main():
    parser = build_parser()
    args = parser.parse_args()
    color_on = not args.no_color
    sound_on = args.sound == "on"

    print_tomato(color_on)
    print("Ctrl+C to exit")
    print("pomotimer -h for help")

    work_time = parse_time(args.work)
    break_time = parse_time(args.break_time)
    long_break_time = parse_time(args.long_break)
    sessions = args.sessions

    for i in range(sessions):
        start_timer(work_time, "Work", sound_on)

        if i < sessions - 1:
            start_timer(break_time, "Short break", sound_on)

    start_timer(long_break_time, "Long break", sound_on)
    print("Pomodoro cycle finished.")

main()
