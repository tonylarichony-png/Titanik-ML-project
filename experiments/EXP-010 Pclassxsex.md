---
id: EXP-010
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

# EXP-010 — Объединение признака pcclass и Sex  в один

← [[experiments/_index.md|Реестр]] · [[docs/05_experiments.md|Эксперименты]]

> [!info] Автоматическая часть
> Повторный запуск заменяет только отчёт между маркерами. Ручной анализ ниже сохраняется.

<!-- auto:experiment-report:start -->

## Контракт эксперимента

| Поле                | Значение                                                                                                                                                                   |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Эксперимент         | EXP-010 — Объединение признака pcclass и Sex  в один                                                                                                                       |
| Гипотеза            |  if сделаю категориальный признак SexPclass, then модели будет удобнее работать, because данный признак будет лучше отражать действительно так как зависимость нелинейная  |
| Одно изменение      | Объединить признаки Pclass и Sex в один приз                                                                                                                               |
| Критерий успеха     | Primary improvement >= +0.0050; add explicit metric guardrails below.                                                                                                      |
| Формальные критерии | failed                                                                                                                                                                     |
| Решение | reject |
| Run                 | exp_010_v1                                                                                                                                                                 |
| Версия данных       | 7d118fef8b6c…                                                                                                                                                              |
| Validation          | stratified_kfold(n_splits=5, shuffle=True, seed=42)                                                                                                                        |
| Reference           | champion_reference                                                                                                                                                         |
| Основной кандидат   | candidate                                                                                                                                                                  |
| Основная метрика    | accuracy                                                                                                                                                                   |
| Цепочка             | EXP-001 → [[experiments/EXP-002 AGE_Experiment.md\|EXP-002]] → [[experiments/EXP-003 Family Size.md\|EXP-003]] → EXP-010                                                   |
| Код эксперимента    | [[src/ml_project/experiments/exp_010_pclassxsex.py\|ml_project.experiments.exp_010_pclassxsex]]                                                                            |
| Hash кода           | e2a4cd461dbf…                                                                                                                                                              |

> [!note] Как читать Δ
> Положительное значение означает улучшение — и для maximize, и для minimize-метрик.

## Проверка pre-registered criteria

| Роль      | Метрика           | Наблюдаемый Δ | Минимальный Δ | Пройден |
| --------- | ----------------- | ------------: | ------------: | ------: |
| primary   | accuracy          |       -0.0056 |        0.0050 |   False |
| guardrail | Balanced accuracy |       -0.0161 |        0.0000 |   False |
| guardrail | Recall            |       -0.0613 |       -0.0100 |   False |
| guardrail | F1                |       -0.0220 |        0.0000 |   False |

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
| candidate          | Balanced accuracy | maximize    | 0.7858 ± 0.0184 |    0.8018 |       -0.0161 |
| candidate          | Precision         | maximize    | 0.8219 ± 0.0254 |    0.7916 |        0.0303 |
| candidate          | Recall            | maximize    | 0.6608 ± 0.0303 |    0.7220 |       -0.0613 |
| candidate          | F1                | maximize    | 0.7324 ± 0.0255 |    0.7544 |       -0.0220 |
| candidate          | ROC-AUC           | maximize    | 0.8663 ± 0.0179 |    0.8612 |        0.0050 |

## Метрика: accuracy

![[assets/experiments/EXP-010/metric-primary-accuracy.png]]

### Сводка

| Модель             |   Mean |    Std |    Min |    Max | Reference | Δ к reference |
| ------------------ | -----: | -----: | -----: | -----: | --------: | ------------: |
| champion_reference | 0.8204 | 0.0176 | 0.8034 | 0.8483 |    0.8204 |        0.0000 |
| candidate          | 0.8148 | 0.0162 | 0.7921 | 0.8315 |    0.8204 |       -0.0056 |

### Значения по folds

| Fold | candidate | champion_reference |
| ---: | --------: | -----------------: |
|    1 |    0.8045 |             0.8101 |
|    2 |    0.7921 |             0.8258 |
|    3 |    0.8202 |             0.8034 |
|    4 |    0.8315 |             0.8146 |
|    5 |    0.8258 |             0.8483 |

## Метрика: Balanced accuracy

![[assets/experiments/EXP-010/metric-secondary_1-balanced-accuracy.png]]

### Сводка

| Модель             |   Mean |    Std |    Min |    Max | Reference | Δ к reference |
| ------------------ | -----: | -----: | -----: | -----: | --------: | ------------: |
| champion_reference | 0.8018 | 0.0247 | 0.7735 | 0.8389 |    0.8018 |        0.0000 |
| candidate          | 0.7858 | 0.0184 | 0.7616 | 0.8047 |    0.8018 |       -0.0161 |

