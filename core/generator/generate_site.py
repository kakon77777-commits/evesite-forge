#!/usr/bin/env python3
"""EveSite Forge reference generator (zero dependencies)."""
from __future__ import annotations

import argparse
import html
import json
import shutil
from pathlib import Path

CSS = r'''
:root{color-scheme:light dark;--bg:#f4f3ed;--surface:#fff;--ink:#171a17;--muted:#676c67;--line:#d5d7d0;--accent:#286652;--soft:#dfece6;--max:1120px}@media(prefers-color-scheme:dark){:root{--bg:#101310;--surface:#181c18;--ink:#eef1ed;--muted:#a8afa9;--line:#343a35;--accent:#8bd0b9;--soft:#20392f}}*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--bg);color:var(--ink);font-family:Inter,system-ui,-apple-system,"Segoe UI","Noto Sans TC",sans-serif;line-height:1.65}a{color:inherit}.shell{width:min(var(--max),calc(100% - 36px));margin:auto}.top{position:sticky;top:0;z-index:10;display:flex;align-items:center;gap:18px;padding:13px max(18px,calc((100vw - var(--max))/2));border-bottom:1px solid var(--line);background:color-mix(in srgb,var(--bg) 88%,transparent);backdrop-filter:blur(16px)}.brand{margin-right:auto;text-decoration:none;font-weight:850}.top nav{display:flex;gap:16px}.top nav a{color:var(--muted);font-size:.84rem;text-decoration:none}.hero{display:grid;grid-template-columns:1.2fr .8fr;gap:56px;align-items:center;min-height:80vh;padding:80px 0}.badge,.tag{display:inline-flex;border-radius:999px;padding:5px 10px;background:var(--soft);color:var(--accent);font-size:.75rem;font-weight:800}.hero h1{margin:22px 0;font-size:clamp(2.8rem,6.5vw,6rem);line-height:1;letter-spacing:-.055em}.lead,.muted{color:var(--muted)}.actions{display:flex;gap:10px;flex-wrap:wrap;margin-top:26px}.button{display:inline-flex;border:1px solid var(--line);border-radius:999px;padding:10px 16px;background:var(--surface);text-decoration:none}.primary{border-color:var(--accent);background:var(--accent);color:var(--bg)}.diagram{display:grid;gap:10px}.diagram article,.card,.panel,.doc{border:1px solid var(--line);border-radius:20px;padding:20px;background:var(--surface)}.diagram small{display:block;color:var(--accent);font-weight:800;text-transform:uppercase}.section{padding:86px 0}.contrast{background:var(--surface)}.heading{display:grid;grid-template-columns:1fr minmax(260px,460px);gap:34px;align-items:end;margin-bottom:34px}.heading h2{margin:7px 0 0;font-size:clamp(2rem,4.5vw,4rem);line-height:1.06;letter-spacing:-.045em}.kicker{color:var(--accent);font-size:.75rem;font-weight:850;text-transform:uppercase;letter-spacing:.08em}.grid{display:grid;gap:16px}.features{grid-template-columns:repeat(4,1fr)}.features .card{min-height:210px}.features h3{margin-top:52px}.two{grid-template-columns:repeat(2,1fr)}.three{grid-template-columns:repeat(3,1fr)}.panel label{display:grid;gap:8px;margin:18px 0;font-weight:750}.panel input[type=range],.panel select{width:100%}.score{font-size:4.5rem;font-weight:900;letter-spacing:-.06em}.track{height:12px;border-radius:999px;background:var(--bg);overflow:hidden}.track span{display:block;height:100%;width:0;background:var(--accent)}.levels{display:grid;gap:9px}.level{border:1px solid var(--line);border-radius:14px;padding:12px;opacity:.5}.level.active{opacity:1;border-color:var(--accent);background:var(--soft)}.semantic{display:flex;flex-wrap:wrap;gap:8px}.semantic span{border:1px solid var(--line);border-radius:999px;padding:8px 11px;background:var(--surface);font-size:.82rem}.formula{overflow:auto;border-radius:14px;padding:16px;background:var(--bg);font-family:"Cambria Math",serif}.docs{display:grid;gap:10px}.doc{display:flex;justify-content:space-between;text-decoration:none}.status{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}.status strong{display:block;margin-top:10px;font-size:2.2rem}.limits{margin-top:22px;border-left:3px solid var(--accent);padding:14px 18px;background:var(--soft)}footer{display:flex;justify-content:space-between;gap:20px;padding:30px 0;border-top:1px solid var(--line);color:var(--muted);font-size:.85rem}@media(max-width:850px){.hero,.heading{grid-template-columns:1fr}.features,.three,.status{grid-template-columns:repeat(2,1fr)}}@media(max-width:560px){.top nav{display:none}.features,.two,.three,.status{grid-template-columns:1fr}.hero{padding:58px 0}.section{padding:66px 0}}
'''


