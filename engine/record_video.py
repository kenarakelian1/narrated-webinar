#!/usr/bin/env python3
"""Record a narrated webinar as MP4: Playwright video + concatenated audio.

Project-driven: reads <project>/webinar.py for the title and segment order,
plays <project>/index.html headlessly through Chromium, and writes
<project>/<title-slug>.mp4. Segment durations are derived from the actual
<project>/audio/*.mp3 files via ffprobe — no hardcoded timings.
"""

import argparse
import re
import shutil
import subprocess
import sys
import threading
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

import build  # same engine dir

PORT = 8766
WIDTH = 1280
HEIGHT = 720


def slugify(title):
    slug = re.sub(r"[^a-z0-9]+", "-", (title or "").lower()).strip("-")
    return slug or "webinar"


def segment_ids(cfg):
    """Ordered segment ids as they appear in CHAPTERS."""
    ids = []
    for ch in cfg.CHAPTERS:
        for seg in ch["segments"]:
            ids.append(seg["id"])
    return ids


def probe_duration(path):
    out = subprocess.run(
        ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(path)],
        capture_output=True, text=True,
    )
    return float(out.stdout.strip())


def start_server(root):
    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *a, **k):
            super().__init__(*a, directory=str(root), **k)

        def log_message(self, *a):
            pass

    httpd = HTTPServer(("127.0.0.1", PORT), Handler)
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    return httpd


def concat_audio(audio_dir, ids, work_dir):
    """Concatenate segment MP3s into one WAV; return (wav_path, total_secs)."""
    concat_list = work_dir / "_concat.txt"
    concat_wav = work_dir / "_combined_audio.wav"
    total = 0.0
    with open(concat_list, "w") as f:
        for seg_id in ids:
            mp3 = audio_dir / f"{seg_id}.mp3"
            f.write(f"file '{mp3}'\n")
            total += probe_duration(mp3)
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_list), "-ac", "2", "-ar", "44100",
        str(concat_wav),
    ], check=True, capture_output=True)
    concat_list.unlink()
    return concat_wav, total


def record_browser(video_dir, total_secs):
    """Play the webinar in Playwright Chromium and capture a silent video."""
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--autoplay-policy=no-user-gesture-required",
                "--disable-features=TranslateUI",
                "--no-first-run",
            ],
        )
        context = browser.new_context(
            viewport={"width": WIDTH, "height": HEIGHT},
            record_video_dir=str(video_dir),
            record_video_size={"width": WIDTH, "height": HEIGHT},
        )
        page = context.new_page()
        page.goto(f"http://127.0.0.1:{PORT}/index.html", wait_until="networkidle")
        time.sleep(2)

        print("  Clicking play...")
        page.click("#play-btn")
        time.sleep(1)

        for attempt in range(3):
            time.sleep(2)
            disp = page.evaluate("""() => {
                const el = document.getElementById('time-display');
                return el ? el.textContent : 'N/A';
            }""")
            print(f"  Audio check {attempt + 1}: time display = {disp}")
            if disp and disp not in ("N/A", "0:00 / 0:00"):
                break

        wait_secs = total_secs + 8
        start_t = time.time()
        while time.time() - start_t < wait_secs:
            elapsed = time.time() - start_t
            print(f"  {int(elapsed) // 60}:{int(elapsed) % 60:02d} / "
                  f"{int(total_secs) // 60}:{int(total_secs) % 60:02d}  ",
                  end="\r", flush=True)
            time.sleep(2)

        print("\n  Playback complete.")
        context.close()
        browser.close()

    videos = list(video_dir.glob("*.webm"))
    if not videos:
        print("ERROR: No video file produced by Playwright")
        sys.exit(1)
    return videos[0]


def merge_video_audio(video_path, audio_path, out_path, audio_offset=3.1):
    """Mux Playwright's silent video with the concatenated audio.

    audio_offset: seconds before audio starts. Tied to the player's start
    sequence — the 600ms play→playSegment delay (player.js, the play-btn
    handler) plus start-screen fade and page load. Adjust if that changes.
    """
    subprocess.run([
        "ffmpeg", "-y",
        "-i", str(video_path),
        "-itsoffset", str(audio_offset), "-i", str(audio_path),
        "-c:v", "libx264", "-preset", "medium", "-crf", "23", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest", "-movflags", "+faststart",
        str(out_path),
    ], check=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--project", required=True,
                    help="project dir holding webinar.py, index.html, audio/")
    args = ap.parse_args()

    proj = Path(args.project).resolve()
    cfg = build.load_config(proj / "webinar.py")
    title = (getattr(cfg, "META", {}) or {}).get("title", "")
    out_path = proj / f"{slugify(title)}.mp4"
    audio_dir = proj / "audio"
    ids = segment_ids(cfg)

    print("=== Narrated Webinar Video Recorder ===\n")

    print("[1/4] Concatenating audio segments...")
    audio_wav, total_secs = concat_audio(audio_dir, ids, proj)
    print(f"  Combined audio: {total_secs:.1f}s across {len(ids)} segments")

    print(f"[2/4] Starting HTTP server on port {PORT}...")
    httpd = start_server(proj)
    time.sleep(0.5)

    video_dir = proj / "_playwright_video"
    video_dir.mkdir(exist_ok=True)
    print("[3/4] Recording browser playback (headless Chromium)...")
    try:
        video_path = record_browser(video_dir, total_secs)
        print(f"  Raw video: {video_path} "
              f"({video_path.stat().st_size / 1024 / 1024:.1f} MB)")
    finally:
        httpd.shutdown()

    print("[4/4] Merging video + audio into final MP4...")
    merge_video_audio(video_path, audio_wav, out_path)

    audio_wav.unlink(missing_ok=True)
    shutil.rmtree(video_dir, ignore_errors=True)

    print(f"\nDone! Video saved to: {out_path}")
    print(f"Size: {out_path.stat().st_size / 1024 / 1024:.1f} MB")


if __name__ == "__main__":
    main()
