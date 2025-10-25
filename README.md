# 📊 Data Collection System — 4chan & Reddit (Continuous)

Continuously ingests posts from selected **4chan boards** and **Reddit subreddits**, persists them in **PostgreSQL**, and uses **Faktory** for background job processing. Once started, it runs hands-off—collecting data close to when it appears without manual intervention.


## Sources Monitored

### 4chan Boards

| **Board Code** | **Board title**           | **Board description** |
|---|---|---|
| **/pol/** | Politically Incorrect | Discussing and debating politics and current events. |
| **/int/** | International | Exchange of foreign language and culture. |
| **/g/** | Technology | Computer hardware/software, programming, general technology. |
| **/out/** | Outdoors | Survival skills and outdoor activities (e.g., hiking). |
| **/sp/** | Sports | Sports discussion. |

### Reddit Subreddits

| **Subreddit** | **Description** |
|---|---|
| **r/geopolitics** | Global political events, trends, analysis. |
| **r/Outdoors** | Experiences, tips, and discussions about outdoor activities. |
| **r/technology** | News and insights on the latest in technology. |
| **r/AutoGPT** | Discussions around AutoGPT and task automation. |
| **r/ArtificialInteligence** | Advancements and news in AI/ML. |
| **r/sports** | General sports news, discussion, and fan content. |

## 🚀 Features
- Continuous ingestion via long-running Faktory workers  
- 4chan + Reddit collectors with configurable sources  
- PostgreSQL persistence (SQL migrations included)  
- 12-factor style config via `.env`  
- Reproducible Python env with `uv` + `pyproject.toml`  
- Linting with `ruff`


## 📂 Repository Layout

    4chan_crawler/
        │── constants/
        │── modal/
        │── utils/
        │── board_crawler.py
        │── thread_crawler.py
        │── chan_client.py
        │── cold_start_crawler.py
        │── crawler.py
        │── migrations/
        │── logs/
    reddit_crawler/
        │── constants/
        │── modal/
        │── utils/
        │── posts_crawler.py
        │── subreddit_crawler.py
        │── reddit_client.py
        │── cold_start_crawler.py
        │── crawler.py
        │── migrations/
        │── logs/
    pyproject.toml
    .python-version
    uv.lock
    README.md

> - The `migrations/` folders contain SQL files for creating/updating tables. 
> - `logs/` holds runtime logs for each crawler.

## ®️ Prerequisites
- Python **3.13+**
- uv
- Rust, SQLX (to run migrations)
- PostgreSQL/ Timescale-db (or compatible)
- Docker (for **Faktory** and Timescale-db)

## Installing Postgres (Timescale db) install with docker

```bash
# grab the latest timescaledb image
> docker pull timescale/timescaledb-ha:pg17

# create a persistent volume
> docker volume create timescaledb-data

# start up timescaledb in detached mode with the persistent volume
> docker run -d --name timescaledb -p 5432:5432 -e POSTGRES_PASSWORD=password -v timescaledb-data:/var/lib/postgresql/data timescale/timescaledb-ha:pg17

# connect to the server with a psql shell
> docker exec -it timescaledb psql -d "postgres://postgres:password@localhost/postgres"
```

### Postgres Commands

```bash
# List all database
> postgre \l or \list

# Connect to database or use database
> postgre \c <database_name>

# List all the tables
> postgre \dt
```

# sqlx migrations

Create a `.env` file.

We will use this to store various environment variables and secrets that will be treated as if they came in as environment variables in our program.

In your `.env` file, add the line: `DATABASE_URL=postgres://postgres:password@localhost:5432/chan_crawler`

Then run

```bash
# make sure we have created our databse
> sqlx database create

> sqlx database drop

> sqlx migrate add -r --source /path/you/want/migrations "some descriptive name"

# run migrations
> sqlx migrate run 

# revert migrations
> sqlx migrate revert
```

# Installing Faktory  install with docker

```bash
> docker pull contribsys/faktory

> docker volume create faktory-data

> docker run -d -it --name faktory \
  -v faktory-data:/var/lib/faktory/db \
  -e "FAKTORY_PASSWORD=password" \
  -p 127.0.0.1:7419:7419 \
  -p 127.0.0.1:7420:7420 \
  contribsys/faktory \
  /faktory -b :7419 -w :7420
```

Go to [http://localhost:7420] in your browser.

## 📚 Python Dependenices

- psycopg2: PostgreSQL database adapter for Python.
- pyfaktory: Client for interacting with the Faktory job queue.
- python-dotenv: Loads environment variables from .env files.
- requests: Simple HTTP library for making requests.
- ruff: Fast, linting tool for Python code.
- dotenv: Manages environment variables in Python applications.

## 🛠️ Tools 
1. **UV**:
    - command-line tool used to simplify the development workflow in Python projects, offering commands for project setup, virtual environments, and syncing dependencies.
        - **uv init**: Initializes a new Python project, setting up required files and configurations.
        - **uv venv**: Creates and manages a virtual environment for the project to isolate dependencies
        - **uv add**: Installs and adds specified dependencies to the project.
        - **uv sync**: Synchronizes project dependencies and ensures everything is up to date.
        ### lint & format
        - **uv run ruff check** : Runs ruff to check Python code for linting issues in the current directory.
        - **uv run ruff format** : Uses ruff to automatically format Python code in the current directory.

2. **Faktory** 
    - Faktory is a background job processing system that allows scheduling and managing queues of tasks across multiple workers. It helps in efficiently handling long-running jobs with support for retries, priorities, and fault tolerance.

3. **Docker** 
    - Docker is a platform for developing, shipping, and running applications in lightweight, portable containers, while TimescaleDB is a time-series database built on PostgreSQL, designed for handling large volumes of time-stamped data efficiently.
    ```bash
    **DOCKER**
      # 1. Status of Docker
         > systemctl status docker

      # 2. List all Docker Containers running
         > docker ps

      # 3. Stop the Docker
         > docker stop <container_id>

      # 4. Removed the container
         > docker rm <container_id>

      # 5. Docker restart
         > docker restart <container_id>
    ```

## 🏃‍♂️ Running the Crawlers

### 4Chan_crawler
```bash
# 1. Start Faktory for updating new boards
> python3 4chan_crawler/cold_start_crawler.py --update-new-boards
   - Example: python3 4chan_crawler/cold_start_crawler.py --update-new-boards
> python3 4chan_crawler/crawler.py --update-new-boards   

# 2. Start Faktory for collecting posts from a single board
> python3 4chan_crawler/cold_start_crawler.py --collect-posts *<board_1>* 
   - Example: python3 4chan_crawler/cold_start_crawler.py --collect-posts "pol" 
> python3 4chan_crawler/crawler.py --collect-posts *<board_1>*
   - Example: python3 4chan_crawler/crawler.py --collect-posts "pol" 

# 3. Start Faktory for multiple Subreddit
> python3 4chan_crawler/cold_start_crawler.py --collect-posts *<board_1>* *<board_2>*
   - Example: python3 4chan_crawler/cold_start_crawler.py --collect-posts "pol" "int" "g" "out" "sp" 
> python3 4chan_crawler/crawler.py --collect-posts *<board_1>* *<board_2>*
   - Example: python3 4chan_crawler/crawler.py --collect-posts "pol" "int" "g" "out" "sp" 

# 4. Show help
> python3 4chan_crawler/cold_start_crawler.py --help   
> python3 4chan_crawler/crawler.py --help   
```
## Reddit crawler
```bash
# 1. Start Faktory for updating new Subreddit
> python3 reddit_crawler/cold_start_crawler.py *--update-new-subreddit*
   - Example: python3 reddit_crawler/cold_start_crawler.py --update-new-subreddit
> python3 reddit_crawler/crawler.py *--update-new-boards*   
   - Example: python3 reddit_crawler/crawler.py --update-new-subreddit

#2. Start Faktory for collecting posts from a single subreddit
> python3 reddit_crawler/cold_start_crawler.py --collect-posts *<subredit_name2>*
> python3 reddit_crawler/crawler.py --collect-posts "Technology"

#3. Start Faktory for collecting post from multiple Subreddit
> python3 reddit_crawler/cold_start_crawler.py --collect-posts *<subredit_name1>* *<subredit_name2>*
   - Example: python3 reddit_crawler/cold_start_crawler.py --collect-posts "Technology" "geopolitics" "Outdoors"
> python3 reddit_crawler/crawler.py --collect-posts *<subredit_name1>* *<subredit_name2>*
   - Example: python3 reddit_crawler/crawler.py --collect-posts "geopolitics" "technology" "AutoGPT" "sports" "ArtificialInteligence"

#4. Start Faktory for collecting comments from multiple Subreddit
> python3 reddit_crawler/cold_start_crawler.py --collect-comments *<subredit_name1>* *<subredit_name2>*
   - Example: python3 reddit_crawler/cold_start_crawler.py --collect-posts "Technology" "geopolitics" "Outdoors"
> python3 reddit_crawler/crawler.py --collect-comments *<subredit_name1>* *<subredit_name2>*
   - Example: python3 reddit_crawler/crawler.py --collect-posts "geopolitics" "technology" "AutoGPT" "sports" "ArtificialInteligence"

#4. Show help
> python3 reddit_crawler/cold_start_crawler.py --help   
> python3 reddit_crawler/crawler.py --help  
``` 

## 👋 Data & Ethics
- Respect each platform’s Terms of Service and robots policies.
- Avoid storing sensitive personal data.
- Be transparent about retention and usage in downstream systems.