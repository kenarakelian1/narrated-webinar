"""Behavioral verification gate: prove the rebuilt example plays faithfully.

Reuses the bundled xpost example's MP3s (ids match the config exactly), so this
costs no ElevenLabs quota. Drives the built index.html with Playwright and
asserts the data-driven player engine behaves: sidebar populates, play activates
the first scene, chapter-jump activates a later scene, and the email scene's
`timedClasses` rule adds `.skimmed` once audio passes its threshold.
"""
import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
EXAMPLE = ROOT / "xpost"

pytest.importorskip("playwright.sync_api")
from playwright.sync_api import sync_playwright  # noqa: E402

# Stub `Audio` so playback is deterministic and file-independent: each created
# instance reports a fixed duration, starts paused, and exposes a settable
# currentTime. The engine's updateProgress() loop reads currentTime to drive
# timedClasses, so the test can force the email scene past its 12s threshold.
AUDIO_STUB = """
window.__audios = [];
class FakeAudio {
  constructor(src) {
    this.src = src; this.currentTime = 0; this.duration = 40;
    this.paused = true; this.ended = false; this.preload = '';
    this.onended = null; this._l = {};
    window.__audios.push(this);
  }
  play() { this.paused = false; return Promise.resolve(); }
  pause() { this.paused = true; }
  addEventListener(ev, fn) {
    (this._l[ev] = this._l[ev] || []).push(fn);
    if (ev === 'loadedmetadata') fn();
  }
  removeEventListener() {}
}
window.Audio = FakeAudio;
"""


@pytest.fixture(scope="module", autouse=True)
def built():
    sys.path.insert(0, str(ROOT / "engine"))
    import build
    if not (EXAMPLE / "audio").exists() or not any((EXAMPLE / "audio").glob("*.mp3")):
        pytest.skip("Example audio not present")
    build.build(EXAMPLE / "webinar.py")


def test_player_starts_and_populates_sidebar():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto((EXAMPLE / "index.html").as_uri())
        # Sidebar chapters render from the CHAPTERS JSON — xpost has 3.
        page.wait_for_selector(".chapter-item")
        assert page.locator(".chapter-item").count() == 3
        # Start playback → the first (email) scene activates.
        page.click("#play-btn")
        page.wait_for_selector('.scene[data-scene="email"].active', timeout=5000)
        # Jump to chapter 3 via the sidebar → the ship scene activates.
        page.locator(".chapter-item").nth(2).click()
        page.wait_for_selector('.scene[data-scene="ship"].active', timeout=5000)
        browser.close()


def test_email_skimmed_triggers_on_time():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.add_init_script(AUDIO_STUB)
        page.goto((EXAMPLE / "index.html").as_uri())
        page.click("#play-btn")
        page.wait_for_selector(".scene-email.active", timeout=5000)
        # Before the threshold the skimmed state must NOT be applied.
        assert page.evaluate(
            "() => document.querySelector('.scene-email').classList.contains('skimmed')"
        ) is False
        # Advance the currently-playing audio past the 12s threshold; the
        # engine's rAF progress loop then applies the timed class.
        page.evaluate("""() => {
            const a = window.__audios.find(a => !a.paused);
            if (a) a.currentTime = 13;
        }""")
        page.wait_for_selector(".scene-email.skimmed", timeout=5000)
        browser.close()
