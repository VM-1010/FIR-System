# FIR-System

A Flask-based FIR (First Information Report) Management System designed to streamline the process of filing, managing, and tracking criminal reports across police stations.

## Current Project Status

### ✅ Completed
1. **Flask Application Setup** (`app.py`)
   - Core Flask application initialized with secret key
   - Session management configured
   - All major routes defined
   
2. **Backend Functions Skeleton** (`backend.py`)
   - Function signatures for all required operations
   - Placeholder implementations ready for database integration
   
3. **HTML Templates (Basic Structure)**
   - `login.html` - Login form with validation
   - `admin.html` - Admin dashboard skeleton
   - `officer.html` - Officer dashboard skeleton
   - `add_officer.html` - Officer registration form
   - `remove_officer.html` - Officer removal form
   - `view_officers.html` - Officer list view
   - `view_firs.html` - FIR list view
   - `close_fir.html` - FIR status update form
   - `fir_details.html` - Individual FIR details
   - `complainant_details.html` - Complainant information
   - `profile.html` - Officer profile page
   - `dashboard.html` - Dashboard view

4. **Static Assets**
   - CSS styling (`static/css/style.css`)
   - JavaScript files (`static/js/login.js`, `admin.js`, `officer.js`, `dashboard.js`)

5. **Routes Implemented** (in `app.py`)
   - `GET /` - Home page (redirects to login if not authenticated)
   - `POST/GET /login` - User login with officer ID, station ID, and password
   - `GET /logout` - User logout with session clearing
   - `POST/GET /add_officer` - Add new officer (admin only)
   - `POST/GET /remove_officer` - Remove officer (admin only)
   - `GET /view_officers` - View all officers (admin only)
   - `GET /firs` - View all FIRs (admin only)
   - `POST/GET /close_fir` - Close/update FIR status (admin only)

---

## 📋 TODO: Frontend Development

**Assigned to: [Frontend Team Member Name]**

The following HTML templates need to be completed with full Jinja2 template syntax and interactivity:

### 1. **Enhance Existing Templates**
   - [ ] **admin.html** - Complete admin dashboard with:
     - Statistics cards (Total FIRs, Active Cases, Closed Cases, etc.)
     - Quick action buttons with proper form integration
     - FIR management interface
     - Officer management section
     - Dynamic data binding using Jinja2
   
   - [ ] **officer.html** - Complete officer dashboard with:
     - Officer-specific FIR statistics
     - FIR creation form
     - Personal FIR list
     - Profile information display
     - Dynamic data rendering with Jinja2
   
   - [ ] **login.html** - Enhance with:
     - Form validation feedback
     - Error message display
     - Loading state management
     - Remember me functionality (optional)

### 2. **Complete Remaining Templates**
   - [ ] **add_officer.html** - Registration form for new officers with:
     - Officer ID input
     - Station ID dropdown/selection
     - Password input with strength indicator
     - Role selection (admin, officer)
     - Form validation
   
   - [ ] **remove_officer.html** - Officer removal interface with:
     - Searchable officer list using Jinja2 loops
     - Confirmation dialog before deletion
     - Officer details display
   
   - [ ] **view_officers.html** - Officer listing with:
     - Table display of all officers
     - Search/filter functionality
     - Edit and delete action buttons
     - Station-wise officer grouping
   
   - [ ] **view_firs.html** - FIR listing with:
     - Table/card view of all FIRs
     - Status filtering (Open, Closed, etc.)
     - Search by FIR ID/title
     - Link to FIR details
     - Quick action buttons
   
   - [ ] **fir_details.html** - Detailed FIR view with:
     - FIR information display
     - Complainant details
     - Timeline of updates
     - Status badges
     - Update/edit functionality
   
   - [ ] **close_fir.html** - FIR closure interface with:
     - FIR selection dropdown
     - Status change form
     - Closure remarks input
     - Confirmation workflow
   
   - [ ] **complainant_details.html** - Complainant information with:
     - Personal details display
     - Contact information
     - FIR history linked to complainant
     - Edit capability
   
   - [ ] **profile.html** - Officer profile page with:
     - Personal information display
     - Station assignment
     - Role display
     - Password change option
     - Statistics (FIRs filed, closed, etc.)

### 3. **JavaScript Enhancement** (`static/js/`)
   - [ ] **login.js** - Form validation and submission handling
   - [ ] **admin.js** - Admin dashboard interactions
   - [ ] **officer.js** - Officer dashboard interactions
   - [ ] **dashboard.js** - General dashboard functionality

### 4. **CSS Styling** (`static/css/style.css`)
   - [ ] Complete responsive design
   - [ ] Dark/Light theme support
   - [ ] Mobile-friendly layouts
   - [ ] Accessibility improvements

---

## 🔧 TODO: Backend Development

**Assigned to: [Backend Team Member Name]**

The following backend functions in `backend.py` need to be fully implemented with database operations:

