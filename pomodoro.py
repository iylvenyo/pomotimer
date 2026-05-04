import time
import os
import sys

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
    while True:
        try:
            parts = input("> ").strip().split()
            if len(parts) != 4:
                print("Enter exactly 4 values: work break long_break iterations")
                continue

            work_time = parse_time(parts[0])
            break_time = parse_time(parts[1])
            long_break_time = parse_time(parts[2])
            iterations = int(parts[3])

            if work_time <= 0 or break_time <= 0 or long_break_time <= 0:
                print("All times must be positive")
                continue
            if iterations < 1:
                print("Iterations must be a positive integer")
                continue

            return work_time, break_time, long_break_time, iterations
        except ValueError as e:
            print(f"Invalid input: {e}")

def play_sound():
    try:
        if sys.platform == "win32":
            import winsound
            winsound.MessageBeep()
        elif sys.platform == "darwin":
            os.system('afplay /System/Library/Sounds/Glass.aiff >/dev/null 2>&1 &')
        else:
            os.system('printf "\\a"')
    except Exception:
        pass

def start_timer(minutes, label):
    total_seconds = minutes * 60
    for remaining in range(total_seconds, 0, -1):
        mins, secs = divmod(remaining, 60)
        print(f"\r{label}: {mins:02d}:{secs:02d}", end="", flush=True)
        time.sleep(1)
    print(f"\r{label}: 00:00")

def main():
    print("Press Ctrl+C to exit during the countdown.")
    print(
        "Enter times for work, break, and long break.\n"
        "Use minutes, like 25 5 15 4, or mixed formats like 1h45 15m 30 3\n"
    )

    work_time, break_time, long_break_time, iterations = set_times()

    while True:
        for i in range(iterations):
            play_sound()
            start_timer(work_time, "Work")
            if i < iterations - 1:
                play_sound()
                start_timer(break_time, "Break")
        play_sound()
        start_timer(long_break_time, "Long break")

if __name__ == "__main__":
    main()
