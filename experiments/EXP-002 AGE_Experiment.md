---
id: EXP-002
type: experiment
experiment_type: hypothesis-test
status: completed
created: 2026-08-02
hypothesis: "Если заполнить Age медианой по Title и Pclass внутри каждого train-fold, то accuracy повысится, потому что эти признаки несут информацию о возрасте."
primary_metric: "accuracy"
decision: adopt
---

# EXP-002 — Заполнение пропусков Age с помощью "title" and "Pclass"

← [[experiments/_index.md|Реестр]] · [[docs/05_experiments.md|Эксперименты]]

> [!info] Автоматическая часть
> Повторный запуск заменяет только отчёт между маркерами. Ручной анализ ниже сохраняется.

<!-- auto:experiment-report:start -->

## Контракт эксперимента

| Поле                | Значение                                                                                                                                             |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| Эксперимент         | EXP-002 — Заполнение пропусков Age с помощью "Title" и "Pclass"                                                                                      |
| Гипотеза            | Если заполнить Age медианой по Title и Pclass внутри каждого train-fold, то accuracy повысится, потому что эти признаки несут информацию о возрасте. |
| Одно изменение      | Новый fold-safe способ заполнения пропусков Age                                                                                                      |
| Критерий успеха     | Legacy pre-registration: accuracy должна вырасти; минимальный эффект и guardrails до первого запуска не были зафиксированы.                          |
| Формальные критерии | passed                                                                                                                                               |
| Решение             | adopt                                                                                                                                                |
| Run                 | exp_002_v1                                                                                                                                           |
| Версия данных       | 7d118fef8b6c…                                                                                                                                        |
| Validation          | stratified_kfold(n_splits=5, shuffle=True, seed=42)                                                                                                  |
| Reference           | baseline_reference                                                                                                                                   |
| Основной кандидат   | candidate                                                                                                                                            |
| Основная метрика    | accuracy                                                                                                                                             |
| Цепочка             | EXP-001 → EXP-002                                                                                                                                    |
| Код эксперимента    | [[src/ml_project/experiments/exp_002_age_imputation.py\|ml_project.experiments.exp_002_age_imputation]]                                              |
| Hash кода           | 7d95d20f5d10…                                                                                                                                        |

> [!note] Как читать Δ
> Положительное значение означает улучшение — и для maximize, и для minimize-метрик.

## Проверка pre-registered criteria

| Роль    | Метрика  | Наблюдаемый Δ | Минимальный Δ | Пройден |
| ------- | -------- | ------------: | ------------: | ------: |
| primary | accuracy |        0.0067 |        0.0000 |    True |

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

![[assets/experiments/EXP-002/metric-primary-accuracy.png]]

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

![[assets/experiments/EXP-002/metric-secondary_1-balanced-accuracy.png]]

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

![[assets/experiments/EXP-002/metric-secondary_2-precision.png]]

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

![[assets/experiments/EXP-002/metric-secondary_3-recall.png]]

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

![[assets/experiments/EXP-002/metric-secondary_4-f1.png]]

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

![[assets/experiments/EXP-002/metric-secondary_5-roc-auc.png]]

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

- **Что произошло:** Замена пропусков Age повысила среднюю аккураси на +0.0067
- **Подтвердилась ли гипотеза:** Гипотеза подтвердилась, хоть улучшение и не значительное, но вторичные метрики доже выросли, кроме рекалл
- **Почему мог получиться такой результат:** Потому что Титул и класс содержат некую информацию о возрасте, и результат будет явно ближе чем просто медиана по возрасту

## Обоснование решения

> Машинный source of truth для `decision` находится в
> `src/ml_project/experiments/exp_002_age_imputation.py`. После выбора решения
> карточка и registry синхронизируются из этого модуля.

- **Итоговое решение:** adopt — принимаем новый fold-safe Age imputer.
- **Следующий шаг:** использовать EXP-002 как champion reference для EXP-003.
