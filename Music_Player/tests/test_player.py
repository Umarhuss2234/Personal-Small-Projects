import contextlib
import io
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import wave

os.environ["SDL_AUDIODRIVER"] = "dummy"

import main as player


class PlayerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)

    def run_player(self, commands):
        output = io.StringIO()
        with patch("builtins.input", side_effect=commands), contextlib.redirect_stdout(output):
            result = player.main(["--music-dir", str(self.folder)])
        self.assertFalse(player.pygame.mixer.get_init())
        return result, output.getvalue()

    def make_wav(self):
        with wave.open(str(self.folder / "test.wav"), "wb") as audio:
            audio.setparams((1, 2, 22050, 0, "NONE", "not compressed"))
            audio.writeframes(b"\0\0" * 22050 * 10)

    def test_empty_folder(self):
        result, output = self.run_player([])
        self.assertEqual(result, 0)
        self.assertIn("No songs found", output)

    def test_play_pause_resume_stop_and_invalid_selection(self):
        self.make_wav()
        result, output = self.run_player(["abc", "0", "2", "1", "p", "r", "s", "q"])
        self.assertEqual(result, 0)
        for expected in ("valid song number", "Choose a number", "Now playing", "Paused", "Resumed", "Stopped"):
            self.assertIn(expected, output)

    def test_quit_during_playback(self):
        self.make_wav()
        self.assertEqual(self.run_player(["1", "q"])[0], 0)

    def test_bad_audio_returns_to_menu(self):
        (self.folder / "broken.mp3").write_bytes(b"not audio")
        result, output = self.run_player(["1", "q"])
        self.assertEqual(result, 0)
        self.assertIn("Could not play", output)

    def test_missing_folder(self):
        self.folder = self.folder / "missing"
        self.assertEqual(self.run_player([])[0], 1)

    def test_filter_and_sort(self):
        for name in ("b.MP3", "A.wav", "notes.txt"):
            (self.folder / name).touch()
        (self.folder / "directory.mp3").mkdir()
        self.assertEqual([p.name for p in player.find_songs(self.folder)], ["A.wav", "b.MP3"])


if __name__ == "__main__":
    unittest.main()
