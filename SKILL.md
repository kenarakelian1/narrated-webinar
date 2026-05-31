---
name: narrated-webinar
description: Use when the user wants to create a narrated, audio-voiced HTML presentation/webinar — a story-driven slideshow with ElevenLabs voiceover, a player UI (chapter sidebar, play/pause, progress, auto-advance), bespoke animated scenes, and optional MP4 recording. Triggers on "make a narrated webinar", "audio walkthrough", "voiced presentation", "webinar like the Compass one".
---

# Narrated Webinar

Build a narrated HTML+voice presentation using the bundled engine. The
deployable artifact is a static folder: `index.html` + `audio/*.mp3` (+ an
optional `.mp4`) — drop it on any static host.

A webinar is **one config file** — `webinar.py` — that is the single source of
truth for chapters, segments, narration, and scenes. Narration lives next to
the scene it belongs to, so structure and voiceover cannot drift.

## Engine (project-agnostic — do not edit per project)

| command | output |
|---------|--------|
| `python engine/generate_audio.py --project <dir> [--only id1,id2]` | `<dir>/audio/<id>.mp3` (needs `ELEVENLABS_API_KEY`) |
| `python engine/build.py --project <dir>` | `<dir>/index.html` |
| `python engine/record_video.py --project <dir>` | `<dir>/<title-slug>.mp4` (needs Playwright + ffmpeg) |

`<dir>` is the project directory containing `webinar.py`. The engine never
writes to its own directory.

## References (read these before authoring)

- `references/config-schema.md` — the exact `webinar.py` contract (META, VOICE,
  SCENES, CHAPTERS; `timedClasses` and `highlight`).
- `references/scene-authoring.md` — how to write a narration-synced CSS scene.
- `examples/compass/webinar.py` — a complete worked example (The Compass).

## Workflow

1. **Gather** — ask for source material (specs, marketing copy, playbooks) and
   the target project directory. **Enforce the citation rule:** every narration
   claim must trace to supplied source material; never fabricate facts, names,
   or citations (see the project's CLAUDE.md). Carry the required branding —
   copyright + `seicheadvisors.com` — into `META`'s property lines.
2. **Draft** — propose chapters/segments + narration text. The user reviews
   **before** any audio spend.
3. **Author scenes** — write bespoke scenes per `references/scene-authoring.md`,
   copying patterns from `examples/compass/webinar.py`. Read
   `references/config-schema.md` for the exact contract.
4. **Generate audio** — `generate_audio.py`; use `--only` for cheap re-rolls of
   changed segments.
5. **Build** — `build.py --project <dir>` → `index.html`. Iterate on scene CSS
   and rebuild freely; only audio costs API quota.
6. **Video (optional)** — `record_video.py --project <dir>` → MP4.
7. **Ship** — preview locally (`python -m http.server -d <dir>`), then deploy to
   Netlify Drop or Cloudflare Pages (DNS already configured for
   `seicheadvisors.com`).

## Starting a new webinar

Copy `examples/compass/webinar.py` into your project dir and replace
`META` / `VOICE` / `SCENES` / `CHAPTERS`. Keep one source of truth — narration
lives in `CHAPTERS`, never duplicated. `VOICE` defaults to Sarah
(`EXAVITQu4vr4xnSDxMaL`); change only if the brand voice is intentionally
different.

---

*© 2026 Seiche Advisors. All rights reserved. seicheadvisors.com — Confidential.*
