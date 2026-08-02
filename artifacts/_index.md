---
type: artifact-index
tags:
  - ml/artifacts
---

# Локальные ML-артефакты

Эта папка предназначена для воспроизводимых результатов запусков, которые не
следует автоматически коммитить в Git: моделей, полных CV-таблиц и metadata.

## Baseline

[[notebooks/03_baseline.ipynb]] сохраняет результаты только при явном включении
`SAVE_ARTIFACTS` или `SAVE_FINAL_MODEL` в
`src/ml_project/baseline_config.py`.

Структура одного запуска:

```text
artifacts/baseline/<RUN_NAME>/
├── cv_fold_scores.csv
├── cv_summary.csv
├── metadata.json
└── model.joblib          # только при SAVE_FINAL_MODEL = True
```

`RUN_NAME` нельзя молча перезаписать: по умолчанию существующий запуск защищён.
Зафиксируйте путь к нужному артефакту в карточке эксперимента.

