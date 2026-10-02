# StudySync (AI110 Tinker Starter)

Starter code for the AI110 **Tinker 1B / 2B / 3B** in-class activities. All three tinkers
build on this one project, each working in a different module.

| Tinker | Focus | Files you'll work in |
|---|---|---|
| 1B, Split the Logic | Writing your first `pytest` test, then a cross-file refactor | `scoring.py`, `scoring_helpers.py`, `test_scoring.py` |
| 2B, Wire It Up | Streamlit `session_state`, input validation, dataclasses, recurring dates | `sessions.py`, `app.py` |
| 3B, Rank & Explain | CSV loading, weighted scoring that returns reasons, ranking, a data-flow diagram | `ranking.py`, `data/study_spots.csv`, `diagram.mmd` |

## Setup

Fork this repo, then clone **your fork**:

```bash
git clone https://github.com/<YOUR-GITHUB-USERNAME>/ai110-tinker-studysync-starter.git
cd ai110-tinker-studysync-starter
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
```

macOS, Linux, Git Bash or WSL:

```bash
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies and run:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m streamlit run app.py
```

Run the tests:

```bash
pytest
```

## Tinker 2B completion

Week 4 `Wire It Up` is implemented in `sessions.py` and connected to the Session Log tab in `app.py`.

- **Part 1:** The fixed counter uses `st.session_state` and increments across Streamlit reruns. The broken counter remains to show why a plain local variable resets.
- **Part 2:** Empty or whitespace-only subjects and durations at or below zero show errors and are not stored. Valid subjects and positive durations are stored.
- **Part 3:** `SessionDC` uses `@dataclass` with the same `subject`, `minutes`, and `priority` fields as `PlainSession`; the standalone demo prints both.
- **Part 4:** `next_occurrence()` handles daily and weekly schedules. `find_conflicts()` returns each pair with the same slot once and safely returns an empty list when there are no conflicts.

### Verification

- `python -B sessions.py` prints the two expected dates, the matching conflict pair, and `[]` for an empty input.
- `python -B -m pytest -p no:cacheprovider -q`: **2 passed**, using the existing scoring tests unchanged. The extra temporary session test file was removed; no new tests are included in this update.
- Streamlit checks confirmed that the fixed counter persists across clicks, invalid session inputs are rejected, valid input is stored, and the full app renders all three tabs.

## Files

- `app.py` — Streamlit entry point, wires the three tabs together
- `scoring.py` — `session_rating()` and the Session Scorer tab
- `scoring_helpers.py` — helpers extracted during Tinker 1B
- `sessions.py` — session log, the Tinker 2B surface
- `ranking.py` — study-spot ranking, the Tinker 3B surface
- `data/study_spots.csv` — sample data for ranking
- `diagram.mmd` — Mermaid data-flow diagram, completed in Tinker 3B
- `test_scoring.py` — starting point for your own tests

Your instructor will tell you which tinker you're on. Follow the activity on the course portal.

## Tinker 1B completion

The Week 2 code was completed on September 17, 2026 and verified again on
September 21 before publication. This section records Split the Logic. Tinker 2B is now completed above;
Tinker 3B remains for its later activity.

### Changes and verification

- Added `test_session_rating_boundary_59_is_skip` before the function move.
- Moved `apply_streak_bonus()` to `scoring_helpers.py` and imported it into
  `scoring.py`; the bonus remains two points per streak day, capped at 100.
- `python -B -m pytest -p no:cacheprovider -q`: **2 passed**, covering
  `session_rating(59) == "Skip"` and `session_rating(90) == "Great"`.
- `python -B scoring.py`: all five demo results match the starter output.

For this activity, the assumed input is an integer score from the normal
nonnegative, capped scoring path; the direct calls below were flagged
outside that contract, so no new validation behavior was added.

| Breaker input | Observed result | Decision |
| --- | --- | --- |
| `-10` | `Skip` | Flag out of scope: the normal scoring controls do not produce negative scores. |
| `125` | `Great` | Flag out of scope: the normal bonus helper caps the score at 100. |
| `87.5` | `Good` | Flag out of scope for the annotated integer contract; Python accepts the decimal at runtime. |

### Part 4 reflection

- **What was broken?** The working `apply_streak_bonus()` function was in
  `scoring.py` instead of the shared helper module, and the starter tested
  only the 90-point rating boundary.
- **AI suggestion accepted:** Add the 59-point assertion and move the bonus
  function with its import, then verify the tests and unchanged demo output.
- **AI suggestion corrected:** The draft reflection's claim that a broad AI
  rewrite had been rejected was removed because the recorded work does not
  support it; the documented scope decision was to leave input validation
  unchanged.
- **Breaker input that mattered:** `87.5` returns `Good` despite the `int`
  annotation, showing that the annotation does not enforce integer inputs
  at runtime.

These are preparation answers; the out-loud group discussion remains an
in-class step. Two passing boundary tests do not establish coverage of all
rating thresholds or invalid input types.
