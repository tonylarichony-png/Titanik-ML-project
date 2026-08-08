---
id: EXP-011
type: experiment
experiment_type: hypothesis-test
status: completed
created: 2026-08-08
hypothesis: " if сделаю категориальный признак SexPclass, then модели будет удобнее работать, because данный признак будет лучше отражать действительно так как зависимость нелинейная "
primary_metric: accuracy
decision: reject
eda_findings:
  - EDA-003
---

# EXP-011 — SexPlcass_V2

← [[experiments/_index.md|Реестр]] · [[docs/05_experiments.md|Эксперименты]]

> [!info] Автоматическая часть
> Повторный запуск заменяет только отчёт между маркерами. Ручной анализ ниже сохраняется.

<!-- auto:experiment-report:start -->

## Контракт эксперимента

| Поле                | Значение                                                                                                                                                                   |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Эксперимент         | EXP-011 — SexPlcass_V2                                                                                                                                                     |
| Гипотеза            |  if сделаю категориальный признак SexPclass, then модели будет удобнее работать, because данный признак будет лучше отражать действительно так как зависимость нелинейная  |
| Одно изменение      | Объединить признаки Pclass и Sex в один приз                                                                                                                               |
| Критерий успеха     | Primary improvement >= +0.0050; add explicit metric guardrails below.                                                                                                      |
| Формальные критерии | failed                                                                                                                                                                     |
| Решение | reject |
| Run                 | exp_011_v1                                                                                                                                                                 |
| Версия данных       | 7d118fef8b6c…                                                                                                                                                              |
| Validation          | stratified_kfold(n_splits=5, shuffle=True, seed=42)                                                                                                                        |
| Reference           | champion_reference                                                                                                                                                         |
| Основной кандидат   | candidate                                                                                                                                                                  |
| Основная метрика    | accuracy                                                                                                                                                                   |
| Цепочка             | EXP-001 → [[experiments/EXP-002 AGE_Experiment.md\|EXP-002]] → [[experiments/EXP-003 Family Size.md\|EXP-003]] → EXP-011                                                   |
| Код эксперимента    | [[src/ml_project/experiments/exp_011_sexplcass_v2.py\|ml_project.experiments.exp_011_sexplcass_v2]]                                                                        |
| Hash кода           | 82edb29c4784…                                                                                                                                                              |

> [!note] Как читать Δ
> Положительное значение означает улучшение — и для maximize, и для minimize-метрик.

## Проверка pre-registered criteria

| Роль      | Метрика           | Наблюдаемый Δ | Минимальный Δ | Пройден |
| --------- | ----------------- | ------------: | ------------: | ------: |
| primary   | accuracy          |       -0.0056 |        0.0050 |   False |
| guardrail | Balanced accuracy |       -0.0155 |        0.0000 |   False |
| guardrail | Recall            |       -0.0583 |       -0.0100 |   False |
| guardrail | F1                |       -0.0211 |        0.0000 |   False |

## Сравнение всех метрик

| Модель             | Метрика           | Направление | mean ± std      | Reference | Δ к reference |
| ------------------ | ----------------- | ----------- | --------------- | --------: | ------------: |
| champion_reference | accuracy          | maximize    | 0.8204 ± 0.0176 |    0.8204 |        0.0000 |
| champion_reference | Balanced accuracy | maximize    | 0.8018 ± 0.0247 |    0.8018 |        0.0000 |
| champion_reference | Precision         | maximize    | 0.7916 ± 0.0125 |    0.7916 |        0.0000 |
| champion_reference | Recall            | maximize    | 0.7220 ± 0.0558 |    0.7220 |        0.0000 |
| champion_reference | F1                | maximize    | 0.7544 ± 0.0327 |    0.7544 |        0.0000 |
| champion_reference | ROC-AUC           | maximize    | 0.8612 ± 0.0230 |    0.8612 |        0.0000 |
| candidate          | accuracy          | maximize    | 0.8148 ± 0.0162 |    0.8204 |       -0.0056 |
| candidate          | Balanced accuracy | maximize    | 0.7864 ± 0.0185 |    0.8018 |       -0.0155 |
| candidate          | Precision         | maximize    | 0.8193 ± 0.0228 |    0.7916 |        0.0277 |
| candidate          | Recall            | maximize    | 0.6638 ± 0.0288 |    0.7220 |       -0.0583 |
| candidate          | F1                | maximize    | 0.7333 ± 0.0254 |    0.7544 |       -0.0211 |
| candidate          | ROC-AUC           | maximize    | 0.8663 ± 0.0179 |    0.8612 |        0.0051 |

