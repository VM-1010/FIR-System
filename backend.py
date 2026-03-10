'''
INTERACTIONS BETWEEN app.py (Flask) AND backend.py
==================================================

This document summarizes how the Flask application (app.py) interacts with the backend logic (backend.py):

1. Authentication & Session Management
-------------------------------------
- `validate_officer_tuple(officerid, stationid, password)`
    Called during login to check officer credentials.
- `get_role(officerid, stationid)`
    Fetches the role (admin/officer) for session management.

2. Officer Management
---------------------
- `add_officer(officerdata)`
    Called by admin to add a new officer. Receives a dict with officer details.
- `remove_officer(officerid, stationid)`
    Removes an officer from the system.
- `get_officers(stationid)`
    Returns a list of officers for a given station (for admin views).

3. FIR Management
-----------------
- `create_fir(fir_data)`
    Registers a new FIR. Receives a dict with FIR details.
- `get_all_firs(stationId=None)`
    Returns all FIRs (optionally filtered by station).
- `get_fir_by_id(fir_id)`
    Returns details for a specific FIR.
- `update_fir(fir_id, fir_data)`
    Updates an existing FIR with new data.
- `set_fir_status(fir_id, status)`
    Changes the status of a FIR (e.g., closed).

4. Complainant Management
------------------------
- `add_complainant(complainant_data)`
    Registers a new complainant. Receives a dict with complainant details.
- `get_complainant_by_id(complainant_id)`
    Returns details for a specific complainant.

5. Profile & Miscellaneous
--------------------------
- `get_officer_by_id(officerid, stationid)`
    Returns officer profile details for the profile page.

All data passed from app.py to backend.py is either a primitive (id, status) or a dictionary (for creation/update). All data returned to app.py is a dictionary or list of dictionaries, suitable for Jinja2 rendering in templates.
'''

from werkzeug.security import generate_password_hash, check_password_hash
import database
import re
from datetime import datetime
# use this when querying : cursor = conn.cursor(dictionary=True), the query should return listof dictionaries instead of tuples, so we can access values by column names instead of index

def validate_officer_tuple(officer_id, station_id, password):
    row = database.fetch_one(
        """
        SELECT *
        FROM pass
        WHERE officer_id=? AND station_id=? AND password=?
        """,
        (officer_id, station_id, password)
    )
    return row is not None

def get_role(officer_id, station_id):
    row = database.fetch_one(
        """
        SELECT role
        FROM officer
        WHERE officer_id=? AND station_id=?
        """,
        (officer_id, station_id)
    )
    return row["role"] if row else "officer"

# generate officer_id by fetching the last officer_id for a station from database table and incrementing it by 1, format should be OFF001, OFF002 etc

