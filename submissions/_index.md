---
type: registry
entity: kaggle-submissions
---

# Kaggle submissions

Каждый SUB-run выбирает один уже измеренный Candidate ID, восстанавливает его
точный feature/model pipeline, выполняет full-train fit и создаёт локальный CSV.

Выбор и официальный запуск: [[notebooks/07_submission.ipynb]].

<!-- auto:submission-registry:start -->

| Submission                          | Candidate                     | Feature set | Model                          | CV              | Rows | Public score |
| ----------------------------------- | ----------------------------- | ----------- | ------------------------------ | --------------- | ---: | ------------ |
| [[submissions/SUB-001.md\|SUB-001]] | MS-001/feature_champion       | EXP-003     | LogisticRegression             | 0.8204 ± 0.0176 |  418 | "0.76315"    |
| [[submissions/SUB-002.md\|SUB-002]] | MS-001/random_forest          | EXP-003     | RandomForestClassifier         | 0.8227 ± 0.0123 |  418 | "0.78708"    |
| [[submissions/SUB-003.md\|SUB-003]] | EXP-013/candidate             | EXP-013     | LogisticRegression             | 0.8126 ± 0.0152 |  418 | "0.78468"    |
| [[submissions/SUB-004.md\|SUB-004]] | MS-002/random_forest          | EXP-013     | RandomForestClassifier         | 0.8182 ± 0.0197 |  418 | "0.77990"    |
| [[submissions/SUB-005.md\|SUB-005]] | MS-003/hist_gradient_boosting | EXP-013     | HistGradientBoostingClassifier | 0.8339 ± 0.0165 |  418 | "0.75358"    |
| [[submissions/SUB-006.md\|SUB-006]] | MS-003/gradient_boosting      | EXP-013     | GradientBoostingClassifier     | 0.8372 ± 0.0223 |  418 | "0.76315"    |

<!-- auto:submission-registry:end -->

## Как читать

- `Candidate` связывает файл с конкретным EXP/MS-результатом;
- fitted pipeline и CSV хранятся локально в `artifacts/submissions/<SUB-ID>/`;
- Public score заполняется вручную в SUB-карточке после загрузки на Kaggle;
- Kaggle score не заменяет локальную валидацию и не назначает champion.
