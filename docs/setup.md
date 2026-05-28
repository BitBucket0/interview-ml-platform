# Local Setup Guide

---

# Start Docker Environment

```
docker compose up -d
```

Verify:

```
docker ps
```

Expected containers:

- mlflow_server
- mlflow_db

---

# Connect to PostgreSQL

```
psql -h localhost -p 5433 -U mlflow_user -d platform_database
```

---

# Alembic Commands

Always use:

```
python -m alembic current
python -m alembic history
python -m alembic upgrade head
python -m alembic downgrade -1
```

Do NOT use the global `alembic` command.

---

# Verify Tables

Inside psql:

```
\dt
```

Expected:

- users
- study_events
- labels
- alembic_version