# The real limits of GitHub Markdown

Before you touch a README you need to know which syntax survives GitHub's web renderer and which gets stripped. Skip that, push the rewrite, and watch the whole thing fall apart on the live page.

## What works

| Syntax | Notes |
| --- | --- |
| `align="center"` | Works on `<p>` `<h1>` `<div>` `<img>`. The only alignment mechanism you have left |
| `<details>` / `<summary>` | The collapsed section. The single most useful tool a README has |
| `<picture>` + `<source media="(prefers-color-scheme: dark)">` | Light and dark image pairs, officially supported by GitHub |
| `<img width="" height="">` | Sets display size. This is your only layout control |
| `<kbd>` `<sub>` `<sup>` `<br>` `<hr>` | All of them work |
| Markdown tables | Render reliably. The only way to get more than one column |
| `> [!NOTE]` / `TIP` / `IMPORTANT` / `WARNING` / `CAUTION` | Coloured callouts. Must be written `> [!TYPE]`, every line below starts with `> `, type name in all caps, and nothing outside those five is recognised |
| ```` ```mermaid ```` | Renders a diagram. Theme colors follow GitHub's light/dark theme and **cannot be customised** |
| Task lists, footnotes, strikethrough, `<!-- comments -->` | All of them work |

## What gets stripped

| What you write | What you get |
| --- | --- |
| `style="..."` attributes | Stripped. Font size, color, margins, border radius: none of it does anything |
| `<style>` / `<script>` / `<iframe>` / `<video>` / `<audio>` | Stripped, or the whole block silently dies |
| `<center>` / `<font>` / `<marquee>` | Deprecated tags. Not rendered |
| Custom `id` / `class` / `data-*` | Stripped. Don't plan on inventing your own anchors |
| CSS to round image corners, add shadows, build cards | Impossible. There is no such thing as a card in a README |

**The conclusion**: any CSS scheme claiming it will make a README "more refined" is a fraud. You get to control structure, not styling.

## Traps that fail quietly

**Markdown inside an HTML block is not always parsed.** Write `<p align="center">**bold**</p>` and the bold may show up as literal asterisks. Inside HTML tags, use `<b>`, `<i>`, `<a href="">`. To mix Markdown in, leave a blank line above and below the HTML block so it stands as its own block.

**Empty links jump back to the top of the page.** `[![badge](...)](#)` is the most common fake link in READMEs. The reader clicks once, the page flies to the top, and your impression takes the hit. If there is no real destination, don't wrap it in a link.

**Relative paths are case-sensitive.** Local macOS is not. GitHub is. `Docs/Demo.gif` and `docs/demo.gif` both display on your machine and both come out broken once pushed.

**Non-ASCII paths and spaces break.** They display, but they drop out when copied to another platform, cached by an image proxy, or processed by a third-party README renderer. Keep filenames ASCII, lowercase, hyphenated.

**Anchors are generated for you.** The rules: lowercase, spaces to `-`, punctuation dropped, CJK preserved (URL-encoded). A second heading with the same name gets `-1` appended. Click the heading on the live page before you hand-write an anchor.

**The content column is narrow.** On a wide screen the body is roughly 1012px, and `width="860"` is the safe value; anything past 1000 gets compressed, and two 410s side by side fit exactly. An image that is too wide produces a horizontal scrollbar on narrow screens.

**There are three themes, and `prefers-color-scheme` only recognises two.** GitHub has light / dark / dimmed, and `dimmed` is handled as dark. So a dark image has to hold up under both dark themes.

**Images go through the camo proxy.** An external image is pulled by the proxy on first load; if that pull fails, it is broken forever. External images also miss repository version control. If it can live in the repo, put it in the repo.

**Size ceiling for animated images.** Past 10 MB GitHub may refuse to render a GIF or load it painfully slowly. Under 5 MB is safest; drop the frame rate or the color count if you have to.

## What only works on GitHub

- The repo homepage renders the README automatically, and **it treats the first image / the opening screen as the reference for the social preview** (the actual og:image comes from repo settings, but this is the screen a reader lands on)
- Issues and PRs support alerts and mermaid too, so what you write in the README carries over
- Relative links to `LICENSE` and `CONTRIBUTING.md` resolve to the rendered page

If the README also gets mirrored to Gitee, GitLab, npm or PyPI, alerts and mermaid will most likely break. Fall back to plain `>` blockquotes and ASCII diagrams. This skill serves GitHub only, and that is the downgrade path when you need to be portable.
