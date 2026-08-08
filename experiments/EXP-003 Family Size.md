---
id: EXP-003
type: experiment
experiment_type: hypothesis-test
status: completed
created: 2026-08-05
hypothesis: " if объединить признаки,и категоризировать then должен улучшиться accuracy, because потому, что данный признак будет лучше определять одиночек, либо семью так как зависимость нелинейная:1,2,3,4,>4 "
primary_metric: "accuracy"
decision: adopt
eda_findings: []
---

# EXP-003 — Объединение SibSp и Parch в признак FamilySizeGroup

← [[experiments/_index.md|Реестр]] · [[docs/05_experiments.md|Эксперименты]]

> [!info] Автоматическая часть
> Повторный запуск заменяет только отчёт между маркерами. Ручной анализ ниже сохраняется.

<!-- auto:experiment-report:start -->

## Контракт эксперимента

| Поле                | Значение                                                                                                                                                                                              |
| ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Эксперимент         | EXP-003 — Объединение SibSp и Parch в признак FamilySizeGroup                                                                                                                                         |
| Гипотеза            |  if объединить признаки,и категоризировать then должен улучшиться accuracy, because потому, что данный признак будет лучше определять одиночек, либо семью так как зависимость нелинейная:1,2,3,4,>4  |
| Одно изменение      | Взять признаки SibSp и Parch и объединить в FamilySize, относительно EXP002 больше ничего не менять                                                                                                   |
| Критерий успеха     | Primary improvement >= +0.0050; add explicit metric guardrails below.                                                                                                                                 |
| Формальные критерии | passed                                                                                                                                                                                                |
| Решение | adopt |
| Run                 | exp_003_v1                                                                                                                                                                                            |
| Версия данных       | 7d118fef8b6c…                                                                                                                                                                                         |
| Validation          | stratified_kfold(n_splits=5, shuffle=True, seed=42)                                                                                                                                                   |
| Reference           | champion_reference                                                                                                                                                                                    |
| Основной кандидат   | candidate                                                                                                                                                                                             |
| Основная метрика    | accuracy                                                                                                                                                                                              |
| Цепочка             | EXP-001 → [[experiments/EXP-002 AGE_Experiment.md\|EXP-002]] → EXP-003                                                                                                                                |
| Код эксперимента    | [[src/ml_project/experiments/exp_003_family_size.py\|ml_project.experiments.exp_003_family_size]]                                                                                                     |
| Hash кода           | 1e4a834e3e0e…                                                                                                                                                                                         |

> [!note] Как читать Δ
> Положительное значение означает улучшение — и для maximize, и для minimize-метрик.

## Проверка pre-registered criteria

| Роль      | Метрика           | Наблюдаемый Δ | Минимальный Δ | Пройден |
| --------- | ----------------- | ------------: | ------------: | ------: |
| primary   | accuracy          |        0.0168 |        0.0050 |    True |
| guardrail | Balanced accuracy |        0.0186 |        0.0000 |    True |
| guardrail | Recall            |        0.0263 |       -0.0100 |    True |
| guardrail | F1                |        0.0236 |        0.0000 |    True |

## Сравнение всех метрик

| Модель             | Метрика           | Направление | mean ± std      | Reference | Δ к reference |
| ------------------ | ----------------- | ----------- | --------------- | --------: | ------------: |
| champion_reference | accuracy          | maximize    | 0.8036 ± 0.0163 |    0.8036 |        0.0000 |
| champion_reference | Balanced accuracy | maximize    | 0.7832 ± 0.0193 |    0.7832 |        0.0000 |
| champion_reference | Precision         | maximize    | 0.7710 ± 0.0285 |    0.7710 |        0.0000 |
| champion_reference | Recall            | maximize    | 0.6958 ± 0.0404 |    0.6958 |        0.0000 |
| champion_reference | F1                | maximize    | 0.7308 ± 0.0264 |    0.7308 |        0.0000 |
| champion_reference | ROC-AUC           | maximize    | 0.8559 ± 0.0224 |    0.8559 |        0.0000 |
| candidate          | accuracy          | maximize    | 0.8204 ± 0.0176 |    0.8036 |        0.0168 |
| candidate          | Balanced accuracy | maximize    | 0.8018 ± 0.0247 |    0.7832 |        0.0186 |
| candidate          | Precision         | maximize    | 0.7916 ± 0.0125 |    0.7710 |        0.0206 |
| candidate          | Recall            | maximize    | 0.7220 ± 0.0558 |    0.6958 |        0.0263 |
| candidate          | F1                | maximize    | 0.7544 ± 0.0327 |    0.7308 |        0.0236 |
| candidate          | ROC-AUC           | maximize    | 0.8612 ± 0.0230 |    0.8559 |        0.0054 |

## Метрика: accuracy

![[assets/experiments/EXP-003/metric-primary-accuracy.png]]

### Сводка

| Модель             |   Mean |    Std |    Min |    Max | Reference | Δ к reference |
| ------------------ | -----: | -----: | -----: | -----: | --------: | ------------: |
| champion_reference | 0.8036 | 0.0163 | 0.7921 | 0.8315 |    0.8036 |        0.0000 |
| candidate          | 0.8204 | 0.0176 | 0.8034 | 0.8483 |    0.8036 |        0.0168 |

