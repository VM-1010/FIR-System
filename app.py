from flask import Flask, render_template, request, redirect, url_for, abort, session, flash
import backend
from datetime import datetime

app = Flask(__name__)  
app.secret_key = 'rockey'

def _extract_id_list(items, primary_keys, fallback_index=0):
    ids = []
    for item in items or []:
        value = None
        if isinstance(item, dict):
            for key in primary_keys:
                if item.get(key) is not None:
                    value = item.get(key)
                    break
        elif isinstance(item, (list, tuple)) and len(item) > fallback_index:
            value = item[fallback_index]
        else:
            value = item
        if value is not None and str(value).strip():
            ids.append(str(value))
    return sorted(set(ids))


def _get_fir_ids(station_id):
    firs = backend.get_all_firs(station_id)
    return _extract_id_list(firs, ['fir_id', 'id', 'fir_no'])


def _get_complainant_ids():
    # Prefer explicit complainant list provider if backend exposes one.
    candidate_sources = []
    if hasattr(backend, 'get_all_complainants'):
        try:
            candidate_sources = backend.get_all_complainants()
        except TypeError:
            candidate_sources = backend.get_all_complainants(None)
    elif hasattr(backend, 'get_complainants'):
        candidate_sources = backend.get_complainants()

    complainant_ids = _extract_id_list(candidate_sources, ['complainant_id', 'id'])
    if complainant_ids:
        return complainant_ids

    # Fallback: derive known complainant IDs from FIR records.
    firs = backend.get_all_firs(session.get('stationId'))
    return _extract_id_list(firs, ['complainant_id'])

def _get_next_fir_preview():
    firs = backend.get_all_firs(None) or []
    max_num = 0
    for row in firs:
        raw = str(row.get('fir_no') or row.get('fir_id') or '')
        digits = ''.join(ch for ch in raw if ch.isdigit())
        if digits:
            max_num = max(max_num, int(digits))
    next_num = max_num + 1
    now = datetime.now()
    return {
        "fir_no": f"FIR{next_num:03d}",
        "date_filed": now.strftime("%Y-%m-%d"),
        "time_filed": now.strftime("%H:%M:%S"),
        "status": "Registered",
    }


def _get_dashboard_stats(station_id=None):
    firs = backend.get_all_firs(station_id) or []
    return {
        "total": len(firs),
        "active": sum(1 for f in firs if f.get("status") == "Under Investigation"),
        "closed": sum(1 for f in firs if f.get("status") == "Closed"),
        "pending": sum(1 for f in firs if f.get("status") == "Pending Review"),
    }

@app.route('/')
def home():
    if not session.get('officerId'):
        return redirect(url_for('login'))
    stats = _get_dashboard_stats(session.get('stationId'))
    if session.get('role') == 'admin':
        return render_template("admin.html", stats=stats)
    return render_template("officer.html", stats=stats)
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if session.get('officerId'):
            return redirect(url_for('home'))
        return render_template('login.html')
    oId = request.form.get('officerId') or request.form.get('officer_id')
    sId = request.form.get('stationId') or request.form.get('station_id')
    password = request.form.get('password')

    print(oId, sId, password)
    print(backend.validate_officer_tuple(oId, sId, password))

    if backend.validate_officer_tuple(oId, sId, password):
        session['officerId'] = oId
        session['stationId'] = sId
        session['role'] = backend.get_role(oId, sId)
        stats = _get_dashboard_stats(sId)

        if session['role'] == 'admin':
            return render_template("admin.html", stats=stats)

        return render_template("officer.html", stats=stats)

    return render_template("login.html")


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))



@app.route('/add_officer', methods=['POST', 'GET'])
def add_officer():
    if request.method == 'GET':
        if session.get('role') != 'admin':
            abort(403)
        return render_template('add_officer.html')
    if session.get('role') != 'admin':
        abort(403)
    officer_data = {
        'name': request.form.get('name'),
        'rank': request.form.get('rank'),
        'badge_no': request.form.get('badge_no') or request.form.get('badgeNo'),
        'contact_no': request.form.get('contact_no') or request.form.get('contactNo'),
        'station_id': session.get('stationId'),
        'role': request.form.get('role', 'officer')
    }
    
    backend.add_officer(officer_data)
    flash('Officer added successfully.')
    return redirect(url_for('home'))

@app.route('/remove_officer', methods=['POST', 'GET'])
def remove_officer():
    if request.method == 'GET':
        if session.get('role') != 'admin':
            abort(403)
        officers = backend.get_officers(session.get('stationId'))
        return render_template('remove_officer.html', officers=officers)
    if session.get('role') != 'admin':
        abort(403)
    oId = request.form.get('officer_id') or request.form.get('officerId')
    sId = session.get('stationId')
    backend.remove_officer(oId, sId)
    flash('Officer removed successfully.')
    return redirect(url_for('home'))

