---
type: registry
entity: experiment
---

# Реестр экспериментов

Перед новой контролируемой проверкой откройте
[[README.md#Как начать новый эксперимент|короткую инструкцию в карточке проекта]].
Общий [[notebooks/04_experiment.ipynb]] сам создаёт карточку, сохраняет
графики/таблицы и обновляет leaderboard. Ручной шаблон нужен только для
нестандартных исследований, которые не проходят через этот конвейер.

## Сейчас выполняется

- …

## Автоматический реестр

<!-- auto:experiment-registry:start -->

| ID / карточка                                                                                              | Run         | Метрика  | Результат | Решение   |
| ---------------------------------------------------------------------------------------------------------- | ----------- | -------- | --------: | --------- |
| [[experiments/EXP-001 Baseline.md\|EXP-001 Baseline]]                                                      | baseline_v1 | accuracy |    0.7969 | reference |
| [[experiments/EXP-002 AGE_Experiment.md\|EXP-002 — Заполнение пропусков Age с помощью "Title" и "Pclass"]] | exp_002_v1  | accuracy |    0.8036 | pending   |

<!-- auto:experiment-registry:end -->

## Все заметки в Obsidian

```query
path:"experiments" -file:"_index"
```
