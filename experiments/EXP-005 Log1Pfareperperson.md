---
id: EXP-005
type: experiment
experiment_type: hypothesis-test
status: completed
created: 2026-08-07
hypothesis: " if создать группы по номеру билета и из за скошенность прологорифмировать, then точнее можно оценить стоимость билета на человека , because это лучше отражает действительноть, ценность билета!"
primary_metric: "accuracy"
decision: reject
eda_findings: []
---

# EXP-005 — Рассчет точной цены билета и лог преобразование

← [[experiments/_index.md|Реестр]] · [[docs/05_experiments.md|Эксперименты]]

> [!info] Автоматическая часть
> Повторный запуск заменяет только отчёт между маркерами. Ручной анализ ниже сохраняется.

<!-- auto:experiment-report:start -->

## Контракт эксперимента

| Поле                | Значение                                                                                                                                                                                         |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Эксперимент         | EXP-005 — Рассчет точной цены билета и лог преобразование                                                                                                                                        |
| Гипотеза            | if создать группы по номеру билета и из за скошенность прологорифмировать, then точнее можно оценить стоимость билета на человека , because это лучше отражает действительноть, ценность билета! |
| Одно изменение      | Создать переменную TicketGroup, которая будет группировать билеты по номеру билета,и рассчитать FarePerPerson и преобразовать log1p относительно EXP003 больше ничего не менять                  |
| Критерий успеха     | Primary improvement >= +0.0050; add explicit metric guardrails below.                                                                                                                            |
| Формальные критерии | failed                                                                                                                                                                                           |
| Решение | reject |
| Run                 | exp_005_v1                                                                                                                                                                                       |
| Версия данных       | 7d118fef8b6c…                                                                                                                                                                                    |
| Validation          | stratified_kfold(n_splits=5, shuffle=True, seed=42)                                                                                                                                              |
| Reference           | champion_reference                                                                                                                                                                               |
| Основной кандидат   | candidate                                                                                                                                                                                        |
| Основная метрика    | accuracy                                                                                                                                                                                         |
| Цепочка             | EXP-001 → [[experiments/EXP-002 AGE_Experiment.md\|EXP-002]] → [[experiments/EXP-003 Family Size.md\|EXP-003]] → EXP-005                                                                         |
| Код эксперимента    | [[src/ml_project/experiments/exp_005_log1pfareperperson.py\|ml_project.experiments.exp_005_log1pfareperperson]]                                                                                  |
| Hash кода           | 310225442557…                                                                                                                                                                                    |

> [!note] Как читать Δ
> Положительное значение означает улучшение — и для maximize, и для minimize-метрик.

## Проверка pre-registered criteria

| Роль      | Метрика           | Наблюдаемый Δ | Минимальный Δ | Пройден |
| --------- | ----------------- | ------------: | ------------: | ------: |
| primary   | accuracy          |       -0.0067 |        0.0050 |   False |
| guardrail | Balanced accuracy |       -0.0066 |        0.0000 |   False |
| guardrail | Recall            |       -0.0058 |       -0.0100 |    True |
| guardrail | F1                |       -0.0081 |        0.0000 |   False |

## Сравнение всех метрик

| Модель             | Метрика           | Направление | mean ± std      | Reference | Δ к reference |
| ------------------ | ----------------- | ----------- | --------------- | --------: | ------------: |
| champion_reference | accuracy          | maximize    | 0.8204 ± 0.0176 |    0.8204 |        0.0000 |
| champion_reference | Balanced accuracy | maximize    | 0.8018 ± 0.0247 |    0.8018 |        0.0000 |
| champion_reference | Precision         | maximize    | 0.7916 ± 0.0125 |    0.7916 |        0.0000 |
| champion_reference | Recall            | maximize    | 0.7220 ± 0.0558 |    0.7220 |        0.0000 |
| champion_reference | F1                | maximize    | 0.7544 ± 0.0327 |    0.7544 |        0.0000 |
| champion_reference | ROC-AUC           | maximize    | 0.8612 ± 0.0230 |    0.8612 |        0.0000 |
| candidate          | accuracy          | maximize    | 0.8137 ± 0.0132 |    0.8204 |       -0.0067 |
| candidate          | Balanced accuracy | maximize    | 0.7953 ± 0.0193 |    0.8018 |       -0.0066 |
| candidate          | Precision         | maximize    | 0.7802 ± 0.0052 |    0.7916 |       -0.0115 |
| candidate          | Recall            | maximize    | 0.7162 ± 0.0455 |    0.7220 |       -0.0058 |
| candidate          | F1                | maximize    | 0.7463 ± 0.0258 |    0.7544 |       -0.0081 |
| candidate          | ROC-AUC           | maximize    | 0.8595 ± 0.0231 |    0.8612 |       -0.0018 |

## Метрика: accuracy

![[assets/experiments/EXP-005/metric-primary-accuracy.png]]

### Сводка

| Модель             |   Mean |    Std |    Min |    Max | Reference | Δ к reference |
| ------------------ | -----: | -----: | -----: | -----: | --------: | ------------: |
| champion_reference | 0.8204 | 0.0176 | 0.8034 | 0.8483 |    0.8204 |        0.0000 |
| candidate          | 0.8137 | 0.0132 | 0.7978 | 0.8315 |    0.8204 |       -0.0067 |

### Значения по folds

| Fold | candidate | champion_reference |
| ---: | --------: | -----------------: |
|    1 |    0.8045 |             0.8101 |
|    2 |    0.8202 |             0.8258 |
|    3 |    0.7978 |             0.8034 |
|    4 |    0.8146 |             0.8146 |
|    5 |    0.8315 |             0.8483 |

## Метрика: Balanced accuracy

