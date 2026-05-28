# Interview ML Platform

This project is a hands-on machine learning platform engineering side project.

The goal is to build a realistic local ML system using:

- Docker
- PostgreSQL
- MLflow
- Alembic migrations
- Structured application data
- Feature engineering
- Model training
- Experiment tracking

---

# System Overview

The system consists of:

- PostgreSQL (Docker container)
- MLflow Tracking Server (Docker container)
- Application database (`platform_database`)
- MLflow tracking database (`mlflow_database`)

The two databases are intentionally separated to prevent migration conflicts and maintain clean ownership boundaries.

---

# Databases

PostgreSQL container:

```
mlflow_db
├── mlflow_database      (MLflow internal tracking)
└── platform_database    (Application data)
```

MLflow stores experiment metadata in `mlflow_database`.

Application data and training data are stored in `platform_database`.

---

# Documentation

See the `docs/` directory:

- `docs/architecture.md` → System design and component relationships
- `docs/schema.md` → Application database schema definition
- `docs/setup.md` → Local setup and commands

---

# Current Status

- Docker environment configured
- PostgreSQL running
- MLflow running
- Alembic migrations configured
- Core application tables created:
  - users
  - study_events
  - labels

---

# Next Steps

- Insert seed data
- Build feature engineering pipeline
- Train baseline model
- Log experiments to MLflow
- Add model serving layer
