"""One editable contract for ``notebooks/04_experiment.ipynb``.

Create a new experiment by copying this file or changing the identity fields.
Metric, split, baseline preprocessing and reference model are intentionally
inherited from ``baseline_config.py`` so the comparison remains fair.

After editing, save the file and rerun the notebook cell "Reload configs";
a kernel restart is not required.
"""

from pathlib import Path


# ---------------------------------------------------------------------------
# 1. Pre-registration — fill BEFORE looking at the result
# ---------------------------------------------------------------------------

EXPERIMENT_ID = "EXP-002"
EXPERIMENT_TITLE = 'Заполнение пропусков Age с помощью "title" and "Pclass"'
EXPERIMENT_NOTE = Path("experiments/EXP-002 AGE_Experiment.md")

# A falsifiable expectation, not merely "try another model".
HYPOTHESIS = " if я заполню возраст более точно, then accuracy должен повысится, because потому что как минимум станет возможно отделить детей и стариков, у которых есть большая зависимость с survived"

# Exactly one main factor changed relative to the reference.
CHANGE_DESCRIPTION ="новый способ заполнения пустот"

# Define the threshold and guardrail before the run.
SUCCESS_CRITERION = "accuracy"


# ---------------------------------------------------------------------------
# 2. Comparison contract
# ---------------------------------------------------------------------------

# The notebook builds this model automatically from baseline_config.py.
REFERENCE_MODEL = "baseline_reference"

# This key must exist in the candidate_models dictionary in the editable cell.
PRIMARY_CANDIDATE = "candidate"

# Record the parameters that explain the experiment. This complements the
# estimator repr and remains readable in metadata.json.
EXPERIMENT_PARAMETERS = {
   "feature": "Age",
    "reference_strategy": "global_median",
    "candidate_strategy": "median_by_Title_and_Pclass",
    "fallback": ["Title", "global_median"],
}

# Change after interpreting the result, then rerun only the save/sync cell.
# Supported: pending, adopt, reject, iterate, inconclusive.
DECISION = "pending"


# ---------------------------------------------------------------------------
# 3. Run identity and output
# ---------------------------------------------------------------------------

# Re-run the same code with the same meaning under the same RUN_NAME.
# Use a new RUN_NAME when parameters or the tested change are different.
RUN_NAME = "exp_002_v1"
ARTIFACT_DIR = Path("artifacts/experiments")
RESULTS_REGISTRY = Path("experiments/results.csv")

SAVE_ARTIFACTS = True
SAVE_METRIC_FIGURES = True
METRIC_FIGURE_DPI = 160

# Saves PRIMARY_CANDIDATE fitted on all train rows. Keep False until CV is
# reviewed; this option does not change the validation estimate.
SAVE_FINAL_MODEL = False

# The experiment card receives graphs, metric tables and artifact links.
SYNC_EXPERIMENT_NOTE = True

# Updates latest experiment and leaderboard blocks in docs/05_experiments.md.
SYNC_DOCS = True

# Safe idempotent rerun: only known generated files are replaced.
ALLOW_OVERWRITE = True
