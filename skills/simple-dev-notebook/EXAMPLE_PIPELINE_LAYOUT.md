# Example — Small Pipeline of Notebooks (dummy, for structure reference only)

This is a fictional, generic example showing the shape a multi-stage dev-notebook pipeline
should take (structure B from the skill). It is not tied to any real project — copy the
*pattern*, not the names.

## Folder layout

```
project/
├── notebooks/
│   ├── 1_Data_Download.ipynb        # pulls raw data, writes data/raw_pull/
│   ├── 2_Clean.ipynb                # reads data/raw_pull/, writes data/processed/
│   ├── 3_Feature_Engineer.ipynb     # reads data/processed/, writes data/features/
│   └── 4_Model_Train.ipynb          # reads data/features/, writes data/model_output/
├── utils/
│   └── connections.py               # tiny, single-level helpers only (e.g. a DB connection getter)
└── data/
    ├── raw_pull/
    ├── processed/
    ├── features/
    └── model_output/
```

## Pattern to copy

- Notebooks are numbered in run order (`1_...`, `2_...`, `3_...`, `4_...`) — the number is the
  contract for what order they must be run in.
- Each notebook reads the previous stage's saved output from `data/` and writes its own output
  back to `data/` — no in-memory handoff between notebooks, no shared kernel.
- Each notebook stays internally flat (see the skill's "Code style" section) — the multi-notebook
  split is about pipeline staging, not about introducing function/class layering within a stage.
- `utils/` holds only trivial, single-level shared helpers (e.g. a connection getter) — never
  business logic, and never a helper that calls another helper.
- **Stage 1 writes to `data/raw_pull/`, not `data/raw/`.** If `project-start` scaffolded this
  project, `data/raw/` is source data that no phase ever writes to — it's for data that's already
  provided, not for what a pipeline stage pulls itself. Give freshly-pulled data its own folder
  name instead of reusing `data/raw/`.
