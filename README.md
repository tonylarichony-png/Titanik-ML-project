---
type: ml-project
status: completed
stage: completed
owner:
best_result: SUB-002 / Random Forest / Kaggle 0.78708
last_reviewed: 2026-10-06
tags:
  - ml/project
---

# Titanic ML Project — Dashboard

> [!abstract] Назначение
> Главная точка входа в проект. Здесь хранится только текущее состояние и навигация; подробности находятся в связанных документах.

## Итог проекта

Проект завершён в формате **notebook-first**: воспроизводимые точки входа —
последовательность notebooks `01`–`07`, versioned-модули экспериментов и
отдельные notebooks MLP/ансамблей. Общий `main.py` намеренно не добавлялся:
notebook здесь одновременно является исполняемым pipeline, учебным объяснением
и видимым отчётом о промежуточных данных, preprocessing и cross-validation.

| Роль                           | Результат                                                                                                                  |
| ------------------------------ | -------------------------------------------------------------------------------------------------------------------------- |
| **Итоговый чемпион по Kaggle** | [[submissions/SUB-002.md\|SUB-002 — Random Forest, MS-001 / EXP-003]], Public score **0.78708**                            |
| Лидеры локальной CV            | [[model-screening/MS-005 ext_boost.md\|MS-005 — XGBoost и LightGBM]], accuracy **0.8417**; внешний результат оказался ниже |
| Принятый MLP-чемпион           | [[mlp-experiments/MLP-024 dpoutmedium.md\|MLP-024]], CV **0.8384 ± 0.0111**, [[submissions/SUB-010.md\|Kaggle 0.76794]]    |
| Финальный stacking             | [[ensembles/ENS-003 Learned weights.md\|ENS-003]], CV **0.8406 ± 0.0218**, [[submissions/SUB-009.md\|Kaggle 0.76076]]      |

Основной практический вывод: на 891 обучающем наблюдении сложные модели дали
оптимистичную локальную оценку, а более простой Random Forest оказался устойчивее
на Kaggle test.

## Как открыть исследования

