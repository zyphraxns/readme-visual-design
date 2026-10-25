# Contributing

Two things are worth contributing here: a new opening paradigm, or a new audit rule. Everything else is probably out of scope.

## Adding an opening paradigm

A paradigm is a structure for the first screen, not a style. If it can't be reduced to a markdown skeleton someone can copy, it isn't a paradigm yet.

Append it to `references/opening-paradigms.md` and include all four parts:

1. **When to use it** — project type plus the assets it requires. If it needs a GIF, say so.
2. **The skeleton** — a fenced markdown block that renders correctly on GitHub as written. Test it by pasting it into a scratch repo; centered HTML blocks and nested fences break more often than you'd think.
3. **The failure mode** — what this paradigm looks like when it's the wrong choice. This is the part that makes the library useful, so don't skip it.
4. **One line in the selection table** at the top, mapping your paradigm to an asset situation.

Do not add a ninth paradigm that is a variation of an existing one. Tune the existing one instead — the library's value is that eight choices is already more than most people can hold in their head.

## Adding an audit rule

`scripts/check_readme.py` is a rule engine with a deliberately low tolerance for false positives. A rule that fires on healthy READMEs trains people to ignore the tool.

Before you open a PR:

1. The rule must be **objectively verifiable** — a broken thing, not a matter of taste. "Badge color is inconsistent" is taste. "Badge URL contains `#` and gets truncated" is a rule.
2. Run it against at least three real READMEs, including one good one. It must not fire on the good one.
3. Add it to the docstring at the top of the file, in the check list.
4. If it's a judgment call rather than a violation, put it in `hints`, not in `errors` or `warns`. Hints are advisory; errors block.

The script uses only the standard library. Do not add dependencies to it.

## Reporting a bad revamp

The most useful issue you can file: a before/after pair where the skill's output was worse than the original. Include both READMEs (or links), what the skill chose, and what you would have done. Those reports are how the paradigm library gets corrected.

## The one rule for the docs

Every instruction has to explain **why**. The skill is read by a model that can follow reasoning but memorizes rules badly. So writing "ALWAYS do X" is a bug, and writing "do X, because Y breaks otherwise" is the norm.

Concretely, when you edit the prose:

- Keep the voice blunt and specific. Short declarative sentences. No hedging, no "you might want to consider".
- Delete adjectives that aren't backed by an example. "Powerful and highly customizable" is what this skill exists to remove.
- If a rule has an exception, state the exception and the reason, not a softer version of the rule.

## Scope

- GitHub's renderer is the only target. PRs that generalize to GitLab or Notion will be declined unless they cost nothing on GitHub.
- No features that need a build step or a network call at runtime.
- No decorative additions to the skill itself. It is a tool, not a brand.
