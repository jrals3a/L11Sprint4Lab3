# S4_3 Lab: Playwright UI Testing (verified solution)

Every phase was built in `task-tracker/` from the instructor's S4_3 starter and run for real, including a real headless Chromium and one headed run.
Final state on `main`: **79 tests passing** (74 + the 5 Playwright tests, with the server running) · **85% coverage** · `mypy app/` clean · `ruff check .` clean · bandit: only the 2 expected B110 findings.

| Branch | Lab phase |
|---|---|
| `feature/rf014-playwright-setup` | 2: `robotframework-browser` removed, `setup_browsers.py` simplified, `tests/ui/conftest.py`, seed test, `pyproject.toml` consolidation (ruff/bandit/pytest config + `ui` marker), `pytest.ini` deleted, ruff fixes, `python-app.yml` (unit/API split, uv and runner pinned), `playwright.yml` |
| `test/rf014-playwright-ui-tests` | 4–5: validation, complete, delete tests, then the E2E test |

The `Merge …` commits are a **local simulation** of the PR merges. Nothing was pushed, there are no PRs or issues on GitHub, and I took no screenshots for you.

## What's in this folder

- `task-tracker/`: the finished repo, with the template at `images/s4/kahsai-S4_3-screenshots.md` (name and date filled in; repo URL and screenshots are yours).
- `evidence/`: raw output from my runs, named after the screenshots they match. The `*.flask.txt` files are Flask's own request log for each run, which is what Screenshots 30 and 32 show.
- `run_suite.sh`: the helper I used to run things with the Flask server (see discrepancy 1).

## Results at each step (compare with your own)

| Step | What I got |
|---|---|
| Baseline (Screenshot 23) | 74 passed |
| `uv pip list \| grep -i robot` (24) | exactly `robotframework 7.4.2` and `robotframework-requests 0.9.7`; `uv sync` uninstalled 12 packages |
| `--collect-only` on the seed test (25) | 1 test collected |
| `ruff check .` (26a) | `Found 28 errors.` / `[*] 24 fixable` (the lab said "roughly 25–30") |
| `ruff check . --fix` (26b) | `Found 28 errors (24 fixed, 4 remaining).` The 4 are the E501 lines the lab lists. |
| `ruff check .` (26c) | `All checks passed!` |
| `bandit -c pyproject.toml -r app/` (26d) | `using config: pyproject.toml` in the header; 2 × B110 at `ui.py:50:4` and `ui.py:59:4` |
| mypy and `--collect-only -q \| tail -1` (27) | `Success: no issues found` and `75 tests collected` |
| Headless seed test (29) | 1 passed. Flask log (30): `POST /tasks/new 302` then `GET /tasks 200`. |
| Four tests (34) | 4 passed |
| Unfilled E2E scaffold | fails after the 30 s default timeout: `Locator.click: Timeout 30000ms exceeded`, pointing at `YOUR_SELECTOR_HERE`. This is the behavior the lab describes. |
| E2E test with `.btn-complete` (36) / all 5 (37) | 1 passed / 5 passed |
| Full suite (38) | 79 passed, 85%; `ui.py` stays at 37% (explained in the lab) |

## Screenshot map: what YOU capture (20 total, in `images/s4/`)

Terminal commands run from the project root. Flask needs to be running in another terminal for 23, 29–34, 36–38: `uv run python -m app`.

