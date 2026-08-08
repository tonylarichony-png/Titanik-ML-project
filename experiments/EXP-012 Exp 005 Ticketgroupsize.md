---
id: EXP-012
type: experiment
experiment_type: hypothesis-test
status: completed
created: 2026-08-08
hypothesis: " if создать группы по номеру билета и из за скошенность прологорифмировать, then точнее можно оценить стоимость билета на человека , because это лучше отражает действительноть, ценность билета!"
primary_metric: accuracy
decision: reject
eda_findings:
  - eda-017
---

# EXP-012 — EXP-005+ticketGroupSize

← [[experiments/_index.md|Реестр]] · [[docs/05_experiments.md|Эксперименты]]

> [!info] Автоматическая часть
> Повторный запуск заменяет только отчёт между маркерами. Ручной анализ ниже сохраняется.

<!-- auto:experiment-report:start -->

## Контракт эксперимента

| Поле                | Значение                                                                                                                                                                                          |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Эксперимент         | EXP-012 — EXP-005+ticketGroupSize                                                                                                                                                                 |
| Гипотеза            |  if создать группы по номеру билета и из за скошенность прологорифмировать, then точнее можно оценить стоимость билета на человека , because это лучше отражает действительноть, ценность билета! |
| Одно изменение      | Создать переменную TicketGroup, которая будет группировать билеты по номеру билета,и рассчитать FarePerPerson и преобразовать log1p относительно EXP003 больше ничего не менять                   |
| Критерий успеха     | Primary improvement >= +0.0050; add explicit metric guardrails below.                                                                                                                             |
| Формальные критерии | failed                                                                                                                                                                                            |
| Решение | reject |
| Run                 | exp_012_v1                                                                                                                                                                                        |
| Версия данных       | 7d118fef8b6c…                                                                                                                                                                                     |
| Validation          | stratified_kfold(n_splits=5, shuffle=True, seed=42)                                                                                                                                               |
| Reference           | champion_reference                                                                                                                                                                                |
| Основной кандидат   | candidate                                                                                                                                                                                         |
| Основная метрика    | accuracy                                                                                                                                                                                          |
| Цепочка             | EXP-001 → [[experiments/EXP-002 AGE_Experiment.md\|EXP-002]] → [[experiments/EXP-003 Family Size.md\|EXP-003]] → EXP-012                                                                          |
| Код эксперимента    | [[src/ml_project/experiments/exp_012_exp_005_ticketgroupsize.py\|ml_project.experiments.exp_012_exp_005_ticketgroupsize]]                                                                         |
| Hash кода           | 37312d67950a…                                                                                                                                                                                     |

> [!note] Как читать Δ
> Положительное значение означает улучшение — и для maximize, и для minimize-метрик.

## Проверка pre-registered criteria

| Роль      | Метрика           | Наблюдаемый Δ | Минимальный Δ | Пройден |
| --------- | ----------------- | ------------: | ------------: | ------: |
| primary   | accuracy          |       -0.0067 |        0.0050 |   False |
| guardrail | Balanced accuracy |       -0.0060 |        0.0000 |   False |
| guardrail | Recall            |       -0.0029 |       -0.0100 |    True |
| guardrail | F1                |       -0.0073 |        0.0000 |   False |

## Сравнение всех метрик

