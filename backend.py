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
    # add officer to database table
    pass

def remove_officer(officerid, stationid):
    # remove officer from database table
    pass

# generate fir_id by fetching the last fir_id from database table and incrementing it by 1, format should be FIR001, FIR002 etc

def create_fir(fir_data):
    # add FIR to database table
    pass

def get_officers(stationid):
    # return list of officers for a station
    return [('officer1', 'station1'), ('officer2', 'station1')]

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
    # add complainant to database table
    pass

def update_fir(fir_id, fir_data):
    # update FIR in database table
    pass

def set_fir_status(fir_id, status):
    # update FIR status in database table
    pass

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
    
    return None

def get_officer_by_id(officer_id):
    # return officer details for a given officer ID
    return None

def get_profile_details(officer_id):
    # return profile details (officer data, and station data, + some statistics) as a dict for a given officer ID
    return None

# add more functions as needed
