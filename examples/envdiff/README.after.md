<h1 align="center">envdiff</h1>

<p align="center">See what changed between two .env files — with every value masked.<br>
One command, no upload, no account.</p>

```console
$ envdiff .env.old .env.new

  + STRIPE_WEBHOOK_SECRET   sk_live_••••••••3f2a
  ~ DATABASE_URL            postgres://app:••••@db.internal:5432/app
  - LEGACY_API_KEY          (removed)

3 changes · 0 secrets printed
```

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-57606a.svg" alt="License: MIT"></a>
  <a href="https://nodejs.org/"><img src="https://img.shields.io/badge/node-18%2B-339933.svg" alt="Node 18 or newer"></a>
  <br>
  <sub><a href="#install">Install</a> · <a href="#options">Options</a> · <a href="#limits">Limits</a></sub>
</p>

> **Not a secret scanner.** Regex parsing, no multi-line values, no CI integration. It covers the five seconds before `git add`, not the whole pipeline.

---

## Why this exists

Every project ends up with two `.env` files: the one on your machine, and the one from a teammate or from last week before you rotated a key. Comparing them by hand works until the file has forty lines, at which point you start missing things.

Existing tools either dump the diff including the secret values — so you can't paste it into a chat — or show nothing useful at all. This one shows the shape of the change: which keys were added, removed or modified, and a masked preview so you can tell which key it is without exposing it.

## Install

```bash
npm install -g envdiff
```

## Usage

```bash
envdiff .env.old .env.new
```

## Options

| Flag | Effect |
| --- | --- |
| `--reveal` | Print unmasked values |
| `--json` | Machine-readable output |
| `--strict` | Exit 1 on any difference |

## Limits

- Regex-based parsing, so a multi-line value containing `#` will confuse it
- No test coverage worth bragging about
- Reads both files in one pass and nothing else: no network, no telemetry, no account

## License

MIT
