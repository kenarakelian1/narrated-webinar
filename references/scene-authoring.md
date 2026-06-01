# Authoring a scene

A **scene** is the bespoke visual that animates behind one (or more) narration
segments. Scenes are hand-authored — the skill ships the *pattern* and the
bundled `xpost` example as a worked reference, not a generic scene library. Copy
an `xpost` scene that is close to what you want and reshape it.

The deal: you write inner HTML + scoped CSS; the engine handles activation,
audio sync, and teardown.

---

## Anatomy

A scene is one entry in `SCENES`:

```python
SCENES = {
    "email": {
        "html": "<div class='email-window'>…</div><div class='email-stamp'>SKIMMED</div>",
        "css":  ".scene-email .email-window { … }",
    },
}
```

- **`html` is inner markup only.** The engine wraps it in
  `<div class="scene scene-email" data-scene="email"> … </div>`. Never
  write that wrapper yourself, and never set the `id`s the player owns
  (`app`, `stage`, `play-btn`, `progress-fill`, etc.).
- **`css` must not bleed into other scenes.** All scene CSS is concatenated into
  a single `<style>`, so a bare `.window { … }` would leak everywhere. Avoid that
  one of two ways: descendant-scope under the wrapper —
  `.scene-email .email-window { … }` — **or** give every class a scene-unique
  prefix, `.email-window { … }` (the convention the `xpost` example uses:
  `.email-*`, `.web-*`, `.ship-*`). Pick one and stay consistent within a scene.

Only one scene is `.active` at a time. On segment change the engine removes
`.active` (and any applied `timedClasses`) from the previous scene and adds
`.active` to the new one.

---

## 1. Entrance animations key off `.scene-NAME.active`

Elements start in their "before" state; the `.active` class on the wrapper
triggers the transition. Stagger children with `transition-delay` choreographed
to the narration.

```css
.scene-webinar .web-out {
  opacity: 0;
  transform: translateX(26px);
  transition: opacity .7s ease, transform .7s ease;
}
.scene-webinar.active .web-out { opacity: 1; transform: translateX(0); }

/* Reveal each output as the narration names it. */
.scene-webinar.active .web-out-voice  { transition-delay: 15.5s; }  /* "…sends your script to ElevenLabs…" */
.scene-webinar.active .web-out-scene  { transition-delay: 19s; }    /* "…animates a bespoke scene…" */
.scene-webinar.active .web-out-player { transition-delay: 23s; }    /* "…wires it into a player…" */
```

That is the `xpost` webinar scene: three output chips reveal across the ~36s of
narration, each delay aligned to when the voice introduces that output. Time the
delays against your narration by reading the segment text and estimating
~150 words/minute.

---

## 2. Narration-synced state changes use `timedClasses`

When a scene must *change state* partway through a segment — not just enter —
declare it on the **segment**, not in CSS timing:

```python
{"id": "s1_email", "scene": "email",
 "narration": "…it lands in an inbox, gets half-skimmed… there's a better way…",
 "timedClasses": [{"at": 12,   "addClass": "skimmed"},
                  {"at": 16.5, "addClass": "better"}]}
```

The engine adds `.skimmed` to `.scene-email` once the segment audio passes 12s
(and removes it if the listener seeks back before 12s), then `.better` at 16.5s.
Your CSS reacts:

```css
.scene-email .email-window { transition: filter 1.2s ease, opacity 1.2s ease; }
.scene-email.skimmed .email-window { filter: grayscale(1) brightness(.82); opacity: .55; }
.scene-email.skimmed .email-stamp  { opacity: .9; }   /* the "SKIMMED" stamp drops in */
.scene-email.better  .email-better { opacity: 1; }    /* "there has to be a better way" */
```

Prefer `timedClasses` over CSS `transition-delay` when the change is tied to a
**moment in the narration** rather than the scene's entrance — it stays correct
even when the listener pauses, and it is removed cleanly on teardown.

`transition-delay` is for *entrance choreography*; `timedClasses` is for
*mid-segment state*.

---

## 3. One scene, several beats → `highlight`

If a single scene is narrated across several segments (e.g. a grid you walk
through), give each segment a `highlight` to spotlight different children:

```python
{"id": "c3_01_overview", "scene": "grid",
 "narration": "…", "highlight": {"selector": ".card", "activeIndices": [0, 1]}},
{"id": "c3_02_detail",  "scene": "grid",
 "narration": "…", "highlight": {"selector": ".card", "activeIndices": [4]}},
```

For each segment the engine adds `.active` to the matched children at those
indices and `.dim` to the rest. Style both states:

```css
.scene-grid .card.active { outline: 2px solid var(--gold-bright); }
.scene-grid .card.dim    { opacity: .35; }
```

(The `xpost` example keeps one segment per scene and does not use `highlight`;
reach for it only when you genuinely reuse a scene across beats.)

---

## 4. Use the shared theme variables

`player.css :root` defines the brand palette. Use these instead of hardcoding
hex values so scenes stay consistent with the player chrome:

| variable | value | use |
|----------|-------|-----|
| `--navy-900` … `--navy-600` | `#050a18` → `#162a4e` | backgrounds, depth |
| `--gold` / `--gold-bright` | `#d4a647` / `#f4c869` | accents, highlights |
| `--red` / `--green` / `--blue` | `#e74c3c` / `#4ade80` / `#60a5fa` | status (no/yes/info) |
| `--text` / `--text-dim` / `--text-dimmer` | `#e8eef8` / `#8a9bb8` / `#5a6a87` | body / secondary / tertiary text |
| `--border` | `rgba(255,255,255,0.1)` | hairlines, card edges |

```css
.scene-webinar .web-out {
  background: rgba(20, 35, 71, 0.55);
  border: 1px solid var(--border);
}
.scene-webinar .web-out-label { color: var(--text); }
```

`player.css` also ships a shared `@keyframes pulse` (a gentle opacity pulse) you
can reference from any scene — the `xpost` close-out CTA uses it,
`animation: pulse 3s ease-out infinite;`, with no need to redefine it. Any other
keyframes a scene needs go in that scene's own `css`.

---

## Checklist before you build

- [ ] `html` has **no** outer `.scene` wrapper and no player-owned ids.
- [ ] Every CSS selector is scoped — `.scene-NAME` descendant or a unique
      `NAME-` class prefix — so nothing bleeds into other scenes.
- [ ] Entrance animations trigger on `.scene-NAME.active`.
- [ ] Mid-narration state changes are declared as segment `timedClasses`, not
      baked into CSS delays.
- [ ] Colors come from the theme variables.
- [ ] `transition-delay` values are timed against the narration text.

Then `python <skill>/engine/build.py --project <dir>` and open `index.html`.
Iterate on the CSS and rebuild — only `generate_audio.py` costs API quota, and
only when narration text changes.
