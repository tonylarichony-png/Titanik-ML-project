---
id: MLP-TUNE-002
type: mlp-tuning-study
status: completed
decision: reject
reference: MLP-024
trials: 630
---

# MLP-TUNE-002 — архитектура и функции активации

← [[mlp-tuning/_index.md|Реестр Optuna studies]]

## Цель

Проверить взаимодействие функции активации с глубиной, шириной, Dropout и
параметрами оптимизации. Исследование продолжило выводы MLP-TUNE-001 в отдельной
SQLite study.

## Контракт

- Notebook: [[notebooks/mlp-tuning/02_optuna_mlp_activations.ipynb]].
- Storage: [[artifacts/optuna/titanic_mlp_tuning_002.db]].
- Trials CSV: [[artifacts/optuna/titanic_mlp_tuning_002_trials.csv]].
- Screening: те же 3 фиксированных folds с seed `2026`.
- Sampler: `TPESampler(seed=43)`; `n_jobs=1`.
- Первая trial: лидер MLP-TUNE-001 с `ReLU`.
- Test.csv не использовался.

## Пространство поиска

| Параметр | Значения |
| --- | --- |
| activation | ReLU, LeakyReLU, GELU, SiLU, SquaredReLU |
| negative_slope | 0.01, 0.05, 0.10 только для LeakyReLU |
| batch_size | 32, 64 |
| learning_rate | 0.0012 … 0.0025, log scale |
| weight_decay | 1e-7, 1e-6, 1e-5, 1e-4 |
| dropout | 0.05 … 0.30 |
| n_layers | 3 … 5 |
| hidden_dim | 4, 8, 12, 16 |

## Анализ активаций

| Активация | Trials | Лучшая accuracy | Медиана | Средняя | В top-20 |
| --- | ---: | ---: | ---: | ---: | ---: |
| ReLU | 262 | 0.8328 | 0.8227 | 0.8213 | 5 |
| LeakyReLU | 288 | 0.8305 | 0.8238 | 0.8226 | 15 |
| GELU | 31 | 0.8249 | 0.8171 | 0.8154 | 0 |
| SiLU | 26 | 0.8227 | 0.8148 | 0.8156 | 0 |
| SquaredReLU | 23 | 0.8193 | 0.7508 | 0.7582 | 0 |

ReLU сохранила самый высокий одиночный screening-результат благодаря контрольной
trial 0. LeakyReLU чаще попадала в top-20 и имела лучшую медиану. GELU и SiLU не
дали преимущества, а SquaredReLU ещё раз показала нестабильное обучение.

Лучшим содержательно новым кандидатом выбрана trial 137: три слоя по 4 нейрона,
`LeakyReLU(0.05)`, Dropout 0.10, batch 32, learning rate `0.0012851267`, decay
`1e-7`. Screening accuracy составила `0.8305`, log loss — `0.4227`.

## Официальная проверка

Trial 137 оформлена как
[[mlp-experiments/MLP-043 Optuna stable LeakyReLU trial 137.md|MLP-043]]. На пяти
folds она получила `0.8238 ± 0.0132` против `0.8384 ± 0.0111` у MLP-024:
`Δ=-0.0146`. Кандидат проиграл по accuracy на всех folds, исправил 11 ошибок и
добавил 24. Trial 193 дала ту же accuracy, но немного худшие balanced accuracy,
F1 и log loss, поэтому отдельным MLP-экспериментом не оформлялась.

## Решение

`reject`. Даже наиболее устойчивое screening-направление не перенеслось на
официальные folds. После 630 trials продолжение подбора на тех же folds увеличит
selection bias. Чемпионом остаётся MLP-024; следующий этап должен менять признаки
или семейство модели.
