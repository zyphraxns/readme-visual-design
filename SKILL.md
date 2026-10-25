---
name: readme-visual-design
description: "Revamp the visual presentation of an existing GitHub README.md (opening screen, badges, screenshots/GIFs, folds, tables, information hierarchy). Use when the user says the README is ugly, has poor presentation or has no pull, wants to beautify / reorder / optimize / audit the README, complains that the opening screen is unwatchable, the badges are a mess or the project's presentation doesn't sell, or asks you to review how a repo's README looks. Revamps existing READMEs only — it does not write a full open-source doc set from scratch. Chinese triggers: README 美化, README 改造, 项目门面."
---

# README Visual Revamp

In Markdown you control only **structure, hierarchy, whitespace and assets**. Font size, color, spacing — none of it. GitHub scrubs all of that out. So this job isn't "tuning styles". It's **deciding what the reader sees in the first 8 seconds, in what order, and what convinces them.**

Revamping a README that already has content is worth more than writing one from scratch, and it's more dangerous. The author's voice and information are assets. Before you touch them, work out what has to survive unchanged.

## What this doesn't do

- Write a whole open-source doc set from scratch
- Touch any file other than the README
- Generate logos or banners, or fill gaps with AI images
- Commit. Leave the diff for the author

---

## Step 1: Read the ground truth

Don't offer opinions yet. Read, in order:

1. **The README itself**, plus every `README.*.md` beside it (`.en`, `.zh-CN`, `.zh` all count — they have to be handled as pairs)
2. **What the repo actually says**: `package.json` / `pyproject.toml` / `Cargo.toml` / `go.mod`, entry files, `LICENSE`, `.github/workflows/`. Every install command, version requirement and CI badge in the README has to match the code. Log whatever doesn't — that's not a visual problem, but the revamp will drag it into the open.
3. **Asset inventory**: every png/jpg/gif/svg/webp/mp4 in the repo, where it lives and how big it is (`find . -type f \( -iname "*.png" -o -iname "*.gif" ... \) -not -path "./node_modules/*" -not -path "./.git/*"`). Check whether the images the README references actually exist, and whether they're absurdly large (a single image over 5 MB stalls page load; a GIF over 10 MB may not render on GitHub at all).
4. **git state** (`git status --porcelain`). If the working tree is dirty, warn the author first, or copy the original to `README.md.bak` before you change anything.

Item 2 above is not optional. A visual revamp is exactly where hallucination slips in — `npm run dev` becomes `pnpm dev`, the port is wrong, a project with no CI at all gets a CI badge. The first thing a reader does is copy the command.

## Step 2: Diagnose

Pin the disease with three questions. One sentence each:

1. **Who is the reader** — fellow developers, prospective users, recruiters, or just the author archiving their own work? This decides what the opening screen has to prove.
2. **What gets read in the first 8 seconds** — list the elements actually visible on the opening screen (roughly two viewports) in order. Most problems are **ordering** problems, not missing elements.
3. **Is there any visual proof** — one screenshot or GIF of the output a reader can understand beats ten lines of adjectives. Learn to tell an *entry screenshot* from an *output screenshot*: a web panel, a directory tree, an editor window are all entry points. The reader wants to see what the thing produces.

Show the diagnosis to the author — three lines is enough, no long-form analysis. Then go straight into the revamp. Don't stop and wait for approval, unless you've judged it a heavy re-layout (see Step 4).

## Step 3: Pick an opening paradigm

Choose one from `references/opening-paradigms.md` and tune it to the project. Don't invent a structure on the spot: give the same project two different treatments and the author can't sign off, and you can't explain yourself.

The choice follows from **project type × what assets you have** — not personal taste. Once you've picked, justify it in one sentence, and that sentence has to name the more tempting option you ruled out and why.

## Step 4: Asset gate

Decide how big the change is first:

- **Light**: ordering, hierarchy, folds, badges, copy density only; the opening visual anchor stays → go ahead, and put missing assets in the gap list at the end.
- **Heavy**: the opening visual anchor has to be redone (new hero image, add a GIF, change paradigm) → if the key assets are missing, **stop**. Tell the author what's missing and the cheapest way to get it. Re-laying out an opening screen with no image is wasted work.

Asset gaps have to be written as instructions: "I need a 1200×750 screenshot of the output — don't shoot the sidebar, shoot the result itself. On macOS use `Cmd+Shift+4` to select the region, save as PNG, drop it in `docs/`."

## Step 5: Rewrite

### Opening screen (the most important 60 lines)

Goal: title + one sentence + one visual anchor. Inside those three, say what this is, who it's for, and what it looks like. Everything else moves down.

The line under the title is not a feature list. Write **a sentence the reader can repeat to someone else**: "Turns an image into ASCII art you can copy or download as PNG" beats "supports multiple character sets, multiple output formats, highly customizable".

### Badges

- Five at most. Past that, cut. More badges doesn't read as more professional — it reads as more noise.
- Every badge must link to **something that proves it**: CI → the workflow file, License → LICENSE, version → the registry page. A badge pointing at `#`, or at nothing at all, is pure decoration. Delete it.
- Two semantic colors per README, no more (a status color plus a brand color, say). Mix shields defaults with custom colors and it looks stitched together at a glance.
- Badges earn their place in exactly three cases: they prove the project is alive (CI/version), they prove it's legally usable (License), or they save the reader a step (npm/pip downloads). Everything else is self-indulgence.

