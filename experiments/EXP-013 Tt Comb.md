---
id: EXP-013
type: experiment
experiment_type: hypothesis-test
status: completed
created: 2026-08-10
hypothesis: " if я объединю датасеты , then улучшу метрики, потому что групповые признаки буду давать более точное представление!, because станет больше наблюдений для формирования групп признаков..."
primary_metric: accuracy
decision: adopt
eda_findings: []
---

# EXP-013 — Train_test_combine

← [[experiments/_index.md|Реестр]] · [[docs/05_experiments.md|Эксперименты]]

> [!info] Автоматическая часть
> Повторный запуск заменяет только отчёт между маркерами. Ручной анализ ниже сохраняется.

<!-- auto:experiment-report:start -->

## Контракт эксперимента

| Поле                | Значение                                                                                                                                                                                   |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Эксперимент         | EXP-013 — Train_test_combine                                                                                                                                                               |
| Гипотеза            |  if я объединю датасеты , then улучшу метрики, потому что групповые признаки буду давать более точное представление!, because станет больше наблюдений для формирования групп признаков... |
| Одно изменение      | ALL IN — применяем все изменения сразу+ объединяем train и test датасеты, относительно EXP012 больше ничего не менять                                                                      |
| Критерий успеха     | Primary improvement >= +0.0050; add explicit metric guardrails below.                                                                                                                      |
| Формальные критерии | failed                                                                                                                                                                                     |
| Решение | adopt |
| Run                 | exp_013_v1                                                                                                                                                                                 |
| Версия данных       | 7d118fef8b6c…                                                                                                                                                                              |
| Validation          | stratified_kfold(n_splits=5, shuffle=True, seed=42)                                                                                                                                        |
| Reference           | champion_reference                                                                                                                                                                         |
| Основной кандидат   | candidate                                                                                                                                                                                  |
| Основная метрика    | accuracy                                                                                                                                                                                   |
| Цепочка             | EXP-001 → [[experiments/EXP-002 AGE_Experiment.md\|EXP-002]] → [[experiments/EXP-003 Family Size.md\|EXP-003]] → EXP-013                                                                   |
| Код эксперимента    | [[src/ml_project/experiments/exp_013_tt_comb.py\|ml_project.experiments.exp_013_tt_comb]]                                                                                                  |
| Hash кода           | 20c232649168…                                                                                                                                                                              |

> [!note] Как читать Δ
> Положительное значение означает улучшение — и для maximize, и для minimize-метрик.

## Проверка pre-registered criteria

| Роль      | Метрика           | Наблюдаемый Δ | Минимальный Δ | Пройден |
| --------- | ----------------- | ------------: | ------------: | ------: |
| primary   | accuracy          |       -0.0079 |        0.0050 |   False |
| guardrail | Balanced accuracy |       -0.0173 |        0.0000 |   False |
| guardrail | Recall            |       -0.0582 |       -0.0100 |   False |
| guardrail | F1                |       -0.0236 |        0.0000 |   False |

## Сравнение всех метрик

| Модель             | Метрика           | Направление | mean ± std      | Reference | Δ к reference |
| ------------------ | ----------------- | ----------- | --------------- | --------: | ------------: |
| champion_reference | accuracy          | maximize    | 0.8204 ± 0.0176 |    0.8204 |        0.0000 |
| champion_reference | Balanced accuracy | maximize    | 0.8018 ± 0.0247 |    0.8018 |        0.0000 |
| champion_reference | Precision         | maximize    | 0.7916 ± 0.0125 |    0.7916 |        0.0000 |
| champion_reference | Recall            | maximize    | 0.7220 ± 0.0558 |    0.7220 |        0.0000 |
| champion_reference | F1                | maximize    | 0.7544 ± 0.0327 |    0.7544 |        0.0000 |
| champion_reference | ROC-AUC           | maximize    | 0.8612 ± 0.0230 |    0.8612 |        0.0000 |
| candidate          | accuracy          | maximize    | 0.8126 ± 0.0152 |    0.8204 |       -0.0079 |
| candidate          | Balanced accuracy | maximize    | 0.7846 ± 0.0184 |    0.8018 |       -0.0173 |
| candidate          | Precision         | maximize    | 0.8141 ± 0.0281 |    0.7916 |        0.0225 |
| candidate          | Recall            | maximize    | 0.6638 ± 0.0365 |    0.7220 |       -0.0582 |
| candidate          | F1                | maximize    | 0.7308 ± 0.0257 |    0.7544 |       -0.0236 |
| candidate          | ROC-AUC           | maximize    | 0.8703 ± 0.0194 |    0.8612 |        0.0091 |

