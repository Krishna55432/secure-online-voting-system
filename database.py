import sqlite3
import csv

def init_db():
    conn = sqlite3.connect("votes.db")
    cursor = conn.cursor()

    # Voters table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS voters(
        voter_id TEXT PRIMARY KEY,
        name TEXT,
        password TEXT,
        voted INTEGER
    )
    """)

    # Results table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS results(
        candidate TEXT PRIMARY KEY,
        votes INTEGER
    )
    """)

    # Load voters from CSV
    with open("electoral_roll_1000.csv", "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            voter_id = row["voter_id"]
            name = row["name"]

            last_digits = voter_id[-3:]
            first_letters = name[:3].lower()

            password = last_digits + first_letters

            cursor.execute(
                "INSERT OR IGNORE INTO voters VALUES (?, ?, ?, 0)",
                (voter_id, name, password)
            )

    # 🔥 4 Candidates
    candidates = ["Vijay", "Stalin", "Annamalai", "EPS"]

    for c in candidates:
        cursor.execute("INSERT OR IGNORE INTO results VALUES (?, 0)", (c,))

    conn.commit()
    conn.close()