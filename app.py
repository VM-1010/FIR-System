from flask import Flask
from flask_session import Session
import redis
import backend
from flask import session, Flask, render_template, request, redirect, url_for, abort

app = Flask(__name__)  
app.secret_key = 'rockey'

@app.route('/')
def home():
    if not session.get('officerId'):
        return redirect(url_for('login'))
    if session.get('role') == 'admin':
        return render_template('admin.html')
    return render_template('officer.html',
                            officer=session.get('officerId'), station=session.get('stationiId'),
                            role=session.get('role'))
    

@app.route('/login', methods=['POST', 'GET'])
def login():
    print(request.method)
    if request.method == 'GET':
        return render_template('login.html')
    oId = request.form.get('officerId')
    sId = request.form.get('stationId')
    
    password = request.form.get('password')

    if  backend.validate_officer_tuple(oId, sId, password):  
        session['officerId'] = oId
        session['stationId'] = sId
        session['role'] = backend.get_role(oId, sId)
        print(session['role'])
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    print("hello")
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
        'badge_no': request.form.get('badgeNo'),
        'contact_no': request.form.get('contactNo'),
        'station_id': session.get('stationId'),
        'role': request.form.get('role')
    }
    
    backend.add_officer(officer_data)
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
    oId = request.form.get('officerId')
    sId = session.get('stationId')
    backend.remove_officer(oId, sId)
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
        else:
            return render_template('close_fir.html')
    fir_id = request.form.get('firId')
    backend.set_fir_status(fir_id, 'closed')
    return redirect(url_for('home'))


@app.route('/new_fir', methods=['POST', 'GET'])
def new_fir():
    if request.method == 'GET':
        return render_template('new_fir.html')
    fir_data = {
        'officer_id': session.get('officerId'),
        'station_id': session.get('stationId'),
        'complainant_name': request.form.get('complainantName'),
        'description': request.form.get('description'),
        'location': request.form.get('location')
    }
    backend.create_fir(fir_data)
    return redirect(url_for('home'))

@app.route('/search_fir', methods=['POST', 'GET'])
def search_fir():
    if request.method == 'GET':
        return render_template('search_fir.html')
    fir_id = request.form.get('firId')
    fir = backend.get_fir_by_id(fir_id)
    return render_template('fir_details.html', fir=fir)

@app.route('/update_fir', methods=['POST', 'GET'])
def update_fir():
    if request.method == 'GET':
        firs = [i.get('fir_id') for i in backend.get_all_fir()]
        return render_template('update_fir.html', firid_list=firs)
    fir_id = request.form.get('firId')
    fir_data = {
        'description': request.form.get('description'),
        'officer_id': session.get('officerId'),
        'place_of_occurrence': request.form.get('placeOfOccurrence'),
        'status': request.form.get('status'),
        'complainant_id': request.form.get('complainantId')
    }
    backend.update_fir(fir_id, fir_data)
    return redirect(url_for('home'))

@app.route('/register_complainant', methods=['POST', 'GET'])
def register_complainant():
    if request.method == 'GET':
        return render_template('register_complainant.html')
    complainant_data = {
        'name': request.form.get('name'),
        'age': request.form.get('age'),
        'gender': request.form.get('gender'),
        'address': request.form.get('address'),
        'contact_no': request.form.get('contactNo'),
        'id_proof': request.form.get('idProof')
    }
    backend.add_complainant(complainant_data)
    return redirect(url_for('home'))

@app.route('/profile/<oIdsId>')
def view_profile(oIdsId):
    # shows profile details (officer details, station details, some statistics) for a given officer Id and station Id passed as oIdsId in the format officerId_stationId
    oid, sid = oIdsId.split('_')
    officer = backend.get_officer_by_id(oid, sid)
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