### Значения по folds

| Fold | candidate | champion_reference |
| ---: | --------: | -----------------: |
|    1 |    0.8101 |             0.7989 |
|    2 |    0.8258 |             0.8034 |
|    3 |    0.8034 |             0.7921 |
|    4 |    0.8146 |             0.7921 |
|    5 |    0.8483 |             0.8315 |

## Метрика: Balanced accuracy

![[assets/experiments/EXP-003/metric-secondary_1-balanced-accuracy.png]]

### Сводка

| Модель             |   Mean |    Std |    Min |    Max | Reference | Δ к reference |
| ------------------ | -----: | -----: | -----: | -----: | --------: | ------------: |
| champion_reference | 0.7832 | 0.0193 | 0.7616 | 0.8145 |    0.7832 |        0.0000 |
| candidate          | 0.8018 | 0.0247 | 0.7735 | 0.8389 |    0.7832 |        0.0186 |

### Значения по folds

| Fold | candidate | champion_reference |
| ---: | --------: | -----------------: |
|    1 |    0.7914 |             0.7796 |
|    2 |    0.8114 |             0.7820 |
|    3 |    0.7735 |             0.7616 |
|    4 |    0.7939 |             0.7785 |
|    5 |    0.8389 |             0.8145 |

## Метрика: Precision

![[assets/experiments/EXP-003/metric-secondary_2-precision.png]]

### Сводка

| Модель             |   Mean |    Std |    Min |    Max | Reference | Δ к reference |
| ------------------ | -----: | -----: | -----: | -----: | --------: | ------------: |
| champion_reference | 0.7710 | 0.0285 | 0.7313 | 0.8095 |    0.7710 |        0.0000 |
| candidate          | 0.7916 | 0.0125 | 0.7778 | 0.8088 |    0.7710 |        0.0206 |

### Значения по folds

| Fold | candidate | champion_reference |
| ---: | --------: | -----------------: |
|    1 |    0.7778 |             0.7619 |
|    2 |    0.7846 |             0.7705 |
|    3 |    0.8000 |             0.7818 |
|    4 |    0.7869 |             0.7313 |
|    5 |    0.8088 |             0.8095 |

## Метрика: Recall

![[assets/experiments/EXP-003/metric-secondary_3-recall.png]]

### Сводка

| Модель             |   Mean |    Std |    Min |    Max | Reference | Δ к reference |
| ------------------ | -----: | -----: | -----: | -----: | --------: | ------------: |
| champion_reference | 0.6958 | 0.0404 | 0.6324 | 0.7391 |    0.6958 |        0.0000 |
| candidate          | 0.7220 | 0.0558 | 0.6471 | 0.7971 |    0.6958 |        0.0263 |

### Значения по folds

| Fold | candidate | champion_reference |
| ---: | --------: | -----------------: |
|    1 |    0.7101 |             0.6957 |
|    2 |    0.7500 |             0.6912 |
|    3 |    0.6471 |             0.6324 |
|    4 |    0.7059 |             0.7206 |
|    5 |    0.7971 |             0.7391 |

## Метрика: F1

![[assets/experiments/EXP-003/metric-secondary_4-f1.png]]

### Сводка

| Модель             |   Mean |    Std |    Min |    Max | Reference | Δ к reference |
| ------------------ | -----: | -----: | -----: | -----: | --------: | ------------: |
| champion_reference | 0.7308 | 0.0264 | 0.6992 | 0.7727 |    0.7308 |        0.0000 |
| candidate          | 0.7544 | 0.0327 | 0.7154 | 0.8029 |    0.7308 |        0.0236 |

### Значения по folds

| Fold | candidate | champion_reference |
| ---: | --------: | -----------------: |
|    1 |    0.7424 |             0.7273 |
|    2 |    0.7669 |             0.7287 |
|    3 |    0.7154 |             0.6992 |
|    4 |    0.7442 |             0.7259 |
|    5 |    0.8029 |             0.7727 |

## Метрика: ROC-AUC

![[assets/experiments/EXP-003/metric-secondary_5-roc-auc.png]]

### Сводка

| Модель             |   Mean |    Std |    Min |    Max | Reference | Δ к reference |
| ------------------ | -----: | -----: | -----: | -----: | --------: | ------------: |
| champion_reference | 0.8559 | 0.0224 | 0.8315 | 0.8831 |    0.8559 |        0.0000 |
| candidate          | 0.8612 | 0.0230 | 0.8362 | 0.8864 |    0.8559 |        0.0054 |

### Значения по folds

| Fold | candidate | champion_reference |
| ---: | --------: | -----------------: |
|    1 |    0.8864 |             0.8728 |
|    2 |    0.8646 |             0.8555 |
|    3 |    0.8362 |             0.8315 |
|    4 |    0.8390 |             0.8364 |
|    5 |    0.8801 |             0.8831 |

## Артефакты

- [[artifacts/experiments/exp_003_v1/cv_fold_scores.csv|cv_fold_scores.csv]]
- [[artifacts/experiments/exp_003_v1/cv_summary.csv|cv_summary.csv]]
- [[artifacts/experiments/exp_003_v1/metadata.json|metadata.json]]

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
