---
type: stage
stage: validation
status: draft
owner:
last_reviewed:
tags:
  - ml/stage
  - ml/validation
---

# 03 — Валидация

← [[docs/02_eda.md|EDA]] · [[README.md|Dashboard]] · Далее → [[docs/04_features.md|Features]]

> [!danger] Главное правило
> Протокол сравнения моделей фиксируется **до** масштабных экспериментов. Если схема меняется, оформите [[templates/decision.md|решение]] и пересчитайте сравниваемые результаты.

## Что имитирует validation

- **Production-сценарий:**
- **Момент предсказания:**
- **Какие объекты приходят в будущем:**
- **Главный distribution shift:**
- **Как offline-оценка связана с online-эффектом:**

## Основная метрика

| Поле                             | Значение                               |
| -------------------------------- | -------------------------------------- |
| Метрика                          | `= [[docs/00_problem]].primary_metric` |
| Направление                      | maximize                               |
| Бизнес-интерпретация             |                                        |
| Формула / implementation         | TP+TN/all                              |
| Порог практической значимости    |                                        |
| Минимальное улучшение к baseline |                                        |

> [!info] Единый источник истины
> Основная метрика автоматически подставляется из [[docs/00_problem.md#Метрика и критерий успеха]]. Чтобы изменить её во всём проекте, отредактируйте поле `primary_metric` там.

Технические параметры CV и scorer для первого запуска задаются в
`src/ml_project/baseline_config.py`; обоснование этих параметров остаётся в этом
документе.

## Вторичные метрики

<!-- auto:secondary-metrics:start -->

| Метрика           | Scorer / implementation | Направление |
| ----------------- | ----------------------- | ----------- |
| Balanced accuracy | balanced_accuracy       | maximize    |
| Precision         | precision               | maximize    |
| Recall            | recall                  | maximize    |
| F1                | f1                      | maximize    |
| ROC-AUC           | roc_auc                 | maximize    |

<!-- auto:secondary-metrics:end -->

Состав и техническая реализация таблицы синхронизируются из
`SECONDARY_SCORERS` в `src/ml_project/baseline_config.py`.

### Порог решения

Если модель выдаёт score:

- как выбирается threshold;
- на какой части данных он настраивается;
- фиксирован ли он при финальной оценке;
- какие бизнес-ограничения учитываются.

## Исполняемый протокол validation

<!-- auto:validation-protocol:start -->

| Параметр                | Исполняемое значение                                |
| ----------------------- | --------------------------------------------------- |
| Тип задачи              | binary_classification                               |
| Протокол                | stratified_kfold(n_splits=5, shuffle=True, seed=42) |
| CV strategy из конфига  | stratified_kfold                                    |
| Число folds             | 5                                                   |
| Shuffle                 | True                                                |
| Seed                    | 42                                                  |
| Group column            | None                                                |
| Time column             | None                                                |
| Основная метрика        | accuracy                                            |
| Основной scorer         | accuracy                                            |
| Направление             | maximize                                            |
| N jobs                  | -1                                                  |
| Error score             | raise                                               |
| Train score сохраняется | False                                               |
| Граница preprocessing   | fit только внутри train fold sklearn Pipeline       |

<!-- auto:validation-protocol:end -->

### Обоснование стратегии

- **Почему этот split имитирует будущие данные:** задача бинарной классификации, а стратификация сохраняет наблюдаемый баланс `Survived` [[02_eda#^6bbfc7]].
- **Какие ограничения данных учтены:**
- **Что агрегируется:** среднее, стандартное отклонение, минимум и максимум метрики по folds.
- **Когда протокол нужно пересмотреть:**

## Holdout policy

- Кто имеет право смотреть holdout?
- Когда он открывается?
- Сколько раз допускается оценка?
- Где хранится результат?
- Что считается утечкой информации из holdout?

## Leakage checklist

- [ ] Один объект / пользователь не попадает в разные части вопреки production-сценарию.
- [ ] Все fit-операции выполняются только на train fold.
- [ ] Imputation, scaling, encoding и feature selection находятся внутри pipeline.
- [ ] Временные признаки используют только прошлое.
- [ ] Target encoding рассчитан out-of-fold.
- [ ] Дубликаты не пер секают split.
- [ ] Подбор threshold не использует holdout.
- [ ] Feature store / joins соблюдают point-in-time correctness.

## Baseline protocol

<!-- auto:baseline-results:start -->

| Baseline            | Версия данных | Протокол                                            | Метрика  | Значение        |
| ------------------- | ------------- | --------------------------------------------------- | -------- | --------------- |
| dummy               | 7d118fef8b6c… | stratified_kfold(n_splits=5, shuffle=True, seed=42) | accuracy | 0.6162 ± 0.0026 |
| logistic_regression | 7d118fef8b6c… | stratified_kfold(n_splits=5, shuffle=True, seed=42) | accuracy | 0.7969 ± 0.0163 |

<!-- auto:baseline-results:end -->

[[notebooks/03_baseline.ipynb]] обновляет этот блок только при явном
`SYNC_DOCS = True`. До синхронизации таблицу можно заполнять вручную внутри
маркеров; текст вне маркеров никогда не перезаписывается.

## Стабильность оценки

- **Разброс по folds / seeds:**
- **Bootstrap CI:**
- **Минимальный размер эффекта:**
- **Статистический тест, если нужен:**
- **Ключевые сегменты для обязательной проверки:**

| Сегмент | Метрика | Минимум | Причина guardrail |
|---|---|---:|---|
|  |  |  |  |

## Политика честного сравнения

Во всех сравниваемых экспериментах фиксируются:

- версия датасета;
- split / folds;
- preprocessing boundary;
- основная метрика;
- seed или набор seeds;
- baseline;
- вычислительный бюджет.

Если изменилось несколько факторов одновременно, результат нельзя однозначно приписать одной гипотезе.

## Воспроизводимость

<!-- auto:reproducibility:start -->

| Поле                    | Значение                                                      |
| ----------------------- | ------------------------------------------------------------- |
| Dataset version         | 7d118fef8b6c…                                                 |
| Baseline config         | `src/ml_project/baseline_config.py`                           |
| Dataset config          | `src/ml_project/config.py`                                    |
| Split / evaluation code | `src/ml_project/modeling/validation.py`                       |
| Feature code            | `src/ml_project/modeling/features.py`                         |
| Run                     | baseline_v1                                                   |
| Validation              | stratified_kfold(n_splits=5, shuffle=True, seed=42)           |
| Seed policy             | RANDOM_STATE=42                                               |
| Environment             | Python 3.12.13; numpy 2.5.1; pandas 3.0.5; scikit-learn 1.9.0 |
| Run artifacts           | `artifacts/baseline/baseline_v1/`                             |
| Final model             | не сохранялась                                                |

<!-- auto:reproducibility:end -->

- **Где сохраняются OOF / test predictions:** пока не сохраняются.
- **Какие ручные действия нужны для полного воспроизведения:**

## Stage Gate: Validation

- [ ] Validation имитирует production-сценарий.
- [ ] Метрика соответствует бизнес-цене ошибок.
- [ ] Split учитывает время, группы и дубликаты.
- [ ] Есть закрытый holdout и правило его использования.
- [ ] Все preprocessing-шаги выполняются без leakage.
- [ ] Зафиксированы baseline и минимальный значимый эффект.
- [ ] Определены guardrail-метрики и важные сегменты.
- [ ] Протокол воспроизводим из кода и конфигурации.
- [ ] Все будущие эксперименты ссылаются на этот документ.

> [!success] Следующий этап
> После выполнения Stage Gate можно переходить к [[docs/04_features.md|04 — Признаки и model-ready выборка]].