### Значения по folds

| Fold | candidate | champion_reference |
| ---: | --------: | -----------------: |
|    1 |    0.7734 |             0.7914 |
|    2 |    0.7616 |             0.8114 |
|    3 |    0.7872 |             0.7735 |
|    4 |    0.8047 |             0.7939 |
|    5 |    0.8020 |             0.8389 |

## Метрика: Precision

![[assets/experiments/EXP-010/metric-secondary_2-precision.png]]

### Сводка

| Модель             |   Mean |    Std |    Min |    Max | Reference | Δ к reference |
| ------------------ | -----: | -----: | -----: | -----: | --------: | ------------: |
| champion_reference | 0.7916 | 0.0125 | 0.7778 | 0.8088 |    0.7916 |        0.0000 |
| candidate          | 0.8219 | 0.0254 | 0.7818 | 0.8462 |    0.7916 |        0.0303 |

### Значения по folds

| Fold | candidate | champion_reference |
| ---: | --------: | -----------------: |
|    1 |    0.8148 |             0.7778 |
|    2 |    0.7818 |             0.7846 |
|    3 |    0.8462 |             0.8000 |
|    4 |    0.8393 |             0.7869 |
|    5 |    0.8276 |             0.8088 |

## Метрика: Recall

![[assets/experiments/EXP-010/metric-secondary_3-recall.png]]

### Сводка

| Модель             |   Mean |    Std |    Min |    Max | Reference | Δ к reference |
| ------------------ | -----: | -----: | -----: | -----: | --------: | ------------: |
| champion_reference | 0.7220 | 0.0558 | 0.6471 | 0.7971 |    0.7220 |        0.0000 |
| candidate          | 0.6608 | 0.0303 | 0.6324 | 0.6957 |    0.7220 |       -0.0613 |

### Значения по folds

| Fold | candidate | champion_reference |
| ---: | --------: | -----------------: |
|    1 |    0.6377 |             0.7101 |
|    2 |    0.6324 |             0.7500 |
|    3 |    0.6471 |             0.6471 |
|    4 |    0.6912 |             0.7059 |
|    5 |    0.6957 |             0.7971 |

## Метрика: F1

![[assets/experiments/EXP-010/metric-secondary_4-f1.png]]

### Сводка

| Модель             |   Mean |    Std |    Min |    Max | Reference | Δ к reference |
| ------------------ | -----: | -----: | -----: | -----: | --------: | ------------: |
| champion_reference | 0.7544 | 0.0327 | 0.7154 | 0.8029 |    0.7544 |        0.0000 |
| candidate          | 0.7324 | 0.0255 | 0.6992 | 0.7581 |    0.7544 |       -0.0220 |

### Значения по folds

| Fold | candidate | champion_reference |
| ---: | --------: | -----------------: |
|    1 |    0.7154 |             0.7424 |
|    2 |    0.6992 |             0.7669 |
|    3 |    0.7333 |             0.7154 |
|    4 |    0.7581 |             0.7442 |
|    5 |    0.7559 |             0.8029 |

## Метрика: ROC-AUC

![[assets/experiments/EXP-010/metric-secondary_5-roc-auc.png]]

### Сводка

| Модель             |   Mean |    Std |    Min |    Max | Reference | Δ к reference |
| ------------------ | -----: | -----: | -----: | -----: | --------: | ------------: |
| champion_reference | 0.8612 | 0.0230 | 0.8362 | 0.8864 |    0.8612 |        0.0000 |
| candidate          | 0.8663 | 0.0179 | 0.8450 | 0.8926 |    0.8612 |        0.0050 |

### Значения по folds

| Fold | candidate | champion_reference |
| ---: | --------: | -----------------: |
|    1 |    0.8926 |             0.8864 |
|    2 |    0.8672 |             0.8646 |
|    3 |    0.8557 |             0.8362 |
|    4 |    0.8450 |             0.8390 |
|    5 |    0.8709 |             0.8801 |

## Диагностика candidate

> [!info] Граница интерпретации
> Диагностика использует fitted-модели тех же CV-folds. Importance описывает предсказания модели, а не причинный эффект признака.

### Контролируемое изменение

| Изменение                       | Признак   |
| ------------------------------- | --------- |
| добавлен в candidate            | SexPclass |
| исключён относительно reference | Pclass    |
| исключён относительно reference | Sex       |

### Путь данных по candidate pipeline

