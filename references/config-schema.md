# `webinar.py` config schema

A narrated webinar is **one Python file** — `webinar.py` — that is the single
source of truth for structure, narration, and scenes. The engine reads it three
ways:

- `build.py` → assembles `index.html` from `META`, `SCENES`, and `CHAPTERS`.
- `generate_audio.py` → reads `narration` out of `CHAPTERS` and `VOICE` for TTS.
- `record_video.py` → reads `META["title"]` (output name) and the segment order.

Because narration lives next to the scene it belongs to, narration and
structure **cannot drift** — the failure mode the old hand-synced
`build_html.py` / `generate_audio.py` split was prone to.

The file must define four module-level names: `META`, `VOICE`, `SCENES`,
`CHAPTERS`.

---

## `META` — start screen, sidebar, and property lines

```python
META = {
    "title":          "Your Webinar Title",   # <title> + start-screen <h1>
    "eyebrow":        "YOUR BRAND",           # small caps above the title
    "subtitle":       "A one-line hook …",    # one-line start-screen subtitle
    "preview": [                              # the start-screen preview pillars
        {"num": "PART ONE",   "title": "First beat"},
        {"num": "PART TWO",   "title": "Second beat"},
        {"num": "PART THREE", "title": "Third beat"},
    ],
    "start_meta":     "10 minutes · narrated · 7 segments",  # under the play btn
    "property_line":  "© 2026 Your Org · …",   # start-screen footer (or "")
    "sidebar_eyebrow":"Series Label",          # small caps in the sidebar header
    "sidebar_title":  "Sidebar Title",         # sidebar header title
    "stage_property": "© 2026 Your Org",       # stage footer (or "")
}
```

(See `xpost/webinar.py` for these filled in with real content.)

All nine keys are **required** — `build.py` raises `KeyError` if one is missing.
Values may contain HTML entities (e.g. `&amp;`); they are injected verbatim.

`property_line` (start-screen footer) and `stage_property` (stage footer) are
where any copyright / confidentiality / domain line goes. Leave them empty if the
project has no branding requirement.

---

## `VOICE` — ElevenLabs settings

```python
VOICE = {
    "id":    "EXAVITQu4vr4xnSDxMaL",     # Sarah (the brand default)
    "model": "eleven_multilingual_v2",
    "settings": {
        "stability":         0.55,
        "similarity_boost":  0.8,
        "style":             0.22,
        "use_speaker_boost": True,
    },
}
```

`generate_audio.py` posts `{"text": …, "model_id": VOICE["model"],
"voice_settings": VOICE["settings"]}` to
`/v1/text-to-speech/<VOICE["id"]>`. To use a different voice, change `id`;
keep the settings unless the brand sound is intentionally changing.

---

## `SCENES` — bespoke visuals, keyed by name

```python
SCENES = {
    "email": {"html": "<…inner markup…>", "css": ".scene-email { … }"},
    "webinar": {"html": "…", "css": "…"},
    # … one entry per distinct scene …
}
```

- `html` is the **inner** markup only. The engine wraps it in
  `<div class="scene scene-NAME" data-scene="NAME"> … </div>`. Do **not**
  include that wrapper yourself.
- `css` is raw CSS text. The engine concatenates every used scene's CSS into one
  `<style>`, so **scope every selector under `.scene-NAME`** to avoid bleed.
- Only scenes referenced by a segment's `scene` key are emitted, in first-use
  order. An unused `SCENES` entry is silently ignored.

See `scene-authoring.md` for how to write one.

---

## `CHAPTERS` — structure + narration

```python
CHAPTERS = [
    {"number": 1, "title": "The Email Nobody Reads", "icon": "1", "segments": [
        {"id": "s1_email", "scene": "email",
         "narration": "You need to explain something …",
         "timedClasses": [{"at": 12, "addClass": "skimmed"},
                          {"at": 16.5, "addClass": "better"}]},
    ]},
    {"number": 2, "title": "Make a Narrated Webinar", "icon": "2", "segments": [
        {"id": "s2_webinar", "scene": "webinar",
         "narration": "Instead of drafting an email …"}],
    },
    # … chapter 3 …
]
```

### Chapter keys (all required)

| key | meaning |
|-----|---------|
| `number` | integer chapter number; used to group/highlight segments |
| `title` | chapter title, shown in the sidebar and the bottom bar |
| `icon` | short string shown in the sidebar bullet (the xpost example uses the number as a string, `"1"`…`"3"`) |
| `segments` | list of one or more segment dicts |

### Segment keys

| key | required | meaning |
|-----|----------|---------|
| `id` | ✅ | unique slug; the audio file is `audio/<id>.mp3` |
| `scene` | ✅ | which `SCENES` entry this segment displays |
| `narration` | ✅ | the spoken text; `generate_audio.py` voices it |
| `timedClasses` | optional | `[{"at": <seconds>, "addClass": "<class>"}]` — adds a class to the scene element once the segment audio passes `at` seconds (and removes it if you seek back). Used for in-scene state changes synced to narration. |
| `highlight` | optional | `{"selector": "<css>", "activeIndices": [int, …]}` — within the active scene, adds `.active` to the matched children at those indices and `.dim` to the rest. Used when one scene serves several narration beats. |

Multiple segments may share one `scene` (e.g. a single grid scene narrated in
several beats, each spotlighting different cards via `highlight`).

### Derived manifest

`build.py` flattens `CHAPTERS` into the two JSON blobs the player reads:

- **SEGMENTS** — `[{id, chapter, chapterTitle, title, scene, [highlight],
  [timedClasses]}]`, in document order. Auto-advance walks this list.
- **CHAPTERS** (player-side) — `[{num, title, icon, firstIdx}]`, where
  `firstIdx` is the index of that chapter's first segment. Clicking a sidebar
  chapter jumps to its `firstIdx`.

---

## Worked snippet — the xpost email scene

```python
CHAPTERS = [
    {"number": 1, "title": "The Email Nobody Reads", "icon": "1", "segments": [
        {"id": "s1_email",
         "scene": "email",
         "narration": ("You need to explain something — a new product, a "
                       "launch, an idea worth understanding. …"),
         "timedClasses": [{"at": 12,   "addClass": "skimmed"},
                          {"at": 16.5, "addClass": "better"}]},
    ]},
    # …
]
```

At 12 seconds of email audio the player adds `.skimmed` to `.scene-email`,
which the scene CSS uses to grey out the email and drop in the "SKIMMED"
stamp; at 16.5 seconds it adds `.better` to reveal the "there has to be a
better way" line — narration-synced state changes declared as data rather
than hardcoded in the engine.

---

## Engine invocation

Run from anywhere; `<dir>` is the project directory holding `webinar.py`.

```bash
# 1. Generate narration MP3s (needs ELEVENLABS_API_KEY in env)
python <skill>/engine/generate_audio.py --project <dir>
python <skill>/engine/generate_audio.py --project <dir> --only id1,id2  # cheap re-roll

# 2. Build the static site
python <skill>/engine/build.py --project <dir>        # → <dir>/index.html

# 3. (optional) Record an MP4
python <skill>/engine/record_video.py --project <dir> # → <dir>/<title-slug>.mp4
```

The engine never writes to its own directory — every output lands in
`<dir>`. A finished project is just `webinar.py` + `index.html` + `audio/*.mp3`
(+ an optional `.mp4`), a static site you can drop on any host.
