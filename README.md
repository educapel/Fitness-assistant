# 💪 Fitness Assistant

Fitness Assistant is your personal exercise companion! Whether you're a beginner or a pro, this project helps you **search, filter, and explore exercises** based on body part, equipment, muscle groups, and more — all in one place.

---

## 🚀 Features

- **Search Exercises:** Quickly find exercises by name or description.  
- **Filter Options:** Filter by type of activity, equipment, body part, and muscle groups.  
- **Detailed Instructions:** Step-by-step guidance for each exercise.  
- **Categorized Workouts:** Organize exercises by type: strength, cardio, flexibility, and more.  
- **Keyword & Text Search:** Supports both exact matches and full-text search.

---

## 📊 Dataset

The dataset used in this project contains information about various exercises, including:

* **Exercise Name:** The name of the exercise (e.g., Push-Ups, Squats).
* **Type of Activity:** The general category of the exercise (e.g., Strength, Mobility, Cardio).
* **Type of Equipment:** The equipment needed for the exercise (e.g., Bodyweight, Dumbbells, Kettlebell).
* **Body Part:** The part of the body primarily targeted by the exercise (e.g., Upper Body, Core, Lower Body).
* **Type:** The movement type (e.g., Push, Pull, Hold, Stretch).
* **Muscle Groups Activated:** The specific muscles engaged during the exercise (e.g., Pectorals, Triceps, Quadriceps).
* **Instructions:** Step-by-step guidance on how to perform the exercise correctly.

---

## 📦 Installation

1. Clone the repository:

```bash
git clone https://github.com/educapel/fitness-assistant.git
cd fitness-assistant
```

2. Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate  # macOS / Linux
.venv\Scripts\activate     # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ⚡ Usage

1. Load the exercise dataset:

```python
import pandas as pd
from minsearch import Index

df = pd.read_csv("exercises.csv")
```

2. Create a search index:

```python
index = Index(
    text_fields=['exercise_name', 'instructions', 'muscle_groups_activated'],
    keyword_fields=['id', 'type_of_activity', 'type_of_equipment', 'body_part', 'type']
)

documents = df.to_dict(orient="records")
index.add(documents)
```

3. Search exercises:

```python
results = index.search("push-up", filters={"body_part": "Upper Body"})
print(results)
```

---

## 🛠️ Tech Stack

* **Python 3.13**
* **pandas** – data manipulation
* **minsearch** – lightweight search engine for exercises
* **scikit-learn** – text analysis
* **Jupyter / IDE** – development & experimentation

---

## 📖 Ingestion 

## 📖 Evaluation 

For the code for evaluation the system you can check the notebook.ipybn/evaluation



## 📖 Retrieval 

USing minsearch with any boosting gave the following metrics : {'hit_rate': 0.9478260869565217, 'mrr': 0.822744038033893}
## 📖 RAG flow 


## 💡 Contribution

Contributions are welcome!

1. Fork the repo
2. Create a new branch (`git checkout -b feature/my-feature`)
3. Make your changes
4. Commit and push (`git commit -am 'Add new feature'`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 🎨 Badges

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)