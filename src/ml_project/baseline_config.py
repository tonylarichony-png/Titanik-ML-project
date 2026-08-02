"""Editable configuration for ``notebooks/03_baseline.ipynb``.

This file contains only project choices and run switches. Reusable logic lives
in ``ml_project.baseline``; dataset paths, target and feature groups remain in
``ml_project.config``.

Workflow after editing:
1. Save this file.
2. Re-run the notebook cell named "Reload configuration".
3. Continue from that cell; a kernel restart is not required.

Minimum first run: fill ``TASK_TYPE``. The metric, target and feature groups are
not duplicated here; the notebook reads them from their existing sources of
truth. File creation remains disabled until ``SAVE_ARTIFACTS`` or
``SAVE_FINAL_MODEL`` is enabled.
"""

from pathlib import Path


# ---------------------------------------------------------------------------
# 1. Task — REQUIRED
# ---------------------------------------------------------------------------

# Set exactly one value:
# - "binary_classification"
# - "multiclass_classification"
# - "regression"
TASK_TYPE = "binary_classification"


# ---------------------------------------------------------------------------
# 2. Features used by the first baseline
# ---------------------------------------------------------------------------

# These names refer to FEATURE_GROUPS in src/ml_project/config.py.
# The default first baseline handles ordinary tabular numeric and categorical
# data. Text, datetime, image and sequence pipelines should be added later as
# explicit transformers rather than silently coerced here.
MODEL_FEATURE_GROUPS = (
    "numeric",
    "count",
    "categorical",
    "ordinal",
)

# Empty INCLUDE_FEATURES means "use every feature from MODEL_FEATURE_GROUPS".
# Fill it only when the baseline must use a strict whitelist.
INCLUDE_FEATURES = ()

# Project-specific exclusions for this baseline. Raw columns are never deleted;
# they are merely omitted from the model matrix and can be revisited later.
EXCLUDE_FEATURES = ("Cabin",)

# If an inference dataset exists, fail early when it lacks a model feature.
REQUIRE_INFERENCE_FEATURES = True


# ---------------------------------------------------------------------------
# 3. Metric implementation
# ---------------------------------------------------------------------------

# The metric contract is NOT duplicated here. By default it is read from the
# Dataview field (primary_metric:: ...) in docs/00_problem.md.
#
# Set PRIMARY_SCORER only when the human-readable contract is not a valid
# scikit-learn scorer name. Example:
# PRIMARY_SCORER = "recall_weighted"  # contract says "Weighted recall"
PRIMARY_SCORER = None

# Optional diagnostics. Keys are labels shown in reports; values are valid
# scikit-learn scorer names. These do not replace the primary metric.
SECONDARY_SCORERS = {
    "Balanced accuracy": "balanced_accuracy",
    "Precision": "precision",
    "Recall": "recall",
    "F1": "f1",
    "ROC-AUC": "roc_auc",
}


# ---------------------------------------------------------------------------
# 4. Validation
# ---------------------------------------------------------------------------

# "auto" resolves to stratified_kfold for classification and kfold for
# regression. For a real project, prefer fixing an explicit strategy after the
# production scenario is understood.
# Supported: auto, stratified_kfold, kfold, group_kfold, time_series.
CV_STRATEGY = "stratified_kfold"
N_SPLITS = 5
SHUFFLE = True
RANDOM_STATE = 42

# Required only by the corresponding strategy. These columns may be excluded
# from model features while still controlling the split.
GROUP_COLUMN = None
TIME_COLUMN = None

# -1 uses all available CPU cores. Use 1 while debugging or when an estimator
# already parallelizes internally.
N_JOBS = -1

# "raise" stops on a broken fold instead of hiding the problem behind NaN.
ERROR_SCORE = "raise"
RETURN_TRAIN_SCORE = False


# ---------------------------------------------------------------------------
# 5. Numeric preprocessing
# ---------------------------------------------------------------------------

# Supported imputers: median, mean, most_frequent, constant.
# Imputation is fitted INSIDE every CV train fold by the sklearn Pipeline.
NUMERIC_IMPUTER = "median"
NUMERIC_FILL_VALUE = 0.0
ADD_NUMERIC_MISSING_INDICATOR = False

# Supported: standard, robust, minmax, none.
# Scaling is useful for the default linear baseline; tree models can use none.
NUMERIC_SCALER = "standard"


# ---------------------------------------------------------------------------
# 6. Categorical preprocessing
# ---------------------------------------------------------------------------

# Supported imputers: most_frequent, constant.
CATEGORICAL_IMPUTER = "most_frequent"
CATEGORICAL_FILL_VALUE = "__MISSING__"

# Unknown inference categories never crash the baseline.
ONEHOT_HANDLE_UNKNOWN = "ignore"

# Optional cardinality controls. None keeps every observed category.
ONEHOT_MIN_FREQUENCY = None
ONEHOT_MAX_CATEGORIES = None

# Sparse output scales better for wide one-hot matrices. Set False for an
# estimator that explicitly requires a dense matrix.
ONEHOT_SPARSE_OUTPUT = True
COLUMN_TRANSFORMER_SPARSE_THRESHOLD = 0.3


# ---------------------------------------------------------------------------
# 7. Reference models
# ---------------------------------------------------------------------------

# The notebook can calculate a no-skill floor and a simple model under exactly
# the same folds and metric.
RUN_DUMMY_BASELINE = True

# "auto" -> prior for classification, mean for regression.
DUMMY_STRATEGY = "auto"
DUMMY_PARAMS = {}

# "auto" -> LogisticRegression for classification, Ridge for regression.
# The baseline module intentionally keeps this registry small. More powerful
# sklearn-compatible estimators can reuse the same preprocessor/evaluator in a
# later experiment notebook.
MODEL_NAME = "auto"
MODEL_PARAMS = {}


# ---------------------------------------------------------------------------
# 8. Experiment report and explicit write actions
# ---------------------------------------------------------------------------

# Experiment identity. The note is created automatically on the first saved
# run and then only its generated block is replaced; manual analysis remains.
EXPERIMENT_ID = "EXP-001"
EXPERIMENT_TITLE = "Baseline"
EXPERIMENT_NOTE = Path("experiments/EXP-001 Baseline.md")

# A run name becomes a directory name; increment it instead of overwriting a
# genuinely different experiment. Re-running the same notebook cell may safely
# refresh the known generated files inside the same RUN_NAME.
RUN_NAME = "baseline_v1"
ARTIFACT_DIR = Path("artifacts/baseline")

# CSV/JSON reports. No files are written while this is False.
SAVE_ARTIFACTS = True

# Save one fold-by-fold PNG for every primary/secondary metric. This flag is
# applied only when SAVE_ARTIFACTS or SAVE_FINAL_MODEL requests a saved run.
SAVE_METRIC_FIGURES = True
METRIC_FIGURE_DPI = 160

# Fit the simple pipeline on all available train rows and save model.joblib.
# Do this only after reviewing CV results. It never changes the CV estimate.
SAVE_FINAL_MODEL = False

# Update only marked auto-blocks in docs/03_validation.md and
# docs/05_experiments.md. Manual text outside the markers is preserved.
SYNC_DOCS = True

# Create/update the auto-report in EXPERIMENT_NOTE after artifacts are saved.
# Fold tables are embedded as Markdown; full tables remain linked as CSV.
SYNC_EXPERIMENT_NOTE = True

# True makes repeated execution idempotent: only known generated baseline files
# are replaced. Unknown/manual files in the run directory are never deleted.
# Change RUN_NAME when the experiment meaning or comparison contract changes.
ALLOW_OVERWRITE = True