| Модель             | Метрика           | Направление | mean ± std      | Reference | Δ к reference |
| ------------------ | ----------------- | ----------- | --------------- | --------: | ------------: |
| champion_reference | accuracy          | maximize    | 0.8204 ± 0.0176 |    0.8204 |        0.0000 |
| champion_reference | Balanced accuracy | maximize    | 0.8018 ± 0.0247 |    0.8018 |        0.0000 |
| champion_reference | Precision         | maximize    | 0.7916 ± 0.0125 |    0.7916 |        0.0000 |
| champion_reference | Recall            | maximize    | 0.7220 ± 0.0558 |    0.7220 |        0.0000 |
| champion_reference | F1                | maximize    | 0.7544 ± 0.0327 |    0.7544 |        0.0000 |
| champion_reference | ROC-AUC           | maximize    | 0.8612 ± 0.0230 |    0.8612 |        0.0000 |
| candidate          | accuracy          | maximize    | 0.8137 ± 0.0113 |    0.8204 |       -0.0067 |
| candidate          | Balanced accuracy | maximize    | 0.7958 ± 0.0179 |    0.8018 |       -0.0060 |
| candidate          | Precision         | maximize    | 0.7788 ± 0.0078 |    0.7916 |       -0.0128 |
| candidate          | Recall            | maximize    | 0.7192 ± 0.0474 |    0.7220 |       -0.0029 |
| candidate          | F1                | maximize    | 0.7470 ± 0.0240 |    0.7544 |       -0.0073 |
| candidate          | ROC-AUC           | maximize    | 0.8603 ± 0.0220 |    0.8612 |       -0.0010 |

## Метрика: accuracy

![[assets/experiments/EXP-012/metric-primary-accuracy.png]]

### Сводка

| Модель             |   Mean |    Std |    Min |    Max | Reference | Δ к reference |
| ------------------ | -----: | -----: | -----: | -----: | --------: | ------------: |
| champion_reference | 0.8204 | 0.0176 | 0.8034 | 0.8483 |    0.8204 |        0.0000 |
| candidate          | 0.8137 | 0.0113 | 0.8034 | 0.8258 |    0.8204 |       -0.0067 |

### Значения по folds

| Fold | candidate | champion_reference |
| ---: | --------: | -----------------: |
|    1 |    0.8045 |             0.8101 |
|    2 |    0.8258 |             0.8258 |
|    3 |    0.8034 |             0.8034 |
|    4 |    0.8090 |             0.8146 |
|    5 |    0.8258 |             0.8483 |

## Метрика: Balanced accuracy

![[assets/experiments/EXP-012/metric-secondary_1-balanced-accuracy.png]]

### Сводка

| Модель             |   Mean |    Std |    Min |    Max | Reference | Δ к reference |
| ------------------ | -----: | -----: | -----: | -----: | --------: | ------------: |
| champion_reference | 0.8018 | 0.0247 | 0.7735 | 0.8389 |    0.8018 |        0.0000 |
| candidate          | 0.7958 | 0.0179 | 0.7763 | 0.8179 |    0.8018 |       -0.0060 |

### Значения по folds

| Fold | candidate | champion_reference |
| ---: | --------: | -----------------: |
|    1 |    0.7842 |             0.7914 |
|    2 |    0.8114 |             0.8114 |
|    3 |    0.7763 |             0.7735 |
|    4 |    0.7893 |             0.7939 |
|    5 |    0.8179 |             0.8389 |

## Метрика: Precision

![[assets/experiments/EXP-012/metric-secondary_2-precision.png]]

### Сводка

| Модель             |   Mean |    Std |    Min |    Max | Reference | Δ к reference |
| ------------------ | -----: | -----: | -----: | -----: | --------: | ------------: |
| champion_reference | 0.7916 | 0.0125 | 0.7778 | 0.8088 |    0.7916 |        0.0000 |
| candidate          | 0.7788 | 0.0078 | 0.7714 | 0.7895 |    0.7916 |       -0.0128 |

### Значения по folds

| Fold | candidate | champion_reference |
| ---: | --------: | -----------------: |
|    1 |    0.7742 |             0.7778 |
|    2 |    0.7846 |             0.7846 |
|    3 |    0.7895 |             0.8000 |
|    4 |    0.7742 |             0.7869 |
|    5 |    0.7714 |             0.8088 |

## Метрика: Recall

![[assets/experiments/EXP-012/metric-secondary_3-recall.png]]

### Сводка

| Модель             |   Mean |    Std |    Min |    Max | Reference | Δ к reference |
| ------------------ | -----: | -----: | -----: | -----: | --------: | ------------: |
| champion_reference | 0.7220 | 0.0558 | 0.6471 | 0.7971 |    0.7220 |        0.0000 |
| candidate          | 0.7192 | 0.0474 | 0.6618 | 0.7826 |    0.7220 |       -0.0029 |

