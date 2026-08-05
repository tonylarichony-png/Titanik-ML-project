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

Повторный запуск того же `RUN_NAME` заменяет только известные сгенерированные
файлы; ручные файлы не удаляются. Для нового смысла эксперимента используйте
новый `RUN_NAME`.

## Контролируемые эксперименты

[[notebooks/04_experiment.ipynb]] сохраняет каждый запуск в
`artifacts/experiments/<RUN_NAME>/`. Конфигурация identity, гипотезы, решения и
write-флагов находится в `src/ml_project/experiment_config.py`. Полные CSV
встраиваются ссылками в карточку эксперимента, а компактные таблицы записываются
непосредственно в Markdown.

Графики метрик baseline и экспериментов хранятся отдельно в отслеживаемом Git
каталоге `assets/experiments/<EXP-ID>/`, чтобы ссылки в карточках работали после
клонирования проекта.
