import json, pathlib, sys
import pytest

ENGINE = pathlib.Path(__file__).resolve().parent.parent / "engine"
sys.path.insert(0, str(ENGINE))
import build  # noqa: E402


def _fixture_project(tmp_path):
    (tmp_path / "webinar.py").write_text('''
META = {"title": "T", "eyebrow": "E", "subtitle": "S", "preview": [{"num": "P1", "title": "One"}],
        "start_meta": "M", "sidebar_eyebrow": "SE", "sidebar_title": "ST",
        "property_line": "PL", "stage_property": "SP"}
VOICE = {"id": "v", "model": "m", "settings": {}}
SCENES = {"alpha": {"html": "<p>A</p>", "css": ".scene-alpha{color:red}"}}
CHAPTERS = [
    {"number": 0, "title": "First", "icon": "0", "segments": [
        {"id": "s0", "scene": "alpha", "narration": "hello",
         "timedClasses": [{"at": 30, "addClass": "calm"}]}]},
    {"number": 1, "title": "Second", "icon": "1", "segments": [
        {"id": "s1", "scene": "alpha", "narration": "world"}]},
]
''')
    return tmp_path


def test_flatten_builds_segments_and_chapters(tmp_path):
    cfg = build.load_config(_fixture_project(tmp_path) / "webinar.py")
    segs, chaps = build.flatten(cfg)
    assert [s["id"] for s in segs] == ["s0", "s1"]
    assert segs[0]["chapter"] == 0 and segs[0]["chapterTitle"] == "First"
    assert segs[0]["title"] == "First"
    assert segs[0]["timedClasses"] == [{"at": 30, "addClass": "calm"}]
    assert "timedClasses" not in segs[1]
    assert chaps == [
        {"num": 0, "title": "First", "icon": "0", "firstIdx": 0},
        {"num": 1, "title": "Second", "icon": "1", "firstIdx": 1},
    ]


def test_build_writes_index_html(tmp_path):
    proj = _fixture_project(tmp_path)
    out = build.build(proj / "webinar.py")
    html = out.read_text()
    assert out.name == "index.html"
    assert "<p>A</p>" in html                       # scene html injected
    assert ".scene-alpha{color:red}" in html        # scene css injected
    assert "T" in html and "PL" in html             # META fields injected
    assert '"id": "s0"' in html or '"id":"s0"' in html  # segment manifest injected
    assert "/*SEGMENTS_JSON*/" not in html          # sentinel consumed
    assert "<!--SCENES_HTML-->" not in html
    assert 'data-scene="alpha"' in html             # wrapper added by build
