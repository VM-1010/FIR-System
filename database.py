"""SQLite database helpers for FIR System.

This module creates and manages a local SQLite database that mirrors the
schema/data from new1.sql (originally MySQL-oriented).
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any, Iterable

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "fir_system.db"


def get_connection() -> sqlite3.Connection:
    """Return a SQLite connection with Row objects and FK checks enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def _schema_script() -> str:
    return """
    CREATE TABLE IF NOT EXISTS user (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        contact_no TEXT,
        address TEXT
    );

    CREATE TABLE IF NOT EXISTS police_station (
        station_id INTEGER PRIMARY KEY AUTOINCREMENT,
        station_name TEXT NOT NULL,
        address TEXT,
        city TEXT,
        district TEXT,
        state TEXT,
        contact_no TEXT
    );

    CREATE TABLE IF NOT EXISTS officer (
        officer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        rank TEXT,
        badge_no TEXT UNIQUE,
        station_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES user(user_id),
        FOREIGN KEY (station_id) REFERENCES police_station(station_id)
    );

    CREATE TABLE IF NOT EXISTS complainant (
        complainant_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        age INTEGER,
        gender TEXT,
        id_proof TEXT,
        FOREIGN KEY (user_id) REFERENCES user(user_id)
    );

    CREATE TABLE IF NOT EXISTS fir (
        fir_id INTEGER PRIMARY KEY AUTOINCREMENT,
        fir_no TEXT UNIQUE,
        date_filed TEXT,
        time_filed TEXT,
        place_of_occurrence TEXT,
        description TEXT,
        status TEXT DEFAULT 'Registered' CHECK (
            status IN ('Registered', 'Under Investigation', 'Pending Review', 'Rejected', 'Closed')
        ),
        complainant_id INTEGER,
        officer_id INTEGER,
        station_id INTEGER,
        FOREIGN KEY (complainant_id) REFERENCES complainant(complainant_id),
        FOREIGN KEY (officer_id) REFERENCES officer(officer_id),
        FOREIGN KEY (station_id) REFERENCES police_station(station_id)
    );

    CREATE TABLE IF NOT EXISTS investigation (
        investigation_id INTEGER PRIMARY KEY AUTOINCREMENT,
        fir_id INTEGER,
        start_date TEXT,
        end_date TEXT,
        investigation_status TEXT,
        remarks TEXT,
        FOREIGN KEY (fir_id) REFERENCES fir(fir_id)
    );

    CREATE TABLE IF NOT EXISTS pass (
        officer_id INTEGER,
        station_id INTEGER,
        password TEXT,
        PRIMARY KEY (officer_id, station_id),
        FOREIGN KEY (officer_id) REFERENCES officer(officer_id),
        FOREIGN KEY (station_id) REFERENCES police_station(station_id)
    );
    """