## Метрика: accuracy

![[assets/experiments/EXP-013/metric-primary-accuracy.png]]

### Сводка

| Модель             |   Mean |    Std |    Min |    Max | Reference | Δ к reference |
| ------------------ | -----: | -----: | -----: | -----: | --------: | ------------: |
| champion_reference | 0.8204 | 0.0176 | 0.8034 | 0.8483 |    0.8204 |        0.0000 |
| candidate          | 0.8126 | 0.0152 | 0.7865 | 0.8258 |    0.8204 |       -0.0079 |

### Значения по folds

| Fold | candidate | champion_reference |
| ---: | --------: | -----------------: |
|    1 |    0.8156 |             0.8101 |
|    2 |    0.8146 |             0.8258 |
|    3 |    0.7865 |             0.8034 |
|    4 |    0.8258 |             0.8146 |
|    5 |    0.8202 |             0.8483 |

## Метрика: Balanced accuracy

![[assets/experiments/EXP-013/metric-secondary_1-balanced-accuracy.png]]

### Сводка

| Модель             |   Mean |    Std |    Min |    Max | Reference | Δ к reference |
| ------------------ | -----: | -----: | -----: | -----: | --------: | ------------: |
| champion_reference | 0.8018 | 0.0247 | 0.7735 | 0.8389 |    0.8018 |        0.0000 |
| candidate          | 0.7846 | 0.0184 | 0.7543 | 0.8029 |    0.8018 |       -0.0173 |

### Значения по folds

| Fold | candidate | champion_reference |
| ---: | --------: | -----------------: |
|    1 |    0.7825 |             0.7914 |
|    2 |    0.7910 |             0.8114 |
|    3 |    0.7543 |             0.7735 |
|    4 |    0.8029 |             0.7939 |
|    5 |    0.7920 |             0.8389 |

## Метрика: Precision

![[assets/experiments/EXP-013/metric-secondary_2-precision.png]]

### Сводка

| Модель             |   Mean |    Std |    Min |    Max | Reference | Δ к reference |
| ------------------ | -----: | -----: | -----: | -----: | --------: | ------------: |
| champion_reference | 0.7916 | 0.0125 | 0.7778 | 0.8088 |    0.7916 |        0.0000 |
| candidate          | 0.8141 | 0.0281 | 0.7778 | 0.8462 |    0.7916 |        0.0225 |

### Значения по folds

| Fold | candidate | champion_reference |
| ---: | --------: | -----------------: |
|    1 |    0.8462 |             0.7778 |
|    2 |    0.7966 |             0.7846 |
|    3 |    0.7778 |             0.8000 |
|    4 |    0.8136 |             0.7869 |
|    5 |    0.8364 |             0.8088 |

## Метрика: Recall

![[assets/experiments/EXP-013/metric-secondary_3-recall.png]]

### Сводка

| Модель             |   Mean |    Std |    Min |    Max | Reference | Δ к reference |
| ------------------ | -----: | -----: | -----: | -----: | --------: | ------------: |
| champion_reference | 0.7220 | 0.0558 | 0.6471 | 0.7971 |    0.7220 |        0.0000 |
| candidate          | 0.6638 | 0.0365 | 0.6176 | 0.7059 |    0.7220 |       -0.0582 |

### Значения по folds

| Fold | candidate | champion_reference |
| ---: | --------: | -----------------: |
|    1 |    0.6377 |             0.7101 |
|    2 |    0.6912 |             0.7500 |
|    3 |    0.6176 |             0.6471 |
|    4 |    0.7059 |             0.7059 |
|    5 |    0.6667 |             0.7971 |

