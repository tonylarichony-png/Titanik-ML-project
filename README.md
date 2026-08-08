---
type: ml-project
status: idea
stage: problem
owner:
best_result:
last_reviewed:
tags:
  - ml/project
---

# ML Project — Dashboard

> [!abstract] Назначение
> Главная точка входа в проект. Здесь хранится только текущее состояние и навигация; подробности находятся в связанных документах.

## Быстрый старт

1. Выберите нужные разделы в [[PROJECT_CONFIG.md|настройке проекта]].
2. Заполните карточку проекта ниже.
3. Сформулируйте задачу в [[docs/00_problem.md]].
4. Поместите исходные файлы в `data/raw/`, запустите [[notebooks/01_data.ipynb|паспорт данных]] и дополните [[docs/01_data.md]].
5. Запустите [[notebooks/02_eda.ipynb|основной EDA]], затем [[notebooks/02_eda_anomalies.ipynb|обзор выбросов]], заполните [[docs/02_eda.md]] и превратите наблюдения в проверяемые рекомендации.
6. Зафиксируйте честную проверку качества в [[docs/03_validation.md]] **до сравнения моделей**.
7. Опишите model-ready выборку и preprocessing в [[docs/04_features.md]].
8. Настройте `src/ml_project/baseline_config.py` и запустите [[notebooks/03_baseline.ipynb|первый воспроизводимый baseline]].
9. Для каждой контролируемой проверки используйте [[#Как начать новый эксперимент|короткую инструкцию создания эксперимента]].
10. Для нестандартных исследований и решений используйте встроенную команду Obsidian **Templates: Insert template**.

Полная инструкция: [[GUIDE.md|Как пользоваться шаблоном]].

## Карточка проекта

| Поле | Значение |
|---|---|
| Проект |  |
| Цель проекта |  |
| ML-задача |  |
| Владелец |  |
| Статус | `idea` |
| Текущий этап | `problem` |
| Основная метрика | `= [[docs/00_problem]].primary_metric` |
| Baseline |  |
| Лучший результат |  |
| Репозиторий / код |  |
| Трекер / MLflow |  |

## Фокус сейчас

> [!todo] Следующее действие
> Одно конкретное действие, которое двигает проект вперёд.

- **Текущая цель:**
- **Активная гипотеза:**
- **Активный эксперимент:**
- **Главный блокер:**
- **Следующая контрольная точка:**

## Как начать новый эксперимент

> [!tip] Новый контролируемый эксперимент
> 1. Активируйте окружение: `conda activate titanik-ml`.
> 2. Из корня проекта запустите `.\new-experiment.cmd`: launcher создаст модуль и локальный workbench.
> 3. Разработайте и проверьте идею в напечатанном `notebooks/workbench/EXP-xxx_*.ipynb`.
> 4. Перенесите проверенную реализацию в созданный модуль `src/ml_project/experiments/exp_xxx_*.py`.
> 5. Перезапустите kernel и выполните строгий [[notebooks/04_experiment.ipynb]] сверху вниз.
> 6. Разберите автоматически сохранённые OOF-ошибки и путь нового признака в
>    [[notebooks/05_diagnostics.ipynb]], если результат требует объяснения.
> 7. В frontmatter карточки эксперимента укажите EDA-основания, например
>    `eda_findings: ["EDA-003"]`.
> 8. После интерпретации измените `decision:` во frontmatter этой же карточки
>    на `adopt`, `reject`, `iterate` или `inconclusive`, затем запустите
>    `sync-experiment-state.cmd`. Переобучение не требуется; следующий launcher
>    автоматически использует последнюю карточку с `decision: adopt`.
>
> Launcher сам предложит следующий `EXP-xxx`, критерии и guardrails, покажет
> preview, родителя и выберет новый модуль. `--from-baseline` создаёт независимую
> проверку без champion. Workbench не пишет официальные результаты и игнорируется
> Git; Python-модуль остаётся source of truth для кода, а Markdown-карточка —
> для решения и EDA-связей.

В experiment-коде `ModelingSettings` описывает способ построения и оценки
модели: `reference_settings` приходят от baseline/чемпиона, а
`candidate_settings` содержат только изменение текущей гипотезы.

Подробности полей, критериев и жизненного цикла: [[GUIDE.md#Новый эксперимент|руководство по новому эксперименту]].

## Pipeline

- [x] 0. [[docs/00_problem.md|Problem — постановка задачи]]
- [x] 1. [[docs/01_data.md|Data — общая информация об исходных файлах]]
- [x] 2. [[docs/02_eda.md|EDA — исследование и рекомендации]]
- [ ] 3. [[docs/03_validation.md|Validation — схема оценки]]
- [ ] 4. [[docs/04_features.md|Features — model-ready выборка и признаки]]
- [ ] 5. [[docs/05_experiments.md|Experiments — эксперименты]]
- [ ] 6. [[docs/06_error_analysis.md|Error analysis — анализ ошибок]]
- [ ] 7. [[docs/07_production.md|Production — внедрение и мониторинг]]

> [!important]
> Этап отмечается завершённым только после выполнения его **Stage Gate**. Pipeline цикличен: анализ ошибок и production-мониторинг могут вернуть проект к данным, валидации или признакам.

## Рабочие реестры

- [[hypotheses/_index.md|Гипотезы]]
- [[experiments/_index.md|Эксперименты]]
- [[decisions/_index.md|Решения]]
- [[issues/_index.md|Проблемы и блокеры]]
- [[assets/_index.md|Артефакты и графики]]
- [[artifacts/_index.md|Локальные модели и результаты запусков]]

## Ключевые результаты

<!-- auto:key-results:start -->

| Версия / эксперимент                                                                                                                           | Метрика  | Значение | Δ к baseline | Решение   |
| ---------------------------------------------------------------------------------------------------------------------------------------------- | -------- | -------: | -----------: | --------- |
| [[experiments/EXP-001 Baseline.md\|EXP-001 Baseline]]                                                                                          | accuracy |   0.7969 |            — | reference |
| [[experiments/EXP-002 AGE_Experiment.md\|EXP-002 — Заполнение пропусков Age с помощью "Title" и "Pclass"]]                                     | accuracy |   0.8036 |      +0.0067 | adopt     |
| [[experiments/EXP-003 Family Size.md\|EXP-003 — Объединение SibSp и Parch в признак FamilySizeGroup]]                                          | accuracy |   0.8204 |      +0.0168 | adopt     |
| [[experiments/EXP-004 Fareperperson.md\|EXP-004 — Рассчет точной цены билета!]]                                                                | accuracy |   0.8160 |      -0.0045 | reject    |
| [[experiments/EXP-005 Log1Pfareperperson.md\|EXP-005 — Рассчет точной цены билета и лог преобразование]]                                       | accuracy |   0.8137 |      -0.0067 | reject    |
| [[experiments/EXP-006 Dobavlenie Novoy Fichi Isnotalone Iz Ticketgroupsize.md\|EXP-006 — Добавление новой Фичи IsnotAlone из TicketGroupSize]] | accuracy |   0.8193 |      -0.0011 | reject    |
| [[experiments/EXP-007 Knowncabin.md\|EXP-007 — Начало работы с CABIN]]                                                                         | accuracy |   0.8182 |      -0.0022 | reject    |
| [[experiments/EXP-008 Deck.md\|EXP-008 — Добавление фичи-Deck- палуба по первой букве CABIN]]                                                  | accuracy |   0.8182 |      -0.0023 | reject    |
| [[experiments/EXP-009 Allin.md\|EXP-009 — ALLIN]]                                                                                              | accuracy |   0.8126 |      -0.0079 | reject    |
| [[experiments/EXP-010 Pclassxsex.md\|EXP-010 — Объединение признака pcclass и Sex  в один]]                                                    | accuracy |   0.8148 |      -0.0056 | reject    |
| [[experiments/EXP-011 Sexplcass V2.md\|EXP-011 — SexPlcass_V2]]                                                                                | accuracy |   0.8148 |      -0.0056 | reject    |
| [[experiments/EXP-012 Exp 005 Ticketgroupsize.md\|EXP-012 — EXP-005+ticketGroupSize]]                                                          | accuracy |   0.8137 |      -0.0067 | reject    |

<!-- auto:key-results:end -->

Блок обновляется автоматически при синхронизации baseline и контролируемых
экспериментов. Подробности результата и выводы хранятся в связанных карточках.

## Последние решения

| Решение | Дата | Причина | Что изменилось |
|---|---|---|---|
|  |  |  |  |

## Риски и блокеры

- [ ]

## Ближайшие действия

- [ ]
- [ ]
- [ ]

## Рабочий принцип

Каждое существенное действие должно отвечать на четыре вопроса:

1. **Почему** это делаем?
2. **Как** проверяем?
3. **Какой результат** получили?
4. **Какое решение** приняли?
