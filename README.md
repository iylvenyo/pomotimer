# pomotimer

A minimal CLI based pomodoro timer for time management.

## Install

Download the release binary for your platform and drop it into a folder that is already on your `PATH`.

### Linux
Common locations:
- `~/.local/bin`
- `/usr/local/bin`

### Windows
Common locations:
- `C:\Users\<you>\bin`
- `C:\Program Files\pomotimer`

If the folder is not already on your `PATH`, add it first, then restart your terminal.

## Usage

```bash
pomotimer [options]
```

If running from source:

```bash
python pomodoro.py [options]
```

## Options

- `-w`, `--work`: Work session length. Accepts minutes like `25` or mixed time like `1h45`.
- `-b`, `--break-time`: Short break length. Accepts minutes like `5` or `15m`.
- `-l`, `--long-break`: Long break length. Accepts minutes like `15`.
- `-s`, `--sessions`: Number of work sessions before the long break. Default: `4`.
- `--no-color`: Disable colored tomato output.
- `--sound on|off`: Enable or disable the alarm sound. Default: `on`.
- `-v`, `--version`: Show version information.

## Examples

```bash
pomotimer
pomotimer --work 50 --break-time 10 --long-break 20 --sessions 6
pomotimer --no-color --sound off
pomotimer --help
```

## Notes

- The tomato art is shown at startup.
- The alarm uses `tinker-ring.mp3` when sound is enabled.
- The timer runs until you stop it with `Ctrl+C`.