### Значения по folds

| Fold | candidate | champion_reference |
| ---: | --------: | -----------------: |
|    1 |    0.6957 |             0.7101 |
|    2 |    0.7500 |             0.7500 |
|    3 |    0.6618 |             0.6471 |
|    4 |    0.7059 |             0.7059 |
|    5 |    0.7826 |             0.7971 |

## Метрика: F1

![[assets/experiments/EXP-012/metric-secondary_4-f1.png]]

### Сводка

| Модель             |   Mean |    Std |    Min |    Max | Reference | Δ к reference |
| ------------------ | -----: | -----: | -----: | -----: | --------: | ------------: |
| champion_reference | 0.7544 | 0.0327 | 0.7154 | 0.8029 |    0.7544 |        0.0000 |
| candidate          | 0.7470 | 0.0240 | 0.7200 | 0.7770 |    0.7544 |       -0.0073 |

### Значения по folds

| Fold | candidate | champion_reference |
| ---: | --------: | -----------------: |
|    1 |    0.7328 |             0.7424 |
|    2 |    0.7669 |             0.7669 |
|    3 |    0.7200 |             0.7154 |
|    4 |    0.7385 |             0.7442 |
|    5 |    0.7770 |             0.8029 |

## Метрика: ROC-AUC

![[assets/experiments/EXP-012/metric-secondary_5-roc-auc.png]]

### Сводка

| Модель             |   Mean |    Std |    Min |    Max | Reference | Δ к reference |
| ------------------ | -----: | -----: | -----: | -----: | --------: | ------------: |
| champion_reference | 0.8612 | 0.0230 | 0.8362 | 0.8864 |    0.8612 |        0.0000 |
| candidate          | 0.8603 | 0.0220 | 0.8328 | 0.8845 |    0.8612 |       -0.0010 |

### Значения по folds

| Fold | candidate | champion_reference |
| ---: | --------: | -----------------: |
|    1 |    0.8845 |             0.8864 |
|    2 |    0.8640 |             0.8646 |
|    3 |    0.8328 |             0.8362 |
|    4 |    0.8430 |             0.8390 |
|    5 |    0.8769 |             0.8801 |

## Диагностика candidate

> [!info] Граница интерпретации
> Диагностика использует fitted-модели тех же CV-folds. Importance описывает предсказания модели, а не причинный эффект признака.

### Контролируемое изменение

| Изменение            | Признак         |
| -------------------- | --------------- |
| добавлен в candidate | TicketGroupSize |
| добавлен в candidate | FarePerPerson   |

### Путь данных по candidate pipeline

| Этап        | Transformer             | Строк | Колонок | Sparse | Плотность | Пропусков |
| ----------- | ----------------------- | ----: | ------: | -----: | --------: | --------: |
| input       | DataFrame               |   179 |      14 |  False |    0.8978 |       162 |
| title       | TitleExtractor          |   179 |      15 |  False |    0.9047 |       162 |
| age_imputer | AgeByTitlePclassImputer |   179 |      15 |  False |    0.9047 |       136 |
| preprocess  | ColumnTransformer       |   179 |      17 |  False |    0.4706 |         0 |

### Paired Δ на одинаковых folds

| Метрика           | Направление | Средний paired Δ | Std paired Δ | Min paired Δ | Max paired Δ |
| ----------------- | ----------- | ---------------: | -----------: | -----------: | -----------: |
| accuracy          | maximize    |          -0.0067 |       0.0092 |      -0.0225 |       0.0000 |
| Balanced accuracy | maximize    |          -0.0060 |       0.0093 |      -0.0210 |       0.0028 |
| Precision         | maximize    |          -0.0128 |       0.0147 |      -0.0374 |       0.0000 |
| Recall            | maximize    |          -0.0029 |       0.0122 |      -0.0145 |       0.0147 |
| F1                | maximize    |          -0.0073 |       0.0117 |      -0.0259 |       0.0046 |
| ROC-AUC           | maximize    |          -0.0010 |       0.0030 |      -0.0033 |       0.0041 |

