---
id: EXP-001
type: experiment
experiment_type: baseline
status: completed
---

# EXP-001 — Baseline

> [!info] Автоматический отчёт
> Перезапуск notebook обновляет только блок ниже. Ручные выводы после него сохраняются.

<!-- auto:baseline-experiment-report:start -->

## Сводка запуска

| Поле             | Значение                                            |
| ---------------- | --------------------------------------------------- |
| Эксперимент      | EXP-001 — Baseline                                  |
| Run              | baseline_v1                                         |
| Версия данных    | 7d118fef8b6c…                                       |
| Validation       | stratified_kfold(n_splits=5, shuffle=True, seed=42) |
| Основная метрика | accuracy                                            |
| Основная модель  | logistic regression                                 |

## Сравнение всех метрик

| Модель              | Метрика           | Направление | mean ± std      |    Min |    Max | Folds |
| ------------------- | ----------------- | ----------- | --------------- | -----: | -----: | ----: |
| dummy               | accuracy          | maximize    | 0.6162 ± 0.0026 | 0.6124 | 0.6180 |     5 |
| dummy               | Balanced accuracy | maximize    | 0.5000 ± 0.0000 | 0.5000 | 0.5000 |     5 |
| dummy               | Precision         | maximize    | 0.0000 ± 0.0000 | 0.0000 | 0.0000 |     5 |
| dummy               | Recall            | maximize    | 0.0000 ± 0.0000 | 0.0000 | 0.0000 |     5 |
| dummy               | F1                | maximize    | 0.0000 ± 0.0000 | 0.0000 | 0.0000 |     5 |
| dummy               | ROC-AUC           | maximize    | 0.5000 ± 0.0000 | 0.5000 | 0.5000 |     5 |
| logistic_regression | accuracy          | maximize    | 0.7969 ± 0.0163 | 0.7809 | 0.8202 |     5 |
| logistic_regression | Balanced accuracy | maximize    | 0.7788 ± 0.0174 | 0.7662 | 0.8080 |     5 |
| logistic_regression | Precision         | maximize    | 0.7547 ± 0.0374 | 0.7101 | 0.7963 |     5 |
| logistic_regression | Recall            | maximize    | 0.7016 ± 0.0448 | 0.6324 | 0.7536 |     5 |
| logistic_regression | F1                | maximize    | 0.7258 ± 0.0233 | 0.7049 | 0.7647 |     5 |
| logistic_regression | ROC-AUC           | maximize    | 0.8514 ± 0.0251 | 0.8267 | 0.8794 |     5 |

## Метрика: accuracy

![[assets/experiments/EXP-001/metric-primary-accuracy.png]]

### Сводка по моделям

| Модель              |   Mean |    Std |    Min |    Max | Folds | Направление |
| ------------------- | -----: | -----: | -----: | -----: | ----: | ----------- |
| dummy               | 0.6162 | 0.0026 | 0.6124 | 0.6180 |     5 | maximize    |
| logistic_regression | 0.7969 | 0.0163 | 0.7809 | 0.8202 |     5 | maximize    |

### Значения по folds

| Fold |  dummy | logistic_regression |
| ---: | -----: | ------------------: |
|    1 | 0.6145 |              0.7821 |
|    2 | 0.6180 |              0.8034 |
|    3 | 0.6180 |              0.7978 |
|    4 | 0.6180 |              0.7809 |
|    5 | 0.6124 |              0.8202 |

## Метрика: Balanced accuracy

![[assets/experiments/EXP-001/metric-secondary_1-balanced-accuracy.png]]

### Сводка по моделям

| Модель              |   Mean |    Std |    Min |    Max | Folds | Направление |
| ------------------- | -----: | -----: | -----: | -----: | ----: | ----------- |
| dummy               | 0.5000 | 0.0000 | 0.5000 | 0.5000 |     5 | maximize    |
| logistic_regression | 0.7788 | 0.0174 | 0.7662 | 0.8080 |     5 | maximize    |

### Значения по folds

| Fold |  dummy | logistic_regression |
| ---: | -----: | ------------------: |
|    1 | 0.5000 |              0.7687 |
|    2 | 0.5000 |              0.7820 |
|    3 | 0.5000 |              0.7662 |
|    4 | 0.5000 |              0.7694 |
|    5 | 0.5000 |              0.8080 |

