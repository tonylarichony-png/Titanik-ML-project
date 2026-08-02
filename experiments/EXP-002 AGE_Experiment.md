---
id: EXP-002
type: experiment
experiment_type: hypothesis-test
status: completed
created: 2026-08-02
hypothesis: " if я заполню возраст более точно, then accuracy должен повысится, because потому что как минимум станет возможно отделить детей и стариков, у которых есть большая зависимость с survived"
primary_metric: "accuracy"
decision: pending
---

# EXP-002 — Заполнение пропусков Age с помощью "title" and "Pclass"

← [[experiments/_index.md|Реестр]] · [[docs/05_experiments.md|Эксперименты]]

> [!info] Автоматическая часть
> Повторный запуск заменяет только отчёт между маркерами. Ручной анализ ниже сохраняется.

<!-- auto:experiment-report:start -->

## Контракт эксперимента

| Поле              | Значение                                                                                                                                                                                   |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Эксперимент       | EXP-002 — Заполнение пропусков Age с помощью "title" and "Pclass"                                                                                                                          |
| Гипотеза          |  if я заполню возраст более точно, then accuracy должен повысится, because потому что как минимум станет возможно отделить детей и стариков, у которых есть большая зависимость с survived |
| Одно изменение    | новый способ заполнения пустот                                                                                                                                                             |
| Критерий успеха   | accuracy                                                                                                                                                                                   |
| Решение           | pending                                                                                                                                                                                    |
| Run               | exp_002_v1                                                                                                                                                                                 |
| Версия данных     | 7d118fef8b6c…                                                                                                                                                                              |
| Validation        | stratified_kfold(n_splits=5, shuffle=True, seed=42)                                                                                                                                        |
| Reference         | baseline_reference                                                                                                                                                                         |
| Основной кандидат | candidate                                                                                                                                                                                  |
| Основная метрика  | accuracy                                                                                                                                                                                   |

> [!note] Как читать Δ
> Положительное значение означает улучшение — и для maximize, и для minimize-метрик.

## Сравнение всех метрик

| Модель             | Метрика           | Направление | mean ± std      | Reference | Δ к reference |
| ------------------ | ----------------- | ----------- | --------------- | --------: | ------------: |
| baseline_reference | accuracy          | maximize    | 0.7969 ± 0.0163 |    0.7969 |        0.0000 |
| baseline_reference | Balanced accuracy | maximize    | 0.7788 ± 0.0174 |    0.7788 |        0.0000 |
| baseline_reference | Precision         | maximize    | 0.7547 ± 0.0374 |    0.7547 |        0.0000 |
| baseline_reference | Recall            | maximize    | 0.7016 ± 0.0448 |    0.7016 |        0.0000 |
| baseline_reference | F1                | maximize    | 0.7258 ± 0.0233 |    0.7258 |        0.0000 |
| baseline_reference | ROC-AUC           | maximize    | 0.8514 ± 0.0251 |    0.8514 |        0.0000 |
| candidate          | accuracy          | maximize    | 0.8036 ± 0.0163 |    0.7969 |        0.0067 |
| candidate          | Balanced accuracy | maximize    | 0.7832 ± 0.0193 |    0.7788 |        0.0044 |
| candidate          | Precision         | maximize    | 0.7710 ± 0.0285 |    0.7547 |        0.0163 |
| candidate          | Recall            | maximize    | 0.6958 ± 0.0404 |    0.7016 |       -0.0058 |
| candidate          | F1                | maximize    | 0.7308 ± 0.0264 |    0.7258 |        0.0050 |
| candidate          | ROC-AUC           | maximize    | 0.8559 ± 0.0224 |    0.8514 |        0.0045 |

## Метрика: accuracy

![[artifacts/experiments/exp_002_v1/metric-primary-accuracy.png]]

### Сводка

| Модель             |   Mean |    Std |    Min |    Max | Reference | Δ к reference |
| ------------------ | -----: | -----: | -----: | -----: | --------: | ------------: |
| baseline_reference | 0.7969 | 0.0163 | 0.7809 | 0.8202 |    0.7969 |        0.0000 |
| candidate          | 0.8036 | 0.0163 | 0.7921 | 0.8315 |    0.7969 |        0.0067 |

### Значения по folds

| Fold | baseline_reference | candidate |
| ---: | -----------------: | --------: |
|    1 |             0.7821 |    0.7989 |
|    2 |             0.8034 |    0.8034 |
|    3 |             0.7978 |    0.7921 |
|    4 |             0.7809 |    0.7921 |
|    5 |             0.8202 |    0.8315 |

## Метрика: Balanced accuracy

![[artifacts/experiments/exp_002_v1/metric-secondary_1-balanced-accuracy.png]]

### Сводка

