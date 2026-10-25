# Opening Screen Paradigm Library

Eight opening-screen structures. Pick one, then adapt it to the project. Don't mix more than two — mixing is the main source of the "designed by committee" look.

How to choose: start with the assets you have (is there a demo GIF or an output screenshot?), then the project type, and only then personal taste.

| Assets on hand | Candidate paradigms |
| --- | --- |
| Animated demo (GIF, or an MP4 you can trim) | 2, 7 |
| Static output screenshots only | 2, 7 |
| Logo only | 1, 3 |
| Nothing at all | 3, 6 |

---

## 1. Centered logo opener

**Use when**: CLI tools, libraries and frameworks with a real logo. Brand impression comes first, and the product itself doesn't screenshot well.

```markdown
<p align="center">
  <img src="docs/logo.svg" alt="Project Name" width="120">
</p>

<h1 align="center">Project Name</h1>

<p align="center">
  One sentence saying what it does. 25 words or fewer.<br>
  <sub>The second line is for the differentiator — "zero dependencies · 5 KB · Node 18+"</sub>
</p>

<p align="center">
  <a href="..."><img src="https://img.shields.io/badge/..."></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg"></a>
</p>

---
```

**Failure mode**: the logo is a geometric shape someone sketched in five minutes, and centering it at 3x size just magnifies the flaws. If the logo isn't good, use paradigm 3 or 6. Don't force it.

---

## 2. Demo first

**Use when**: tools with visible output — image generation, editors, games, visualizations, recorded CLI sessions. **This is the best answer for visual projects**, and the one that gets wasted most often.

```markdown
<h1 align="center">Project Name</h1>

<p align="center">One sentence saying what it does. Runs entirely in the browser — no backend, nothing uploaded.</p>

<p align="center">
  <img src="docs/demo.gif" alt="Demo: type one sentence and a fake sponsor line scrolls into the card" width="720">
</p>

---
```

The rule: **the GIF goes right after that one sentence, with nothing in between**. Badges, language switchers, disclaimers, tables of contents — all of it moves down. Readers watch the GIF before they'll look at a second element.

**Failure mode**: the GIF opens on a blank or loading frame, so it never plays unless the reader moves the mouse. Or it runs eight seconds and the point is still unclear. Cut it to four, loop it seamlessly.

---

## 3. Terminal anchor

**Use when**: pure developer tools. There's no screenshot to show, so let a single command carry the visual weight.

````markdown
# Project Name

One sentence saying what it does.

```bash
npx project-name --input photo.jpg --out ascii.txt
```

---
````

The command block is the opening screen's "image". Requirements: a command that actually runs (one that fails is worse than none), a real sample of its output, and no pile of flags.

**Failure mode**: the block is five optional flags and a comment, and the reader still can't tell what happens when they run it.

---

## 4. Comparison matrix opener

**Use when**: libraries with obvious alternatives ("faster than X", "does Z without needing Y"). Turning the difference into a table answers the reader's question before they ask it.

```markdown
# Project Name

One sentence saying what it does, and what it replaces.

| | Project Name | Alternative A | Alternative B |
| --- | --- | --- | --- |
| Runtime dependencies | 0 | 12 | 4 |
| Bundle size | 5 KB | 40 KB | 18 KB |
| Needs a backend | No | Yes | No |
| Export formats | PNG / SVG / PDF | PNG | PNG |

---
```

**Failure mode**: you pit your strongest row against their weakest and the table turns into an ad. Experienced readers spot it instantly and stop trusting everything below it. Pick the rows your readers actually care about, and skip the ones you win that nobody asked about.

---

## 5. Dense index

**Use when**: collections, lists, template libraries, awesome-lists. Readers came here to find something, not to be persuaded.

```markdown
<h1 align="center">Project Name</h1>

<p align="center">One sentence + a count (9 tools, all running in the browser, no ads, no tracking)</p>

<p align="center">
  <a href="#tools">Tools</a> · <a href="#self-hosting">Self-hosting</a> · <a href="#development">Development</a>
</p>

---

## Tools

| Tool | What it does |
| --- | --- |
| [Name](link) | One sentence |
| [Name](link) | One sentence |
```

**Failure mode**: you build the table, get it right, then stack nine screenshots underneath it anyway. An index persuades through density and scannability; images destroy both. If you need pictures, collapse them.

---

## 6. Minimal statement

**Use when**: experimental projects, projects with a strong authorial voice, internal tools, things you only want to archive. Zero decoration is itself a show of confidence.

````markdown
# Project Name

One sentence.

```bash
install command
```

Everything else — usage, limitations, license — follows below. No dividers, no badges, no images.
````

**Failure mode**: the content can't hold it up. Minimal looks clean when the information is dense, and merely bare when there's nothing there.

---

## 7. Screenshot gallery grid

**Use when**: themes, UI component libraries, template sets — the output *is* a set of images, and a wall of them is the best documentation you can write.

```markdown
<p align="center">
  <img src="docs/shot-1.png" alt="Task board in the dark theme" width="410">
  <img src="docs/shot-2.png" alt="The same board in the light theme" width="410"><br>
  <img src="docs/shot-3.png" alt="Mobile layout" width="410">
  <img src="docs/shot-4.png" alt="Empty state" width="410">
</p>
```

Rules: **images in the same row share one width and height** (guess at it and the baselines go ragged, which reads as sloppy at a glance); two rows of four on the opening screen at most, the rest collapsed; every alt text distinct, describing what's happening in that image.

**Failure mode**: nine screenshots at nine different sizes, widths guessed by eye, and a page that looks like a broken grid.

---

## 8. Status board

**Use when**: cross-platform libraries, projects that have to prove compatibility ("runs on Windows, macOS and Linux", "supports 12 languages"). The opening screen is a status matrix.

```markdown
# Project Name

One sentence saying what it does.

| Platform | Status | Notes |
| --- | --- | --- |
| Windows 10+ | Full support | |
| macOS 12+ | Full support | |
| Linux | Supported | Requires glibc 2.31+ |
| Web | Preview only | No export |

---
```

**Failure mode**: every cell says "supported" and the reader knows immediately that the matrix carries no information. Spelling out the limits is more convincing than filling the grid with checkmarks.

---

## The only sanctioned mix

Paradigm A on the opening screen; by the second screen you're in the body structure anyway. That isn't mixing.

What isn't allowed: a centered logo, a big GIF, a comparison table and a badge wall all on the opening screen at once. That isn't information-rich. It's a failure to choose.