## Метрика: Precision

![[assets/experiments/EXP-001/metric-secondary_2-precision.png]]

### Сводка по моделям

| Модель              |   Mean |    Std |    Min |    Max | Folds | Направление |
| ------------------- | -----: | -----: | -----: | -----: | ----: | ----------- |
| dummy               | 0.0000 | 0.0000 | 0.0000 | 0.0000 |     5 | maximize    |
| logistic_regression | 0.7547 | 0.0374 | 0.7101 | 0.7963 |     5 | maximize    |

### Значения по folds

| Fold |  dummy | logistic_regression |
| ---: | -----: | ------------------: |
|    1 | 0.0000 |              0.7206 |
|    2 | 0.0000 |              0.7705 |
|    3 | 0.0000 |              0.7963 |
|    4 | 0.0000 |              0.7101 |
|    5 | 0.0000 |              0.7761 |

## Метрика: Recall

![[assets/experiments/EXP-001/metric-secondary_3-recall.png]]

### Сводка по моделям

| Модель              |   Mean |    Std |    Min |    Max | Folds | Направление |
| ------------------- | -----: | -----: | -----: | -----: | ----: | ----------- |
| dummy               | 0.0000 | 0.0000 | 0.0000 | 0.0000 |     5 | maximize    |
| logistic_regression | 0.7016 | 0.0448 | 0.6324 | 0.7536 |     5 | maximize    |

### Значения по folds

| Fold |  dummy | logistic_regression |
| ---: | -----: | ------------------: |
|    1 | 0.0000 |              0.7101 |
|    2 | 0.0000 |              0.6912 |
|    3 | 0.0000 |              0.6324 |
|    4 | 0.0000 |              0.7206 |
|    5 | 0.0000 |              0.7536 |

## Метрика: F1

![[assets/experiments/EXP-001/metric-secondary_4-f1.png]]

### Сводка по моделям

| Модель              |   Mean |    Std |    Min |    Max | Folds | Направление |
| ------------------- | -----: | -----: | -----: | -----: | ----: | ----------- |
| dummy               | 0.0000 | 0.0000 | 0.0000 | 0.0000 |     5 | maximize    |
| logistic_regression | 0.7258 | 0.0233 | 0.7049 | 0.7647 |     5 | maximize    |

### Значения по folds

| Fold |  dummy | logistic_regression |
| ---: | -----: | ------------------: |
|    1 | 0.0000 |              0.7153 |
|    2 | 0.0000 |              0.7287 |
|    3 | 0.0000 |              0.7049 |
|    4 | 0.0000 |              0.7153 |
|    5 | 0.0000 |              0.7647 |

## Метрика: ROC-AUC

![[assets/experiments/EXP-001/metric-secondary_5-roc-auc.png]]

### Сводка по моделям

| Модель              |   Mean |    Std |    Min |    Max | Folds | Направление |
| ------------------- | -----: | -----: | -----: | -----: | ----: | ----------- |
| dummy               | 0.5000 | 0.0000 | 0.5000 | 0.5000 |     5 | maximize    |
| logistic_regression | 0.8514 | 0.0251 | 0.8267 | 0.8794 |     5 | maximize    |

### Значения по folds

| Fold |  dummy | logistic_regression |
| ---: | -----: | ------------------: |
|    1 | 0.5000 |              0.8741 |
|    2 | 0.5000 |              0.8501 |
|    3 | 0.5000 |              0.8267 |
|    4 | 0.5000 |              0.8267 |
|    5 | 0.5000 |              0.8794 |

## Артефакты

- Полная таблица folds: [[artifacts/baseline/baseline_v1/cv_fold_scores.csv|cv_fold_scores.csv]]
- Полная сводка: [[artifacts/baseline/baseline_v1/cv_summary.csv|cv_summary.csv]]
- Конфигурация запуска: [[artifacts/baseline/baseline_v1/metadata.json|metadata.json]]

<!-- auto:baseline-experiment-report:end -->

## Анализ и выводы

- Что показало сравнение с dummy: Логистическая регрессия превосходит дамми модель на порядок !
- Насколько результат стабилен между folds: вмеру стабилен...
- Какие метрики расходятся и почему это важно:
- Что проверить следующим экспериментом:начать фиче инжениринг, заполнять пропуски смотреть результаты лог. регрессии