@app.route('/view_officers')
def view_officers():
    if session.get('role') != 'admin':
        abort(403)
    stationId = session.get('stationId')
    officers = backend.get_officers(stationId)   
    return render_template('view_officers.html', officers=officers)

@app.route('/firs')
def view_fir():
    if session.get('role') != 'admin':
        abort(403)
    stationId = session.get('stationId')
    firs = backend.get_all_firs(stationId)
    return render_template('view_firs.html', firs=firs)

@app.route('/close_fir', methods=['POST', 'GET'])
def close_fir():
    if request.method == 'GET':
        if session.get('role') != 'admin':
            abort(403)
        firs = backend.get_all_firs(session.get('stationId'))
        return render_template('close_fir.html', firs=firs)
    fir_id = request.form.get('fir_id') or request.form.get('firId')
    backend.set_fir_status(fir_id, 'Closed')
    flash('FIR closed successfully.')
    return redirect(url_for('home'))


@app.route('/new_fir', methods=['POST', 'GET'])
def new_fir():
    if not session.get('officerId'):
        abort(403)
    if request.method == 'GET':
        complainant_ids = _get_complainant_ids()
        preview = _get_next_fir_preview()
        return render_template('new_fir.html', complainant_ids=complainant_ids, preview=preview)
    place = request.form.get('place_of_occurrence') or request.form.get('location')
    fir_data = {
        'officer_id': session.get('officerId'),
        'station_id': session.get('stationId'),
        'fir_no': request.form.get('fir_no'),
        'date_filed': request.form.get('date_filed'),
        'time_filed': request.form.get('time_filed'),
        'status': request.form.get('status', 'Registered'),
        'complainant_id': request.form.get('complainant_id'),
        'complainant_name': request.form.get('complainantName'),
        'description': request.form.get('description'),
        'place_of_occurrence': place,
        'location': place
    }
    backend.create_fir(fir_data)
    flash('FIR registered successfully.')
    return redirect(url_for('home'))

@app.route('/search_fir', methods=['POST', 'GET'])
def search_fir():
    if not session.get('officerId'):
        abort(403)
    if request.method == 'GET':
        fir_ids = _get_fir_ids(session.get('stationId'))
        return render_template('search_fir.html', fir_ids=fir_ids)
    fir_id = request.form.get('fir_id') or request.form.get('firId')
    fir = backend.get_fir_by_id(fir_id)
    if not fir:
        flash('No FIR found with this ID.')
        return redirect(url_for('search_fir'))
    return render_template('fir_details.html', fir=fir)

@app.route('/update_fir', methods=['POST', 'GET'])
def update_fir():
    if not session.get('officerId'):
        abort(403)
    if request.method == 'GET':
        firs_raw = backend.get_all_firs(session.get('stationId'))
        firs = [i.get('fir_id', i.get('id')) for i in firs_raw]
        return render_template('update_fir.html', firid_list=firs)
    fir_id = request.form.get('fir_id') or request.form.get('firId')
    fir_data = {
        'description': request.form.get('description'),
        'officer_id': session.get('officerId'),
        'place_of_occurrence': request.form.get('place_of_occurrence') or request.form.get('placeOfOccurrence'),
        'status': request.form.get('status'),
        'complainant_id': request.form.get('complainant_id') or request.form.get('complainantId')
    }
    backend.update_fir(fir_id, fir_data)
    flash('FIR updated successfully.')
    return redirect(url_for('home'))

@app.route('/register_complainant', methods=['POST', 'GET'])
def register_complainant():
    if not session.get('officerId'):
        abort(403)
    if request.method == 'GET':
        return render_template('register_complainant.html')
    complainant_data = {
        'name': request.form.get('name'),
        'age': request.form.get('age'),
        'gender': request.form.get('gender'),
        'address': request.form.get('address'),
        'contact_no': request.form.get('contact_no') or request.form.get('contactNo'),
        'id_proof': request.form.get('id_proof') or request.form.get('idProof')
    }
    backend.add_complainant(complainant_data)
    flash('Complainant registered successfully.')
    return redirect(url_for('home'))

@app.route('/profile/<oIdsId>')
def view_profile(oIdsId):
    # shows profile details (officer details, station details, some statistics) for a given officer Id and station Id passed as oIdsId in the format officerId_stationId
    oid, sid = oIdsId.split('_', 1) if '_' in oIdsId else (oIdsId, session.get('stationId'))
    try:
        officer = backend.get_officer_by_id(oid, sid)
    except TypeError:
        officer = backend.get_officer_by_id(oid)
    return render_template('profile.html', officer=officer)

@app.route('/complainant/<complainant_id>')
def view_complainant_details(complainant_id):
    # shows complainant profile (basic data, statistics )
    complainant = backend.get_complainant_by_id(complainant_id)
    return render_template('complainant_details.html', complainant=complainant)

@app.route('/fir/<fir_id>')
def view_fir_details(fir_id):
    # shows FIR details for a given FIR ID
    fir = backend.get_fir_by_id(fir_id)
    return render_template('fir_details.html', fir=fir)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