![[assets/experiments/EXP-005/metric-secondary_1-balanced-accuracy.png]]

### Сводка

| Модель             |   Mean |    Std |    Min |    Max | Reference | Δ к reference |
| ------------------ | -----: | -----: | -----: | -----: | --------: | ------------: |
| champion_reference | 0.8018 | 0.0247 | 0.7735 | 0.8389 |    0.8018 |        0.0000 |
| candidate          | 0.7953 | 0.0193 | 0.7718 | 0.8225 |    0.8018 |       -0.0066 |

### Значения по folds

| Fold | candidate | champion_reference |
| ---: | --------: | -----------------: |
|    1 |    0.7842 |             0.7914 |
|    2 |    0.8040 |             0.8114 |
|    3 |    0.7718 |             0.7735 |
|    4 |    0.7939 |             0.7939 |
|    5 |    0.8225 |             0.8389 |

## Метрика: Precision

![[assets/experiments/EXP-005/metric-secondary_2-precision.png]]

### Сводка

| Модель             |   Mean |    Std |    Min |    Max | Reference | Δ к reference |
| ------------------ | -----: | -----: | -----: | -----: | --------: | ------------: |
| champion_reference | 0.7916 | 0.0125 | 0.7778 | 0.8088 |    0.7916 |        0.0000 |
| candidate          | 0.7802 | 0.0052 | 0.7742 | 0.7869 |    0.7916 |       -0.0115 |

### Значения по folds

| Fold | candidate | champion_reference |
| ---: | --------: | -----------------: |
|    1 |    0.7742 |             0.7778 |
|    2 |    0.7812 |             0.7846 |
|    3 |    0.7759 |             0.8000 |
|    4 |    0.7869 |             0.7869 |
|    5 |    0.7826 |             0.8088 |

## Метрика: Recall

![[assets/experiments/EXP-005/metric-secondary_3-recall.png]]

### Сводка

| Модель             |   Mean |    Std |    Min |    Max | Reference | Δ к reference |
| ------------------ | -----: | -----: | -----: | -----: | --------: | ------------: |
| champion_reference | 0.7220 | 0.0558 | 0.6471 | 0.7971 |    0.7220 |        0.0000 |
| candidate          | 0.7162 | 0.0455 | 0.6618 | 0.7826 |    0.7220 |       -0.0058 |

### Значения по folds

| Fold | candidate | champion_reference |
| ---: | --------: | -----------------: |
|    1 |    0.6957 |             0.7101 |
|    2 |    0.7353 |             0.7500 |
|    3 |    0.6618 |             0.6471 |
|    4 |    0.7059 |             0.7059 |
|    5 |    0.7826 |             0.7971 |

## Метрика: F1

![[assets/experiments/EXP-005/metric-secondary_4-f1.png]]

### Сводка

| Модель             |   Mean |    Std |    Min |    Max | Reference | Δ к reference |
| ------------------ | -----: | -----: | -----: | -----: | --------: | ------------: |
| champion_reference | 0.7544 | 0.0327 | 0.7154 | 0.8029 |    0.7544 |        0.0000 |
| candidate          | 0.7463 | 0.0258 | 0.7143 | 0.7826 |    0.7544 |       -0.0081 |

### Значения по folds

| Fold | candidate | champion_reference |
| ---: | --------: | -----------------: |
|    1 |    0.7328 |             0.7424 |
|    2 |    0.7576 |             0.7669 |
|    3 |    0.7143 |             0.7154 |
|    4 |    0.7442 |             0.7442 |
|    5 |    0.7826 |             0.8029 |

## Метрика: ROC-AUC

![[assets/experiments/EXP-005/metric-secondary_5-roc-auc.png]]

### Сводка

| Модель             |   Mean |    Std |    Min |    Max | Reference | Δ к reference |
| ------------------ | -----: | -----: | -----: | -----: | --------: | ------------: |
| champion_reference | 0.8612 | 0.0230 | 0.8362 | 0.8864 |    0.8612 |        0.0000 |
| candidate          | 0.8595 | 0.0231 | 0.8356 | 0.8872 |    0.8612 |       -0.0018 |

### Значения по folds

| Fold | candidate | champion_reference |
| ---: | --------: | -----------------: |
|    1 |    0.8872 |             0.8864 |
|    2 |    0.8595 |             0.8646 |
|    3 |    0.8356 |             0.8362 |
|    4 |    0.8377 |             0.8390 |
|    5 |    0.8773 |             0.8801 |

## Артефакты

- [[artifacts/experiments/exp_005_v1/cv_fold_scores.csv|cv_fold_scores.csv]]
- [[artifacts/experiments/exp_005_v1/cv_summary.csv|cv_summary.csv]]
- [[artifacts/experiments/exp_005_v1/metadata.json|metadata.json]]

<!-- auto:experiment-report:end -->

## EDA-основания

<!-- auto:experiment-eda-links:start -->

> EDA-основания пока не указаны. Добавьте ID в frontmatter: `eda_findings: ["EDA-003"]`, затем запустите `sync-experiment-links.cmd`.

<!-- auto:experiment-eda-links:end -->

## Анализ результата — заполнить вручную

- **Что произошло:** Почему то метрики ухудшились, ну это полный бред, я не понимаю почему, ведь это ближе к истине!! Модель может понять более точно цену билета, Как же так блин!
- **Подтвердилась ли гипотеза:**
- **Почему мог получиться такой результат:**
- **Стабильность по folds / seeds:**
- **Ограничения и возможный leakage:**

## Обоснование решения — заполнить вручную

> Source of truth для `decision` — поле во frontmatter этой карточки. После изменения запустите `sync-experiment-state.cmd`; переобучение не требуется.

- **Почему выбрано это решение:**
- **Следующий шаг:**
