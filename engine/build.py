#!/usr/bin/env python3
"""Assemble a narrated-webinar index.html from a project's webinar.py config."""
import argparse
import importlib.util
import json
import pathlib

ENGINE = pathlib.Path(__file__).resolve().parent


def load_config(config_path):
    config_path = pathlib.Path(config_path)
    spec = importlib.util.spec_from_file_location("webinar_config", config_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def flatten(cfg):
    segments = []
    chapters = []
    for ch in cfg.CHAPTERS:
        chapters.append({"num": ch["number"], "title": ch["title"],
                         "icon": ch["icon"], "firstIdx": len(segments)})
        for seg in ch["segments"]:
            item = {"id": seg["id"], "chapter": ch["number"],
                    "chapterTitle": ch["title"], "title": ch["title"],
                    "scene": seg["scene"]}
            if "highlight" in seg:
                item["highlight"] = seg["highlight"]
            if "timedClasses" in seg:
                item["timedClasses"] = seg["timedClasses"]
            segments.append(item)
    return segments, chapters


def _render_pillars(preview):
    return "\n".join(
        f'<div class="preview-pillar"><div class="preview-pillar-num">{p["num"]}</div>'
        f'<div class="preview-pillar-title">{p["title"]}</div></div>'
        for p in preview)


def _render_scenes(scenes_dict, order):
    return "\n".join(
        f'<div class="scene scene-{name}" data-scene="{name}">{scenes_dict[name]["html"]}</div>'
        for name in order)


def build(config_path):
    cfg = load_config(config_path)
    proj_dir = pathlib.Path(config_path).resolve().parent
    segments, chapters = flatten(cfg)

    order = []
    for s in segments:
        if s["scene"] not in order:
            order.append(s["scene"])

    scene_css = "\n".join(cfg.SCENES[name]["css"] for name in order)
    scenes_html = _render_scenes(cfg.SCENES, order)
    player_css = (ENGINE / "player.css").read_text()
    player_js = (ENGINE / "player.js").read_text()
    shell = (ENGINE / "shell.html").read_text()

    m = cfg.META
    replacements = {
        "/*PLAYER_CSS*/": player_css,
        "/*SCENE_CSS*/": scene_css,
        "<!--EYEBROW-->": m["eyebrow"],
        "<!--TITLE-->": m["title"],
        "<!--SUBTITLE-->": m["subtitle"],
        "<!--PREVIEW_PILLARS-->": _render_pillars(m["preview"]),
        "<!--START_META-->": m["start_meta"],
        "<!--PROPERTY_LINE-->": m["property_line"],
        "<!--SIDEBAR_EYEBROW-->": m["sidebar_eyebrow"],
        "<!--SIDEBAR_TITLE-->": m["sidebar_title"],
        "<!--SCENES_HTML-->": scenes_html,
        "<!--STAGE_PROPERTY-->": m["stage_property"],
        "/*PLAYER_JS*/": player_js,
    }
    html = shell
    for token, value in replacements.items():
        html = html.replace(token, value)
    html = html.replace("/*SEGMENTS_JSON*/", json.dumps(segments))
    html = html.replace("/*CHAPTERS_JSON*/", json.dumps(chapters))

    out = proj_dir / "index.html"
    out.write_text(html)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True, help="project dir containing webinar.py")
    args = ap.parse_args()
    out = build(pathlib.Path(args.project) / "webinar.py")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
