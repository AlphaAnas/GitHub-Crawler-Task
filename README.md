
### 1. Prerequisites

* **Python 3.9+**
* **Docker** (for the database)
* A **GitHub Personal Access Token** (Classic or Fine-grained is fine).

### 2. Setup & Installation

**Clone the repo:**

```bash
git clone https://github.com/AlphaAnas/GitHub-Crawler-Task.git
cd GitHub-Crawler-Task

```

**Create your environment file:**
Create a `.env` file in the root folder and add your credentials. You can copy the structure below:

```ini
# .env
GITHUB_TOKEN=ghp_your_actual_token_here
DB_URL=postgresql://user:password@localhost:5432/github_data

```

**Start the Database:**
We use Docker to spin up Postgres quickly. Run this command in your terminal:

```bash
docker run --name github-crawler-db \
  -e POSTGRES_USER=user \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=github_data \
  -p 5432:5432 \
  -d postgres

```

**Install Dependencies:**

```bash
# Create and activate venv
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install libraries
pip install -r requirements.txt

```

### 3. Running the Crawler

**Step 1: Initialize the Database**
Before crawling, we need to create the tables.

```bash
python main.py --mode=setup

```

**Step 2: Start Crawling**
This will fetch the repositories and save them to your local Postgres container.

```bash
python main.py --mode=crawl

```

### CI/CD Pipeline

This repo includes a **GitHub Actions** workflow (`.github/workflows/pipeline.yml`) that automatically:

1. Spins up a temporary Postgres service.
2. Sets up the schema.
3. Crawls data using the default `GITHUB_TOKEN`.
4. Dumps the results to a CSV artifact.
