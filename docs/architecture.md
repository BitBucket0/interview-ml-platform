# System Architecture

This document describes how the components of the ML platform interact.

---

# Docker Components

Two containers are running:

1. PostgreSQL (`mlflow_db`)
2. MLflow Tracking Server (`mlflow_server`)

Port mappings:

```
MLflow UI:
localhost:5000 → mlflow_server:5000

PostgreSQL:
localhost:5433 → mlflow_db:5432
```

---

# Database Separation Model

PostgreSQL server contains two databases:

```
mlflow_db (Postgres Server)
├── mlflow_database
└── platform_database
```

## mlflow_database

Owned and managed by MLflow.

Stores:

- experiments
- runs
- metrics
- params
- tags
- registered_models
- model_versions
- alembic_version

## platform_database

Owned by this project.

Stores:

- users
- study_events
- labels
- alembic_version (project-specific)

---

# Data Flow

```
platform_database
    ↓
feature engineering
    ↓
model training
    ↓
MLflow logging
    ↓
mlflow_database
```

Application data is separate from experiment tracking metadata.

---

# Connection Contexts

From Mac terminal:

```
Host: localhost
Port: 5433
```

From inside Docker:

```
Host: mlflow_db
Port: 5432
```