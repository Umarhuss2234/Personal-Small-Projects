"""A terminal music player inspired by Bro Code's Python tutorial."""

import argparse
import os
from pathlib import Path

os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

try:
    import pygame
except ImportError:
    raise SystemExit(
        "Missing pygame. Install dependencies with: python -m pip install -r requirements.txt"
    )


MUSIC_FOLDER = Path(__file__).resolve().parent / "music"
SUPPORTED_FORMATS = {".mp3", ".wav", ".ogg"}


def find_songs(folder):
    """Return supported audio files in a predictable, alphabetical order."""
    return sorted(
        (file for file in Path(folder).iterdir()
         if file.is_file() and file.suffix.lower() in SUPPORTED_FORMATS),
        key=lambda file: file.name.casefold(),
    )


def play_music(song):
    """Play one song until the listener stops it or quits."""
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        pygame.mixer.music.load(str(song))
        pygame.mixer.music.play()
    except (pygame.error, OSError) as error:
        print(f"Could not play {song.name}: {error}")
        return False

    print(f"\nNow playing: {song.name}")
    print("Commands: [P]ause, [R]esume, [S]top, [Q]uit")
    paused = False
    try:
        while True:
            command = input("> ").strip().lower()
            if command == "q":
                return True
            if command == "s":
                print("Stopped.")
                return False
            if not paused and not pygame.mixer.music.get_busy():
                print("Song finished. Returning to the song list.")
                return False
            if command == "p":
                pygame.mixer.music.pause()
                paused = True
                print("Paused.")
            elif command == "r":
                pygame.mixer.music.unpause()
                paused = False
                print("Resumed.")
            else:
                print("Enter P, R, S, or Q.")
    finally:
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()


def main(argv=None):
    parser = argparse.ArgumentParser(description="Play local music from your terminal.")
    parser.add_argument("--music-dir", type=Path, default=MUSIC_FOLDER,
                        help="Folder containing MP3, WAV, or OGG files")
    args = parser.parse_args(argv)
    try:
        while True:
            try:
                songs = find_songs(args.music_dir)
            except OSError as error:
                print(f"Cannot read music folder: {error}")
                return 1

            print("\n***** MP3 PLAYER *****")
            if not songs:
                print(f"No songs found. Add MP3, WAV, or OGG files to:\n{args.music_dir}")
                return 0

            print("My song list:")
            for number, song in enumerate(songs, start=1):
                print(f"{number}. {song.name}")

            choice = input("\nEnter the song # to play (or 'Q' to quit): ").strip()
            if choice.lower() == "q":
                return 0
            try:
                index = int(choice) - 1
            except ValueError:
                print("Enter a valid song number.")
                continue
            if not 0 <= index < len(songs):
                print(f"Choose a number from 1 to {len(songs)}.")
                continue
            if play_music(songs[index]):
                return 0
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")
        return 0
    finally:
        pygame.mixer.quit()


if __name__ == "__main__":
    raise SystemExit(main())
