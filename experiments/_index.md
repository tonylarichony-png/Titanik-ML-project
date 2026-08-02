---
type: registry
entity: experiment
---

# Реестр экспериментов

Создайте заметку с именем `EXP-xxx Короткое название`, затем вставьте [[templates/experiment.md|шаблон эксперимента]]. Сводные результаты ведите в [[docs/05_experiments.md]].

Для контролируемого модельного сравнения используйте [[notebooks/04_experiment.ipynb]]:
он сам создаёт карточку, сохраняет графики/таблицы и обновляет leaderboard.

## Сейчас выполняется

- …

## Все заметки

```query
path:"experiments" -file:"_index"
```