def _seed_data(conn: sqlite3.Connection) -> None:
    # Skip seeding if data already exists.
    existing = conn.execute("SELECT COUNT(*) AS c FROM police_station").fetchone()["c"]
    if existing:
        return

    conn.executemany(
        """
        INSERT INTO police_station (station_name, address, city, district, state, contact_no)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        [
            ("Central Police Station", "MG Road", "Kochi", "Ernakulam", "Kerala", "9876500001"),
            ("North Station", "North Street", "Kochi", "Ernakulam", "Kerala", "9876500002"),
            ("South Station", "South Avenue", "Kochi", "Ernakulam", "Kerala", "9876500003"),
            ("East Station", "East End", "Thrissur", "Thrissur", "Kerala", "9876500004"),
            ("West Station", "West Market", "Calicut", "Kozhikode", "Kerala", "9876500005"),
            ("Hill Station", "Hill Road", "Idukki", "Idukki", "Kerala", "9876500006"),
            ("City Crime Branch", "City Center", "Kochi", "Ernakulam", "Kerala", "9876500007"),
            ("Traffic Station", "Main Junction", "Kochi", "Ernakulam", "Kerala", "9876500008"),
            ("Cyber Cell", "Tech Park", "Trivandrum", "Trivandrum", "Kerala", "9876500009"),
            ("Rural Station", "Village Road", "Alappuzha", "Alappuzha", "Kerala", "9876500010"),
        ],
    )

    conn.executemany(
        "INSERT INTO user (name, contact_no, address) VALUES (?, ?, ?)",
        [
            ("Rahul Sharma", "9000000001", "Kochi"),
            ("Anita Singh", "9000000002", "Kochi"),
            ("Vikram Das", "9000000003", "Thrissur"),
            ("Arjun Mehta", "9000000004", "Calicut"),
            ("Neha Patel", "9000000005", "Idukki"),
            ("Karan Verma", "9000000006", "Trivandrum"),
            ("Meera Nair", "9000000007", "Alappuzha"),
            ("Rohit Menon", "9000000008", "Kochi"),
            ("Sneha Pillai", "9000000009", "Thrissur"),
            ("Ajay Kumar", "9000000010", "Calicut"),
        ],
    )

    conn.executemany(
        "INSERT INTO officer (user_id, rank, badge_no, station_id) VALUES (?, ?, ?, ?)",
        [
            (1, "Inspector", "INSP1001", 1),
            (2, "Sub Inspector", "SI2002", 1),
            (3, "Head Constable", "HC3003", 2),
            (4, "Inspector", "INSP1004", 3),
            (5, "Sub Inspector", "SI2005", 4),
            (6, "Inspector", "INSP1006", 5),
            (7, "Sub Inspector", "SI2007", 6),
            (8, "Head Constable", "HC3008", 7),
            (9, "Inspector", "INSP1009", 8),
            (10, "Sub Inspector", "SI2010", 9),
        ],
    )

    conn.executemany(
        "INSERT INTO complainant (user_id, age, gender, id_proof) VALUES (?, ?, ?, ?)",
        [
            (1, 34, "Male", "Aadhaar"),
            (2, 29, "Female", "PAN"),
            (3, 42, "Male", "Voter ID"),
            (4, 31, "Male", "Driving License"),
            (5, 27, "Female", "Aadhaar"),
            (6, 38, "Male", "PAN"),
            (7, 25, "Female", "Aadhaar"),
            (8, 45, "Male", "Passport"),
            (9, 30, "Female", "Voter ID"),
            (10, 50, "Male", "Driving License"),
        ],
    )

    conn.executemany(
        """
        INSERT INTO fir
        (fir_no, date_filed, time_filed, place_of_occurrence, description, status, complainant_id, officer_id, station_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            ("FIR001", "2026-03-01", "10:00:00", "MG Road", "Theft complaint", "Registered", 1, 1, 1),
            ("FIR002", "2026-03-02", "11:00:00", "North Street", "Accident case", "Under Investigation", 2, 2, 1),
            ("FIR003", "2026-03-03", "12:00:00", "South Avenue", "Robbery", "Pending Review", 3, 3, 2),
            ("FIR004", "2026-03-04", "13:00:00", "East End", "Cyber fraud", "Registered", 4, 4, 3),
            ("FIR005", "2026-03-05", "14:00:00", "West Market", "Vehicle theft", "Closed", 5, 5, 4),
            ("FIR006", "2026-03-06", "15:00:00", "Hill Road", "Missing person", "Registered", 6, 6, 5),
            ("FIR007", "2026-03-07", "16:00:00", "City Center", "Assault case", "Under Investigation", 7, 7, 6),
            ("FIR008", "2026-03-08", "17:00:00", "Main Junction", "Traffic violation", "Registered", 8, 8, 7),
            ("FIR009", "2026-03-09", "18:00:00", "Tech Park", "Online scam", "Pending Review", 9, 9, 8),
            ("FIR010", "2026-03-10", "19:00:00", "Village Road", "Property dispute", "Registered", 10, 10, 9),
        ],
    )

    conn.executemany(
        """
        INSERT INTO investigation (fir_id, start_date, end_date, investigation_status, remarks)
        VALUES (?, ?, ?, ?, ?)
        """,
        [
            (1, "2026-03-02", None, "Ongoing", "Evidence collection"),
            (2, "2026-03-03", None, "Ongoing", "Witness statements"),
            (3, "2026-03-04", None, "Pending", "Under review"),
            (4, "2026-03-05", None, "Ongoing", "Cyber analysis"),
            (5, "2026-03-06", "2026-03-15", "Completed", "Case closed"),
            (6, "2026-03-07", None, "Ongoing", "Search operation"),
            (7, "2026-03-08", None, "Ongoing", "Medical report awaited"),
            (8, "2026-03-09", None, "Ongoing", "Traffic CCTV review"),
            (9, "2026-03-10", None, "Pending", "Bank details check"),
            (10, "2026-03-11", None, "Ongoing", "Legal consultation"),
        ],
    )

    conn.executemany(
        "INSERT INTO pass (officer_id, station_id, password) VALUES (?, ?, ?)",
        [
            (1, 1, "pass1"),
            (2, 1, "pass2"),
            (3, 2, "pass3"),
            (4, 3, "pass4"),
            (5, 4, "pass5"),
            (6, 5, "pass6"),
            (7, 6, "pass7"),
            (8, 7, "pass8"),
            (9, 8, "pass9"),
            (10, 9, "pass10"),
        ],
    )


def init_db(seed: bool = True) -> None:
    """Create tables and optionally seed default records."""
    with get_connection() as conn:
        conn.executescript(_schema_script())
        if seed:
            _seed_data(conn)
        conn.commit()


def fetch_all(query: str, params: Iterable[Any] = ()) -> list[dict[str, Any]]:
    """Execute SELECT query and return rows as dictionaries."""
    with get_connection() as conn:
        rows = conn.execute(query, tuple(params)).fetchall()
    return [dict(row) for row in rows]


def fetch_one(query: str, params: Iterable[Any] = ()) -> dict[str, Any] | None:
    """Execute SELECT query and return the first row as dictionary."""
    with get_connection() as conn:
        row = conn.execute(query, tuple(params)).fetchone()
    return dict(row) if row else None


def execute(query: str, params: Iterable[Any] = ()) -> int:
    """Execute INSERT/UPDATE/DELETE and return the last inserted row id."""
    with get_connection() as conn:
        cursor = conn.execute(query, tuple(params))
        conn.commit()
        return cursor.lastrowid


def execute_many(query: str, params_list: Iterable[Iterable[Any]]) -> None:
    """Execute INSERT/UPDATE query for many rows."""
    with get_connection() as conn:
        conn.executemany(query, params_list)
        conn.commit()


if __name__ == "__main__":
    init_db(seed=True)
    print(f"SQLite database initialized at: {DB_PATH}")