## Метрика: F1

![[assets/experiments/EXP-013/metric-secondary_4-f1.png]]

### Сводка

| Модель             |   Mean |    Std |    Min |    Max | Reference | Δ к reference |
| ------------------ | -----: | -----: | -----: | -----: | --------: | ------------: |
| champion_reference | 0.7544 | 0.0327 | 0.7154 | 0.8029 |    0.7544 |        0.0000 |
| candidate          | 0.7308 | 0.0257 | 0.6885 | 0.7559 |    0.7544 |       -0.0236 |

### Значения по folds

| Fold | candidate | champion_reference |
| ---: | --------: | -----------------: |
|    1 |    0.7273 |             0.7424 |
|    2 |    0.7402 |             0.7669 |
|    3 |    0.6885 |             0.7154 |
|    4 |    0.7559 |             0.7442 |
|    5 |    0.7419 |             0.8029 |

## Метрика: ROC-AUC

![[assets/experiments/EXP-013/metric-secondary_5-roc-auc.png]]

### Сводка

| Модель             |   Mean |    Std |    Min |    Max | Reference | Δ к reference |
| ------------------ | -----: | -----: | -----: | -----: | --------: | ------------: |
| champion_reference | 0.8612 | 0.0230 | 0.8362 | 0.8864 |    0.8612 |        0.0000 |
| candidate          | 0.8703 | 0.0194 | 0.8522 | 0.8997 |    0.8612 |        0.0091 |

### Значения по folds

| Fold | candidate | champion_reference |
| ---: | --------: | -----------------: |
|    1 |    0.8997 |             0.8864 |
|    2 |    0.8786 |             0.8646 |
|    3 |    0.8522 |             0.8362 |
|    4 |    0.8551 |             0.8390 |
|    5 |    0.8660 |             0.8801 |

## Диагностика candidate

> [!info] Граница интерпретации
> Диагностика использует fitted-модели тех же CV-folds. Importance описывает предсказания модели, а не причинный эффект признака.

### Контролируемое изменение

| Изменение                       | Признак         |
| ------------------------------- | --------------- |
| добавлен в candidate            | TicketGroupSize |
| добавлен в candidate            | FarePerPerson   |
| добавлен в candidate            | IsnotAlone      |
| добавлен в candidate            | CabinKnown      |
| добавлен в candidate            | Deck            |
| добавлен в candidate            | SexPclass       |
| исключён относительно reference | Pclass          |
| исключён относительно reference | Sex             |

### Путь данных по candidate pipeline

| Этап        | Transformer             | Строк | Колонок | Sparse | Плотность | Пропусков |
| ----------- | ----------------------- | ----: | ------: | -----: | --------: | --------: |
| input       | DataFrame               |   179 |      18 |  False |    0.8271 |       162 |
| title       | TitleExtractor          |   179 |      19 |  False |    0.8362 |       162 |
| age_imputer | AgeByTitlePclassImputer |   179 |      19 |  False |    0.8362 |       136 |
| preprocess  | ColumnTransformer       |   179 |      30 |  False |    0.3333 |         0 |

### Paired Δ на одинаковых folds

| Метрика           | Направление | Средний paired Δ | Std paired Δ | Min paired Δ | Max paired Δ |
| ----------------- | ----------- | ---------------: | -----------: | -----------: | -----------: |
| accuracy          | maximize    |          -0.0079 |       0.0162 |      -0.0281 |       0.0112 |
| Balanced accuracy | maximize    |          -0.0173 |       0.0203 |      -0.0469 |       0.0091 |
| Precision         | maximize    |           0.0225 |       0.0326 |      -0.0222 |       0.0684 |
| Recall            | maximize    |          -0.0582 |       0.0491 |      -0.1304 |       0.0000 |
| F1                | maximize    |          -0.0236 |       0.0262 |      -0.0610 |       0.0117 |
| ROC-AUC           | maximize    |           0.0091 |       0.0130 |      -0.0140 |       0.0161 |

### Изменение OOF-ошибок

