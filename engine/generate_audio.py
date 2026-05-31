#!/usr/bin/env python3
"""Generate webinar narration MP3s via ElevenLabs from a project's webinar.py."""
import argparse
import json
import os
import pathlib
import urllib.request

import build  # same engine dir


def collect_segments(cfg, only=None):
    items = []
    for ch in cfg.CHAPTERS:
        for seg in ch["segments"]:
            if only is None or seg["id"] in only:
                items.append((seg["id"], seg["narration"]))
    return items


def build_payload(voice, text):
    return json.dumps({
        "text": text,
        "model_id": voice["model"],
        "voice_settings": voice["settings"],
    }).encode("utf-8")


def generate_segment(api_key, voice, seg_id, text, out_dir):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice['id']}"
    req = urllib.request.Request(
        url, data=build_payload(voice, text),
        headers={"xi-api-key": api_key, "Content-Type": "application/json",
                 "Accept": "audio/mpeg"})
    out_path = out_dir / f"{seg_id}.mp3"
    with urllib.request.urlopen(req) as resp:
        out_path.write_bytes(resp.read())
    print(f"  {seg_id}.mp3 — {out_path.stat().st_size/1024:.0f} KB")
    return out_path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--only", help="comma-separated segment ids")
    args = ap.parse_args()

    api_key = os.environ.get("ELEVENLABS_API_KEY", "")
    if not api_key:
        raise SystemExit("ELEVENLABS_API_KEY not set")

    proj = pathlib.Path(args.project)
    cfg = build.load_config(proj / "webinar.py")
    out_dir = proj / "audio"
    out_dir.mkdir(exist_ok=True)
    only = set(args.only.split(",")) if args.only else None
    items = collect_segments(cfg, only)
    total = sum(len(t) for _, t in items)
    print(f"Characters: {total:,}  Segments: {len(items)}\n")
    for seg_id, text in items:
        generate_segment(api_key, cfg.VOICE, seg_id, text, out_dir)
    print(f"\nDone! {len(items)} segments → {out_dir}")


if __name__ == "__main__":
    main()
