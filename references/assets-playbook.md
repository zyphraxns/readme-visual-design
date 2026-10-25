# The asset playbook

The ceiling on a README's impression is set by its assets. A revamp can only get the assets you already have to perform. So take inventory first, then talk about layout.

## Inventory checklist

```bash
find . -type f \( -iname "*.png" -o -iname "*.jpg" -o -iname "*.jpeg" \
  -o -iname "*.gif" -o -iname "*.svg" -o -iname "*.webp" \
  -o -iname "*.mp4" -o -iname "*.webm" \) \
  -not -path "./node_modules/*" -not -path "./.git/*" -not -path "./dist/*" \
  -exec du -h {} + | sort -h
```

Sort by purpose, not by directory:

| Category | How to tell | Where it goes |
| --- | --- | --- |
| Output screenshot | Something this project produced (a generated image, an exported file, a computed result) | The opening screen, top priority |
| Entry screenshot | The UI, a panel, the file tree, an editor | Second screen onwards, or to show how it is used |
| Explanatory diagram | Architecture, flow, state | The section it belongs to |
| Badges / icons | Small SVGs | The title area |

**Entry screenshots with no output screenshot is the single biggest gap you can have**, far worse than a missing logo. Readers care what the thing produces, not what your UI looks like.

## What a good output screenshot looks like

- **The result is legible**: someone who has not read the README can tell this is a successful output, not a half-finished run or an error state
- **Crop the irrelevant**: no full-screen captures. Leaving the window frame and browser chrome in is the most amateur move available
- **Real data**: `test`, `foo`, `123` make the image read as a placeholder. Use content that looks like the real thing
- **At least 1200px wide**: GitHub displays it at 860, so a small original goes soft
- **Alt text that says what happened**: `alt="final score calculator showing 87.5"`, not `alt="screenshot"`

## Animated images

An animated image is far more persuasive than a still, and it costs more: file size, load time, production time.

Producing one (macOS, zero-cost path):
1. `Cmd+Shift+5`, select a region, record 3-5 seconds
2. `ffmpeg -i in.mov -vf "fps=15,scale=800:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse" out.gif`
3. Target: <= 4 seconds, <= 3 MB, loops seamlessly at both ends

How to decide whether it is worth it: **is the project's whole selling point something you only see when it moves?** If yes, make one. If not, a still is enough. Image generators, animation tools and interactive tools earn one. CLIs, libraries and static sites do not.

## Light and dark pairs

You only need two sets when the project has its own brand color, or when the screenshot is itself dark. How:

```html
<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/shot-dark.png">
    <img src="docs/shot-light.png" alt="Task board in both the dark and the light theme">
  </picture>
</p>
```

Note that GitHub's dimmed theme takes the dark branch, so do not make the dark image pure black. Use a neutral dark somewhere around #0d1117.

## Naming and placement

- All lowercase ASCII, hyphen separated: `docs/demo.gif`, `docs/shot-export.png`
- One directory, either `docs/` or `.github/assets/`. Images scattered through `docs/dev-log/xxx-acceptance-shots/` will break the next time you refactor
- No version numbers, no dates (`screenshot-v2-final.png` is a maintenance disaster)
- When you swap an image, overwrite the same filename instead of adding a new one. Then nothing in the README has to move

## When you have nothing

Downgrade in this order. Do not skip steps:

1. **Can you produce one output screenshot in five minutes?** Run the project once, capture the result. Most of the time this is the correct answer
2. **Can you turn CLI output into a code block?** Command plus real output is a visual anchor in itself (pattern 3)
3. **Can you draw a minimal architecture diagram?** ASCII or mermaid outside a `<details>` block. Cheap, and it works
4. **Drop the decoration and go to pattern 6**: the minimal statement style, carried by the quality of the prose

**What not to do**: have AI generate a cyberpunk banner, ship a placeholder image, or pad the README with screenshots borrowed from another project. Readers spot all three, and they conclude the project was not taken seriously.
