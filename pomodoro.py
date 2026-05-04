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

    if 'h' in s:
        hours_part, rest = s.split('h', 1)
        hours = int(hours_part) if hours_part else 0
        minutes = int(rest) if rest else 0
        return hours * 60 + minutes

    if s.endswith('m'):
        return int(s[:-1])

    return int(s)

def set_times():
    parts = input("times (work break long iterations): ").strip().split()
    return parse_time(parts[0]), parse_time(parts[1]), parse_time(parts[2]), int(parts[3])

def play_sound():
    return subprocess.Popen(["mpg123", "-q", "--loop", "2", resource_path("tinker-ring.mp3")])

def start_timer(minutes, label):
    total_seconds = minutes * 60
    for remaining in range(total_seconds, 0, -1):
        mins, secs = divmod(remaining, 60)
        print(f"\r{label}: {mins:02d}:{secs:02d}", end="", flush=True)
        time.sleep(1)
    print(f"\r{label}: 00:00")

def build_parser():
    parser = argparse.ArgumentParser(
        prog="pomotimer",
        description="A simple CLI based pomodoro timer."
    )
    parser.add_argument("-w", "--work", default="25", help="work time, e.g. 25 or 1h45")
    parser.add_argument("-b", "--break-time", default="5", help="short break time, e.g. 5 or 15m")
    parser.add_argument("-l", "--long-break", default="15", help="long break time, e.g. 15")
    parser.add_argument("-s", "--sessions", type=int, default=4, help="number of work sessions before the long break")
    parser.add_argument("--no-color", action="store_true", help="disable colored output")
    parser.add_argument("--sound", choices=["on", "off"], default="on", help="enable or disable sound")
    parser.add_argument("-v", "--version", action="version", version="pomotimer 1.0") 
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

    while True:
        for i in range(sessions):
            start_timer(work_time, "Work")
            if sound_on:
                play_sound()

            if i < sessions - 1:
                start_timer(break_time, "Break")
                if sound_on:
                    play_sound()

        start_timer(long_break_time, "Long break")
        if sound_on:
            play_sound()
main()
