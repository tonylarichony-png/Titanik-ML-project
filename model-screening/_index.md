---
type: registry
entity: model-screening
---

# Реестр группового screening моделей

Screening начинается после завершения основной серии feature experiments.
Каждый запуск берёт один принятый feature reference, одну группу стартовых
моделей и неизменный validation contract.

Настройки и параметры: `src/ml_project/model_screening_config.py`.
Официальный запуск: [[notebooks/06_model_screening.ipynb]].

<!-- auto:model-screening-registry:start -->

| Screening                                              | Feature set | Group            | Model                  | Metric   |   Mean |    Std | Δ vs champion | Rank | Shortlist |
| ------------------------------------------------------ | ----------- | ---------------- | ---------------------- | -------- | -----: | -----: | ------------: | ---: | --------: |
| [[model-screening/MS-001 Tree Bagging.md\|MS-001]]     | EXP-003     | tree_bagging     | random_forest          | accuracy | 0.8227 | 0.0123 |        0.0022 |    1 |      True |
| [[model-screening/MS-001 Tree Bagging.md\|MS-001]]     | EXP-003     | tree_bagging     | feature_champion       | accuracy | 0.8204 | 0.0176 |        0.0000 |    2 |     False |
| [[model-screening/MS-001 Tree Bagging.md\|MS-001]]     | EXP-003     | tree_bagging     | extra_trees            | accuracy | 0.8070 | 0.0148 |       -0.0135 |    3 |      True |
| [[model-screening/MS-001 Tree Bagging.md\|MS-001]]     | EXP-003     | tree_bagging     | decision_tree          | accuracy | 0.8036 | 0.0225 |       -0.0168 |    4 |     False |
| [[model-screening/MS-002 Tree Bagging.md\|MS-002]]     | EXP-013     | tree_bagging     | random_forest          | accuracy | 0.8182 | 0.0197 |        0.0056 |    1 |      True |
| [[model-screening/MS-002 Tree Bagging.md\|MS-002]]     | EXP-013     | tree_bagging     | decision_tree          | accuracy | 0.8137 | 0.0239 |        0.0011 |    2 |      True |
| [[model-screening/MS-002 Tree Bagging.md\|MS-002]]     | EXP-013     | tree_bagging     | feature_champion       | accuracy | 0.8126 | 0.0152 |        0.0000 |    3 |     False |
| [[model-screening/MS-002 Tree Bagging.md\|MS-002]]     | EXP-013     | tree_bagging     | extra_trees            | accuracy | 0.8114 | 0.0152 |       -0.0011 |    4 |     False |
| [[model-screening/MS-003 sklearn_boosting.md\|MS-003]] | EXP-013     | sklearn_boosting | gradient_boosting      | accuracy | 0.8372 | 0.0223 |        0.0247 |    1 |      True |
| [[model-screening/MS-003 sklearn_boosting.md\|MS-003]] | EXP-013     | sklearn_boosting | hist_gradient_boosting | accuracy | 0.8339 | 0.0165 |        0.0213 |    2 |      True |
| [[model-screening/MS-003 sklearn_boosting.md\|MS-003]] | EXP-013     | sklearn_boosting | feature_champion       | accuracy | 0.8126 | 0.0152 |        0.0000 |    3 |     False |
| [[model-screening/MS-004 sklearn_boosting.md\|MS-004]] | EXP-013     | sklearn_boosting | hist_gradient_boosting | accuracy | 0.8350 | 0.0213 |        0.0224 |    1 |      True |
| [[model-screening/MS-004 sklearn_boosting.md\|MS-004]] | EXP-013     | sklearn_boosting | gradient_boosting      | accuracy | 0.8350 | 0.0199 |        0.0224 |    2 |      True |
| [[model-screening/MS-004 sklearn_boosting.md\|MS-004]] | EXP-013     | sklearn_boosting | feature_champion       | accuracy | 0.8126 | 0.0152 |        0.0000 |    3 |     False |

<!-- auto:model-screening-registry:end -->

## Как читать результат

- `Δ vs champion > 0` — средняя primary metric лучше feature champion;
- `Wins/Ties/Losses` — парное сравнение на тех же folds;
- `Shortlist` — модель стоит проверить tuning-ом, но она ещё не новый champion;
- решение и объяснение хранятся в отдельной `MS-xxx` карточке.
