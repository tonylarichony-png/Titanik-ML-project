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
Незавершённую функцию сначала разрабатывайте в локальном
`notebooks/workbench/EXP-xxx_*.ipynb`; официальный runner запускайте только
после переноса кода в experiment-модуль.
Новый эксперимент по умолчанию наследует модуль последней карточки с
`decision: adopt`; точный parent и вся цепочка фиксируются в карточке.
Решение меняйте только во frontmatter карточки и применяйте командой
`.\sync-experiment-state.cmd` — Python-модуль и его hash не изменяются.

## Сейчас выполняется

- …

## Автоматический реестр

<!-- auto:experiment-registry:start -->

| ID / карточка                                                                                                                                  | Run        | Метрика  | Результат | Решение   |
| ---------------------------------------------------------------------------------------------------------------------------------------------- | ---------- | -------- | --------: | --------- |
| [[experiments/EXP-001 Baseline.md\|EXP-001 Baseline]]                                                                                          | baseline   | accuracy |    0.7969 | reference |
| [[experiments/EXP-002 AGE_Experiment.md\|EXP-002 — Заполнение пропусков Age с помощью "Title" и "Pclass"]]                                     | exp_002_v1 | accuracy |    0.8036 | adopt     |
| [[experiments/EXP-003 Family Size.md\|EXP-003 — Объединение SibSp и Parch в признак FamilySizeGroup]]                                          | exp_003_v1 | accuracy |    0.8204 | adopt     |
| [[experiments/EXP-004 Fareperperson.md\|EXP-004 — Рассчет точной цены билета!]]                                                                | exp_004_v1 | accuracy |    0.8160 | reject    |
| [[experiments/EXP-005 Log1Pfareperperson.md\|EXP-005 — Рассчет точной цены билета и лог преобразование]]                                       | exp_005_v1 | accuracy |    0.8137 | reject    |
| [[experiments/EXP-006 Dobavlenie Novoy Fichi Isnotalone Iz Ticketgroupsize.md\|EXP-006 — Добавление новой Фичи IsnotAlone из TicketGroupSize]] | exp_006_v1 | accuracy |    0.8193 | reject    |
| [[experiments/EXP-007 Knowncabin.md\|EXP-007 — Начало работы с CABIN]]                                                                         | exp_007_v1 | accuracy |    0.8182 | reject    |
| [[experiments/EXP-008 Deck.md\|EXP-008 — Добавление фичи-Deck- палуба по первой букве CABIN]]                                                  | exp_008_v1 | accuracy |    0.8182 | reject    |
| [[experiments/EXP-009 Allin.md\|EXP-009 — ALLIN]]                                                                                              | exp_009_v1 | accuracy |    0.8126 | reject    |
| [[experiments/EXP-010 Pclassxsex.md\|EXP-010 — Объединение признака pcclass и Sex  в один]]                                                    | exp_010_v1 | accuracy |    0.8148 | reject    |
| [[experiments/EXP-011 Sexplcass V2.md\|EXP-011 — SexPlcass_V2]]                                                                                | exp_011_v1 | accuracy |    0.8148 | reject    |
| [[experiments/EXP-012 Exp 005 Ticketgroupsize.md\|EXP-012 — EXP-005+ticketGroupSize]]                                                          | exp_012_v1 | accuracy |    0.8137 | reject    |

<!-- auto:experiment-registry:end -->

## Все заметки в Obsidian

```query
path:"experiments" -file:"_index"
```
