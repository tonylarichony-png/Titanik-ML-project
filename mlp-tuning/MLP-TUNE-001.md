---
id: MLP-TUNE-001
type: mlp-tuning-study
status: completed
decision: reject
reference: MLP-024
trials: 140
---

# MLP-TUNE-001 — базовый подбор гиперпараметров

← [[mlp-tuning/_index.md|Реестр Optuna studies]]

## Цель

Проверить, может ли автоматический подбор размера batch, learning rate, weight
decay, Dropout, глубины и общей ширины сети улучшить принятую MLP-024 при
неизменных признаках, `ReLU`, отсутствии BatchNorm и Dropout после последнего
скрытого слоя.

## Контракт

- Notebook: [[notebooks/mlp-tuning/01_optuna_mlp.ipynb]].
- Storage: [[artifacts/optuna/titanic_mlp_tuning_001.db]].
- Trials CSV: [[artifacts/optuna/titanic_mlp_tuning_001_trials.csv]].
- Screening: 3 фиксированных stratified folds, `shuffle=True`, seed `2026`.
- Sampler: `TPESampler(seed=42)`; последовательное выполнение `n_jobs=1`.
- Target: средняя accuracy на screening-folds.
- Test.csv не использовался.

## Пространство поиска

| Параметр | Значения |
| --- | --- |
| batch_size | 16, 32, 64 |
| learning_rate | 3e-4 … 3e-3, log scale |
| weight_decay | 0, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3 |
| dropout | 0.10 … 0.30 |
| n_layers | 2 … 4 |
| hidden_dim | 8, 16, 24, 32 |

## Screening

Контрольная trial 0 повторяла MLP-024 и получила `0.8159`. Лучший результат
нашла trial 86:

| Параметр | Значение |
| --- | ---: |
| screening accuracy | 0.832772 |
| std | 0.023888 |
| log loss | 0.454552 |
| batch_size | 32 |
| learning_rate | 0.0017503535 |
| weight_decay | 0.0001 |
| dropout | 0.30 |
| n_layers | 4 |
| hidden_dim | 8 |

После trial 86 следующие 53 запуска максимум не улучшили. Несмотря на прирост
screening accuracy, log loss был хуже контрольного, поэтому конфигурация
рассматривалась только как кандидат.

## Официальная проверка

Конфигурация оформлена как
[[mlp-experiments/MLP-042 Optuna best ReLU trial 0.md|MLP-042]]. На пяти folds с
seed 42 она получила `0.8193 ± 0.0094` против `0.8384 ± 0.0111` у MLP-024:
`Δ=-0.0191`. Кандидат проиграл на четырёх folds и сравнялся на одном, исправил 13
ошибок и добавил 30.

## Решение

`reject`. Рост на трёх screening-folds не обобщился. Фиксированные folds после
многих trials стали частью процесса подбора, поэтому их лидер оказался подогнан
под screening. MLP-024 остаётся чемпионом.
