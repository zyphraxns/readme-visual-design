#!/usr/bin/env python3
"""Render a GitHub-styled before/after preview of a README's first screen, with a light/dark toggle.

Usage:
    python preview_firstscreen.py --before old.md --after new.md \
        --out preview.html --title "Project" --repo /path/to/repo

Requires python-markdown (pip install markdown). Rendering differs slightly from GitHub;
it is meant to help the author judge the first screen, not to reproduce it pixel for pixel.
"""

import argparse
import base64
import html
import re
import sys
from pathlib import Path

try:
    import markdown
except ImportError:
    sys.exit("Missing dependency: python -m pip install markdown")

ALERT_BLOCK = re.compile(
    r"^>[ \t]*\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\][ \t]*\n((?:>[^\n]*\n?)*)", re.M
)
ALERT_TITLE = {
    "NOTE": "Note",
    "TIP": "Tip",
    "IMPORTANT": "Important",
    "WARNING": "Warning",
    "CAUTION": "Caution",
}
ALERT_COLOR = {
    "NOTE": "#0969da",
    "TIP": "#1a7f37",
    "IMPORTANT": "#8250df",
    "WARNING": "#9a6700",
    "CAUTION": "#cf222e",
}

CSS = """
*{box-sizing:border-box}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans",Helvetica,Arial,sans-serif;
  background:#f6f8fa;color:#1f2328;font-size:16px;line-height:1.5}
.bar{position:sticky;top:0;z-index:10;display:flex;align-items:center;gap:16px;
  padding:10px 24px;background:#fff;border-bottom:1px solid #d0d7de;font-size:13px}
.bar b{font-size:14px}
.bar .spacer{flex:1}
.bar label{cursor:pointer;padding:4px 10px;border:1px solid #d0d7de;border-radius:6px;color:#57606a}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:20px;padding:20px;align-items:start}
.col{min-width:0;overflow:hidden}
.tag{font-size:12px;font-weight:600;letter-spacing:.04em;text-transform:uppercase;
  color:#57606a;margin:0 0 8px;padding-left:2px}
.tag.after{color:#1a7f37}
/* Lay out at GitHub's 1012px content width, then scale down, so side-by-side images wrap as they do live */
.gh{width:1012px;zoom:.62;background:#fff;border:1px solid #d0d7de;border-radius:8px;padding:32px 40px;overflow:hidden}
.markdown-body{font-size:16px;line-height:1.6;word-wrap:break-word}
.markdown-body h1,.markdown-body h2,.markdown-body h3{font-weight:600;line-height:1.25;margin:24px 0 16px}
.markdown-body h1{font-size:2em;border-bottom:1px solid #d8dee4;padding-bottom:.3em;margin-top:0}
.markdown-body h2{font-size:1.5em;border-bottom:1px solid #d8dee4;padding-bottom:.3em;margin-top:32px}
.markdown-body h3{font-size:1.25em}
.markdown-body p{margin:0 0 16px}
.markdown-body a{color:#0969da;text-decoration:none}
.markdown-body a:hover{text-decoration:underline}
.markdown-body img{max-width:100%;border-style:none}
.markdown-body code{background:#eff1f3;padding:.2em .4em;border-radius:6px;font-size:85%;
  font-family:ui-monospace,SFMono-Regular,"SF Mono",Menlo,monospace}
.markdown-body pre{background:#f6f8fa;padding:16px;border-radius:6px;overflow:auto;margin:0 0 16px}
.markdown-body pre code{background:none;padding:0;font-size:85%}
.markdown-body blockquote{margin:0 0 16px;padding:0 1em;color:#59636e;border-left:.25em solid #d1d9e0}
.markdown-body hr{height:.25em;padding:0;margin:24px 0;background:#d1d9e0;border:0}
.markdown-body table{border-collapse:collapse;display:block;width:max-content;max-width:100%;
  overflow:auto;margin:0 0 16px;font-size:14px}
.markdown-body th,.markdown-body td{border:1px solid #d1d9e0;padding:6px 13px}
.markdown-body th{font-weight:600;background:#f6f8fa}
.markdown-body ul,.markdown-body ol{padding-left:2em;margin:0 0 16px}
.markdown-body li{margin:.25em 0}
.markdown-body details{margin:0 0 16px;padding:8px 12px;border:1px solid #d1d9e0;border-radius:6px}
.markdown-body summary{cursor:pointer;font-weight:600}
.markdown-body .alert{border-left:.25em solid #d1d9e0;padding:8px 16px;margin:0 0 16px;border-radius:4px}
.markdown-body .alert-title{font-weight:600;margin:0 0 4px;font-size:14px}
.markdown-body kbd{background:#f6f8fa;border:1px solid #d1d9e0;border-radius:6px;padding:2px 6px;font-size:80%}
#dark:checked ~ .cols .gh{background:#0d1117;border-color:#30363d}
#dark:checked ~ .cols .markdown-body{color:#e6edf3}
#dark:checked ~ .cols .markdown-body h1,
#dark:checked ~ .cols .markdown-body h2{border-bottom-color:#3d444d}
#dark:checked ~ .cols .markdown-body a{color:#4493f8}
#dark:checked ~ .cols .markdown-body code{background:#151b23}
#dark:checked ~ .cols .markdown-body pre{background:#151b23}
#dark:checked ~ .cols .markdown-body blockquote{color:#9198a1;border-left-color:#3d444d}
#dark:checked ~ .cols .markdown-body hr{background:#3d444d}
#dark:checked ~ .cols .markdown-body th,
#dark:checked ~ .cols .markdown-body td{border-color:#3d444d}
#dark:checked ~ .cols .markdown-body th{background:#151b23}
#dark:checked ~ .cols .markdown-body details{border-color:#3d444d}
#dark:checked ~ body,#dark:checked ~ .cols{background:#010409}
body:has(#dark:checked){background:#010409;color:#e6edf3}
body:has(#dark:checked) .bar{background:#161b22;border-color:#30363d;color:#e6edf3}
body:has(#dark:checked) .tag{color:#9198a1}
.note{font-size:12px;color:#59636e;padding:0 24px 24px}
@media(max-width:1400px){.cols{grid-template-columns:1fr}.gh{width:auto;zoom:1}}
@media(max-width:1000px){.cols{grid-template-columns:1fr}}
"""


