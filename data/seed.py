import os
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5433")

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)
print(DATABASE_URL)
TOPICS = [
    "arrays", "two_pointers", "dp",
    "graphs", "sql", "system_design",
    "ml_basics", "trees"
]

DIFFICULTY_DISTRIBUTION = ["easy"] * 5 + ["medium"] * 3 + ["hard"] * 2


def random_outcome(difficulty):
    if difficulty == "easy":
        return random.choices(
            ["solved", "solved_after_hint", "failed"],
            weights=[0.6, 0.3, 0.1]
        )[0]
    elif difficulty == "medium":
        return random.choices(
            ["solved", "solved_after_hint", "failed"],
            weights=[0.4, 0.3, 0.3]
        )[0]
    else:
        return random.choices(
            ["solved", "solved_after_hint", "failed"],
            weights=[0.2, 0.3, 0.5]
        )[0]


def seed_users(conn, num_users=200):
    users = []
    for i in range(num_users):
        users.append({
            "email": f"user{i}@example.com",
            "display_name": f"User {i}"
        })

    conn.execute(
        text("""
        INSERT INTO users (email, display_name)
        VALUES (:email, :display_name)
        ON CONFLICT (email) DO NOTHING
        """),
        users
    )


def seed_study_events(conn, num_users=200):
    events = []
    now = datetime.utcnow()

    for user_id in range(1, num_users + 1):
        num_events = random.randint(50, 100)

        for _ in range(num_events):
            difficulty = random.choice(DIFFICULTY_DISTRIBUTION)

            events.append({
                "user_id": user_id,
                "topic_tag": random.choice(TOPICS),
                "leetcode_id": random.randint(1, 500),
                "difficulty": difficulty,
                "minutes_spent": random.randint(10, 90),
                "outcome": random_outcome(difficulty),
                "ts": now - timedelta(days=random.randint(0, 30))
            })

    conn.execute(
        text("""
        INSERT INTO study_events
        (user_id, topic_tag, leetcode_id, difficulty, minutes_spent, outcome, ts)
        VALUES
        (:user_id, :topic_tag, :leetcode_id, :difficulty,
         :minutes_spent, :outcome, :ts)
        """),
        events
    )

    print(f"Inserted {len(events)} study_events")


def seed_labels(conn, num_users=200):
    labels = []
    query = text("""
        SELECT user_id, COUNT(*) FILTER (WHERE outcome = 'solved')::float / COUNT(*) AS success_rate 
        FROM study_events 
        GROUP BY user_id
    """)
    success_rates = {row.user_id: row.success_rate for row in conn.execute(query)}
    for user_id in range(1, num_users + 1):
        user_rate = success_rates.get(user_id, 0.0)
        is_successful_student = user_rate >= .5
        labels.append({
            "user_id": user_id,
            "next_success_7d": is_successful_student
        })

    conn.execute(
        text("""
        INSERT INTO labels (user_id, next_success_7d)
        VALUES (:user_id, :next_success_7d)
        """),
        labels
    )


def main():
    with engine.begin() as conn:
        conn.execute(text("""
TRUNCATE labels, study_events, users
RESTART IDENTITY CASCADE
"""))
        seed_users(conn)
        seed_study_events(conn)
        seed_labels(conn)

    print("Database seeded successfully.")


if __name__ == "__main__":
    main()