## Метрика: accuracy

![[assets/experiments/EXP-011/metric-primary-accuracy.png]]

### Сводка

| Модель             |   Mean |    Std |    Min |    Max | Reference | Δ к reference |
| ------------------ | -----: | -----: | -----: | -----: | --------: | ------------: |
| champion_reference | 0.8204 | 0.0176 | 0.8034 | 0.8483 |    0.8204 |        0.0000 |
| candidate          | 0.8148 | 0.0162 | 0.7978 | 0.8371 |    0.8204 |       -0.0056 |

### Значения по folds

| Fold | candidate | champion_reference |
| ---: | --------: | -----------------: |
|    1 |    0.8045 |             0.8101 |
|    2 |    0.7978 |             0.8258 |
|    3 |    0.8090 |             0.8034 |
|    4 |    0.8371 |             0.8146 |
|    5 |    0.8258 |             0.8483 |

## Метрика: Balanced accuracy

![[assets/experiments/EXP-011/metric-secondary_1-balanced-accuracy.png]]

### Сводка

| Модель             |   Mean |    Std |    Min |    Max | Reference | Δ к reference |
| ------------------ | -----: | -----: | -----: | -----: | --------: | ------------: |
| champion_reference | 0.8018 | 0.0247 | 0.7735 | 0.8389 |    0.8018 |        0.0000 |
| candidate          | 0.7864 | 0.0185 | 0.7690 | 0.8120 |    0.8018 |       -0.0155 |

### Значения по folds

| Fold | candidate | champion_reference |
| ---: | --------: | -----------------: |
|    1 |    0.7734 |             0.7914 |
|    2 |    0.7690 |             0.8114 |
|    3 |    0.7781 |             0.7735 |
|    4 |    0.8120 |             0.7939 |
|    5 |    0.7993 |             0.8389 |

## Метрика: Precision

![[assets/experiments/EXP-011/metric-secondary_2-precision.png]]

### Сводка

| Модель             |   Mean |    Std |    Min |    Max | Reference | Δ к reference |
| ------------------ | -----: | -----: | -----: | -----: | --------: | ------------: |
| champion_reference | 0.7916 | 0.0125 | 0.7778 | 0.8088 |    0.7916 |        0.0000 |
| candidate          | 0.8193 | 0.0228 | 0.7857 | 0.8421 |    0.7916 |        0.0277 |

### Значения по folds

| Fold | candidate | champion_reference |
| ---: | --------: | -----------------: |
|    1 |    0.8148 |             0.7778 |
|    2 |    0.7857 |             0.7846 |
|    3 |    0.8148 |             0.8000 |
|    4 |    0.8421 |             0.7869 |
|    5 |    0.8393 |             0.8088 |

## Метрика: Recall

![[assets/experiments/EXP-011/metric-secondary_3-recall.png]]

### Сводка

| Модель             |   Mean |    Std |    Min |    Max | Reference | Δ к reference |
| ------------------ | -----: | -----: | -----: | -----: | --------: | ------------: |
| champion_reference | 0.7220 | 0.0558 | 0.6471 | 0.7971 |    0.7220 |        0.0000 |
| candidate          | 0.6638 | 0.0288 | 0.6377 | 0.7059 |    0.7220 |       -0.0583 |