| Этап        | Transformer             | Строк | Колонок | Sparse | Плотность | Пропусков |
| ----------- | ----------------------- | ----: | ------: | -----: | --------: | --------: |
| input       | DataFrame               |   179 |      13 |  False |    0.8908 |       162 |
| title       | TitleExtractor          |   179 |      14 |  False |    0.8986 |       162 |
| age_imputer | AgeByTitlePclassImputer |   179 |      14 |  False |    0.8986 |       136 |
| preprocess  | ColumnTransformer       |   179 |      16 |  False |    0.3125 |         0 |

### Paired Δ на одинаковых folds

| Метрика           | Направление | Средний paired Δ | Std paired Δ | Min paired Δ | Max paired Δ |
| ----------------- | ----------- | ---------------: | -----------: | -----------: | -----------: |
| accuracy          | maximize    |          -0.0056 |       0.0228 |      -0.0337 |       0.0169 |
| Balanced accuracy | maximize    |          -0.0161 |       0.0282 |      -0.0497 |       0.0136 |
| Precision         | maximize    |           0.0303 |       0.0224 |      -0.0028 |       0.0524 |
| Recall            | maximize    |          -0.0613 |       0.0521 |      -0.1176 |       0.0000 |
| F1                | maximize    |          -0.0220 |       0.0375 |      -0.0677 |       0.0179 |
| ROC-AUC           | maximize    |           0.0050 |       0.0102 |      -0.0092 |       0.0195 |

### Изменение OOF-ошибок

| Переход      | Строк |   Доля |
| ------------ | ----: | -----: |
| both_correct |   709 | 0.7957 |
| broken       |    22 | 0.0247 |
| both_wrong   |   143 | 0.1605 |
| fixed        |    17 | 0.0191 |

### Validation permutation importance candidate

| Признак         | Mean importance |    Std |
| --------------- | --------------: | -----: |
| SexPclass       |          0.2389 | 0.0337 |
| Age             |          0.0243 | 0.0128 |
| FamilySizeGroup |          0.0229 | 0.0218 |
| Pclass          |          0.0041 | 0.0065 |
| Fare            |          0.0029 | 0.0028 |
| Name            |          0.0009 | 0.0069 |
| Cabin           |          0.0000 | 0.0000 |
| PassengerId     |          0.0000 | 0.0000 |
| Parch           |          0.0000 | 0.0000 |
| SibSp           |          0.0000 | 0.0000 |
| Sex             |          0.0000 | 0.0000 |
| Ticket          |          0.0000 | 0.0000 |
| Embarked        |         -0.0006 | 0.0095 |

![[assets/experiments/EXP-010/diagnostics/diagnostic-prediction-changes.png]]

![[assets/experiments/EXP-010/diagnostics/diagnostic-permutation-importance.png]]

![[assets/experiments/EXP-010/diagnostics/diagnostic-thresholds.png]]

### Диагностические таблицы

- [[artifacts/experiments/exp_010_v1/diagnostics/pipeline_stages.csv|pipeline_stages.csv]]
- [[artifacts/experiments/exp_010_v1/diagnostics/transformed_features.csv|transformed_features.csv]]
- [[artifacts/experiments/exp_010_v1/diagnostics/transformed_preview.csv|transformed_preview.csv]]
- [[artifacts/experiments/exp_010_v1/diagnostics/paired_fold_deltas.csv|paired_fold_deltas.csv]]
- [[artifacts/experiments/exp_010_v1/diagnostics/oof_predictions.csv|oof_predictions.csv]]
- [[artifacts/experiments/exp_010_v1/diagnostics/prediction_changes.csv|prediction_changes.csv]]
- [[artifacts/experiments/exp_010_v1/diagnostics/confusion.csv|confusion.csv]]
- [[artifacts/experiments/exp_010_v1/diagnostics/permutation_importance.csv|permutation_importance.csv]]
- [[artifacts/experiments/exp_010_v1/diagnostics/native_importance.csv|native_importance.csv]]
- [[artifacts/experiments/exp_010_v1/diagnostics/threshold_metrics.csv|threshold_metrics.csv]]
- [[artifacts/experiments/exp_010_v1/diagnostics/slice_metrics.csv|slice_metrics.csv]]

Подробный интерактивный разбор: [[notebooks/05_diagnostics.ipynb|05_diagnostics.ipynb]].

## Артефакты

- [[artifacts/experiments/exp_010_v1/cv_fold_scores.csv|cv_fold_scores.csv]]
- [[artifacts/experiments/exp_010_v1/cv_summary.csv|cv_summary.csv]]
- [[artifacts/experiments/exp_010_v1/metadata.json|metadata.json]]

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
