---
id: MLP-043
type: mlp-experiment
status: completed
decision: reject
implementation_module: ml_project.mlp_experiments.mlp_043_optuna_leaky_trial137
---

# MLP-043 — Optuna stable LeakyReLU trial 137

← [[mlp-experiments/_index.md|Реестр MLP]]

> [!info] Автоматическая часть
> Повторный запуск заменяет только отчёт между маркерами.

<!-- auto:mlp-experiment-report:start -->

## Контракт эксперимента

| Поле             | Значение                                                                                                                                                                             |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Эксперимент      | MLP-043 — Optuna stable LeakyReLU trial 137                                                                                                                                          |
| Гипотеза         | If the most consistently strong LeakyReLU configuration from MLP-TUNE-002 is evaluated on the official five folds, then its better screening stability and log loss will generalize. |
| Одно изменение   | Apply MLP-TUNE-002 trial 137 as one selected bundle: three 4-unit LeakyReLU(0.05) layers, dropout 0.10, lr 0.0012851267 and decay 1e-7.                                              |
| Решение          | reject |
| Reference        | MLP-024_reference: ml_project.mlp_experiments.mlp_024_dpoutmedium                                                                                                                    |
| Validation       | stratified_kfold(n_splits=5, shuffle=True, seed=42)                                                                                                                                  |
| Основная метрика | accuracy                                                                                                                                                                             |
| Критерии         | failed                                                                                                                                                                               |
| Код              | ml_project.mlp_experiments.mlp_043_optuna_leaky_trial137                                                                                                                             |
| Hash кода        | ddf8a7d8cf4c…                                                                                                                                                                        |

## Проверка pre-registered criteria

| role      | metric            | observed_improvement | minimum_improvement | passed |
| --------- | ----------------- | -------------------: | ------------------: | -----: |
| primary   | accuracy          |              -0.0146 |              0.0000 |  False |
| guardrail | balanced_accuracy |              -0.0156 |              0.0000 |  False |
| guardrail | recall            |              -0.0204 |             -0.0100 |  False |
| guardrail | f1                |              -0.0209 |              0.0000 |  False |

## Сравнение всех метрик

| model             | metric            |   mean |    std |    min |    max |
| ----------------- | ----------------- | -----: | -----: | -----: | -----: |
| MLP-024_reference | accuracy          | 0.8384 | 0.0111 | 0.8258 | 0.8547 |
| MLP-024_reference | balanced_accuracy | 0.8176 | 0.0111 | 0.8019 | 0.8278 |
| MLP-024_reference | precision         | 0.8324 | 0.0394 | 0.7969 | 0.8909 |
| MLP-024_reference | recall            | 0.7281 | 0.0351 | 0.6765 | 0.7647 |
| MLP-024_reference | f1                | 0.7756 | 0.0148 | 0.7541 | 0.7903 |
| MLP-024_reference | roc_auc           | 0.8780 | 0.0215 | 0.8592 | 0.9140 |
| MLP-024_reference | log_loss          | 0.4058 | 0.0244 | 0.3786 | 0.4403 |
| mlp_candidate     | accuracy          | 0.8238 | 0.0132 | 0.8034 | 0.8380 |
| mlp_candidate     | balanced_accuracy | 0.8020 | 0.0168 | 0.7763 | 0.8187 |
| mlp_candidate     | precision         | 0.8105 | 0.0300 | 0.7879 | 0.8571 |
| mlp_candidate     | recall            | 0.7077 | 0.0417 | 0.6618 | 0.7647 |
| mlp_candidate     | f1                | 0.7547 | 0.0223 | 0.7200 | 0.7761 |
| mlp_candidate     | roc_auc           | 0.8741 | 0.0189 | 0.8491 | 0.8998 |
| mlp_candidate     | log_loss          | 0.4114 | 0.0262 | 0.3930 | 0.4568 |

## Paired Δ по folds