### Images

- Two at most on the opening screen, and both must be **output**, not entry points.
- Relative paths, ASCII lowercase filenames with hyphens (`screenshot-home.png`). CJK characters and spaces in paths break when copied to another platform or cached by camo — showing up on GitHub doesn't mean it shows up anywhere else.
- Every image needs alt text, and the alt must describe **what's happening in the image**, not "screenshot".
- More than three images? Don't tile them. Put two on the opening screen, push the rest into a `<details>` gallery, or just delete them — nobody reads nine screenshots to the end.
- Light and dark variants go through `<picture>` + `prefers-color-scheme`. Don't ship two images and make the reader pick.

### Long content

- Comparison data (formats, platforms, limits, parameters) always goes in a table, never a bullet list.
- `<details>` is for "only if you want it" material: full config options, changelog, platform difference tables. **Don't fold away your selling points** — folding something says you've decided it doesn't matter.
- More than six H2s and a visibly long page? Add a short table of contents. Fewer than six, skip it — a TOC is noise too.

### Upfront warnings, disclaimers, experimental notices

This kind of block usually sits at the very top because it matters to the author. It doesn't matter to the reader, and it's eating the most valuable real estate on the opening screen.

Handling: compress it to one line after the opening screen, or stuff the whole thing into `<details><summary>Disclaimer</summary>`. The exception is genuine legal or safety risk (a tool that deletes files, one that makes network requests) — that keeps one visible line, but not three paragraphs.

### Tone

**Never turn the author's honest sentences into marketing copy.** Lines like "this is a hobby project, maintained when I have time" or "Windows isn't supported, don't ask" are trust assets; rewriting them makes the README look suspicious. Polish only: redundancy, repetition, word order, unclear references. If you delete a sentence, be able to say why.

**Write what you hand back in the language the author used.** The diagnosis, the change log and the gap list all follow the language of the request, not the language of this file. The README itself keeps whatever language it already had — never translate a README as part of a visual revamp.

## Step 6: Validate and deliver

1. Run the audit and fix what it reports (image paths, dead links, heading hierarchy, alert syntax, unclosed details, table column counts, in-page anchors, image sizes):

   ```bash
   python scripts/check_readme.py README.md README.zh-CN.md --repo .
   ```

   The "opening screen element order" it prints is exactly the fact you needed for the Step 2 diagnosis, and "diagnostic hints" are structural problems. Run it again after the edits; the hints should be empty.

2. Generate a before/after preview of the opening screen. The author can't judge whether a README looks good from a terminal — you have to show them:

   ```bash
   python scripts/preview_firstscreen.py --before README.bak.md --after README.md \
       --out /tmp/readme-preview.html --title "Project Name" --repo .
   ```

   Open the generated HTML: old on the left, new on the right, dark mode toggle in the top right. It lays out at GitHub's body width (1012px) and then scales, so whether two 410px images sit side by side or a table overflows is exactly what you'd see in production.

3. Deliver three things: the revised README (two copies if bilingual), a change log (item by item: what was deleted, why, and where wording changed), and the asset gap list.
4. No commit. Tell the author to run `git diff README.md` and look for themselves, and `git checkout -- README.md` if they don't like it.
5. Back up before you start: `cp README.md README.bak.md`. The preview needs the old file; let the author delete the backup when they're done.

## Bilingual mirror

When `README.md` sits alongside `README.en.md` / `README.zh-CN.md`:

- Change both. Structure, images, tables and fold positions must correspond exactly.
- The language switch goes in the same place in both (usually the title block or under the badges), each pointing at the other.
- Technical terms stay in their original form in both (`WebCodecs`, `JSON Patch`). Don't translate them.
- Cross-check when you're done: both files must have the same number of H2s and the same number of images. Counts that don't match mean you missed something.

## A set of common bad smells

Scan for these while you work. If they're there, deal with them:

| Symptom | The real problem |
| --- | --- |
| The opening screen is a disclaimer / origin story / long background | The author's perspective, not the reader's |
| The opening screen is a screenshot of the home UI | You shot the entry point, not the output |
| Nine equal-width screenshots tiled | Using quantity instead of persuasion |
| Every feature opens with a bold label, all the same length | Reads as auto-generated; readers skip it |
| Badges in mismatched colors, some pointing at `#` | Decoration, not information |
| Emoji used as section-heading decoration throughout | Looks cheap unless the project's tone is memes to begin with |
| Whole paragraphs stuffed into table cells | Tables are for comparing across, not reading down like prose |
| Three "highly customizable / powerful / elegant" in one sentence | Adjectives aren't evidence |

## Dependencies

`check_readme.py` uses only the standard library. `preview_firstscreen.py` needs `markdown` (`python -m pip install markdown`). If it won't install, skip the preview and hand the author the revised README plus the change log — the preview is a bonus, not a blocker.

Images in the preview are inlined as data URIs, so the generated HTML can be sent to someone on its own without the repo paths. The cost is size (around 3 MB with a GIF).
