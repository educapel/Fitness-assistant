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

## 📑 Table of Contents
- [Features](#-features)
- [Dataset](#-dataset)
- [Installation](#-installation)
- [Usage](#-usage)
- [Tech Stack](#-tech-stack)
- [Data Ingestion](#-data-ingestion)
- [Evaluation](#-evaluation)
- [Retrieval](#-retrieval)
- [RAG Flow](#-rag-flow)
- [Preparation](#preparation)
  - [API Key Setup](#api-key-setup)
  - [Dependencies](#dependencies)
- [Running the Application](#running-the-application)
  - [Database Configuration](#database-configuration)
  - [Running with Docker-Compose](#running-with-docker-compose)
  - [Running Locally](#running-locally)
  - [Running with Docker (without compose)](#running-with-docker-without-compose)
  - [Time Configuration](#time-configuration)
- [Using the Application](#using-the-application)
  - [CLI](#cli)
  - [Using Requests](#using-requests)
  - [CURL](#curl)
  - [Sending Feedback](#sending-feedback)
- [Code Structure](#code-structure)
- [API Endpoints](#api-endpoints)
- [Environment Variables](#environment-variables)
- [Requirements](#requirements)
- [Getting Started](#getting-started)
- [Monitoring](#monitoring)
- [License](#-license)

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
* **Flask** – web framework for API
* **PostgreSQL** – database for logging and analytics
* **Grafana** – monitoring and visualization
* **DeepSeek API** (via OpenRouter) – AI-powered responses
* **Docker** – containerization and deployment

---

## 📖 Data Ingestion

The system ingests exercise data from CSV files and creates searchable indexes using the minsearch library. The ingestion process includes:

- Loading exercise data from `exercises.csv`
- Creating text and keyword field mappings
- Building searchable indexes for fast retrieval
- Storing processed data for RAG operations

---

## 📖 Evaluation

For the code for evaluation the system, you can check the `notebooks/evaluation.ipynb`. The evaluation process includes:

- **Ground Truth Dataset:** Manually curated question-answer pairs
- **Retrieval Quality:** Measuring hit rate and MRR (Mean Reciprocal Rank)
- **Response Quality:** Evaluating AI-generated answers
- **Performance Metrics:** Response times and system throughput

---

## 📖 Retrieval

Using minsearch with optimized boosting parameters achieved the following metrics:
- **Hit Rate:** 94.78% (0.9478260869565217)
- **MRR (Mean Reciprocal Rank):** 82.27% (0.822744038033893)

The retrieval system uses a combination of text search and keyword filtering to find the most relevant exercises based on user queries.

---

## 📖 RAG Flow

The Retrieval-Augmented Generation (RAG) flow consists of:

1. **Query Processing:** User question is analyzed and processed
2. **Document Retrieval:** Relevant exercises are retrieved using minsearch
3. **Context Building:** Retrieved documents are formatted into context
4. **AI Generation:** DeepSeek API generates responses based on context
5. **Response Formatting:** Final answer is structured and returned

---

## Preparation

### API Key Setup

Since we use DeepSeek API through OpenRouter, you need to provide the API key.  
You can get a free DeepSeek API key from [OpenRouter](https://openrouter.ai/) by creating an account.

Set your OpenRouter API key as an environment variable:

```bash
export OPENROUTER_API_KEY=your_openrouter_api_key_here
```

Or create a `.env` file in your project root with:

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

### Dependencies

Install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

---

## Running the Application

### Database Configuration

Before the application starts for the first time, the database needs to be initialized.

1. Run postgres:
   ```bash
   docker-compose up postgres
   ```

2. Then run the `db_prep.py` script:
   ```bash
   cd fitness_assistant
   export POSTGRES_HOST=localhost
   python db_prep.py
   ```

3. Check the content of the database with `pgcli`:
   ```bash
   pgcli -h localhost -U your_username -d course_assistant -W
   ```

4. View schema:
   ```sql
   \d conversations;
   ```

5. Inspect records:
   ```sql
   select * from conversations;
   ```

### Running with Docker-Compose

The easiest way to run the application:

```bash
docker-compose up
```

App will be available at `http://localhost:8000`.

### Running Locally

1. Start only postgres and grafana:
   ```bash
   docker-compose up postgres grafana
   ```

2. If you previously started everything with `docker-compose up`, stop the app:
   ```bash
   docker-compose stop app
   ```

3. Run app locally:
   ```bash
   cd fitness_assistant
   export POSTGRES_HOST=localhost
   python app.py
   ```

### Running with Docker (without compose)

For debugging, you may run the app in Docker directly.

1. Build image:
   ```bash
   docker build -t fitness-assistant .
   ```

2. Run it:
   ```bash
   docker run -it --rm \
        --network="fitness-assistant_default" \
        --env-file=".env" \
        -e OPENROUTER_API_KEY=${OPENROUTER_API_KEY} \
        -e DATA_PATH="data/data.csv" \
        -p 8000:8000 \
        fitness-assistant
   ```

### Time Configuration

When inserting logs into the database, ensure timestamps are correct.

Sample log output:

```
Database timezone: Etc/UTC
Database current time (UTC): 2025-09-17 23:43:12.169624+00:00
Database current time (Europe/London): 2025-09-18 00:43:12.169624+01:00
Python current time: 2025-09-18 00:43:12.170246+01:00
Inserted time (UTC): 2025-09-17 23:43:12.170246+00:00
Inserted time (Europe/London): 2025-09-18 00:43:12.170246+01:00
Selected time (UTC): 2025-09-17 23:43:12.170246+00:00
Selected time (Europe/London): 2025-09-18 00:43:12.170246+01:00
```

Set timezone in `.env` with:

```env
TZ=UTC
```

### WSL Clock Sync Issue

In WSL, Docker clock may get out of sync. Check with:

```bash
docker run ubuntu date
```

If incorrect, sync clock:

```bash
wsl
sudo apt install ntpdate
sudo ntpdate time.windows.com
```

---

## Using the Application

### CLI

Start CLI:

```bash
python cli.py
```

Run with random question:

```bash
python cli.py --random
```

### Using Requests

Test using script:

```bash
python test.py
```

### CURL

Example query:

```bash
URL=http://localhost:8000
QUESTION="Is the Lat Pulldown considered a strength training activity, and if so, why?"
DATA='{
    "question": "'${QUESTION}'"
}'

curl -X POST \
    -H "Content-Type: application/json" \
    -d "${DATA}" \
    ${URL}/question
```

Response:

```json
{
    "answer": "Yes, the Lat Pulldown is considered a strength training activity...",
    "conversation_id": "4e1cef04-bfd9-4a2c-9cdd-2771d8f70e4d",
    "question": "Is the Lat Pulldown considered a strength training activity, and if so, why?"
}
```

### Sending Feedback

```bash
ID="4e1cef04-bfd9-4a2c-9cdd-2771d8f70e4d"
URL=http://localhost:8000
FEEDBACK_DATA='{
    "conversation_id": "'${ID}'",
    "feedback": 1
}'

curl -X POST \
    -H "Content-Type: application/json" \
    -d "${FEEDBACK_DATA}" \
    ${URL}/feedback
```

Response:

```json
{
    "message": "Feedback received for conversation 4e1cef04-bfd9-4a2c-9cdd-2771d8f70e4d: 1"
}
```

---

## Code Structure

**fitness_assistant/**
- `app.py` – Flask API entrypoint
- `rag.py` – RAG logic for retrieval and prompting
- `ingest.py` – load knowledge base
- `minsearch.py` – in-memory search engine
- `db.py` – Postgres logging logic
- `db_prep.py` – initialize database

**notebooks/**
- `evaluation.ipynb` – system evaluation and metrics

**Root directory**
- `test.py` – random question tester
- `cli.py` – interactive CLI
- `exercises.csv` – exercise dataset
- `docker-compose.yml` – Docker services configuration

---

## API Endpoints

### POST /question

**Request:**
```json
{
    "question": "Your fitness question here"
}
```

**Response:**
```json
{
    "answer": "AI-generated answer",
    "conversation_id": "unique-conversation-id",
    "question": "Your original question"
}
```

### POST /feedback

**Request:**
```json
{
    "conversation_id": "conversation-id-from-question-response",
    "feedback": 1
}
```

**Response:**
```json
{
    "message": "Feedback received for conversation {conversation_id}: {feedback}"
}
```

---

## Environment Variables

`.env` file:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
POSTGRES_HOST=postgres
POSTGRES_DB=course_assistant
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
TZ=UTC
DATA_PATH=data/data.csv
```

---

## Requirements

`requirements.txt`:

```txt
flask
requests
pandas
scikit-learn
psycopg2-binary
questionary
python-dotenv
```

---

## Getting Started

1. Clone repo:
   ```bash
   git clone https://github.com/educapel/fitness-assistant.git
   cd fitness-assistant
   ```

2. Set OpenRouter API key (`.env` or export variable)

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run with Docker Compose:
   ```bash
   docker-compose up
   ```

5. Access app at `http://localhost:8000`

---

## Monitoring

- **Grafana** is included for monitoring
- When running with Docker Compose, Grafana will be available for metrics and logs
- Monitor system performance, response times, and user interactions
- Track retrieval quality and AI response effectiveness

---

## 📄 License

This project is licensed under the MIT License.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 🎨 Badges

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)