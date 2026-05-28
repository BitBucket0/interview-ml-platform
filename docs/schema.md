# Database Schema

Database: platform_database

---

## Table: users

| Column        | Type                       | Nullable | Description |
|---------------|---------------------------|----------|-------------|
| id            | INTEGER                   | No       | Primary key (auto-increment) |
| email         | VARCHAR(255)              | No       | Unique email address |
| display_name  | VARCHAR(255)              | Yes      | Optional display name |
| created_at    | TIMESTAMP WITH TIME ZONE  | No       | Creation timestamp |
| updated_at    | TIMESTAMP WITH TIME ZONE  | No       | Update timestamp |

Example:

| id | email            | display_name | created_at              | updated_at              |
|----|------------------|--------------|-------------------------|-------------------------|
| 1  | alex@example.com | Alex Chen    | 2026-05-26 10:15:00-04  | 2026-05-26 10:15:00-04  |

---

## Table: study_events

| Column         | Type                       | Nullable | Description |
|----------------|---------------------------|----------|-------------|
| id             | INTEGER                   | No       | Primary key (auto-increment) |
| user_id        | INTEGER                   | No       | Foreign key → users.id |
| topic_tag      | VARCHAR(100)              | No       | Topic studied |
| leetcode_id    | INTEGER                   | Yes      | Optional LeetCode ID |
| difficulty     | VARCHAR(20)               | No       | easy / medium / hard |
| minutes_spent  | INTEGER                   | No       | Minutes spent |
| outcome        | VARCHAR(100)              | No       | Result of study |
| ts             | TIMESTAMP WITH TIME ZONE  | No       | Study event timestamp |

Indexes:
- ix_study_events_user_id
- ix_study_events_topic_tag
- ix_study_events_ts

Example:

| id | user_id | topic_tag     | leetcode_id | difficulty | minutes_spent | outcome            | ts                      |
|----|---------|--------------|-------------|------------|--------------|-------------------|-------------------------|
| 1  | 1       | two_pointers | 283         | easy       | 25           | solved_after_hint | 2026-05-26 11:00:00-04  |

---

## Table: labels

| Column          | Type                       | Nullable | Description |
|-----------------|---------------------------|----------|-------------|
| id              | INTEGER                   | No       | Primary key (auto-increment) |
| user_id         | INTEGER                   | No       | Foreign key → users.id |
| next_success_7d | BOOLEAN                   | No       | Target label |
| created_at      | TIMESTAMP WITH TIME ZONE  | No       | Label creation timestamp |

Index:
- ix_labels_user_id

Example:

| id | user_id | next_success_7d | created_at              |
|----|---------|----------------|-------------------------|
| 1  | 1       | true           | 2026-05-26 12:00:00-04  |

---

## Relationships

users.id → study_events.user_id  
users.id → labels.user_id