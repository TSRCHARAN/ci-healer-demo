# ci-healer demo 🩺

A live demo of [**ci-healer**](https://github.com/TSRCHARAN/ci-healer), a GitHub Action that
watches CI, works out *why* a run failed, and responds the way a careful engineer would.

`main` is a tiny, healthy Python project. Each `demo/*` branch breaks CI on purpose, and has an
open pull request so you can see what ci-healer did about it, in the PR itself, in the bot's
fix PRs, and in the **ci-healer** workflow runs (each has a job summary with the diagnosis).

| Scenario | How CI breaks | What ci-healer should do |
|---|---|---|
| `demo/1-lint` | an unused import (ruff F401) | recognise it by rule (no LLM call) and open a **fix PR** |
| `demo/2-flaky` | a timing test that fails about half the time | **re-run** the failed job; if the same commit then passes, record the test as flaky |
| `demo/3-bug` | off-by-one in `median()` | diagnose with the LLM and open a small, guarded **fix PR** |
| `demo/4-missing-secret` | a test needs `PAYMENTS_API_KEY`, which isn't set | diagnose it as a config problem and **comment** — no code change |

How it's wired: [.github/workflows/ci-healer.yml](.github/workflows/ci-healer.yml) runs after
every `ci` run with `on: workflow_run`.

Everything here is intentionally broken in public. Nothing in these branches is meant to be merged.
