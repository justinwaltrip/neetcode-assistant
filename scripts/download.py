"""Download solution transcripts for NeetCode problems from YouTube.

To download only the captions for a video using the yt-dlp CLI,

```bash
yt-dlp --write-auto-sub --skip-download https://www.youtube.com/watch?v=3OamzN90kPg
```
"""

import json
from pathlib import Path

from yt_dlp import YoutubeDL

PROBLEMS_PATH = "data/raw/problems.json"
OUT_DIR = Path("data/raw/transcripts")
OUT_DIR.mkdir(exist_ok=True, parents=True)


with open(PROBLEMS_PATH) as f:
    problems = json.load(f)


video_links = [problem["video_link"] for problem in problems]

with YoutubeDL(
    {
        "writeautomaticsub": True,
        "skip_download": True,
        "outtmpl": f"{OUT_DIR}/%(id)s.%(ext)s",
    }
) as ydl:
    ydl.download(video_links)
