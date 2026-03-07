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
        station_id TEXT PRIMARY KEY,
        station_name TEXT NOT NULL,
        address TEXT,
        city TEXT,
        district TEXT,
        state TEXT,
        contact_no TEXT
    );

    CREATE TABLE IF NOT EXISTS officer (
        officer_id TEXT PRIMARY KEY,
        user_id INTEGER NOT NULL,
        rank TEXT NOT NULL,
        badge_no TEXT UNIQUE NOT NULL,
        station_id TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'officer' CHECK (role IN ('admin', 'officer')),
        FOREIGN KEY (user_id) REFERENCES user(user_id),
        FOREIGN KEY (station_id) REFERENCES police_station(station_id)
    );

    CREATE TABLE IF NOT EXISTS complainant (
        complainant_id TEXT PRIMARY KEY,
        user_id INTEGER NOT NULL,
        age INTEGER,
        gender TEXT,
        id_proof TEXT,
        FOREIGN KEY (user_id) REFERENCES user(user_id)
    );

    CREATE TABLE IF NOT EXISTS fir (
        fir_id TEXT PRIMARY KEY,
        fir_no TEXT UNIQUE NOT NULL,
        date_filed TEXT NOT NULL,
        time_filed TEXT NOT NULL,
        place_of_occurrence TEXT NOT NULL,
        description TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Registered' CHECK (
            status IN ('Registered', 'Under Investigation', 'Pending Review', 'Rejected', 'Closed')
        ),
        complainant_id TEXT NOT NULL,
        officer_id TEXT NOT NULL,
        station_id TEXT NOT NULL,
        FOREIGN KEY (complainant_id) REFERENCES complainant(complainant_id),
        FOREIGN KEY (officer_id) REFERENCES officer(officer_id),
        FOREIGN KEY (station_id) REFERENCES police_station(station_id)
    );

    CREATE TABLE IF NOT EXISTS pass (
        officer_id TEXT NOT NULL,
        station_id TEXT NOT NULL,
        password TEXT NOT NULL,
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
        INSERT INTO police_station (station_id, station_name, address, city, district, state, contact_no)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        [
            ("ST01", "Central Police Station", "MG Road", "Kochi", "Ernakulam", "Kerala", "9876500001"),
            ("ST02", "North Station", "North Street", "Kochi", "Ernakulam", "Kerala", "9876500002"),
            ("ST03", "South Station", "South Avenue", "Kochi", "Ernakulam", "Kerala", "9876500003"),
            ("ST04", "East Station", "East End", "Thrissur", "Thrissur", "Kerala", "9876500004"),
            ("ST05", "West Station", "West Market", "Calicut", "Kozhikode", "Kerala", "9876500005"),
            ("ST06", "Hill Station", "Hill Road", "Idukki", "Idukki", "Kerala", "9876500006"),
            ("ST07", "City Crime Branch", "City Center", "Kochi", "Ernakulam", "Kerala", "9876500007"),
            ("ST08", "Traffic Station", "Main Junction", "Kochi", "Ernakulam", "Kerala", "9876500008"),
            ("ST09", "Cyber Cell", "Tech Park", "Trivandrum", "Trivandrum", "Kerala", "9876500009"),
            ("ST10", "Rural Station", "Village Road", "Alappuzha", "Alappuzha", "Kerala", "9876500010"),
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
        "INSERT INTO officer (officer_id, user_id, rank, badge_no, station_id, role) VALUES (?, ?, ?, ?, ?, ?)",
        [
            ("OF01", 1, "Inspector", "INSP1001", "ST01", "admin"),
            ("OF02", 2, "Sub Inspector", "SI2002", "ST01", "officer"),
            ("OF03", 3, "Head Constable", "HC3003", "ST02", "officer"),
            ("OF04", 4, "Inspector", "INSP1004", "ST03", "officer"),
            ("OF05", 5, "Sub Inspector", "SI2005", "ST04", "officer"),
            ("OF06", 6, "Inspector", "INSP1006", "ST05", "officer"),
            ("OF07", 7, "Sub Inspector", "SI2007", "ST06", "officer"),
            ("OF08", 8, "Head Constable", "HC3008", "ST07", "officer"),
            ("OF09", 9, "Inspector", "INSP1009", "ST08", "officer"),
            ("OF10", 10, "Sub Inspector", "SI2010", "ST09", "officer"),
        ],
    )

    conn.executemany(
        "INSERT INTO complainant (complainant_id, user_id, age, gender, id_proof) VALUES (?, ?, ?, ?, ?)",
        [
            ("C01", 1, 34, "Male", "Aadhaar"),
            ("C02", 2, 29, "Female", "PAN"),
            ("C03", 3, 42, "Male", "Voter ID"),
            ("C04", 4, 31, "Male", "Driving License"),
            ("C05", 5, 27, "Female", "Aadhaar"),
            ("C06", 6, 38, "Male", "PAN"),
            ("C07", 7, 25, "Female", "Aadhaar"),
            ("C08", 8, 45, "Male", "Passport"),
            ("C09", 9, 30, "Female", "Voter ID"),
            ("C10", 10, 50, "Male", "Driving License"),
        ],
    )

    conn.executemany(
        """
        INSERT INTO fir
        (fir_id, fir_no, date_filed, time_filed, place_of_occurrence, description, status, complainant_id, officer_id, station_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            ("F01", "FIR001", "2026-03-01", "10:00:00", "MG Road", "Theft complaint", "Registered", "C01", "OF01", "ST01"),
            ("F02", "FIR002", "2026-03-02", "11:00:00", "North Street", "Accident case", "Under Investigation", "C02", "OF02", "ST01"),
            ("F03", "FIR003", "2026-03-03", "12:00:00", "South Avenue", "Robbery", "Pending Review", "C03", "OF03", "ST02"),
            ("F04", "FIR004", "2026-03-04", "13:00:00", "East End", "Cyber fraud", "Registered", "C04", "OF04", "ST03"),
            ("F05", "FIR005", "2026-03-05", "14:00:00", "West Market", "Vehicle theft", "Closed", "C05", "OF05", "ST04"),
            ("F06", "FIR006", "2026-03-06", "15:00:00", "Hill Road", "Missing person", "Registered", "C06", "OF06", "ST05"),
            ("F07", "FIR007", "2026-03-07", "16:00:00", "City Center", "Assault case", "Under Investigation", "C07", "OF07", "ST06"),
            ("F08", "FIR008", "2026-03-08", "17:00:00", "Main Junction", "Traffic violation", "Registered", "C08", "OF08", "ST07"),
            ("F09", "FIR009", "2026-03-09", "18:00:00", "Tech Park", "Online scam", "Pending Review", "C09", "OF09", "ST08"),
            ("F10", "FIR010", "2026-03-10", "19:00:00", "Village Road", "Property dispute", "Registered", "C10", "OF10", "ST09"),
        ],
    )

    conn.executemany(
        "INSERT INTO pass (officer_id, station_id, password) VALUES (?, ?, ?)",
        [
            ("OF01", "ST01", "pass1"),
            ("OF02", "ST01", "pass2"),
            ("OF03", "ST02", "pass3"),
            ("OF04", "ST03", "pass4"),
            ("OF05", "ST04", "pass5"),
            ("OF06", "ST05", "pass6"),
            ("OF07", "ST06", "pass7"),
            ("OF08", "ST07", "pass8"),
            ("OF09", "ST08", "pass9"),
            ("OF10", "ST09", "pass10"),
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