Для полноценного просмотра установите [Obsidian](https://obsidian.md/download)
и откройте **корень этого проекта** как vault. Тогда будут работать Wiki-ссылки,
граф связей и переходы между EDA, EXP, MLP, screening, ансамблями и submission.
Без Obsidian файлы остаются обычным Markdown, но навигация вида `[[...]]` будет
менее удобной.

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
10. Для PyTorch MLP используйте [[#Как начать MLP-эксперимент|отдельный воспроизводимый launcher]].
11. Когда feature set стабилизирован, переходите к [[#Как начать групповой screening моделей|групповому screening моделей]].
12. Для проверки выбранного кандидата на Kaggle используйте [[#Как сделать Kaggle submission|универсальный submission notebook]].
13. Для нестандартных исследований и решений используйте встроенную команду Obsidian **Templates: Insert template**.

Полная инструкция: [[GUIDE.md|Как пользоваться шаблоном]].

Учебная практика: [[notebooks/Pytorch/08_pytorch_learning.ipynb|Первая нейросеть на Titanic в PyTorch]] — пошаговая тетрадь с 11 заданиями, подсказками и самопроверкой. Открывайте с kernel **Python (titanik-ml)**; установка PyTorch описана в начале тетради.

## Карточка проекта

| Поле | Значение |
|---|---|
| Проект | Titanic — предсказание выживания пассажиров |
| Цель проекта | Построить и сравнить воспроизводимые табличные модели и PyTorch MLP |
| ML-задача | Бинарная классификация |
| Владелец |  |
| Статус | `completed` |
| Текущий этап | `completed` |
| Основная метрика | `= [[docs/00_problem]].primary_metric` |
| Baseline | [[experiments/EXP-001 Baseline.md\|EXP-001]] — CV accuracy 0.7969 |
| Лучший результат | [[submissions/SUB-002.md\|SUB-002 Random Forest]] — Kaggle 0.78708 |
| Репозиторий / код |  |
| Трекер / MLflow |  |

## Фокус сейчас

> [!todo] Следующее действие
> Одно конкретное действие, которое двигает проект вперёд.

- **Текущая цель:** завершена;
- **Активная гипотеза:** нет;
- **Активный эксперимент:** нет;
- **Главный блокер:** нет;
- **Следующая контрольная точка:** проект готов к просмотру и сдаче.

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

## Как начать MLP-эксперимент

> [!tip] Воспроизводимый PyTorch-цикл
> 1. Активируйте окружение: `conda activate titanik-ml`.
> 2. Из корня проекта запустите `.\new-MLPexperiment.cmd`.
> 3. Launcher скопирует реализацию последнего принятого MLP в новый модуль `src/ml_project/mlp_experiments/mlp_xxx_*.py` и создаст связанный notebook `notebooks/mlp-experiments/MLP-xxx_*.ipynb`.
> 4. Измените в копии ровно одну гипотезу: признак, preprocessing, параметр обучения или архитектуру сети.
> 5. В notebook выполните Restart Kernel → Run All. Outer CV заново обучает preprocessing и сеть на каждом fold; inner split выбирает число эпох.
> 6. Запишите вывод до финального fit. Для новой гипотезы создайте следующий `MLP-xxx`, чтобы старый результат оставался воспроизводимым.

В новый модуль копируются `prepare_features`, списки признаков,
`build_fold_transformer`, `MLPTrainingConfig` и `build_network`. Launcher назначает
новые ID, название и карточку, записывает принятый MLP в `parent_mlp_module` и
очищает описание гипотезы. Это независимая versioned-копия: последующие изменения
референса не меняют уже созданный эксперимент. Пока принятого MLP нет, launcher
создаёт чистый стартовый шаблон и сравнивает его с принятым sklearn-чемпионом.

Детерминированные построчные признаки создаются в `prepare_features`. Статистики
по нескольким строкам — частоты, групповые средние, target encoding — создаются
через `build_fold_transformer`: его `fit` видит только train fold, а `transform`
применяет сохранённые статистики к validation/test без leakage.

После запуска notebook создаёт карточку в `mlp-experiments/` и сравнивает candidate
с reference на одинаковых folds. Решение меняется в карточке и синхронизируется
командой `.\sync-MLPexperiment-state.cmd`. Следующий launcher использует последний
`decision: adopt` одновременно как MLP-чемпиона для сравнения и как исходный код
следующего кандидата.

Для автоматического подбора используйте
[[notebooks/mlp-tuning/01_optuna_mlp.ipynb|MLP-TUNE-001 — Optuna]]. Notebook
проводит screening на фиксированных folds, последовательно сохраняет trials в
`artifacts/optuna/` и не создаёт официальные MLP-карточки. Лучшую конфигурацию
нужно перенести в новый `MLP-xxx` и проверить обычным paired CV до решения
`adopt`. Итог исследования: [[mlp-tuning/MLP-TUNE-001.md|карточка MLP-TUNE-001]].

Второй этап находится в
[[notebooks/mlp-tuning/02_optuna_mlp_activations.ipynb|MLP-TUNE-002 — архитектура и активации]].
Он использует отдельную SQLite study и подбирает `ReLU`, `LeakyReLU`, `GELU`,
`SiLU` или `SquaredReLU` вместе с глубиной, шириной и параметрами обучения.
Итог: [[mlp-tuning/MLP-TUNE-002.md|карточка MLP-TUNE-002]]. Общий реестр:
[[mlp-tuning/_index.md|Optuna studies]].

### Результаты PyTorch MLP

<!-- auto:mlp-results:start -->

| Эксперимент                                                                                                   | Reference         | Результат       | Δ       | Решение |
| ------------------------------------------------------------------------------------------------------------- | ----------------- | --------------- | ------- | ------- |
| [[mlp-experiments/MLP-001 Baseline.md\|MLP-001 — First reproducible MLP baseline]]                            | sklearn_champion  | 0.8148 ± 0.0134 | +0.0022 | pending |
| [[mlp-experiments/MLP-002 8 Neurons Baseline.md\|MLP-002 — Компактный MLP baseline — 8 скрытых нейронов]]     | sklearn_champion  | 0.8137 ± 0.0205 | +0.0011 | adopt   |
| [[mlp-experiments/MLP-003 mlp_16neurons.md\|MLP-003 — mlp_16neurons]]                                         | MLP-002_reference | 0.8137 ± 0.0209 | +0.0000 | reject  |
| [[mlp-experiments/MLP-004 mlp_32neurons.md\|MLP-004 — mlp_32neurons]]                                         | MLP-002_reference | 0.8148 ± 0.0134 | +0.0011 | reject  |
| [[mlp-experiments/MLP-005 FE_Family_size.md\|MLP-005 — FE_Family_size]]                                       | MLP-002_reference | 0.8103 ± 0.0172 | -0.0034 | reject  |
| [[mlp-experiments/MLP-006 FE_FAmilySize_16Neurons.md\|MLP-006 — FE_FAmilySize_16Neurons]]                     | MLP-002_reference | 0.8103 ± 0.0108 | -0.0034 | reject  |
| [[mlp-experiments/MLP-007 FE_familySize_32Neurons.md\|MLP-007 — FE_familySize_32Neurons]]                     | MLP-002_reference | 0.8103 ± 0.0231 | -0.0033 | reject  |
| [[mlp-experiments/MLP-008 Age median by Title.md\|MLP-008 — Заполнение Age медианой по Title]]                | MLP-002_reference | 0.8114 ± 0.0137 | -0.0022 | reject  |
| [[mlp-experiments/MLP-009 TABDDPM.md\|MLP-009 — TABDDPM]]                                                     | MLP-002_reference | 0.8126 ± 0.0182 | -0.0011 | reject  |
| [[mlp-experiments/MLP-010 MLP_ALLIN.md\|MLP-010 — MLP All In — все созданные признаки]]                       | MLP-002_reference | 0.8193 ± 0.0138 | +0.0056 | adopt   |
| [[mlp-experiments/MLP-011 MLP_16neurons.md\|MLP-011 — MLP_16neurons]]                                         | MLP-010_reference | 0.8148 ± 0.0134 | -0.0045 | reject  |
| [[mlp-experiments/MLP-012 ALLIN_16neurons.md\|MLP-012 — All In — 16 скрытых нейронов]]                        | MLP-010_reference | 0.8260 ± 0.0119 | +0.0067 | adopt   |
| [[mlp-experiments/MLP-013 ALLIN32_neurons.md\|MLP-013 — ALLIN32_neurons]]                                     | MLP-012_reference | 0.8193 ± 0.0184 | -0.0067 | reject  |
| [[mlp-experiments/MLP-014 ALLIN16BAtchnorm.md\|MLP-014 — ALLIN16BAtchnorm]]                                   | MLP-012_reference | 0.8170 ± 0.0143 | -0.0090 | reject  |
| [[mlp-experiments/MLP-015 Allin16plus new layer.md\|MLP-015 — Allin16plus new layer]]                         | MLP-012_reference | 0.8260 ± 0.0140 | -0.0000 | reject  |
| [[mlp-experiments/MLP-016 ALLin16plus16layer.md\|MLP-016 — ALLin16plus16layer]]                               | MLP-012_reference | 0.8271 ± 0.0154 | +0.0011 | adopt   |
| [[mlp-experiments/MLP-017 ALLIN16168.md\|MLP-017 — ALLIN16168]]                                               | MLP-016_reference | 0.8227 ± 0.0098 | -0.0045 | reject  |
| [[mlp-experiments/MLP-018 ALLIN161616.md\|MLP-018 — ALLIN161616]]                                             | MLP-016_reference | 0.8316 ± 0.0128 | +0.0045 | adopt   |
| [[mlp-experiments/MLP-019 323232.md\|MLP-019 — 323232]]                                                       | MLP-018_reference | 0.8227 ± 0.0129 | -0.0090 | reject  |
| [[mlp-experiments/MLP-020 16Batch1616.md\|MLP-020 — 16Batch1616]]                                             | MLP-018_reference | 0.8193 ± 0.0115 | -0.0123 | reject  |
| [[mlp-experiments/MLP-021 1616btch16.md\|MLP-021 — 1616btch16]]                                               | MLP-018_reference | 0.8103 ± 0.0146 | -0.0213 | reject  |
| [[mlp-experiments/MLP-022 161616batch.md\|MLP-022 — 161616batch]]                                             | MLP-018_reference | 0.8249 ± 0.0169 | -0.0067 | reject  |
| [[mlp-experiments/MLP-023 Dpoutlight.md\|MLP-023 — Dpoutlight]]                                               | MLP-018_reference | 0.8294 ± 0.0155 | -0.0023 | reject  |
| [[mlp-experiments/MLP-024 dpoutmedium.md\|MLP-024 — dpoutmedium]]                                             | MLP-018_reference | 0.8384 ± 0.0111 | +0.0067 | adopt   |
| [[mlp-experiments/MLP-025 dpoutmed-hard.md\|MLP-025 — dpoutmed-hard]]                                         | MLP-024_reference | 0.8271 ± 0.0186 | -0.0112 | reject  |
| [[mlp-experiments/MLP-026 Dpoutlight 1layer.md\|MLP-026 — Dpoutlight 1layer]]                                 | MLP-024_reference | 0.8238 ± 0.0170 | -0.0146 | reject  |
| [[mlp-experiments/MLP-027 Dpoutmed 1layer.md\|MLP-027 — Dpoutmed 1layer]]                                     | MLP-024_reference | 0.8171 ± 0.0123 | -0.0213 | reject  |
| [[mlp-experiments/MLP-028 dpout_2ndlayerlight.md\|MLP-028 — dpout_2ndlayerlight]]                             | MLP-024_reference | 0.8271 ± 0.0178 | -0.0112 | reject  |
| [[mlp-experiments/MLP-029 GELU.md\|MLP-029 — GELU]]                                                           | MLP-024_reference | 0.8271 ± 0.0103 | -0.0112 | reject  |
| [[mlp-experiments/MLP-030 Leakyrelu.md\|MLP-030 — Leakyrelu]]                                                 | MLP-024_reference | 0.8305 ± 0.0137 | -0.0079 | reject  |
| [[mlp-experiments/MLP-031 LeakyRelu01.md\|MLP-031 — LeakyRelu01]]                                             | MLP-024_reference | 0.8271 ± 0.0153 | -0.0112 | reject  |
| [[mlp-experiments/MLP-032 squaredReLU.md\|MLP-032 — squaredReLU]]                                             | MLP-024_reference | 0.8384 ± 0.0111 | +0.0000 | reject  |
| [[mlp-experiments/MLP-033 squearedRELU.md\|MLP-033 — squearedRELU]]                                           | MLP-024_reference | 0.7712 ± 0.0877 | -0.0671 | reject  |
| [[mlp-experiments/MLP-034 batchsize16.md\|MLP-034 — batchsize16]]                                             | MLP-024_reference | 0.8305 ± 0.0210 | -0.0079 | reject  |
| [[mlp-experiments/MLP-036 Batch64.md\|MLP-036 — Batch64]]                                                     | MLP-024_reference | 0.8271 ± 0.0172 | -0.0112 | reject  |
| [[mlp-experiments/MLP-037 decay0001.md\|MLP-037 — decay0.001]]                                                | MLP-024_reference | 0.8328 ± 0.0158 | -0.0056 | reject  |
| [[mlp-experiments/MLP-038 middecay.md\|MLP-038 — middecay]]                                                   | MLP-024_reference | 0.8215 ± 0.0109 | -0.0168 | reject  |
| [[mlp-experiments/MLP-039 decaye-5.md\|MLP-039 — decaye-5]]                                                   | MLP-024_reference | 0.8260 ± 0.0219 | -0.0123 | reject  |
| [[mlp-experiments/MLP-040 LRe-4.md\|MLP-040 — LRe-4]]                                                         | MLP-024_reference | 0.8260 ± 0.0115 | -0.0123 | reject  |
| [[mlp-experiments/MLP-041 LR-4mindelta.md\|MLP-041 — LR-4mindelta]]                                           | MLP-024_reference | 0.8271 ± 0.0117 | -0.0112 | reject  |
| [[mlp-experiments/MLP-042 Optuna best ReLU trial 0.md\|MLP-042 — Optuna best ReLU trial 0]]                   | MLP-024_reference | 0.8193 ± 0.0094 | -0.0191 | reject  |
| [[mlp-experiments/MLP-043 Optuna stable LeakyReLU trial 137.md\|MLP-043 — Optuna stable LeakyReLU trial 137]] | MLP-024_reference | 0.8238 ± 0.0132 | -0.0146 | reject  |
| [[mlp-experiments/MLP-044 Scheduler.md\|MLP-044 — Scheduler]]                                                 | MLP-024_reference | 0.8316 ± 0.0157 | -0.0067 | reject  |
| [[mlp-experiments/MLP-045 Embeddings.md\|MLP-045 — Embeddings]]                                               | MLP-024_reference | 0.8182 ± 0.0217 | -0.0202 | pending |

<!-- auto:mlp-results:end -->

Подробности полей, критериев и жизненного цикла: [[GUIDE.md#Новый эксперимент|руководство по новому эксперименту]].

## Как начать групповой screening моделей

> [!tip] Выбор семейства после feature engineering
> 1. В `src/ml_project/model_screening_config.py` один раз укажите
>    `feature_reference_module` принятого feature champion.
> 2. Выберите `active_group` и проверьте все стартовые параметры моделей в
>    `MODEL_GROUPS`. Это screening-параметры, а не скрытый tuning.
> 3. Выполните [[notebooks/06_model_screening.ipynb]] сверху вниз. Все модели,
>    включая точный feature champion, получат одинаковые строки, folds и метрики.
> 4. Разберите mean ± std, парные fold wins/losses, OOF-исправления ошибок и
>    importance выбранной диагностической модели.
> 5. Заполните созданную `model-screening/MS-xxx ...md` карточку. Для следующей
>    группы задайте новый `MS-ID`, note и `run_name`, затем повторите notebook.
> 6. После всех групп перенесите 2–3 разных семейства в coarse tuning. Победа
>    стартовой конфигурации сама по себе не регистрирует нового champion.

Старые feature-эксперименты целиком повторять для каждой модели не нужно:
сначала сравниваются семейства на лучшем feature set, затем для shortlist
делаются точечные ablation/retest действительно спорных признаков.

## Как сделать Kaggle submission

> [!tip] Один notebook для любого измеренного кандидата
> 1. Откройте [[notebooks/07_submission.ipynb]] и выполните каталог кандидатов.
> 2. В ячейке выбора задайте новый `SUBMISSION_ID` и один устойчивый
>    `SELECTED_CANDIDATE`, например `MS-001/feature_champion` или
>    `MS-001/random_forest`.
> 3. Проверьте source, feature set, estimator, CV и inference audit до fit.
> 4. Выполните full-train fit, проверьте строки, ключ и распределение prediction.
> 5. Только затем выполните финальную ячейку сохранения и загрузите напечатанный
>    CSV в Kaggle.
> 6. В созданной SUB-карточке вручную запишите Public score и наблюдение.

Notebook не позволяет свободно соединять признаки одного EXP с estimator другого
MS-run: Candidate ID всегда обозначает уже измеренный целый pipeline. EXP со
статусом reject остаются доступными, но контекстно-зависимый raw feature hook
будет остановлен train-serving audit.

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
- [[model-screening/_index.md|Screening моделей]]
- [[ensembles/_index.md|Ансамбли]]
- [[submissions/_index.md|Kaggle submissions]]
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
| [[experiments/EXP-013 Tt Comb.md\|EXP-013 — Train_test_combine]]                                                                               | accuracy |   0.8126 |      -0.0079 | adopt     |

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
