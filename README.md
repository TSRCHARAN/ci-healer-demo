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

## What actually happened (live runs)

| Scenario | ci-healer's diagnosis | What it did | Result |
|---|---|---|---|
| [#1 lint](https://github.com/TSRCHARAN/ci-healer-demo/pull/1) | `lint_format`, matched by rule (no LLM call) | opened fix PR [#5](https://github.com/TSRCHARAN/ci-healer-demo/pull/5) | ✅ CI passed on the fix PR, recorded as verified |
| [#2 flaky](https://github.com/TSRCHARAN/ci-healer-demo/pull/2) | `flaky_test` (0.95, Gemini) | [re-ran the failed job](https://github.com/TSRCHARAN/ci-healer-demo/actions/runs/44589381569) | ✅ attempt 2 passed, so the test was recorded as flaky |
| [#3 bug](https://github.com/TSRCHARAN/ci-healer-demo/pull/3) | `code_break` (0.95), root cause named correctly | commented; judged the fix non-trivial | ⚠️ safe but cautious, see note |
| [#4 missing secret](https://github.com/TSRCHARAN/ci-healer-demo/pull/4) | `config` (0.95): missing `PAYMENTS_API_KEY` | commented, no code change | ✅ exactly right |

Each **ci-healer** run in the [Actions tab](https://github.com/TSRCHARAN/ci-healer-demo/actions/workflows/ci-healer.yml)
has a job summary with the full diagnosis.

**Note on #3:** these runs used a free-tier Gemini key that was being rate-limited (429/503).
The primary model gave up after its retries and the fallback model answered. It diagnosed the
off-by-one correctly but declined to write the fix. Declining is an allowed outcome: ci-healer
only opens a PR when the model is confident the fix is small and obvious.

**Note on #2:** the flaky test is *simulated* (slow on a run's first attempt, fast on re-run) so
the demo shows the retry → learn path every time instead of on a coin toss.

## What the demo taught ci-healer

- A model overloaded under concurrent load: v1.0.1 added patient retries and a fallback model.
- Parallel Action runs overwrote each other's cached history: v1.0.2 reads the previous
  attempt's failures straight from GitHub.
- A lint fix that re-wrapped an `assert` line was rejected by the "never rewrite assertions in
  tests" guardrail, which is conservative by design.

Everything here is intentionally broken in public. Nothing in these branches is meant to be merged.