def esc(value) -> str:
    return html.escape(str(value or ""))


def section(data: dict, item: dict) -> str:
    kind = item.get("kind")
    title = esc(item.get("title"))
    description = esc(item.get("description"))
    head = f'<div class="heading"><div><span class="kicker">{esc(kind)}</span><h2>{title}</h2></div><p class="muted">{description}</p></div>'
    if kind == "features":
        cards = "".join(f'<article class="card"><span class="tag">{i+1:02}</span><h3>{esc(x.get("title"))}</h3><p class="muted">{esc(x.get("description"))}</p></article>' for i,x in enumerate(item.get("items",[])))
        body = f'<div class="grid features">{cards}</div>'
    elif kind == "interactive":
        body = interactive(data.get("interactive",{}))
    elif kind == "formal":
        formal = data.get("formal",{})
        public = "".join(f"<li>{esc(x)}</li>" for x in formal.get("public",[]))
        exact = "".join(f"<li>{esc(x)}</li>" for x in formal.get("formal",[]))
        semantic = "".join(f"<span>{esc(x)}</span>" for x in formal.get("semantic_units",[]))
        body = f'<div class="grid two"><article class="card"><span class="tag">Public</span><ul>{public}</ul></article><article class="card"><span class="tag">Formal</span><ul>{exact}</ul></article></div><div class="semantic">{semantic}</div><pre class="formula">{esc(formal.get("formula"))}</pre>'
    elif kind == "experiments":
        cards = "".join(f'<article class="card"><span class="tag">{esc(x.get("id"))}</span><h3>{esc(x.get("title"))}</h3><p class="muted">{esc(x.get("description"))}</p><small>{esc(x.get("evidence"))}</small></article>' for x in data.get("experiments",[]))
        body = f'<div class="grid three">{cards}</div>'
    elif kind == "documents":
        docs = "".join(f'<a class="doc" href="{esc(x.get("path"))}"><span><strong>{esc(x.get("title"))}</strong><small>{esc(x.get("description"))}</small></span><b>{esc(x.get("role"))}</b></a>' for x in data.get("documents",[]))
        body = f'<div class="docs">{docs}</div>'
    else:
        status = data.get("status",{})
        metrics = "".join(f'<article class="card"><span>{esc(x.get("label"))}</span><strong>{esc(x.get("value"))}</strong><small>{esc(x.get("note"))}</small></article>' for x in status.get("metrics",[]))
        limits = "".join(f"<li>{esc(x)}</li>" for x in data.get("limitations",[]))
        body = f'<div class="status">{metrics}</div><div class="limits"><strong>Limitations</strong><ul>{limits}</ul></div>'
    return f'<section class="section shell" id="{esc(item.get("id"))}">{head}{body}</section>'


def interactive(cfg: dict) -> str:
    typ = cfg.get("type", "none")
    if typ == "weighted-risk":
        controls = "".join(f'<label>{esc(c.get("label"))}<input type="range" min="{c.get("min",0)}" max="{c.get("max",1)}" step="{c.get("step",.01)}" value="{c.get("default",0)}" data-weight="{c.get("weight",1)}"><output>{c.get("default",0)}</output></label>' for c in cfg.get("controls",[]))
        return f'<div class="grid two"><article class="panel"><h3>{esc(cfg.get("title"))}</h3>{controls}</article><article class="panel"><span class="kicker">Combined state</span><div class="score" id="score">0.00</div><div class="track"><span id="bar"></span></div><p id="event" class="muted"></p></article></div>'
    if typ == "maturity-ladder":
        levels = cfg.get("levels",[])
        options = "".join(f'<option value="{i}">L{i} — {esc(x.get("title"))}</option>' for i,x in enumerate(levels))
        nodes = "".join(f'<article class="level" data-level="{i}"><strong>L{i} — {esc(x.get("title"))}</strong><p>{esc(x.get("description"))}</p></article>' for i,x in enumerate(levels))
        return f'<div class="grid two"><article class="panel"><h3>{esc(cfg.get("title"))}</h3><label>成熟度<select id="maturity">{options}</select></label></article><div class="levels">{nodes}</div></div>'
    return '<article class="panel"><p class="muted">This site type has no interactive module.</p></article>'


