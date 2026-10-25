# envdiff

[![Build](https://github.com/example/envdiff/actions/workflows/ci.yml/badge.svg)](https://github.com/example/envdiff/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Node](https://img.shields.io/badge/node-%3E%3D18-339933.svg)](https://nodejs.org/)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-orange.svg)](#)

> ### Before you use this
>
> envdiff started as a weekend script to stop me from committing a production key
> by accident. It is not audited, it has no test coverage worth bragging about,
> and the parsing is regex-based, which means it will trip over a multi-line
> value with a `#` in it.
>
> It is also not a replacement for secret scanning in CI. If you need that, use
> one of the established tools. This is a convenience for the five seconds before
> you run `git add`.
>
> The project is MIT licensed and there are no plans to commercialise it.

## Why another env tool

Every project ends up with a `.env` file, and every project eventually has two of
them: the one on your machine and the one that came from a teammate, or the one
from last week before you rotated a key. Comparing them by hand is fine until the
file has forty lines, at which point you start missing things.

The existing tools either show you the diff of everything, including the secret
values, which means you cannot paste the output into a chat, or they show you
nothing useful at all. envdiff shows you the shape of the change: which keys were
added, removed or modified, and a masked preview of the value so you can tell
which key it is without exposing it.

## Features

- **Fast** — reads both files in a single pass
- **Safe by default** — values are masked unless you pass `--reveal`
- **Node 18+** — no build step, installed from npm
- **Zero dependencies** — the whole thing is 300 lines
- **Works with any .env dialect** — export prefixes, quoted values, comments
- **Exit codes for CI** — returns 1 when keys are missing on one side

## Install

```
npm install -g envdiff
```

## Usage

```
envdiff .env.old .env.new
```

## Options

| Flag | Effect |
| --- | --- |
| `--reveal` | print unmasked values |
| `--json` | machine-readable output |
| `--strict` | exit 1 on any difference |

## License

MIT
