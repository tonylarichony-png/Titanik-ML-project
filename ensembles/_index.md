# Ансамбли

| Эксперимент | Метод | Accuracy | Лучший одиночный | Δ | Решение |
|---|---|---:|---:|---:|---|
| [[ensembles/ENS-001 Probability averaging.md\|ENS-001]] | Среднее вероятностей пяти моделей | 0.8395 ± 0.0232 | XGBoost: 0.8417 ± 0.0176 | -0.0023 | pending |
| [[ensembles/ENS-002 Strong models averaging.md\|ENS-002]] | XGBoost + LightGBM + CatBoost + MLP-024 | 0.8294 ± 0.0207 | XGBoost: 0.8417 ± 0.0176 | -0.0124 | pending |
| [[ensembles/ENS-003 Learned weights.md\|ENS-003]] | Nested-CV автоматически обученные веса | 0.8406 ± 0.0218 | XGBoost: 0.8417 ± 0.0176 | -0.0011 | pending |
