"""Convert WebVTT to plain text.

Inspired by https://stackoverflow.com/a/52223298
"""

from pathlib import Path

import webvtt
from tqdm import tqdm


IN_DIR = "data/raw/transcripts"
OUT_DIR = Path("data/processed/transcripts")
OUT_DIR.mkdir(exist_ok=True, parents=True)

for file in tqdm(list(Path(IN_DIR).glob("*.vtt"))):
    vtt = webvtt.read(file)
    transcript = ""

    lines = []
    for line in vtt:
        # Strip the newlines from the end of the text.
        # Split the string if it has a newline in the middle
        # Add the lines to an array
        lines.extend(line.text.strip().splitlines())

    # Remove repeated lines
    previous = None
    for line in lines:
        if line == previous:
            continue
        transcript += " " + line
        previous = line

    # Write the transcript to a file
    out_file = OUT_DIR / f"{file.stem}.txt"
    out_file.write_text(transcript.strip())