| fold | metric            | reference | candidate | improvement |
| ---: | ----------------- | --------: | --------: | ----------: |
|    1 | accuracy          |    0.8547 |    0.8380 |     -0.0168 |
|    2 | accuracy          |    0.8371 |    0.8315 |     -0.0056 |
|    3 | accuracy          |    0.8315 |    0.8034 |     -0.0281 |
|    4 | accuracy          |    0.8427 |    0.8258 |     -0.0169 |
|    5 | accuracy          |    0.8258 |    0.8202 |     -0.0056 |
|    1 | balanced_accuracy |    0.8278 |    0.8115 |     -0.0163 |
|    2 | balanced_accuracy |    0.8233 |    0.8187 |     -0.0045 |
|    3 | balanced_accuracy |    0.8019 |    0.7763 |     -0.0255 |
|    4 | balanced_accuracy |    0.8250 |    0.8086 |     -0.0164 |
|    5 | balanced_accuracy |    0.8099 |    0.7947 |     -0.0152 |
|    1 | precision         |    0.8909 |    0.8571 |     -0.0338 |
|    2 | precision         |    0.8000 |    0.7879 |     -0.0121 |
|    3 | precision         |    0.8519 |    0.7895 |     -0.0624 |
|    4 | precision         |    0.8226 |    0.7937 |     -0.0289 |
|    5 | precision         |    0.7969 |    0.8246 |      0.0277 |
|    1 | recall            |    0.7101 |    0.6957 |     -0.0145 |
|    2 | recall            |    0.7647 |    0.7647 |      0.0000 |
|    3 | recall            |    0.6765 |    0.6618 |     -0.0147 |
|    4 | recall            |    0.7500 |    0.7353 |     -0.0147 |
|    5 | recall            |    0.7391 |    0.6812 |     -0.0580 |
|    1 | f1                |    0.7903 |    0.7680 |     -0.0223 |
|    2 | f1                |    0.7820 |    0.7761 |     -0.0058 |
|    3 | f1                |    0.7541 |    0.7200 |     -0.0341 |
|    4 | f1                |    0.7846 |    0.7634 |     -0.0213 |
|    5 | f1                |    0.7669 |    0.7460 |     -0.0209 |
|    1 | roc_auc           |    0.9140 |    0.8998 |     -0.0142 |
|    2 | roc_auc           |    0.8779 |    0.8810 |      0.0031 |
|    3 | roc_auc           |    0.8592 |    0.8491 |     -0.0100 |
|    4 | roc_auc           |    0.8747 |    0.8644 |     -0.0103 |
|    5 | roc_auc           |    0.8643 |    0.8760 |      0.0117 |
|    1 | log_loss          |    0.3786 |    0.3947 |     -0.0161 |
|    2 | log_loss          |    0.4027 |    0.3930 |      0.0097 |
|    3 | log_loss          |    0.4403 |    0.4568 |     -0.0165 |
|    4 | log_loss          |    0.3891 |    0.4029 |     -0.0138 |
|    5 | log_loss          |    0.4184 |    0.4095 |      0.0089 |

## OOF-изменения ошибок

| Исправлено ошибок reference | Добавлено новых ошибок | Fold wins | Fold losses | Ties |
| --------------------------: | ---------------------: | --------: | ----------: | ---: |
|                          11 |                     24 |         0 |           5 |    0 |

## Артефакты

- Run: [[artifacts/mlp-experiments/MLP-043/ddf8a7d8cf4c/metadata.json|metadata.json]]
- OOF: [[artifacts/mlp-experiments/MLP-043/ddf8a7d8cf4c/oof_predictions.csv|oof_predictions.csv]]
- Paired folds: [[artifacts/mlp-experiments/MLP-043/ddf8a7d8cf4c/paired_deltas.csv|paired_deltas.csv]]
- Training history: [[artifacts/mlp-experiments/MLP-043/ddf8a7d8cf4c/training_history.png|training_history.png]]

<!-- auto:mlp-experiment-report:end -->

## Анализ и решение

- Гипотеза не подтвердилась. LeakyReLU была самой устойчивой альтернативой во
  втором screening: медиана `0.8238`, 15 попаданий в top-20 и лучший результат
  `0.8305`. На официальных folds accuracy составила только `0.8238` против
  `0.8384` у MLP-024 (`Δ=-0.0146`).
- Кандидат исправил 11 ошибок reference и добавил 24 новых. Он проиграл по
  accuracy на всех пяти folds; balanced accuracy и F1 также снизились. Log loss
  `0.4114` оказался близок к MLP-024 (`0.4058`), но не превзошёл его.
- Early stopping выбрал эпохи 45, 74, 31, 89 и 75. Сеть обучалась дольше, однако
  дополнительное обучение не дало лучшего обобщения.
- Решение: `reject`. Устойчивость LeakyReLU внутри 630 trials на фиксированных
  screening-folds не перенеслась на официальную проверку. Чемпионом остаётся
  MLP-024.
- Следующий шаг: новые признаки или ансамбль; повторять поиск активаций на тех же
  folds не следует.