def add_officer(officerdata):
    try:
        conn = database.get_connection()
        cursor = conn.cursor()
        try:
            # 1) Create user row
            cursor.execute(
                """
                INSERT INTO user (name, contact_no, address)
                VALUES (?, ?, ?)
                """,
                (
                    officerdata.get("name"),
                    officerdata.get("contact_no"),
                    officerdata.get("address"),
                ),
            )
            user_id = cursor.lastrowid

            # 2) Generate next officer_id in OF001 format
            rows = cursor.execute("SELECT officer_id FROM officer").fetchall()
            max_num = 0
            for row in rows:
                oid = str(row["officer_id"] if "officer_id" in row.keys() else "")
                m = re.search(r"(\d+)$", oid)
                if m:
                    max_num = max(max_num, int(m.group(1)))
            next_num = max_num + 1
            officer_id = f"OF{next_num:03d}"

            # 3) Insert officer
            cursor.execute(
                """
                INSERT INTO officer (officer_id, user_id, rank, badge_no, station_id, role)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    officer_id,
                    user_id,
                    officerdata.get("rank"),
                    officerdata.get("badge_no"),
                    officerdata.get("station_id"),
                    officerdata.get("role", "officer"),
                ),
            )

            # 4) Insert password in pass table
            cursor.execute(
                """
                INSERT INTO pass (officer_id, station_id, password)
                VALUES (?, ?, ?)
                """,
                (
                    officer_id,
                    officerdata.get("station_id"),
                    officerdata.get("password"),
                ),
            )
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
        return True
    except Exception:
        return False

def remove_officer(officerid, stationid):
    try:
        row = database.fetch_one(
            """
            SELECT officer_id
            FROM officer
            WHERE officer_id=? AND station_id=?
            """,
            (officerid, stationid),
        )
        if not row:
            return False

        database.execute(
            "DELETE FROM pass WHERE officer_id=? AND station_id=?",
            (officerid, stationid),
        )
        database.execute(
            "DELETE FROM officer WHERE officer_id=? AND station_id=?",
            (officerid, stationid),
        )
        return True
    except Exception:
        return False

# generate fir_id by fetching the last fir_id from database table and incrementing it by 1, format should be FIR001, FIR002 etc

def create_fir(fir_data):
    try:
        # Generate next FIR id/no in FIR001 format
        rows = database.fetch_all("SELECT fir_id, fir_no FROM fir")
        max_num = 0
        for row in rows:
            for key in ("fir_id", "fir_no"):
                raw = str(row.get(key, ""))
                m = re.search(r"(\d+)$", raw)
                if m:
                    max_num = max(max_num, int(m.group(1)))
        next_num = max_num + 1
        fir_id = f"FIR{next_num:03d}"
        fir_no = f"FIR{next_num:03d}"

        now = datetime.now()
        date_filed = fir_data.get("date_filed") or now.strftime("%Y-%m-%d")
        time_filed = fir_data.get("time_filed") or now.strftime("%H:%M:%S")

        database.execute(
            """
            INSERT INTO fir (
                fir_id, fir_no, date_filed, time_filed, place_of_occurrence,
                description, status, complainant_id, officer_id, station_id
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                fir_id,
                fir_data.get("fir_no") or fir_no,
                date_filed,
                time_filed,
                fir_data.get("place_of_occurrence") or fir_data.get("location"),
                fir_data.get("description"),
                fir_data.get("status") or "Registered",
                fir_data.get("complainant_id"),
                fir_data.get("officer_id"),
                fir_data.get("station_id"),
            ),
        )
        return fir_id
    except Exception:
        return None

def get_officers(stationid):
    return database.fetch_all(
        """
        SELECT o.officer_id, u.name, o.rank, o.badge_no
        FROM officer o
        JOIN user u ON u.user_id = o.user_id
        WHERE o.station_id=?
        ORDER BY o.officer_id
        """,
        (stationid,),
    )

def get_all_firs(stationId):
    # return list of all FIRs for a station or all FIRs if stationId is None
    if stationId:
        return database.fetch_all(
            """
            SELECT fir_id, fir_no, date_filed, time_filed, place_of_occurrence, description, status,
                   complainant_id, officer_id, station_id
            FROM fir
            WHERE station_id = ?
            ORDER BY date_filed DESC, time_filed DESC
            """,
            (stationId,),
        )
    return database.fetch_all(
        """
        SELECT fir_id, fir_no, date_filed, time_filed, place_of_occurrence, description, status,
               complainant_id, officer_id, station_id
        FROM fir
        ORDER BY date_filed DESC, time_filed DESC
        """
    )
    

#generate complainant_id by fetching the last complainant_id from database table and incrementing it by 1, format should be COMP001, COMP002 etc