### Изменение OOF-ошибок

| Переход      | Строк |   Доля |
| ------------ | ----: | -----: |
| both_correct |   723 | 0.8114 |
| both_wrong   |   158 | 0.1773 |
| fixed        |     2 | 0.0022 |
| broken       |     8 | 0.0090 |

### Validation permutation importance candidate

| Признак         | Mean importance |    Std |
| --------------- | --------------: | -----: |
| Sex             |          0.2079 | 0.0158 |
| FamilySizeGroup |          0.0309 | 0.0104 |
| Age             |          0.0289 | 0.0160 |
| Pclass          |          0.0279 | 0.0156 |
| FarePerPerson   |          0.0035 | 0.0127 |
| Name            |          0.0008 | 0.0013 |
| PassengerId     |          0.0000 | 0.0000 |
| SibSp           |          0.0000 | 0.0000 |
| Cabin           |          0.0000 | 0.0000 |
| Parch           |          0.0000 | 0.0000 |
| Ticket          |          0.0000 | 0.0000 |
| Fare            |         -0.0006 | 0.0033 |
| Embarked        |         -0.0007 | 0.0056 |
| TicketGroupSize |         -0.0008 | 0.0033 |

![[assets/experiments/EXP-012/diagnostics/diagnostic-prediction-changes.png]]

![[assets/experiments/EXP-012/diagnostics/diagnostic-permutation-importance.png]]

![[assets/experiments/EXP-012/diagnostics/diagnostic-thresholds.png]]

### Диагностические таблицы

- [[artifacts/experiments/exp_012_v1/diagnostics/pipeline_stages.csv|pipeline_stages.csv]]
- [[artifacts/experiments/exp_012_v1/diagnostics/transformed_features.csv|transformed_features.csv]]
- [[artifacts/experiments/exp_012_v1/diagnostics/transformed_preview.csv|transformed_preview.csv]]
- [[artifacts/experiments/exp_012_v1/diagnostics/paired_fold_deltas.csv|paired_fold_deltas.csv]]
- [[artifacts/experiments/exp_012_v1/diagnostics/oof_predictions.csv|oof_predictions.csv]]
- [[artifacts/experiments/exp_012_v1/diagnostics/prediction_changes.csv|prediction_changes.csv]]
- [[artifacts/experiments/exp_012_v1/diagnostics/confusion.csv|confusion.csv]]
- [[artifacts/experiments/exp_012_v1/diagnostics/permutation_importance.csv|permutation_importance.csv]]
- [[artifacts/experiments/exp_012_v1/diagnostics/native_importance.csv|native_importance.csv]]
- [[artifacts/experiments/exp_012_v1/diagnostics/threshold_metrics.csv|threshold_metrics.csv]]
- [[artifacts/experiments/exp_012_v1/diagnostics/slice_metrics.csv|slice_metrics.csv]]

Подробный интерактивный разбор: [[notebooks/05_diagnostics.ipynb|05_diagnostics.ipynb]].

## Артефакты

- [[artifacts/experiments/exp_012_v1/cv_fold_scores.csv|cv_fold_scores.csv]]
- [[artifacts/experiments/exp_012_v1/cv_summary.csv|cv_summary.csv]]
- [[artifacts/experiments/exp_012_v1/metadata.json|metadata.json]]

<!-- auto:experiment-report:end -->

## EDA-основания

<!-- auto:experiment-eda-links:start -->

| EDA-наблюдение                                         | Признаки | Ключевой вывод                                                           |
| ------------------------------------------------------ | -------- | ------------------------------------------------------------------------ |
| [[eda/findings/EDA-017.md\|EDA-017 — Повторы билетов]] | Ticket   | Можно дать более точную Fare ведь один билет покупался на группу людей!! |

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
