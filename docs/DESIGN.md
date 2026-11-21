# ResumeIQ design rules

Follow these in every UI task. The score is an estimate of document alignment, never a hiring prediction.

## Palette (only these, plus opacity of them)

| Colour | Use |
|---|---|
| `#F1F7F7` | page background, widget fill, text on buttons |
| `#D5E5E5` | sidebar, inset panels |
| `#BDD7D8` | borders, dividers, matched chips, chart primary |
| `#DDD3D3` | neutral chips (additional skills), chart secondary |
| `#F7CBCA` | gaps and missing items only, plus at most one highlight per page |
| `#5D6B6B` | all text, primary buttons, icons, focus outline |

Text on pink or light-teal fills is always `#5D6B6B`. Never place light text on a light fill. Constants live in `ui/theme.py`.

## Look and feel

- Quiet and editorial. Whitespace, left-aligned, no centred hero sections.
- No emojis, no icon-in-a-circle, no gradients, glows, glass or drop shadows. Separate with 1px `#BDD7D8` borders.
- Radius 6px everywhere. Chips are 999px and small.
- Fonts: DM Sans for UI and body; Newsreader (weight 400) for page titles and the large score number only.
- Type scale: page title 30px Newsreader; section label 12px uppercase, 0.08em tracking, 70% opacity; body 15px; captions 13px at 70% opacity.
- Copy is plain, specific, sentence case. No exclamation marks, no "Welcome back", no marketing phrases.
- Streamlit header, footer and main menu are hidden. Sidebar nav is plain text; the active page is a `#BDD7D8` pill. `app.py` only redirects, so its nav entry is hidden.
- Widgets are restyled in `ui/styles.css`: 1px `#BDD7D8` border, `#F1F7F7` fill, `#5D6B6B` focus outline.

## Page template

```python
from ui.components import page_header, section_label
from ui.theme import setup_page

setup_page("Job match")      # must be first: set_page_config, CSS, sidebar brand
page_header("Job match", "One line of context.")
```

## Components (`ui/components.py`)

`page_header`, `section_label`, `score_display`, `component_bars`, `skill_chips(skills, kind)` with kind `matched | missing | extra`, `empty_state`, `note`.
`score_display` defaults its caption to "Estimated resume-to-job alignment. Not a hiring prediction." and match pages must show it.

## Charts

Template `resumeiq` is registered and set as the Plotly default by importing `ui.theme`. Transparent backgrounds, faint horizontal gridlines only, DM Sans in `#5D6B6B`, no in-figure titles (use `section_label`), no 3D, no rainbow palettes, minimal legends. Primary series `#BDD7D8`, secondary `#DDD3D3`; use `#5D6B6B` sparingly for emphasis.

## Session state keys

| Key | Type | Meaning |
|---|---|---|
| `resume_analysis` | `resume_analysis` dict or absent | analysed resume for the current session |
| `jobs` | list of `job_analysis` | job descriptions added this session |
| `match_results` | dict of `match_result` keyed by job title | results for the current resume against each job |

`resume_file_id` (tuple of file name and size) is an internal marker so the same upload is not re-analysed on each rerun.

The UI calls `src/` only through `ui/adapters.py` (`load_resume(file)`, which raises `ResumeLoadError` with kind `empty | unsupported | corrupted | text_poor`).

Shapes are defined in `docs/ui_contracts.md`. UI code must not read anything else from `src/`.

