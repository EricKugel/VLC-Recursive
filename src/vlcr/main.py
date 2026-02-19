import sys
from pathlib import Path
import random
import audio_metadata
import math
import tempfile
import subprocess

def main():
    # Ensure user typed in a path
    if len(sys.argv) == 1:
        print(f"Usage: {sys.argv[0]} DIR")
        quit()

    root = Path(sys.argv[1])

    # Can't delete tmp files, so add randomness
    filepath = Path.joinpath(Path(tempfile.gettempdir()), f"vlcr-playlist-{random.randint(0, 999_999)}.m3u")
    playlist_file = open(filepath, "w")
    playlist_file.write("#EXTM3U\n")

    # This creates the actual playlist entry string
    def create_entry(path):
        try:
            metadata = audio_metadata.load(path)
            # Duration in seconds
            duration = math.ceil(metadata["streaminfo"]["duration"])
            # VLC expects uris
            filepath = path.as_uri()
            try:
                title = metadata["tags"]["title"][0]
            except:
                # This song doesn't have a title
                title = str(path)
            # m3u standard
            return f"#EXTINF:{duration},{title}\n{filepath}\n"
        except audio_metadata.exceptions.UnsupportedFormat:
            # This is not an audio file
            return ""

    # Recursively finds all files.
    def recurse_dir(path):
        if path.is_file():
            entry = create_entry(path)
            playlist_file.write(entry)
        else:
            for child in path.iterdir():
                recurse_dir(child)
    recurse_dir(root)

    playlist_file.close()

    # Starts vlc with the playlist, decoupled from the process.
    subprocess.Popen(
        ["vlc", filepath.as_posix()],
        start_new_session=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )