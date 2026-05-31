import pathlib, sys
ENGINE = pathlib.Path(__file__).resolve().parent.parent / "engine"
sys.path.insert(0, str(ENGINE))
import build, generate_audio as ga  # noqa: E402


def _cfg(tmp_path):
    (tmp_path / "webinar.py").write_text('''
META = {}
VOICE = {"id": "v", "model": "m", "settings": {"stability": 0.5}}
SCENES = {"a": {"html": "", "css": ""}}
CHAPTERS = [{"number": 0, "title": "C", "icon": "0", "segments": [
    {"id": "s0", "scene": "a", "narration": "alpha text"},
    {"id": "s1", "scene": "a", "narration": "beta text"}]}]
''')
    return build.load_config(tmp_path / "webinar.py")


def test_collect_segments_all(tmp_path):
    items = ga.collect_segments(_cfg(tmp_path), only=None)
    assert [i[0] for i in items] == ["s0", "s1"]
    assert items[0][1] == "alpha text"


def test_collect_segments_only(tmp_path):
    items = ga.collect_segments(_cfg(tmp_path), only={"s1"})
    assert [i[0] for i in items] == ["s1"]


def test_payload_uses_voice_settings(tmp_path):
    cfg = _cfg(tmp_path)
    payload = ga.build_payload(cfg.VOICE, "hello")
    import json
    data = json.loads(payload)
    assert data["model_id"] == "m"
    assert data["voice_settings"]["stability"] == 0.5
    assert data["text"] == "hello"