def script(data: dict) -> str:
    cfg = data.get("interactive",{})
    if cfg.get("type") == "weighted-risk":
        threshold = float(cfg.get("threshold", .75))
        return f'''const inputs=[...document.querySelectorAll('input[type=range]')];function update(){{let total=0,weights=0;inputs.forEach(i=>{{i.nextElementSibling.value=i.value;const w=+i.dataset.weight||1;total+=+i.value*w;weights+=w}});const score=weights?total/weights:0;document.querySelector('#score').textContent=score.toFixed(2);document.querySelector('#bar').style.width=Math.min(100,score*100)+'%';document.querySelector('#event').textContent=score>={threshold}?'Threshold reached: event conditions are active.':'Below threshold: no event is triggered.'}}inputs.forEach(i=>i.addEventListener('input',update));update();'''
    if cfg.get("type") == "maturity-ladder":
        return "const select=document.querySelector('#maturity');const nodes=[...document.querySelectorAll('.level')];function update(){nodes.forEach(n=>n.classList.toggle('active',+n.dataset.level<=+select.value))}select.addEventListener('change',update);update();"
    return ""


def generate(data: dict, source_dir: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    project, thesis, evidence = data["project"], data["thesis"], data["evidence"]
    nav = "".join(f'<a href="#{esc(x.get("id"))}">{esc(x.get("title"))}</a>' for x in data.get("sections",[]))
    sections = "".join(section(data,x) for x in data.get("sections",[]))
    authors = " · ".join(project.get("authors",[]))
    page = f'''<!doctype html><html lang="{esc(project.get('language','zh-Hant'))}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{esc(thesis.get('summary'))}"><title>{esc(project.get('short_title'))} — {esc(project.get('title'))}</title><link rel="stylesheet" href="styles.css"></head><body><header class="top"><a class="brand" href="#overview">{esc(project.get('short_title'))}</a><nav>{nav}</nav></header><main><section class="hero shell" id="overview"><div><span class="badge">{esc(project.get('status'))} · {esc(project.get('version'))}</span><h1>{esc(thesis.get('headline'))}</h1><p class="lead">{esc(thesis.get('summary'))}</p><div class="actions"><a class="button primary" href="#explore">開始探索</a><a class="button" href="#formal">正式層</a></div><div class="limits"><strong>{esc(evidence.get('level'))} · {esc(evidence.get('label'))}</strong><br>{esc(evidence.get('disclaimer'))}</div></div><div class="diagram"><article><small>Problem</small><strong>{esc(thesis.get('problem'))}</strong></article><article><small>Method</small><strong>{esc(thesis.get('method'))}</strong></article><article><small>Goal</small><strong>{esc(thesis.get('goal'))}</strong></article></div></section>{sections}</main><footer class="shell"><span>{esc(project.get('title'))}</span><span>{esc(authors)} · {esc(project.get('date'))}</span></footer><script src="app.js"></script></body></html>'''
    (output_dir/"index.html").write_text(page,encoding="utf-8")
    (output_dir/"styles.css").write_text(CSS,encoding="utf-8")
    (output_dir/"app.js").write_text(script(data),encoding="utf-8")
    (output_dir/"theory.json").write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
    for doc in data.get("documents",[]):
        src=source_dir/Path(doc["path"]); dst=output_dir/Path(doc["path"])
        if src.exists(): dst.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(src,dst)


def main() -> None:
    parser=argparse.ArgumentParser(); parser.add_argument("source"); parser.add_argument("output"); args=parser.parse_args()
    source=Path(args.source).resolve(); generate(json.loads(source.read_text(encoding="utf-8")),source.parent,Path(args.output).resolve())

if __name__ == "__main__": main()