### Значения по folds

| Fold | candidate | champion_reference |
| ---: | --------: | -----------------: |
|    1 |    0.6377 |             0.7101 |
|    2 |    0.6471 |             0.7500 |
|    3 |    0.6471 |             0.6471 |
|    4 |    0.7059 |             0.7059 |
|    5 |    0.6812 |             0.7971 |

## Метрика: F1

![[assets/experiments/EXP-011/metric-secondary_4-f1.png]]

### Сводка

| Модель             |   Mean |    Std |    Min |    Max | Reference | Δ к reference |
| ------------------ | -----: | -----: | -----: | -----: | --------: | ------------: |
| champion_reference | 0.7544 | 0.0327 | 0.7154 | 0.8029 |    0.7544 |        0.0000 |
| candidate          | 0.7333 | 0.0254 | 0.7097 | 0.7680 |    0.7544 |       -0.0211 |

### Значения по folds

| Fold | candidate | champion_reference |
| ---: | --------: | -----------------: |
|    1 |    0.7154 |             0.7424 |
|    2 |    0.7097 |             0.7669 |
|    3 |    0.7213 |             0.7154 |
|    4 |    0.7680 |             0.7442 |
|    5 |    0.7520 |             0.8029 |

## Метрика: ROC-AUC

![[assets/experiments/EXP-011/metric-secondary_5-roc-auc.png]]

### Сводка

| Модель             |   Mean |    Std |    Min |    Max | Reference | Δ к reference |
| ------------------ | -----: | -----: | -----: | -----: | --------: | ------------: |
| champion_reference | 0.8612 | 0.0230 | 0.8362 | 0.8864 |    0.8612 |        0.0000 |
| candidate          | 0.8663 | 0.0179 | 0.8454 | 0.8927 |    0.8612 |        0.0051 |

### Значения по folds

| Fold | candidate | champion_reference |
| ---: | --------: | -----------------: |
|    1 |    0.8927 |             0.8864 |
|    2 |    0.8663 |             0.8646 |
|    3 |    0.8555 |             0.8362 |
|    4 |    0.8454 |             0.8390 |
|    5 |    0.8716 |             0.8801 |

## Диагностика candidate

> [!info] Граница интерпретации
> Диагностика использует fitted-модели тех же CV-folds. Importance описывает предсказания модели, а не причинный эффект признака.

### Контролируемое изменение

| Изменение            | Признак   |
| -------------------- | --------- |
| добавлен в candidate | SexPclass |

### Путь данных по candidate pipeline

| Этап        | Transformer             | Строк | Колонок | Sparse | Плотность | Пропусков |
| ----------- | ----------------------- | ----: | ------: | -----: | --------: | --------: |
| input       | DataFrame               |   179 |      13 |  False |    0.8908 |       162 |
| title       | TitleExtractor          |   179 |      14 |  False |    0.8986 |       162 |
| age_imputer | AgeByTitlePclassImputer |   179 |      14 |  False |    0.8986 |       136 |
| preprocess  | ColumnTransformer       |   179 |      21 |  False |    0.3333 |         0 |

### Paired Δ на одинаковых folds

| Метрика           | Направление | Средний paired Δ | Std paired Δ | Min paired Δ | Max paired Δ |
| ----------------- | ----------- | ---------------: | -----------: | -----------: | -----------: |
| accuracy          | maximize    |          -0.0056 |       0.0206 |      -0.0281 |       0.0225 |
| Balanced accuracy | maximize    |          -0.0155 |       0.0267 |      -0.0424 |       0.0182 |
| Precision         | maximize    |           0.0277 |       0.0208 |       0.0011 |       0.0552 |
| Recall            | maximize    |          -0.0583 |       0.0555 |      -0.1159 |       0.0000 |
| F1                | maximize    |          -0.0211 |       0.0353 |      -0.0572 |       0.0238 |
| ROC-AUC           | maximize    |           0.0051 |       0.0100 |      -0.0085 |       0.0194 |

