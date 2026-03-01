from werkzeug.security import generate_password_hash, check_password_hash
# use this when querying : cursor = conn.cursor(dictionary=True), the query should return listof dictionaries instead of tuples, so we can access values by column names instead of index

def validate_officer_tuple(officerid, stationid, password):
    # validate officer tuple from database table, password is hashed with werkzeug.security
    return True

def get_role(officerid, stationid) -> str:
    # return role from database table for the composite key
    return 'admin' if officerid == 'admin' else 'officer'

def add_officer(officerdata):
    # add officer to database table
    pass

def remove_officer(officerid, stationid):
    # remove officer from database table
    pass

def create_fir(fir_data):
    # add FIR to database table
    pass

def get_officers(stationid):
    # return list of officers for a station
    return [('officer1', 'station1'), ('officer2', 'station1')]

def get_all_firs(stationId=None):
    # return list of all FIRs for a station or all FIRs if stationId is None
    return [
        {
            'id': 'FIR001',
            'title': 'Theft Case',
            'status': 'open',
            'date': '2024-01-15'
        },
        {
            'id': 'FIR002',
            'title': 'Assault Incident',
            'status': 'closed',
            'date': '2024-01-16'
        }
    ]
    

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
    return {
        'id': fir_id,
        'title': 'Sample FIR',
        'description': 'This is a sample FIR description.',
        'status': 'open',
        'date': '2024-01-15'
    }
    
def get_complainant_by_id(complainant_id):
    # return complainant details for a given complainant ID
    
    return None

def get_officer_by_id(officer_id):
    # return officer details for a given officer ID
    return None

def get_profile_details(officer_id):
    # return profile details (officer data, and station data, + some statistics) as a dict for a given officer ID
    return None