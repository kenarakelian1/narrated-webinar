# narrated-webinar

A [Claude Code](https://claude.com/claude-code) skill for building **narrated,
audio-voiced HTML presentations** — story-driven walkthroughs with an ElevenLabs
voiceover, a player UI (chapter sidebar, play/pause, progress bar,
audio-synced auto-advance), bespoke animated CSS scenes, and an optional MP4
recording.

The deployable artifact is a plain static folder — `index.html` +
`audio/*.mp3` — that drops onto any static host.

## Why

Each webinar is **one config file**, `webinar.py`, that is the single source of
truth for chapters, segments, narration, *and* scenes. Because narration lives
next to the scene it belongs to, structure and voiceover can't drift — the
failure mode of keeping a separate "narration script" and "slide builder" in
sync by hand.

The reusable **engine** is project-agnostic; each webinar is a small **project
directory** holding `webinar.py` plus its generated outputs.

## Layout

```
SKILL.md                    workflow Claude follows when the skill is invoked
engine/
  build.py                  reads webinar.py → assembles index.html
  generate_audio.py         ElevenLabs TTS; --only for selective regen
  record_video.py           Playwright playback → MP4
  player.css                player chrome (sidebar, controls, progress, scene frame)
  player.js                 audio-sync engine, auto-advance, keyboard, chapter jump
  shell.html                HTML frame that scenes slot into
references/
  config-schema.md          the webinar.py contract
  scene-authoring.md         how to write a narration-synced CSS scene
xpost/
  webinar.py                a complete worked example (this skill, pitched)
  index.html, audio/, *.mp4 its built + recorded output
tests/                      pytest unit tests + a Playwright behavioral gate
```

## Usage

From a project directory containing `webinar.py`:

```bash
# 1. Generate narration MP3s (needs ELEVENLABS_API_KEY in env)
python engine/generate_audio.py --project <dir>
python engine/generate_audio.py --project <dir> --only id1,id2   # cheap re-roll

# 2. Build the static site
python engine/build.py --project <dir>            # → <dir>/index.html

# 3. (optional) Record an MP4
python engine/record_video.py --project <dir>     # → <dir>/<title-slug>.mp4
```

The engine never writes to its own directory — all output lands in the project
dir. A finished webinar is just `webinar.py` + `index.html` + `audio/*.mp3`
(+ an optional `.mp4`).

Start a new webinar by copying `xpost/webinar.py` and replacing
`META` / `VOICE` / `SCENES` / `CHAPTERS`. See `references/config-schema.md` for
the full contract and `references/scene-authoring.md` for authoring scenes.

## Requirements

- Python 3.8+
- An ElevenLabs API key in `ELEVENLABS_API_KEY` (for audio generation only)
- `playwright` + Chromium and `ffmpeg`/`ffprobe` (for video recording only)

Building HTML and running the tests need neither an API key nor network access.

## Tests

```bash
pip install pytest playwright
playwright install chromium
pytest -q
```

The suite covers the build/flatten contract, the audio-segment collection and
payload shaping, and a Playwright **behavioral gate** that replays the bundled
`xpost` example through the engine — asserting the sidebar populates, scenes
activate on play and chapter-jump, and narration-synced `timedClasses` fire on
time. The gate stubs `Audio` so it is deterministic and costs no API quota.

## License

The engine and skill are provided as-is. The bundled `xpost/` content is a
worked example, included only as an authoring reference.
