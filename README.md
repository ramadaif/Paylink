# PayLink

PayLink is a bill-payment and wallet backend: customers pay utility bills (electricity, water, mobile top-up, internet) from a digital wallet. This repository is the Year Work Project.

**Status:** Phase 1 (requirements, design, DevOps foundation). The app is an empty skeleton with a health endpoint.

## Tech stack

- Backend: Python, FastAPI
- Database: PostgreSQL 16
- Containers: Docker and Docker Compose
- CI: GitHub Actions (build, lint with ruff, test with pytest, build Docker image)

## Run it

You need Docker Desktop installed and running.

```
git clone https://github.com/ramadaif/Paylink.git
cd Paylink
docker compose up --build
```

Then open http://localhost:8000/health. You should see:

```
{"status":"ok"}
```

Stop everything with `Ctrl+C`, then `docker compose down`.

## Run lint and tests without Docker

```
pip install -r requirements.txt
ruff check .
pytest
```

## Project structure

```
app/                  Application code (FastAPI)
tests/                Automated tests
docs/requirements.md  Requirements pack
docs/design/          Diagram sources (PlantUML or Mermaid)
docs/prompt-log.md    Log of AI prompts and verdicts
Dockerfile            Builds the app image
docker-compose.yml    Starts the app and the database
.github/workflows/    CI pipeline
```

## Team workflow

- `main` is protected: all changes go through a pull request.
- Another teammate reviews every pull request before it is merged.
- When AI wrote more than half of a change, the AI tool is named in the commit message.
