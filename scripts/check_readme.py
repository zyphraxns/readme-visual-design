#!/usr/bin/env python3
"""README audit: find what silently breaks on GitHub.

Usage:
    python check_readme.py README.md
    python check_readme.py README.md README.zh-CN.md --repo .

Checks:
    image relative paths exist / file size / missing alt text
    empty links, in-page anchors that match no heading
    shields.io badge URLs are valid
    heading levels that skip, alert syntax, unclosed details, table column counts
    first-screen element order (diagnostic only, not an error)
"""

import argparse
import os
import re
import sys

IMAGE_MD = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
IMAGE_HTML = re.compile(r"<img\b[^>]*?\bsrc=[\"']([^\"']+)[\"'][^>]*>", re.I)
ALT_HTML = re.compile(r"<img\b[^>]*?\balt=[\"']([^\"']*)[\"'][^>]*>", re.I)
LINK_MD = re.compile(r"(?<!!)\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
FENCE = re.compile(r"^\s*(```+|~~~+)")
ALERT = re.compile(r"^>\s*\[!(\w+)\]")
SHIELDS = re.compile(r"https?://img\.shields\.io/(badge|github|npm|pypi|endpoint|static)/\S+")
VALID_ALERTS = {"NOTE", "TIP", "IMPORTANT", "WARNING", "CAUTION"}
SKIP_SCHEMES = ("http://", "https://", "data:", "mailto:", "#", "ftp:")
MAX_IMAGE_MB = 5.0


def slug(text: str) -> str:
    """GitHub heading anchor rules: lowercase, strip punctuation, spaces to hyphens, keep CJK."""
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"\*\*([^*]*)\*\*", r"\1", text)
    text = re.sub(r"\*([^*]*)\*", r"\1", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = text.strip().lower()
    text = re.sub(r"[^\w\- ]", "", text, flags=re.UNICODE)
    return text.replace(" ", "-")


def is_fence_line(line: str) -> bool:
    return bool(FENCE.match(line))


def check(path: str, repo: str) -> int:
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()

    root = repo or os.path.dirname(os.path.abspath(path))
    errors, warns, infos = [], [], []

    for i, line in enumerate(lines, 1):
        if is_fence_line(line):
            infos.append((i, "Code fence opens/closes here; later checks skip fenced content", "trace"))

    anchors = []
    in_fence = False
    for i, line in enumerate(lines, 1):
        if is_fence_line(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = HEADING.match(line)
        if m:
            anchors.append(slug(m.group(2)))
    anchors.extend(["readme", "top"])  # GitHub's built-in in-page anchors

    dup_note = None
    tmp = {}
    for a in anchors:
        tmp[a] = tmp.get(a, 0) + 1
    if any(v > 1 for v in tmp.values()):
        dup_note = "Duplicate headings: GitHub suffixes the second with -1, so check hand-written anchors"

    in_fence = False
    table_run = []
    last_level = 0

    def report_table(run):
        if len(run) >= 2:
            counts = {ln: len([c for c in row.strip().strip("|").split("|")]) for ln, row in run}
            if len(set(counts.values())) > 1:
                base = max(set(counts.values()), key=list(counts.values()).count)
                bad = [ln for ln, c in counts.items() if c != base]
                for ln in bad:
                    errors.append((ln, f"Table column count differs from neighboring rows (expected {base})", "table"))

    for i, line in enumerate(lines, 1):
        if is_fence_line(line):
            report_table(table_run)
            table_run = []
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        if line.strip().startswith("|"):
            table_run.append((i, line))
        else:
            report_table(table_run)
            table_run = []

        # Images (Markdown syntax)
        for alt, src in IMAGE_MD.findall(line):
            check_image(i, alt, src, root, errors, warns)
        # Images (HTML syntax)
        for m in re.finditer(r"<img\b[^>]*>", line, re.I):
            tag = m.group(0)
            src_m = re.search(r"\bsrc=[\"']([^\"']+)[\"']", tag, re.I)
            alt_m = re.search(r"\balt=[\"']([^\"']*)[\"']", tag, re.I)
            if src_m:
                check_image(i, alt_m.group(1) if alt_m else "", src_m.group(1), root, errors, warns)

        # Links
        for text, href in LINK_MD.findall(line):
            if href in ("#", ""):
                errors.append((i, "Empty link `#`: clicking it jumps to the top of the page", "link"))
            elif href.startswith("#"):
                if href[1:] not in anchors:
                    warns.append((i, f"In-page anchor #{href[1:]} matches no heading", "link"))
            if "img.shields.io" in href:
                check_badge(i, href, errors, warns)

        for m in re.finditer(r"<a\b[^>]*\bhref=[\"']([^\"']+)[\"'][^>]*>", line, re.I):
            if m.group(1) == "#":
                errors.append((i, "Empty link href=\"#\": clicking it jumps to the top", "link"))

        # [![alt](img)](href) — the outer link of a badge. LINK_MD cannot see it
        # because the label contains a closing bracket.
        for href in re.findall(r"!\[[^\]]*\]\([^)]*\)\]\(([^)\s]+)\)", line):
            if href in ("#", ""):
                errors.append(
                    (i, "Badge links to `#`: clicking it jumps to the top of the page", "link")
                )
            elif "img.shields.io" in href:
                check_badge(i, href, errors, warns)

        # alerts
        m = ALERT.match(line.strip())
        if m:
            kind = m.group(1)
            if kind not in VALID_ALERTS:
                errors.append((i, f"Invalid alert type {kind}; only {'/'.join(sorted(VALID_ALERTS))} are accepted", "alert"))
            if i < len(lines) and not lines[i].strip().startswith(">"):
                warns.append((i, "Line after the alert does not start with `> `, so the block ends early", "alert"))

        # Heading levels
        hm = HEADING.match(line)
        if hm:
            level = len(hm.group(1))
            if last_level and level > last_level + 1:
                errors.append((i, f"Heading jumps from h{last_level} to h{level}, skipping a level", "heading"))
            last_level = level

        # Markdown emphasis mixed inside an HTML block
        if re.search(r"<(p|h1|h2|div)\b[^>]*align=", line, re.I) and "**" in line:
            warns.append((i, "`**bold**` inside an HTML block: GitHub may print the asterisks literally, use <b>", "html"))

    report_table(table_run)

    # details pairing — ignore anything quoted as code, or every README that
    # documents the <details> syntax would fail its own audit
    body = "\n".join(lines)
    prose = re.sub(r"^```.*?^```", "", body, flags=re.S | re.M)
    prose = re.sub(r"`[^`\n]*`", "", prose)
    opened = len(re.findall(r"<details\b", prose, re.I))
    closed = len(re.findall(r"</details>", prose, re.I))
    if opened != closed:
        errors.append((0, f"<details> tags unbalanced: {opened} opened, {closed} closed", "details"))

    # ---------- first-screen diagnosis ----------
    first = []
    in_fence = False
    for i, line in enumerate(lines, 1):
        if is_fence_line(line):
            in_fence = not in_fence
            first.append((i, "Code block"))
            continue
        if in_fence:
            continue
        s = line.strip()
        if not s:
            continue
        # Bare wrapper tags do not count on the first screen (<p align="center"> and friends)
        if re.match(r"^</?p\b[^>]*>$", s, re.I) or re.match(r"^<br\s*/?>$", s, re.I):
            continue
        if "img.shields.io" in s or "shields.io" in s or "badge.svg" in s:
            kind = "Badge"
        elif re.match(r"^<h[1-6]\b", s, re.I) or HEADING.match(s):
            kind = "Heading"
        elif IMAGE_MD.search(s) or IMAGE_HTML.search(s):
            kind = "Image"
        elif s.startswith(">"):
            kind = "Quote/alert block"
        elif s.startswith("|"):
            kind = "Table"
        elif s.startswith("<"):
            kind = "HTML block"
        else:
            kind = "Body text"
        # Adjacent body/HTML blocks are one visual paragraph, so count them once
        if first and kind in ("Body text", "HTML block") and first[-1][1] in ("Body text", "HTML block"):
            pass
        else:
            first.append((i, kind))
        if len(first) >= 10:
            break

    hints = []
    if first:
        kinds = [k for _, k in first]
        first_img = next((n for n, k in enumerate(kinds, 1) if k in ("Image", "Code block")), None)
        if first_img and first_img > 3:
            hints.append(f"Visual anchor too late: the first real visual element is at position {first_img}")
        first_quote = next((n for n, k in enumerate(kinds, 1) if k == "Quote/alert block"), None)
        if first_quote and (first_img is None or first_quote < first_img):
            hints.append("First screen opens with a quote/alert block, image or result below — author view beating reader view")
        badge_run = 0
        for k in kinds:
            if k == "Badge":
                badge_run += 1
                if badge_run == 4:
                    hints.append("4+ badges in a row on the first screen: more visual noise than signal")
                    break
            else:
                badge_run = 0

    visible = re.sub(r"<details\b.*?</details>", "", body, flags=re.S | re.I)
    if len(IMAGE_MD.findall(visible)) + len(re.findall(r"<img\b", visible, re.I)) > 6:
        hints.append("More than 6 uncollapsed images: keep two up front, move the rest into <details>, or delete them")
    h2_count = len([a for a in re.findall(r"^##\s+\S", body, re.M)])
    has_nav = bool(re.search(r"\]\(#[^)]", body) or re.search(r"<a\b[^>]*href=\"#[^\"]", body, re.I))
    if len(lines) > 120 and h2_count >= 7 and not has_nav:
        hints.append(f"{len(lines)} lines and {h2_count} h2 sections, but no table of contents or top nav")

    # ---------- output ----------
    print(f"\n■ {path}")
    print(f"  Repo root: {root}")
    print(f"  Lines: {len(lines)}  Headings: {len(anchors) - 2}  Images: {len(IMAGE_MD.findall(body)) + len(re.findall(r'<img\b', body, re.I))}")

    print("\n  First-screen element order (what readers actually see first):")
    for ln, kind in first:
        print(f"    {ln:>4}  {kind}")

    if dup_note:
        print(f"\n  · {dup_note}")

    if hints:
        print("\n  Diagnostic hints (structure, not errors):")
        for h in hints:
            print(f"    - {h}")

    for label, items in (("ERROR", errors), ("WARN", warns)):
        if items:
            print(f"\n  {label}:")
            for ln, msg, _cat in items:
                loc = f"L{ln}" if ln else "  -"
                print(f"    {loc:>6}  {msg}")

    if not errors and not warns and not hints:
        print("\n  No issues found.")

    print(f"\n  Total: {len(errors)} errors, {len(warns)} warnings")
    return len(errors)


def check_image(line_no, alt, src, root, errors, warns):
    if not alt.strip():
        warns.append((line_no, f"Image has no alt text: {src}", "img"))
    if src.startswith(SKIP_SCHEMES):
        return
    rel = src.split("?")[0].split("#")[0]
    abs_path = os.path.normpath(os.path.join(root, rel.replace("%20", " ")))
    if not os.path.exists(abs_path):
        errors.append((line_no, f"Image file does not exist: {rel} (shows as a broken image locally)", "img"))
        return
    size_mb = os.path.getsize(abs_path) / (1024 * 1024)
    if size_mb > MAX_IMAGE_MB:
        warns.append((line_no, f"Image is {size_mb:.1f} MB, over the {MAX_IMAGE_MB:g} MB limit and slow to load: {rel}", "img"))


def check_badge(line_no, url, errors, warns):
    if "#" in url:
        errors.append((line_no, "Badge URL contains `#`, which cuts the link off there", "badge"))
        return
    if " " in url:
        warns.append((line_no, "Badge URL contains a space; encode it as %20 or _", "badge"))
    m = SHIELDS.search(url)
    if not m:
        return
    kind = m.group(1)
    if kind != "badge":
        return
    slug_part = url.split("/badge/", 1)[1].split("?")[0].rstrip("/")
    # Format: label-message-color / label-message / message
    parts = slug_part.replace("--", "\x00").split("-")
    parts = [p.replace("\x00", "-") for p in parts]
    if len(parts) < 3:
        warns.append(
            (line_no, f"Static badge needs three parts, label-message-color; found {len(parts)}: {slug_part}", "badge")
        )


def main():
    ap = argparse.ArgumentParser(description="README audit")
    ap.add_argument("files", nargs="+", help="path to a README file")
    ap.add_argument("--repo", default=None, help="repo root for resolving relative image paths (defaults to the file's directory)")
    args = ap.parse_args()

    total = 0
    for f in args.files:
        if not os.path.exists(f):
            print(f"File not found: {f}", file=sys.stderr)
            total += 1
            continue
        total += check(f, args.repo)

    print()
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
