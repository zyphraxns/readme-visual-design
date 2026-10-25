# Badge rules

Badges are one of the worst returns on effort in the whole decoration catalogue, and the easiest place to look "AI generated". Use few, use the right ones, make them click.

## How many

0 to 5. The test is not "what could I put there" but "does this stop the reader asking a question".

Worth adding:

| Badge | Why it earns its place | The link must point to |
| --- | --- | --- |
| CI / build status | Proves the project is alive and the build is not broken | The actions page for `.github/workflows/xxx.yml` |
| License | Proves it can legally be used | The `LICENSE` file |
| Package version / install count | Saves the reader a search | The npm / PyPI / crates page |
| Supported platforms (only when genuinely cross-platform) | Answers "will it run on my machine" | No link is acceptable, but do not point it at `#` |

Not worth adding: language or stack (the README says so anyway), "PRs welcome", "made with love", star count (narcissistic, and it moves as the repo loses stars), anything that has to point at `#`.

## Anatomy of a shields.io URL

```
https://img.shields.io/badge/<label>-<message>-<color>
```

Three hard rules:

1. **Encode spaces and special characters**: a space is `%20` (or `_`, which shields turns into a space), the hyphen `-` is itself the separator so it has to be written `--`, and `#` cannot appear in a color value at all (no `#` in the color argument)
2. **Hex colors without the hash**: `3178c6` is right, `#3178c6` is wrong
3. **All three segments are required**: leave out message or color and you get no error, just `invalid` or scrambled colors

Common mistakes:

| What you write | What you get |
| --- | --- |
| `badge/license-MIT` | No color. Renders grey or invalid |
| `badge/license-MIT-#3178c6` | The `#` cuts the whole URL short |
| `badge/TypeScript%20strict-3178c6` | No label, so "TypeScript strict" ends up as part of the wrong segment |
| `badge/My Project-type-ts-blue` | The `-` in the middle is read as a separator and the output is garbled, so write `My%20Project` |

Dynamic badges (`/github/v/release/...`, `/npm/v/...`) save you guessing a color, but they depend on shields reaching your repo, so they do not work on private repos.

## Visual consistency

Badges in one README have to share a single style, or they read as assembled from scraps:

- All default `flat`, or all `flat-square`. Never mixed
- Two semantic colors at most: a status color (green/red/yellow) plus one brand color. Four badges in four colors is the most common failing
- Fixed order: status first (CI, version), credentials next (License), platform last
- Skip `for-the-badge` and that oversized look. It turns noisy in a README

## Self-hosted CI badges

A GitHub Actions badge URL has to carry the workflow file name, not the workflow's name:

```
GOOD  https://github.com/USER/REPO/actions/workflows/ci.yml/badge.svg
WRONG https://github.com/USER/REPO/actions/workflows/CI/badge.svg
WRONG https://github.com/USER/REPO/workflows/CI/badge.svg
```

The first one also needs a link to `https://github.com/USER/REPO/actions/workflows/ci.yml`, so one click shows the build history. **A badge without a link carries no information.**

## What not to add

- **Star count**: it falls, and it says nothing about quality
- **Third-party "awesome" endorsements**: unless you are actually listed
- **Language breakdown cards and contribution graphs (github-readme-stats and friends)**: they run on someone else's public instance, they get rate limited, they 503, they are unreliable from inside China, and you do not control the visual style. Do not outsource the front of your repo to a free service
- **Self-congratulatory static badges like "No backend" or "Zero deps"**: that belongs in one sentence of body copy, where it is more convincing