### 1. **Authentication & User Management**
   - [ ] **validate_officer_tuple(officerid, stationid, password)**
     - Query database for officer with composite key (officerid, stationid)
     - Verify password using werkzeug.security.check_password_hash()
     - Return True/False based on validation
   
   - [ ] **get_role(officerid, stationid)**
     - Query database for officer role
     - Return role string ('admin' or 'officer')
   
   - [ ] **add_officer(officerid, stationid, password, role)**
     - Hash password using werkzeug.security.generate_password_hash()
     - Insert new officer record into database
     - Include error handling for duplicate entries
   
   - [ ] **remove_officer(officerid, stationid)**
     - Delete officer record from database
     - Validate officer exists before deletion
     - Handle foreign key constraints if any

### 2. **Officer Management**
   - [ ] **get_officers(stationid)**
     - Query database for all officers at a specific station
     - Return list of officer tuples/objects with (id, name, role, station)
   
   - [ ] **get_all_officers()**
     - Query database for all officers across all stations
     - Return complete officer list with station information

### 3. **FIR (First Information Report) Management**
   - [ ] **create_fir(fir_data)**
     - Accept FIR data dictionary with: title, description, complainant_id, officer_id, station_id, date, etc.
     - Insert new FIR record into database
     - Return generated FIR ID
     - Set initial status as 'open'
   
   - [ ] **get_all_firs(stationId=None)**
     - Query database for all FIRs
     - If stationId provided, filter by station
     - Return list of FIR objects with: id, title, description, status, date, officer, complainant
   
   - [ ] **get_fir_by_id(fir_id)**
     - Query database for specific FIR
     - Return complete FIR object with all details
     - Include related complainant and officer information
   
   - [ ] **update_fir(fir_id, fir_data)**
     - Update existing FIR record with new data
     - Support partial updates
     - Update modification timestamp
   
   - [ ] **set_fir_status(fir_id, status)**
     - Update FIR status ('open', 'closed', 'pending', etc.)
     - Record status change timestamp
     - Validate status values

### 4. **Complainant Management**
   - [ ] **add_complainant(complainant_data)**
     - Accept complainant data: name, address, phone, email, etc.
     - Insert new complainant record into database
     - Return generated complainant ID
     - Include validation for required fields

### 5. **Database Setup** (`database.py`)
   - [ ] Initialize database connection (SQLite/PostgreSQL/MySQL)
   - [ ] Define database schemas:
     - **officers**: id, station_id, password_hash, role, created_at
     - **firs**: fir_id, title, description, status, officer_id, station_id, created_at, updated_at
     - **complainants**: id, name, address, phone, email, created_at
     - **fir_complainants**: fir_id, complainant_id (junction table)
   - [ ] Create database initialization script
   - [ ] Implement connection pooling for performance

---

## 🏗️ Project Structure

```
FIR-System/
├── app.py                 # Main Flask application with route definitions
├── backend.py             # Backend functions (needs implementation)
├── database.py            # Database configuration and models (needs setup)
├── userservice.py         # User service functions (if applicable)
├── README.md              # Project documentation
├── static/
│   ├── css/
│   │   └── style.css      # Main stylesheet
│   └── js/
│       ├── login.js       # Login page functionality
│       ├── admin.js       # Admin dashboard functionality
│       ├── officer.js     # Officer dashboard functionality
│       └── dashboard.js   # General dashboard functionality
└── templates/
    ├── login.html         # Login form
    ├── admin.html         # Admin dashboard
    ├── officer.html       # Officer dashboard
    ├── add_officer.html   # Add officer form
    ├── remove_officer.html # Remove officer form
    ├── view_officers.html # Officers list
    ├── view_firs.html     # FIRs list
    ├── fir_details.html   # FIR details page
    ├── close_fir.html     # Close FIR form
    ├── complainant_details.html # Complainant details
    └── profile.html       # Officer profile
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.7+
- Flask
- Flask-Session
- Werkzeug (for password hashing)
- Database (SQLite/PostgreSQL/MySQL)

### Installation
```bash
# Install dependencies
pip install flask flask-session werkzeug

# Run the application
python app.py
```

The application will be available at `http://127.0.0.1:5000`

---

## 🔐 Key Features

- **User Authentication**: Officer login with ID, Station ID, and password
- **Role-Based Access Control**: Admin and Officer roles with different permissions
- **FIR Management**: Create, view, update, and close FIRs
- **Officer Management**: Add and remove officers (admin only)
- **Session Management**: Secure session handling with Flask sessions
- **Password Hashing**: Secure password storage using Werkzeug

---

## 📝 Notes

- All passwords are hashed using `werkzeug.security.generate_password_hash()`
- Password validation uses `werkzeug.security.check_password_hash()`
- Session data includes: officerId, stationId, role
- All admin routes require `session['role'] == 'admin'` check
- Logout clears the session and redirects to login page

---
