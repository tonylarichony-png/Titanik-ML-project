"""Project-specific dataset configuration shared by all notebooks."""

from pathlib import Path

RAW_DIR = Path("data/raw")

# Edit this mapping once; both 01_data.ipynb and 02_eda.ipynb import it.
DATASETS = {
    "train": {
        "filename": "train.csv",
        "role": "train",
        "required": True,
    },
    "test": {
        "filename": "test.csv",
        "role": "inference",
        "required": False,
    },
    "gender_submission": {
        "filename": "gender_submission.csv",
        "role": "submission_example",
        "required": False,
    },
}

TRAIN_DATASET = "train"
INFERENCE_DATASET = "test"
KEY = "PassengerId"
TARGET = "Survived"

# Assign every train column except TARGET to exactly one group.
# numeric + count are used in numeric EDA;
# categorical + ordinal are used in categorical EDA.
FEATURE_GROUPS = {
    "numeric": ["Age", "Fare"],
    "count": ["SibSp", "Parch"],
    "categorical": ["Sex", "Cabin", "Embarked"],
    "ordinal": ["Pclass"],
    "text": ["Name"],
    "datetime": [],
    "identifier": ["PassengerId", "Ticket"],
    "ignored": [],
}

# Optional human-readable column descriptions used in docs/01_data.md.
FIELD_DESCRIPTIONS = {
    'PassengerId': 'уникальный id пассажира ',
    'Survived': 'таргет 1-выжил, 0- не выжил',
    'Pclass': 'класс обслуживания',
    'Name': 'Имя Пассажира',
    'Sex': 'Пол',
    'Age': 'Возраст',
    'SibSp': 'Наличие горизонтальной родни(брат, муж)',
    'Parch': 'Наличие вертикальной родни(Дочь, Отец)',
    'Ticket': 'Номер билета',
    'Fare': 'Стоимость проезда',
    'Cabin': 'Номер каюты',
    'Embarked': 'Порт посадки \n C: (Шербур, Франция)\n Q:  (Квинстаун, Ирландия)\n S:(Саутгемптон, Англия)',
}