| Переход      | Строк |   Доля |
| ------------ | ----: | -----: |
| both_correct |   698 | 0.7834 |
| broken       |    33 | 0.0370 |
| both_wrong   |   134 | 0.1504 |
| fixed        |    26 | 0.0292 |

### Validation permutation importance candidate

| Признак         | Mean importance |    Std |
| --------------- | --------------: | -----: |
| SexPclass       |          0.1994 | 0.0272 |
| FamilySizeGroup |          0.0241 | 0.0219 |
| Age             |          0.0222 | 0.0074 |
| Name            |          0.0044 | 0.0095 |
| Pclass          |          0.0020 | 0.0056 |
| TicketGroupSize |          0.0001 | 0.0047 |
| Cabin           |          0.0000 | 0.0000 |
| Parch           |          0.0000 | 0.0000 |
| PassengerId     |          0.0000 | 0.0000 |
| Sex             |          0.0000 | 0.0000 |
| SibSp           |          0.0000 | 0.0000 |
| Ticket          |          0.0000 | 0.0000 |
| Deck            |         -0.0007 | 0.0086 |
| IsnotAlone      |         -0.0018 | 0.0024 |
| Fare            |         -0.0034 | 0.0045 |

![[assets/experiments/EXP-013/diagnostics/diagnostic-prediction-changes.png]]

![[assets/experiments/EXP-013/diagnostics/diagnostic-permutation-importance.png]]

![[assets/experiments/EXP-013/diagnostics/diagnostic-thresholds.png]]

### Диагностические таблицы

- [[artifacts/experiments/exp_013_v1/diagnostics/pipeline_stages.csv|pipeline_stages.csv]]
- [[artifacts/experiments/exp_013_v1/diagnostics/transformed_features.csv|transformed_features.csv]]
- [[artifacts/experiments/exp_013_v1/diagnostics/transformed_preview.csv|transformed_preview.csv]]
- [[artifacts/experiments/exp_013_v1/diagnostics/paired_fold_deltas.csv|paired_fold_deltas.csv]]
- [[artifacts/experiments/exp_013_v1/diagnostics/oof_predictions.csv|oof_predictions.csv]]
- [[artifacts/experiments/exp_013_v1/diagnostics/prediction_changes.csv|prediction_changes.csv]]
- [[artifacts/experiments/exp_013_v1/diagnostics/confusion.csv|confusion.csv]]
- [[artifacts/experiments/exp_013_v1/diagnostics/permutation_importance.csv|permutation_importance.csv]]
- [[artifacts/experiments/exp_013_v1/diagnostics/native_importance.csv|native_importance.csv]]
- [[artifacts/experiments/exp_013_v1/diagnostics/threshold_metrics.csv|threshold_metrics.csv]]
- [[artifacts/experiments/exp_013_v1/diagnostics/slice_metrics.csv|slice_metrics.csv]]

Подробный интерактивный разбор: [[notebooks/05_diagnostics.ipynb|05_diagnostics.ipynb]].

## Артефакты

- [[artifacts/experiments/exp_013_v1/cv_fold_scores.csv|cv_fold_scores.csv]]
- [[artifacts/experiments/exp_013_v1/cv_summary.csv|cv_summary.csv]]
- [[artifacts/experiments/exp_013_v1/metadata.json|metadata.json]]

<!-- auto:experiment-report:end -->

## EDA-основания

<!-- auto:experiment-eda-links:start -->

> EDA-основания пока не указаны. Добавьте ID в frontmatter: `eda_findings: ["EDA-003"]`, затем запустите `sync-experiment-links.cmd`.

<!-- auto:experiment-eda-links:end -->

## Анализ результата — заполнить вручную

- **Что произошло:**
- **Подтвердилась ли гипотеза:**
- **Почему мог получиться такой результат:**
- **Стабильность по folds / seeds:**
- **Ограничения и возможный leakage:**

## Обоснование решения — заполнить вручную

> Source of truth для `decision` — поле во frontmatter этой карточки. После изменения запустите `sync-experiment-state.cmd`; переобучение не требуется.

- **Почему выбрано это решение:**
- **Следующий шаг:**
