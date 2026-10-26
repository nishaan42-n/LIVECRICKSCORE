
"""Insert clearly labelled demo records for SQL Analytics testing."""

import os
import sqlite3
from datetime import date, timedelta

from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.getenv("DATABASE_PATH", "cricbuzz.db")


def main():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row

    try:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            country TEXT NOT NULL,
            role TEXT NOT NULL,
            runs INTEGER NOT NULL DEFAULT 0,
            wickets INTEGER NOT NULL DEFAULT 0,
            matches INTEGER NOT NULL DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            team1 TEXT NOT NULL,
            team2 TEXT NOT NULL,
            venue TEXT,
            match_date TEXT,
            winner TEXT,
            victory_margin INTEGER,
            victory_type TEXT
        );

        CREATE TABLE IF NOT EXISTS venues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            city TEXT,
            country TEXT,
            capacity INTEGER
        );

        CREATE TABLE IF NOT EXISTS series (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            host_country TEXT,
            match_type TEXT,
            start_date TEXT,
            planned_matches INTEGER DEFAULT 0
        );
        """)

        # Insert demo rows only when the tables are empty.
        if db.execute("SELECT COUNT(*) FROM players").fetchone()[0] == 0:
            players = [
                ("Demo Player India A", "India", "Batsman", 1250, 2, 30),
                ("Demo Player India B", "India", "Bowler", 180, 65, 25),
                ("Demo Player India C", "India", "All-rounder", 1400, 60, 40),
                ("Demo Player Australia A", "Australia", "Batsman", 980, 0, 28),
                ("Demo Player England A", "England", "Wicket-keeper", 720, 0, 22),
                ("Demo Player South Africa A", "South Africa", "Bowler", 240, 55, 26),
            ]

            db.executemany("""
                INSERT INTO players
                    (name, country, role, runs, wickets, matches)
                VALUES (?, ?, ?, ?, ?, ?)
            """, players)

        if db.execute("SELECT COUNT(*) FROM matches").fetchone()[0] == 0:
            today = date.today()
            matches = []

            for i in range(1, 16):
                match_day = today - timedelta(days=i * 2)
                team1 = "India" if i % 2 else "Australia"
                team2 = "England" if i % 3 else "South Africa"
                winner = team1 if i % 2 else team2

                matches.append((
                    f"DEMO - ODI Match {i}",
                    team1,
                    team2,
                    "Demo Cricket Ground, India",
                    match_day.isoformat(),
                    winner,
                    10 + i,
                    "runs" if i % 2 else "wickets",
                ))

            db.executemany("""
                INSERT INTO matches
                    (description, team1, team2, venue, match_date,
                     winner, victory_margin, victory_type)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, matches)

        if db.execute("SELECT COUNT(*) FROM venues").fetchone()[0] == 0:
            db.executemany("""
                INSERT INTO venues (name, city, country, capacity)
                VALUES (?, ?, ?, ?)
            """, [
                ("Demo National Cricket Ground", "Demo City", "India", 65000),
                ("Demo International Stadium", "Demo City", "Australia", 42000),
            ])

        if db.execute("SELECT COUNT(*) FROM series").fetchone()[0] == 0:
            db.execute("""
                INSERT INTO series
                    (name, host_country, match_type, start_date, planned_matches)
                VALUES (?, ?, ?, ?, ?)
            """, (
                "DEMO - 2024 Cricket Series",
                "India",
                "ODI",
                "2024-06-01",
                5,
            ))

        db.commit()

        print("Demo database records are ready.")
        print("Players:", db.execute("SELECT COUNT(*) FROM players").fetchone()[0])
        print("Matches:", db.execute("SELECT COUNT(*) FROM matches").fetchone()[0])
        print("Venues:", db.execute("SELECT COUNT(*) FROM venues").fetchone()[0])
        print("Series:", db.execute("SELECT COUNT(*) FROM series").fetchone()[0])
        print("These records are demo data, not verified real match statistics.")

    finally:
        db.close()


if __name__ == "__main__":
    main()