| # | File | Command / action |
|---|---|---|
| 23 | `23_s4_3_start.png` | Phase 1, server running: `uv run python -m pytest -v` → 74 passed, 0 skipped |
| 24 | `24_browser_lib_removed.png` | After the removal + `uv sync`: `uv pip list \| grep -i robot` |
| 25 | `25_seed_test_collected.png` | `uv run python -m pytest tests/ui/test_ui.py --collect-only` |
| 26a/b/c | `26a_ruff_findings.png`, `26b_ruff_autofix.png`, `26c_ruff_clean.png` | `uv run ruff check .`, then `… --fix`, then (after the 4 hand fixes) `uv run ruff check .` |
| 26d | `26d_bandit_findings.png` | `uv run bandit -c pyproject.toml -r app/` (the `using config: pyproject.toml` line must be visible) |
| 27 | `27_mypy_pytest_collect.png` | `uv run mypy app/` then `uv run python -m pytest --collect-only -q \| tail -1` |
| 28 | `28_phase2_pr_two_checks.png` | GitHub: your Phase 2 PR with **both** checks green |
| 29 / 30 | `29_headless_pytest_output.png`, `30_headless_flask_terminal.png` | `uv run python -m pytest tests/ui/test_ui.py -v`; Flask terminal alongside |
| 31 | `31_headed_browser_open.png` | `PWDEBUG=1 uv run python -m pytest tests/ui/test_ui.py -v`, press Step over (F10) once, capture the Chromium window |
| 32 | `32_headed_flask_terminal.png` | Flask terminal after the headed run |
| 33 | `33_slowmo_browser.png` | `uv run python -m pytest tests/ui/test_ui.py -v --headed --slowmo 3000` |
| 34 | `34_four_tests_passing.png` | After Phase 4: `uv run python -m pytest tests/ui/test_ui.py -v` |
| 35 | `35_devtools_element_picker.png` | Phase 5 Part 1, in your browser: DevTools (Cmd+Option+I) → picker → click Complete; capture the highlighted `class="btn-small btn-complete"` |
| 36 / 37 | `36_e2e_test_passing.png`, `37_all_ui_tests_passing.png` | `…::test_end_to_end_workflow -v` then the whole `tests/ui/test_ui.py -v` |
| 38 | `38_full_coverage.png` | `uv run python -m pytest -v` (server running) → 79 passed, 0 skipped |
| 39 | `39_coverage_html.png` | open `htmlcov/index.html` |

## Discrepancies and things to know

1. **macOS AirPlay on port 5000 (important for you).** AirPlay Receiver answers `403` on port 5000, so Flask can't serve there and your Playwright tests (which hit `127.0.0.1:5000`) and the 3 API tests fail. Turn it off first: System Settings → General → AirDrop & Handoff → AirPlay Receiver. I ran everything on port 5050 with the test URLs temporarily swapped and then restored (`grep 5050 tests` finds nothing). Final files use 5000, as the lab says.
2. **Student exercise.** The lab has you find the Complete-button selector with DevTools. I filled it with `.btn-complete` (the answer the lab gives) so the repo is complete. Screenshot 35 still needs your own DevTools capture.
3. **Headed runs.** I ran the headed seed test once, so a Chromium window briefly opened on your screen. I did not use the Inspector or slow motion, so Screenshots 31 and 33 are yours. `PWDEBUG=1 uv run …` works as written in zsh on a Mac.
4. **Bandit.** The `[tool.bandit]` block is only read with `-c pyproject.toml`. I verified the header line shows it.
5. **Ruff auto-fixed 24 findings across many files (about 25).** All were import reordering and blank lines, as the lab says, plus the 4 hand fixes. I also removed the leftover `# ← add this line` comments in `app/__init__.py`.
6. **`ui.py` coverage stays at 37%** even with the UI tests passing. The browser tests hit the Flask server process, which pytest-cov doesn't measure.
7. **CI is not tested here.** The two workflows are valid YAML and use `ubuntu-24.04` and uv `0.13.0`, as the revised lab specifies. Your PR's checks are the real test. They need the `CI: pin uv version` issue number for `Closes #N` in the Phase 2 PR (your S3_2 `#N` placeholders in the docs still need it too).
8. **The 30 s timeout** on the unfilled scaffold means a student who runs it before filling in the selector waits half a minute for the failure.

## Your GitHub Desktop / GitHub.com part

- Branches, commits (messages are in `git log`), publish, and PRs titled `[s4_3] feat: RF014 Playwright UI testing setup` and `[s4_3] test: RF014 Playwright UI tests`. Wait for **both** checks (Python application and Playwright UI Tests). **Do not delete branches.**
- PR 1 description: `Related to #N` (RF014) and `Closes #N` (CI: pin uv version). PR 2: `Closes #N` (RF014). Don't reference the Epic.
- Export `kahsai-S4_3-screenshots.md` to PDF as `kahsai-S4_3-screenshots.pdf` and submit it on Blackboard under **S4_3 Lab**. The S4_3 Agile Documentation assignment and Reflection are separate.