def first_screen(text: str, max_lines: int) -> str:
    """Cut off at the third h2 or at max_lines, approximating "the first two screens"."""
    out, h2_seen, in_fence = [], 0, False
    for line in text.splitlines():
        if re.match(r"^\s*(```|~~~)", line):
            in_fence = not in_fence
        if not in_fence and re.match(r"^##\s+", line):
            h2_seen += 1
            if h2_seen >= 3:
                break
        out.append(line)
        if len(out) >= max_lines:
            break
    return "\n".join(out)


def convert(text: str, repo: Path) -> str:
    def repl(m):
        kind = m.group(1)
        body = "\n".join(
            re.sub(r"^>[ \t]?", "", ln) for ln in m.group(2).splitlines()
        ).strip()
        inner = markdown.markdown(body, extensions=["tables", "fenced_code", "sane_lists"])
        return (
            f'<div class="alert" style="border-left-color:{ALERT_COLOR[kind]}">'
            f'<p class="alert-title" style="color:{ALERT_COLOR[kind]}">{ALERT_TITLE[kind]}</p>'
            f"{inner}</div>\n"
        )

    text = ALERT_BLOCK.sub(repl, text)
    body = markdown.markdown(
        text,
        extensions=["tables", "fenced_code", "md_in_html", "sane_lists", "attr_list"],
    )

    def fix(m):
        attr, src = m.group(1), m.group(2)
        if re.match(r"^(https?:|data:|#|mailto:)", src):
            return m.group(0)
        p = (repo / src.split("?")[0]).resolve()
        if p.exists():
            return f'{attr}="{p.as_uri()}"'
        return m.group(0)

    body = re.sub(r'(src|srcset)="([^"]+)"', fix, body)

    # Inline local images so file:// is not blocked by some browsers
    def inline(m):
        url = m.group(1)
        if not url.startswith("file://"):
            return m.group(0)
        p = Path(url[7:])
        try:
            data = base64.b64encode(p.read_bytes()).decode()
        except OSError:
            return m.group(0)
        suffix = p.suffix.lower().lstrip(".")
        mime = {"jpg": "jpeg", "svg": "svg+xml"}.get(suffix, suffix)
        return f'src="data:image/{mime};base64,{data}"'

    body = re.sub(r'src="(file://[^"]+)"', inline, body)
    return body


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--before", required=True)
    ap.add_argument("--after", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--title", default="README")
    ap.add_argument("--repo", default=None, help="repo root, used to resolve relative image paths")
    ap.add_argument("--max-lines", type=int, default=90)
    args = ap.parse_args()

    repo = Path(args.repo).resolve() if args.repo else Path(args.after).resolve().parent
    before = first_screen(Path(args.before).read_text(encoding="utf-8"), args.max_lines)
    after = first_screen(Path(args.after).read_text(encoding="utf-8"), args.max_lines)

    doc = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>{html.escape(args.title)} · README first screen</title>
<style>{CSS}</style></head>
<body>
<input type="checkbox" id="dark" hidden>
<div class="bar">
  <b>{html.escape(args.title)}</b>
  <span style="color:#8b949e">First screen · top of the file only, not the full page</span>
  <span class="spacer"></span>
  <label for="dark">Toggle dark</label>
</div>
<div class="cols">
  <section class="col">
    <p class="tag">Before</p>
    <div class="gh"><article class="markdown-body">{convert(before, repo)}</article></div>
  </section>
  <section class="col">
    <p class="tag after">After</p>
    <div class="gh"><article class="markdown-body">{convert(after, repo)}</article></div>
  </section>
</div>
<p class="note">Approximate rendering: fonts, line height and image proxying differ slightly from GitHub. Use it to judge structure and feel, not final pixels.</p>
</body></html>"""

    Path(args.out).write_text(doc, encoding="utf-8")
    print(f"Wrote: {args.out}")


if __name__ == "__main__":
    main()
