# Python Music Player

A terminal music player based on [Bro Code's tutorial](https://www.youtube.com/watch?v=xf71dRBRP6o).
Choose a numbered song, then pause, resume, or stop playback.

## Run on Windows

Open PowerShell in `Music_Player`:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

The virtual environment is already installed in this workspace, so you can use
just the last command. Place your own MP3 files in `music` first.

To use another folder:

```powershell
.\.venv\Scripts\python.exe main.py --music-dir "C:\Users\you\Music"
```

## Controls

- Enter a song number to play it.
- `P`: pause.
- `R`: resume.
- `S`: stop and return to the list.
- `Q`: quit from either prompt.
- `Ctrl+C`: exit.

After a song ends, press Enter to return to the list. The terminal waits for input.

## Tutorial notes

The video's opening and final preview frames were inspected to verify its terminal
interface, numbered MP3 list, and P/R/S controls. Captions were unavailable; this
is an independent implementation of those features, not an exact code transcription.

This version adds input validation, useful file/audio error messages, a configurable
music folder, WAV/OGG support, and clean shutdown. It uses `pygame-ce`, which provides
the `pygame` import used by the tutorial and supports this workspace's Python 3.14.
Your earlier `python/hello_world.py` exercise is still available.

## Checks

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Tests use a temporary generated WAV and SDL's dummy audio driver; no speakers or
downloaded songs are required.