### Изменение OOF-ошибок

| Переход      | Строк |   Доля |
| ------------ | ----: | -----: |
| both_correct |   710 | 0.7969 |
| both_wrong   |   144 | 0.1616 |
| fixed        |    16 | 0.0180 |
| broken       |    21 | 0.0236 |

### Validation permutation importance candidate

| Признак         | Mean importance |    Std |
| --------------- | --------------: | -----: |
| Sex             |          0.1515 | 0.0329 |
| Age             |          0.0281 | 0.0081 |
| Pclass          |          0.0218 | 0.0112 |
| FamilySizeGroup |          0.0216 | 0.0212 |
| SexPclass       |          0.0105 | 0.0199 |
| Fare            |          0.0022 | 0.0043 |
| Name            |          0.0013 | 0.0070 |
| Embarked        |          0.0008 | 0.0077 |
| Cabin           |          0.0000 | 0.0000 |
| PassengerId     |          0.0000 | 0.0000 |
| Parch           |          0.0000 | 0.0000 |
| SibSp           |          0.0000 | 0.0000 |
| Ticket          |          0.0000 | 0.0000 |

![[assets/experiments/EXP-011/diagnostics/diagnostic-prediction-changes.png]]

![[assets/experiments/EXP-011/diagnostics/diagnostic-permutation-importance.png]]

![[assets/experiments/EXP-011/diagnostics/diagnostic-thresholds.png]]

### Диагностические таблицы

- [[artifacts/experiments/exp_011_v1/diagnostics/pipeline_stages.csv|pipeline_stages.csv]]
- [[artifacts/experiments/exp_011_v1/diagnostics/transformed_features.csv|transformed_features.csv]]
- [[artifacts/experiments/exp_011_v1/diagnostics/transformed_preview.csv|transformed_preview.csv]]
- [[artifacts/experiments/exp_011_v1/diagnostics/paired_fold_deltas.csv|paired_fold_deltas.csv]]
- [[artifacts/experiments/exp_011_v1/diagnostics/oof_predictions.csv|oof_predictions.csv]]
- [[artifacts/experiments/exp_011_v1/diagnostics/prediction_changes.csv|prediction_changes.csv]]
- [[artifacts/experiments/exp_011_v1/diagnostics/confusion.csv|confusion.csv]]
- [[artifacts/experiments/exp_011_v1/diagnostics/permutation_importance.csv|permutation_importance.csv]]
- [[artifacts/experiments/exp_011_v1/diagnostics/native_importance.csv|native_importance.csv]]
- [[artifacts/experiments/exp_011_v1/diagnostics/threshold_metrics.csv|threshold_metrics.csv]]
- [[artifacts/experiments/exp_011_v1/diagnostics/slice_metrics.csv|slice_metrics.csv]]

Подробный интерактивный разбор: [[notebooks/05_diagnostics.ipynb|05_diagnostics.ipynb]].

## Артефакты

- [[artifacts/experiments/exp_011_v1/cv_fold_scores.csv|cv_fold_scores.csv]]
- [[artifacts/experiments/exp_011_v1/cv_summary.csv|cv_summary.csv]]
- [[artifacts/experiments/exp_011_v1/metadata.json|metadata.json]]

<!-- auto:experiment-report:end -->

## EDA-основания

<!-- auto:experiment-eda-links:start -->

| EDA-наблюдение                                                               | Признаки    | Ключевой вывод                                                                                                                                                                |
| ---------------------------------------------------------------------------- | ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [[eda/findings/EDA-003.md\|EDA-003 — Влиние класса билета и пола на таргет]] | Pclass, Sex | 1 и второй класс по женщинам практически не различается 97и92 а вот 3й класс женщины всего 50%, по мужчинам 2й и 3й класс почти не различаются 16,14, а вот первый класс 37%. |

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