def add_complainant(complainant_data):
    try:
        # 1) Insert user
        user_id = database.execute(
            """
            INSERT INTO user (name, contact_no, address)
            VALUES (?, ?, ?)
            """,
            (
                complainant_data.get("name"),
                complainant_data.get("contact_no"),
                complainant_data.get("address"),
            ),
        )

        # 2) Generate complainant_id C001 format
        rows = database.fetch_all("SELECT complainant_id FROM complainant")
        max_num = 0
        for row in rows:
            cid = str(row.get("complainant_id", ""))
            m = re.search(r"(\d+)$", cid)
            if m:
                max_num = max(max_num, int(m.group(1)))
        complainant_id = f"C{max_num + 1:03d}"

        # 3) Insert complainant
        database.execute(
            """
            INSERT INTO complainant (complainant_id, user_id, age, gender, id_proof)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                complainant_id,
                user_id,
                complainant_data.get("age"),
                complainant_data.get("gender"),
                complainant_data.get("id_proof"),
            ),
        )
        return complainant_id
    except Exception:
        return None

def update_fir(fir_id, fir_data):
    try:
        set_parts = []
        params = []

        place = fir_data.get("place_of_occurrence")
        desc = fir_data.get("description")
        status = fir_data.get("status")

        if place:
            set_parts.append("place_of_occurrence=?")
            params.append(place)
        if desc:
            set_parts.append("description=?")
            params.append(desc)
        if status:
            set_parts.append("status=?")
            params.append(status)

        if not set_parts:
            return False

        params.extend([fir_id, fir_id])
        database.execute(
            f"UPDATE fir SET {', '.join(set_parts)} WHERE fir_id=? OR fir_no=?",
            tuple(params),
        )
        return True
    except Exception:
        return False

def set_fir_status(fir_id, status):
    try:
        database.execute(
            "UPDATE fir SET status=? WHERE fir_id=? OR fir_no=?",
            (status, fir_id, fir_id),
        )
        return True
    except Exception:
        return False

def get_fir_by_id(fir_id):
    # return FIR details for a given FIR ID
    return database.fetch_one(
        """
        SELECT fir_id, fir_no, date_filed, time_filed, place_of_occurrence, description, status,
               complainant_id, officer_id, station_id
        FROM fir
        WHERE fir_id = ? OR fir_no = ?
        """,
        (fir_id, fir_id),
    )


def get_total_firs():
    row = database.fetch_one("SELECT COUNT(*) AS total FROM fir")
    return int(row["total"]) if row else 0


def get_active_firs():
    row = database.fetch_one(
        """
        SELECT COUNT(*) AS total
        FROM fir
        WHERE status = 'Under Investigation'
        """
    )
    return int(row["total"]) if row else 0


def get_recent_firs():
    return database.fetch_all(
        """
        SELECT fir_no, place_of_occurrence, status
        FROM fir
        ORDER BY date_filed DESC
        LIMIT 5
        """
    )
    
def get_complainant_by_id(complainant_id):
    # return complainant details for a given complainant ID
    return database.fetch_one(
        """
        SELECT c.complainant_id, u.name, u.contact_no, u.address, c.age, c.gender, c.id_proof
        FROM complainant c
        JOIN user u ON u.user_id = c.user_id
        WHERE c.complainant_id=?
        """,
        (complainant_id,),
    )

def get_officer_by_id(officer_id, station_id=None):
    # return officer details for a given officer ID
    if station_id:
        return database.fetch_one(
            """
            SELECT o.officer_id, o.rank, o.badge_no, o.role, o.station_id,
                   u.name, u.contact_no, u.address,
                   ps.station_name, ps.city, ps.district, ps.state
            FROM officer o
            JOIN user u ON u.user_id = o.user_id
            JOIN police_station ps ON ps.station_id = o.station_id
            WHERE o.officer_id=? AND o.station_id=?
            """,
            (officer_id, station_id),
        )
    return database.fetch_one(
        """
        SELECT o.officer_id, o.rank, o.badge_no, o.role, o.station_id,
               u.name, u.contact_no, u.address,
               ps.station_name, ps.city, ps.district, ps.state
        FROM officer o
        JOIN user u ON u.user_id = o.user_id
        JOIN police_station ps ON ps.station_id = o.station_id
        WHERE o.officer_id=?
        """,
        (officer_id,),
    )

def get_profile_details(officer_id):
    # return profile details (officer data, and station data, + some statistics) as a dict for a given officer ID
    officer = get_officer_by_id(officer_id)
    if not officer:
        return None

    total = database.fetch_one(
        "SELECT COUNT(*) AS total_firs FROM fir WHERE officer_id=?",
        (officer_id,),
    )
    active = database.fetch_one(
        """
        SELECT COUNT(*) AS active_firs
        FROM fir
        WHERE officer_id=? AND status='Under Investigation'
        """,
        (officer_id,),
    )

    return {
        "officer": officer,
        "station": {
            "station_id": officer.get("station_id"),
            "station_name": officer.get("station_name"),
            "city": officer.get("city"),
            "district": officer.get("district"),
            "state": officer.get("state"),
        },
        "total_firs": (total or {}).get("total_firs", 0),
        "active_firs": (active or {}).get("active_firs", 0),
    }

# add more functions as needed
