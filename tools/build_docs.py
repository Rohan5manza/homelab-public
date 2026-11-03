#!/usr/bin/env python3
"""Build the portable, dependency-light documentation portal from Markdown.

Requires mistune>=3. This generates real static HTML so deploying GitHub Pages
never requires a live backend or custom server routing.
"""
from pathlib import Path
import html
import os
import re
import shutil
from urllib.parse import urlsplit
import mistune

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
OUT = ROOT / 'site/lab/docs'
SITE = ROOT / 'site/lab'
ITEMS = [
    ('index.md', 'Overview'),
    ('architecture.md', 'Platform architecture'),
    ('projects/ml-platform.md', 'GPU / ML platform'),
    ('mlops.md', 'MLOps workflow'),
    ('services.md', 'Self-hosted apps'),
    ('projects/thermostat.md', 'Smart thermostat'),
    ('projects/observability.md', 'Observability'),
    ('ai-demo.md', 'AI demo deployment'),
    ('security.md', 'Security boundary'),
    ('evidence.md', 'Evidence register'),
]

markdown = mistune.create_markdown(plugins=['table', 'strikethrough', 'task_lists'])


def out_for(src: Path) -> Path:
    rel = src.relative_to(DOCS)
    return OUT / (rel.parent if rel.name == 'index.md' else rel.with_suffix('')) / 'index.html'


def relative(from_file: Path, to_file: Path) -> str:
    return os.path.relpath(to_file, from_file.parent).replace(os.sep, '/')


def rewrite_links(rendered: str, src: Path, dest: Path) -> str:
    # Markdown rendering already encodes attributes. Relative asset and .md
    # links are rewritten for directory-style static HTML paths.
    def repl(match):
        attr, raw = match.group(1), html.unescape(match.group(2))
        u = urlsplit(raw)
        if u.scheme or raw.startswith(('#', '//', '/')):
            return match.group(0)
        t = (src.parent / u.path).resolve()
        if attr == 'href' and t.suffix.lower() == '.md' and t.is_relative_to(DOCS.resolve()):
            t = out_for(t)
        if attr == 'src' and not t.exists():
            raise FileNotFoundError(f'Missing doc asset: {src}: {u.path}')
        return f'{attr}="{html.escape(relative(dest, t) + ("#" + u.fragment if u.fragment else ""), quote=True)}"'
    return re.sub(r'(href|src)="([^"]+)"', repl, rendered)


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    for filename, label in ITEMS:
        src = DOCS / filename
        dest = out_for(src)
        dest.parent.mkdir(parents=True, exist_ok=True)
        content = rewrite_links(markdown(src.read_text(encoding='utf-8')), src, dest)
        sidebar = []
        for other, name in ITEMS:
            url = relative(dest, out_for(DOCS / other))
            active = ' class="active"' if other == filename else ''
            sidebar.append(f'<a{active} href="{html.escape(url, quote=True)}">{html.escape(name)}</a>')
        main = relative(dest, SITE / 'index.html')
        css = relative(dest, SITE / 'assets/styles.css')
        icon = relative(dest, SITE / 'assets/favicon.svg')
        doccss = relative(dest, OUT / 'docs.css')
        site_title = 'Buffy Lab / Documentation'
        page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#050b15"><title>{html.escape(label)} / {site_title}</title><link rel="stylesheet" href="{css}"><link rel="stylesheet" href="{doccss}"><link rel="icon" href="{icon}" type="image/svg+xml"></head><body class="docs-body"><header class="docs-top"><a href="{main}" class="docs-brand"><strong>BUFFY</strong> / SYSTEMS LAB</a><span>ENGINEERING NOTEBOOK</span><a class="docs-website-link" href="{main}">← RETURN TO LAB</a></header><div class="docs-layout"><aside class="docs-nav"><div class="nav-overline">THE SYSTEMS / 2026</div><input id="docSearch" type="search" placeholder="Filter chapters..." aria-label="Filter chapters"/><nav id="docLinks" aria-label="Documentation chapters">{''.join(sidebar)}</nav><div class="docs-caution">Explore how the lab is built, with clear boundaries between public demonstrations and private tools.</div></aside><main class="docs-main"><div class="docs-breadcrumb">LAB / DOCUMENTATION / {html.escape(label.upper())}</div><article class="docs-content">{content}</article><div class="docs-end">END OF DOCUMENT / BUFFY ENGINEERING LAB</div></main><aside class="docs-aside"><span>RESEARCH NOTES</span><p>Build → measure → document → repeat.</p><div class="docs-aside-box">STATUS<br><b>ONGOING WORK</b></div><a href="{relative(dest, out_for(DOCS / 'evidence.md'))}">EXPLORE RESULTS &amp; EVIDENCE ↗</a></aside></div><script>const s=document.querySelector('#docSearch');s.addEventListener('input',()=>{{const t=s.value.toLowerCase();document.querySelectorAll('#docLinks a').forEach(a=>a.hidden=!a.textContent.toLowerCase().includes(t));}})</script></body></html>'''
        dest.write_text(page, encoding='utf-8')
        print('built', dest.relative_to(ROOT))
    shutil.copyfile(ROOT / 'tools/docs.css', OUT / 'docs.css')


if __name__ == '__main__':
    build()