| Модель             |   Mean |    Std |    Min |    Max | Reference | Δ к reference |
| ------------------ | -----: | -----: | -----: | -----: | --------: | ------------: |
| baseline_reference | 0.7788 | 0.0174 | 0.7662 | 0.8080 |    0.7788 |        0.0000 |
| candidate          | 0.7832 | 0.0193 | 0.7616 | 0.8145 |    0.7788 |        0.0044 |

### Значения по folds

| Fold | baseline_reference | candidate |
| ---: | -----------------: | --------: |
|    1 |             0.7687 |    0.7796 |
|    2 |             0.7820 |    0.7820 |
|    3 |             0.7662 |    0.7616 |
|    4 |             0.7694 |    0.7785 |
|    5 |             0.8080 |    0.8145 |

## Метрика: Precision

![[artifacts/experiments/exp_002_v1/metric-secondary_2-precision.png]]

### Сводка

| Модель             |   Mean |    Std |    Min |    Max | Reference | Δ к reference |
| ------------------ | -----: | -----: | -----: | -----: | --------: | ------------: |
| baseline_reference | 0.7547 | 0.0374 | 0.7101 | 0.7963 |    0.7547 |        0.0000 |
| candidate          | 0.7710 | 0.0285 | 0.7313 | 0.8095 |    0.7547 |        0.0163 |

### Значения по folds

| Fold | baseline_reference | candidate |
| ---: | -----------------: | --------: |
|    1 |             0.7206 |    0.7619 |
|    2 |             0.7705 |    0.7705 |
|    3 |             0.7963 |    0.7818 |
|    4 |             0.7101 |    0.7313 |
|    5 |             0.7761 |    0.8095 |

## Метрика: Recall

![[artifacts/experiments/exp_002_v1/metric-secondary_3-recall.png]]

### Сводка

| Модель             |   Mean |    Std |    Min |    Max | Reference | Δ к reference |
| ------------------ | -----: | -----: | -----: | -----: | --------: | ------------: |
| baseline_reference | 0.7016 | 0.0448 | 0.6324 | 0.7536 |    0.7016 |        0.0000 |
| candidate          | 0.6958 | 0.0404 | 0.6324 | 0.7391 |    0.7016 |       -0.0058 |

### Значения по folds

| Fold | baseline_reference | candidate |
| ---: | -----------------: | --------: |
|    1 |             0.7101 |    0.6957 |
|    2 |             0.6912 |    0.6912 |
|    3 |             0.6324 |    0.6324 |
|    4 |             0.7206 |    0.7206 |
|    5 |             0.7536 |    0.7391 |

## Метрика: F1

![[artifacts/experiments/exp_002_v1/metric-secondary_4-f1.png]]

### Сводка

| Модель             |   Mean |    Std |    Min |    Max | Reference | Δ к reference |
| ------------------ | -----: | -----: | -----: | -----: | --------: | ------------: |
| baseline_reference | 0.7258 | 0.0233 | 0.7049 | 0.7647 |    0.7258 |        0.0000 |
| candidate          | 0.7308 | 0.0264 | 0.6992 | 0.7727 |    0.7258 |        0.0050 |

### Значения по folds

| Fold | baseline_reference | candidate |
| ---: | -----------------: | --------: |
|    1 |             0.7153 |    0.7273 |
|    2 |             0.7287 |    0.7287 |
|    3 |             0.7049 |    0.6992 |
|    4 |             0.7153 |    0.7259 |
|    5 |             0.7647 |    0.7727 |

## Метрика: ROC-AUC

![[artifacts/experiments/exp_002_v1/metric-secondary_5-roc-auc.png]]

### Сводка

| Модель             |   Mean |    Std |    Min |    Max | Reference | Δ к reference |
| ------------------ | -----: | -----: | -----: | -----: | --------: | ------------: |
| baseline_reference | 0.8514 | 0.0251 | 0.8267 | 0.8794 |    0.8514 |        0.0000 |
| candidate          | 0.8559 | 0.0224 | 0.8315 | 0.8831 |    0.8514 |        0.0045 |

### Значения по folds

| Fold | baseline_reference | candidate |
| ---: | -----------------: | --------: |
|    1 |             0.8741 |    0.8728 |
|    2 |             0.8501 |    0.8555 |
|    3 |             0.8267 |    0.8315 |
|    4 |             0.8267 |    0.8364 |
|    5 |             0.8794 |    0.8831 |

## Артефакты

- [[artifacts/experiments/exp_002_v1/cv_fold_scores.csv|cv_fold_scores.csv]]
- [[artifacts/experiments/exp_002_v1/cv_summary.csv|cv_summary.csv]]
- [[artifacts/experiments/exp_002_v1/metadata.json|metadata.json]]

<!-- auto:experiment-report:end -->

## Анализ результата — заполнить вручную

- **Что произошло:**
- **Подтвердилась ли гипотеза:**
- **Почему мог получиться такой результат:**
- **Стабильность по folds / seeds:**
- **Ограничения и возможный leakage:**

## Решение — заполнить вручную

- **Outcome:** adopt / reject / iterate / inconclusive.
- **Следующий шаг:**
