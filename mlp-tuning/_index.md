# Optuna studies для PyTorch MLP

Эти исследования отбирают кандидатов на фиксированных screening-folds. Они не
меняют MLP-чемпиона напрямую: лучшие конфигурации оформляются обычными
`MLP-xxx`, проверяются на пяти официальных folds и только затем получают решение.

| Study | Trials | Лучший screening | Официальная проверка | Решение |
| --- | ---: | ---: | --- | --- |
| [[mlp-tuning/MLP-TUNE-001.md|MLP-TUNE-001 — базовый подбор]] | 140 | 0.8328 | [[mlp-experiments/MLP-042 Optuna best ReLU trial 0.md|MLP-042: 0.8193, Δ=-0.0191]] | reject |
| [[mlp-tuning/MLP-TUNE-002.md|MLP-TUNE-002 — архитектура и активации]] | 630 | 0.8328 | [[mlp-experiments/MLP-043 Optuna stable LeakyReLU trial 137.md|MLP-043: 0.8238, Δ=-0.0146]] | reject |

Текущий MLP-чемпион: [[mlp-experiments/MLP-024 dpoutmedium.md|MLP-024]],
официальная accuracy `0.8384 ± 0.0111`.
