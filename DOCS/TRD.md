# TECHNICAL REQUIREMENTS DOCUMENT (TRD)

## Online Student Result Analysis System

**Version:** 1.0  
**Date:** September 1, 2026  
**Project Type:** Diploma Final-Year Project  
**Document Type:** Technical Requirements Document  
**Based On:** PRD v1.0  

---

## DOCUMENT PURPOSE

This Technical Requirements Document (TRD) translates the approved Product Requirements Document (PRD) into detailed technical specifications, architecture decisions, and implementation guidelines. Every requirement in this TRD traces back to one or more PRD requirements.

**Key Objectives:**
- Define the technical architecture and technology stack
- Specify database schema, API endpoints, and data models
- Provide implementation-ready specifications for developers
- Establish technical constraints and patterns
- Define testing and deployment procedures

---

## TABLE OF CONTENTS

1. [Technical Overview](#1-technical-overview)
2. [System Architecture](#2-system-architecture)
3. [Technology Stack](#3-technology-stack)
4. [Backend Architecture](#4-backend-architecture)
5. [Frontend Architecture](#5-frontend-architecture)
6. [Database Architecture](#6-database-architecture)
7. [Database Tables, Fields, Relationships, Keys and Constraints](#7-database-tables-fields-relationships-keys-and-constraints)
8. [API / Route Specifications](#8-api--route-specifications)
9. [Authentication and Authorization](#9-authentication-and-authorization)
10. [Student Management Technical Requirements](#10-student-management-technical-requirements)
11. [Subject Management Technical Requirements](#11-subject-management-technical-requirements)
12. [Marks Management Technical Requirements](#12-marks-management-technical-requirements)
13. [Result Calculation Logic](#13-result-calculation-logic)
14. [Result Analysis and Analytics](#14-result-analysis-and-analytics)
15. [Validation Rules](#15-validation-rules)
16. [Error Handling](#16-error-handling)
17. [Security Requirements](#17-security-requirements)
18. [Project Folder/Module Responsibilities](#18-project-foldermodule-responsibilities)
19. [Testing Requirements](#19-testing-requirements)
20. [Deployment Requirements](#20-deployment-requirements)
21. [Environment Configuration](#21-environment-configuration)
22. [PRD → TRD Traceability Matrix](#22-prd--trd-traceability-matrix)
23. [Technical Dependencies](#23-technical-dependencies)
24. [Technical Risks and Mitigation](#24-technical-risks-and-mitigation)
25. [Definition of Done](#25-definition-of-done)

---

## 1. TECHNICAL OVERVIEW

### 1.1 Project Summary

**TR-OVERVIEW-001:** The Online Student Result Analysis System shall be implemented as a server-side rendered web application using Python Flask framework with HTML/CSS/JavaScript frontend.

**TR-OVERVIEW-002:** The system shall follow a Model-View-Controller (MVC) architectural pattern adapted for Flask (Models, Routes, Templates).

**TR-OVERVIEW-003:** The application shall be a monolithic architecture with frontend and backend deployed together on Render free tier.

**TR-OVERVIEW-004:** The system shall use Supabase PostgreSQL as the primary database with direct SQL queries or SQLAlchemy ORM.

**TR-OVERVIEW-005:** The application shall be stateless except for admin session management using Flask sessions.

### 1.2 Technical Constraints

**TR-OVERVIEW-006:** All technologies must be free and open-source (no paid licenses).

**TR-OVERVIEW-007:** The application must be deployable on Render free tier (512 MB RAM, automatic sleep after 15 min inactivity).

**TR-OVERVIEW-008:** Database must fit within Supabase free tier limits (500 MB storage, 2 GB bandwidth/month).

**TR-OVERVIEW-009:** No build tools or transpilers required (use vanilla JavaScript, no React/Vue/Angular).

**TR-OVERVIEW-010:** Application must handle cold start delays gracefully (30-60 seconds first request after sleep).

### 1.3 Development Principles

**TR-OVERVIEW-011:** Code shall follow PEP 8 style guidelines for Python.

**TR-OVERVIEW-012:** Functions shall be modular with single responsibility principle.

**TR-OVERVIEW-013:** Database queries shall use parameterized queries to prevent SQL injection.

**TR-OVERVIEW-014:** All user inputs shall be validated on both frontend and backend.

**TR-OVERVIEW-015:** Error handling shall be comprehensive with user-friendly messages.

---

## 2. SYSTEM ARCHITECTURE

### 2.1 High-Level Architecture

**TR-ARCH-001:** The system shall implement a 3-tier architecture:
- **Presentation Tier:** HTML/CSS/JavaScript (rendered by Flask templates)
- **Application Tier:** Python Flask backend (business logic, routing)
- **Data Tier:** Supabase PostgreSQL database

**TR-ARCH-002:** Architecture diagram (conceptual):

```
┌─────────────────────────────────────────────────────────┐
│                     Web Browser                         │
│  (HTML/CSS/JS - Rendered by Flask Jinja2 Templates)   │
└──────────────────────┬──────────────────────────────────┘
                       │ HTTP/HTTPS
                       │ (GET/POST Requests)
┌──────────────────────▼──────────────────────────────────┐
│               Python Flask Application                   │
│  ┌─────────────────────────────────────────────────┐   │
│  │           Routes (Controllers)                  │   │
│  │  /login, /dashboard, /students, /marks, etc.   │   │
│  └──────────────────┬──────────────────────────────┘   │
│  ┌──────────────────▼──────────────────────────────┐   │
│  │         Business Logic Layer                    │   │
│  │  (Result Calculation, Validation, Analytics)    │   │
│  └──────────────────┬──────────────────────────────┘   │
│  ┌──────────────────▼──────────────────────────────┐   │
│  │           Data Access Layer                     │   │
│  │  (Database queries via psycopg2/SQLAlchemy)    │   │
│  └──────────────────┬──────────────────────────────┘   │
└───────────────────────┼──────────────────────────────────┘
                       │ PostgreSQL Protocol (SSL)
┌──────────────────────▼──────────────────────────────────┐
│            Supabase PostgreSQL Database                 │
│  Tables: admins, students, subjects, marks             │
└─────────────────────────────────────────────────────────┘
```

### 2.2 Request Flow

**TR-ARCH-003:** Admin authentication request flow:
1. User submits login form (POST /login)
2. Flask route receives request
3. Backend validates credentials against database
4. If valid, create Flask session with admin_id
5. Redirect to /dashboard
6. All subsequent requests check session before allowing access

**TR-ARCH-004:** Student result lookup request flow:
1. Student submits lookup form (POST /result-lookup)
2. Flask route receives Roll Number + DOB
3. Backend queries database for matching student
4. If found, fetch all marks for that student
5. Calculate results (total, percentage, grade, status)
6. Render result page with calculations
7. No session created (stateless)

**TR-ARCH-005:** Data modification request flow:
1. Admin submits form (POST /students/add, /marks/add, etc.)
2. Flask route validates session
3. Backend validates form data
4. If valid, execute database INSERT/UPDATE/DELETE
5. Commit transaction
6. Redirect with success message or show error

### 2.3 Deployment Architecture

**TR-ARCH-006:** Deployment shall use the following architecture:

```
┌─────────────────────────────────────────────────────────┐
│                   Internet Users                        │
└──────────────────────┬──────────────────────────────────┘
                       │ HTTPS
┌──────────────────────▼──────────────────────────────────┐
│                 Render Web Service                      │
│  - Auto-assigned subdomain: app-name.onrender.com      │
│  - HTTPS enforced (automatic SSL certificate)          │
│  - Health checks: / or /health                         │
│  - Auto-deploy from GitHub main branch                 │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│           Flask App (Gunicorn WSGI Server)             │
│  - Entry point: app.py                                 │
│  - Workers: 1 (sufficient for free tier)               │
│  - Static files served by Flask                        │
└──────────────────────┬──────────────────────────────────┘
                       │ PostgreSQL over SSL
┌──────────────────────▼──────────────────────────────────┐
│           Supabase PostgreSQL Database                  │
│  - Connection string from environment variable          │
│  - SSL required                                        │
│  - Connection pooling via psycopg2                     │
└─────────────────────────────────────────────────────────┘
```

---

## 3. TECHNOLOGY STACK

### 3.1 Backend Technologies

**TR-TECH-001:** Python 3.11.x shall be the runtime environment.

**TR-TECH-002:** Flask 3.0.0+ shall be the web framework.

**TR-TECH-003:** flask-session or built-in Flask sessions shall manage admin sessions.

**TR-TECH-004:** bcrypt 4.1.1+ shall be used for password hashing (cost factor 12).

**TR-TECH-005:** psycopg2-binary 2.9.9+ shall be the PostgreSQL database adapter.

**TR-TECH-006:** python-dotenv 1.0.0+ shall load environment variables from .env file.

**TR-TECH-007:** gunicorn 21.2.0+ shall be the production WSGI HTTP server.

**TR-TECH-008:** Optional: Flask-SQLAlchemy 3.1.1+ can be used as ORM (or use raw SQL with psycopg2).

### 3.2 Frontend Technologies

**TR-TECH-009:** HTML5 shall be used for semantic markup.

**TR-TECH-010:** CSS3 shall be used for styling (no preprocessors like SASS/LESS).

**TR-TECH-011:** Vanilla JavaScript (ES6+) shall be used for client-side interactivity.

**TR-TECH-012:** Chart.js 4.x shall be used for data visualizations (loaded from CDN).

**TR-TECH-013:** No frontend frameworks (React, Vue, Angular) shall be used.

**TR-TECH-014:** No build tools (Webpack, Vite, etc.) shall be required.

### 3.3 Database

**TR-TECH-015:** Supabase PostgreSQL (latest version) shall be the database.

**TR-TECH-016:** PostgreSQL connection shall use SSL/TLS encryption.

**TR-TECH-017:** Database schema shall use standard PostgreSQL data types.

### 3.4 Development Tools

**TR-TECH-018:** Git shall be used for version control.

**TR-TECH-019:** GitHub shall host the repository.

**TR-TECH-020:** VS Code or PyCharm recommended for development (not required).

**TR-TECH-021:** Postman or similar tools recommended for API testing (optional).

### 3.5 Third-Party Libraries

**TR-TECH-022:** Chart.js CDN link:
```
https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js
```

**TR-TECH-023:** No other third-party frontend libraries shall be required.

**TR-TECH-024:** All Python dependencies shall be listed in requirements.txt.

### 3.6 Version Control

**TR-TECH-025:** requirements.txt content:
```
Flask==3.0.0
psycopg2-binary==2.9.9
bcrypt==4.1.1
python-dotenv==1.0.0
gunicorn==21.2.0
```

**TR-TECH-026:** Optional: Flask-SQLAlchemy==3.1.1 (if using ORM).

**TR-TECH-027:** Python version specified in runtime.txt:
```
python-3.11.6
```

---

## 4. BACKEND ARCHITECTURE

### 4.1 Flask Application Structure

**TR-BE-001:** The Flask application entry point shall be BACKEND/app.py.

**TR-BE-002:** Application structure:
```
BACKEND/
├── app.py                 # Main Flask application
├── config.py              # Configuration management
├── models.py              # Database models (if using ORM) or SQL queries
├── routes/
│   ├── __init__.py
│   ├── auth.py            # Authentication routes
│   ├── dashboard.py       # Dashboard routes
│   ├── students.py        # Student CRUD routes
│   ├── subjects.py        # Subject CRUD routes
│   ├── marks.py           # Marks CRUD routes
│   ├── results.py         # Results display routes
│   ├── analysis.py        # Analytics routes
│   └── reports.py         # Reports routes
├── utils/
│   ├── __init__.py
│   ├── db.py              # Database connection utilities
│   ├── validators.py      # Input validation functions
│   ├── calculations.py    # Result calculation logic
│   └── helpers.py         # Helper functions
├── static/
│   ├── css/
│   │   ├── main.css       # Main stylesheet
│   │   └── print.css      # Print-specific styles
│   ├── js/
│   │   ├── main.js        # Common JavaScript
│   │   ├── charts.js      # Chart.js configurations
│   │   └── validation.js  # Frontend validation
│   └── images/
│       └── logo.png       # Application logo
├── templates/
│   ├── base.html          # Base template with navigation
│   ├── auth/
│   │   └── login.html
│   ├── dashboard/
│   │   └── index.html
│   ├── students/
│   │   ├── list.html
│   │   ├── add.html
│   │   └── edit.html
│   ├── subjects/
│   │   ├── list.html
│   │   ├── add.html
│   │   └── edit.html
│   ├── marks/
│   │   ├── list.html
│   │   └── add.html
│   ├── results/
│   │   ├── admin_list.html
│   │   ├── student_lookup.html
│   │   └── student_result.html
│   ├── analysis/
│   │   └── index.html
│   └── reports/
│       ├── index.html
│       ├── individual.html
│       └── class.html
├── requirements.txt
├── runtime.txt
├── .env.example
└── .gitignore
```

### 4.2 Flask Application Initialization

**TR-BE-003:** app.py shall initialize Flask with the following configuration:
```python
from flask import Flask, session
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = True if os.getenv('FLASK_ENV') == 'production' else False
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30 minutes
```

**TR-BE-004:** Database connection shall be initialized in utils/db.py:
```python
import psycopg2
from psycopg2.extras import RealDictCursor
import os

def get_db_connection():
    conn = psycopg2.connect(
        os.getenv('DATABASE_URL'),
        cursor_factory=RealDictCursor,
        sslmode='require'
    )
    return conn
```

### 4.3 Route Registration

**TR-BE-005:** All routes shall be registered using Flask Blueprints for modularity.

**TR-BE-006:** Blueprint registration in app.py:
```python
from routes import auth, dashboard, students, subjects, marks, results, analysis, reports

app.register_blueprint(auth.bp)
app.register_blueprint(dashboard.bp)
app.register_blueprint(students.bp)
app.register_blueprint(subjects.bp)
app.register_blueprint(marks.bp)
app.register_blueprint(results.bp)
app.register_blueprint(analysis.bp)
app.register_blueprint(reports.bp)
```

### 4.4 Session Management

**TR-BE-007:** Admin sessions shall store: dmin_id, username, email.

**TR-BE-008:** Session shall be created upon successful login:
```python
session['admin_id'] = admin['id']
session['username'] = admin['username']
session['email'] = admin['email']
session.permanent = True
```

**TR-BE-009:** Session shall be destroyed on logout:
```python
session.clear()
```

**TR-BE-010:** Protected routes shall check for admin_id in session:
```python
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function
```

### 4.5 Error Handling

**TR-BE-011:** Global error handlers shall be defined in app.py:
```python
@app.errorhandler(404)
def not_found(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500
```

**TR-BE-012:** Database errors shall be caught and logged:
```python
try:
    # database operation
except psycopg2.Error as e:
    app.logger.error(f'Database error: {e}')
    return jsonify({'error': 'Database error occurred'}), 500
```

### 4.6 Logging

**TR-BE-013:** Logging shall be configured in app.py:
```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler('app.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
```

**TR-BE-014:** Production logging shall output to stdout for Render logs:
```python
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
app.logger.addHandler(stream_handler)
```

---

## 5. FRONTEND ARCHITECTURE

### 5.1 Template Engine

**TR-FE-001:** Jinja2 (built into Flask) shall be the template engine.

**TR-FE-002:** Base template shall provide consistent layout:
```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Student Result System{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/print.css') }}" media="print">
    {% block extra_css %}{% endblock %}
</head>
<body>
    {% if session.get('admin_id') %}
        {% include 'partials/navigation.html' %}
    {% endif %}
    
    <main class="container">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        {% block content %}{% endblock %}
    </main>
    
    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
```

### 5.2 CSS Architecture

**TR-FE-003:** CSS shall follow BEM naming convention (Block__Element--Modifier).

**TR-FE-004:** Color scheme constants in main.css:
```css
:root {
    --color-primary: #2563eb;
    --color-success: #16a34a;
    --color-danger: #dc2626;
    --color-warning: #ea580c;
    --color-info: #0891b2;
    --color-bg: #f8fafc;
    --color-bg-card: #ffffff;
    --color-text-primary: #1e293b;
    --color-text-secondary: #64748b;
    --color-border: #e2e8f0;
}
```

**TR-FE-005:** Responsive breakpoints:
```css
/* Mobile: < 768px */
/* Tablet: 768px - 1023px */
/* Desktop: >= 1024px */

@media (max-width: 767px) {
    /* Mobile styles */
}

@media (min-width: 768px) and (max-width: 1023px) {
    /* Tablet styles */
}

@media (min-width: 1024px) {
    /* Desktop styles */
}
```

**TR-FE-006:** Print styles in print.css:
```css
@media print {
    .no-print, nav, .btn, .alert {
        display: none !important;
    }
    
    body {
        background: white;
        color: black;
    }
}
```

### 5.3 JavaScript Architecture

**TR-FE-007:** JavaScript shall be modular using ES6 modules or IIFE patterns.

**TR-FE-008:** Common utilities in main.js:
```javascript
// Form validation helper
function validateForm(formId, rules) {
    const form = document.getElementById(formId);
    // validation logic
}

// Display toast notification
function showToast(message, type) {
    // notification logic
}

// Confirmation dialog
function confirmDelete(message) {
    return confirm(message);
}

// Format date
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-GB');
}
```

**TR-FE-009:** Chart initialization in charts.js:
```javascript
function initGradeDistributionChart(canvasId, data) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['A', 'B', 'C', 'D', 'F'],
            datasets: [{
                label: 'Number of Students',
                data: data,
                backgroundColor: [
                    '#16a34a', // A - Green
                    '#84cc16', // B - Light Green
                    '#eab308', // C - Yellow
                    '#ea580c', // D - Orange
                    '#dc2626'  // F - Red
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}

function initPassFailPieChart(canvasId, passCount, failCount) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Pass', 'Fail'],
            datasets: [{
                data: [passCount, failCount],
                backgroundColor: ['#16a34a', '#dc2626']
            }]
        },
        options: {
            responsive: true
        }
    });
}
```

### 5.4 Form Handling

**TR-FE-010:** All forms shall use POST method for data modifications.

**TR-FE-011:** CSRF protection shall be implemented using Flask-WTF or custom token.

**TR-FE-012:** Form submission flow:
1. Frontend validates input using JavaScript
2. If valid, submit form to backend
3. Backend validates again
4. Backend processes and returns response
5. Frontend displays success message or errors

**TR-FE-013:** Example form structure:
```html
<form id="studentForm" method="POST" action="/students/add">
    <div class="form-group">
        <label for="roll_number">Roll Number *</label>
        <input type="text" id="roll_number" name="roll_number" required>
        <span class="error-message" id="roll_number-error"></span>
    </div>
    <!-- more fields -->
    <button type="submit" class="btn btn-primary">Add Student</button>
</form>
```

### 5.5 Client-Side Search and Filter

**TR-FE-014:** Search shall be implemented using JavaScript array filtering:
```javascript
function filterTable(searchTerm, tableId, columnIndex) {
    const table = document.getElementById(tableId);
    const rows = table.getElementsByTagName('tr');
    
    for (let i = 1; i < rows.length; i++) {
        const cell = rows[i].getElementsByTagName('td')[columnIndex];
        if (cell) {
            const text = cell.textContent.toLowerCase();
            if (text.includes(searchTerm.toLowerCase())) {
                rows[i].style.display = '';
            } else {
                rows[i].style.display = 'none';
            }
        }
    }
}
```

**TR-FE-015:** Search shall debounce user input by 300ms to reduce frequent filtering.

### 5.6 Chart.js Integration

**TR-FE-016:** Chart.js shall be loaded from CDN in dashboard template:
```html
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
```

**TR-FE-017:** Charts shall be initialized after page load:
```javascript
document.addEventListener('DOMContentLoaded', function() {
    // Initialize charts with data from backend
    const gradeData = JSON.parse('{{ grade_data|tojson }}');
    initGradeDistributionChart('gradeChart', gradeData);
});
```

---

## 6. DATABASE ARCHITECTURE

### 6.1 Database Connection

**TR-DB-001:** Database connection shall use connection pooling to handle multiple requests efficiently.

**TR-DB-002:** Connection parameters:
- Host: Extracted from Supabase DATABASE_URL
- Port: 5432 (default PostgreSQL)
- Database: From Supabase project
- SSL Mode: require (mandatory for Supabase)

**TR-DB-003:** Connection pooling configuration (if using SQLAlchemy):
```python
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 5,
    'pool_recycle': 3600,
    'pool_pre_ping': True
}
```

**TR-DB-004:** Connection error handling:
```python
def get_db_connection():
    try:
        conn = psycopg2.connect(
            os.getenv('DATABASE_URL'),
            cursor_factory=RealDictCursor,
            sslmode='require',
            connect_timeout=10
        )
        return conn
    except psycopg2.OperationalError as e:
        app.logger.error(f'Database connection failed: {e}')
        raise
```

### 6.2 Query Patterns

**TR-DB-005:** All database queries shall use parameterized queries:
```python
# Correct (parameterized)
cursor.execute("SELECT * FROM students WHERE roll_number = %s", (roll_number,))

# NEVER do this (vulnerable to SQL injection)
cursor.execute(f"SELECT * FROM students WHERE roll_number = '{roll_number}'")
```

**TR-DB-006:** SELECT queries shall specify columns explicitly (avoid SELECT *):
```python
cursor.execute("""
    SELECT id, roll_number, name, email, date_of_birth, gender, contact_number
    FROM students
    WHERE id = %s
""", (student_id,))
```

**TR-DB-007:** INSERT queries shall return the generated ID:
```python
cursor.execute("""
    INSERT INTO students (roll_number, name, email, date_of_birth, gender, contact_number)
    VALUES (%s, %s, %s, %s, %s, %s)
    RETURNING id
""", (roll_number, name, email, dob, gender, contact))
new_id = cursor.fetchone()['id']
```

**TR-DB-008:** UPDATE queries shall check affected rows:
```python
cursor.execute("""
    UPDATE students
    SET name = %s, email = %s
    WHERE id = %s
""", (name, email, student_id))
if cursor.rowcount == 0:
    raise ValueError('Student not found')
```

**TR-DB-009:** DELETE queries shall use transactions:
```python
try:
    cursor.execute("DELETE FROM marks WHERE student_id = %s", (student_id,))
    cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
    conn.commit()
except Exception as e:
    conn.rollback()
    raise
```

### 6.3 Transaction Management

**TR-DB-010:** All data modifications shall use transactions with commit/rollback.

**TR-DB-011:** Transaction pattern:
```python
conn = get_db_connection()
cursor = conn.cursor()
try:
    # Execute one or more queries
    cursor.execute(query1, params1)
    cursor.execute(query2, params2)
    conn.commit()
except Exception as e:
    conn.rollback()
    app.logger.error(f'Transaction failed: {e}')
    raise
finally:
    cursor.close()
    conn.close()
```

### 6.4 Database Indexing Strategy

**TR-DB-012:** Indexes shall be created for frequently queried columns:
- students.roll_number (UNIQUE)
- students.(roll_number, date_of_birth) (for result lookup)
- subjects.subject_code (UNIQUE)
- marks.(student_id, subject_id) (UNIQUE composite)
- marks.student_id (foreign key)
- marks.subject_id (foreign key)

**TR-DB-013:** Index creation SQL (executed during database setup):
```sql
CREATE UNIQUE INDEX idx_students_roll_number ON students(roll_number);
CREATE INDEX idx_students_lookup ON students(roll_number, date_of_birth);
CREATE UNIQUE INDEX idx_subjects_code ON subjects(subject_code);
CREATE UNIQUE INDEX idx_marks_student_subject ON marks(student_id, subject_id);
CREATE INDEX idx_marks_student ON marks(student_id);
CREATE INDEX idx_marks_subject ON marks(subject_id);
```

---

## 7. DATABASE TABLES, FIELDS, RELATIONSHIPS, KEYS AND CONSTRAINTS

### 7.1 Table: admins

**TR-DB-TABLE-001:** Admin table specification:

| Column Name | Data Type | Constraints | Description | PRD Ref |
|-------------|-----------|-------------|-------------|---------|
| id | SERIAL | PRIMARY KEY | Auto-increment admin ID | DB-001 |
| username | VARCHAR(50) | UNIQUE, NOT NULL | Admin username for login | DB-001 |
| email | VARCHAR(100) | UNIQUE, NOT NULL | Admin email address | DB-001 |
| password_hash | VARCHAR(255) | NOT NULL | Bcrypt hashed password | DB-001, SEC-001 |
| full_name | VARCHAR(100) | NOT NULL | Admin display name | DB-001 |
| created_at | TIMESTAMP | DEFAULT NOW() | Account creation timestamp | DB-001 |
| last_login | TIMESTAMP | NULL | Last successful login time | DB-001 |

**TR-DB-TABLE-002:** CREATE TABLE SQL for admins:
```sql
CREATE TABLE admins (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP NULL
);
```

**TR-DB-TABLE-003:** Constraints on admins table:
- UNIQUE constraint on username prevents duplicate usernames
- UNIQUE constraint on email prevents duplicate emails
- NOT NULL on password_hash ensures every admin has a password

### 7.2 Table: students

**TR-DB-TABLE-004:** Students table specification:

| Column Name | Data Type | Constraints | Description | PRD Ref |
|-------------|-----------|-------------|-------------|---------|
| id | SERIAL | PRIMARY KEY | Auto-increment student ID | DB-002 |
| roll_number | VARCHAR(20) | UNIQUE, NOT NULL | Student roll number (unique identifier) | DB-002, FR-013 |
| name | VARCHAR(100) | NOT NULL | Student full name | DB-002, FR-013 |
| email | VARCHAR(100) | NULL | Student email (optional) | DB-002, FR-013 |
| date_of_birth | DATE | NOT NULL | Date of birth (for result lookup auth) | DB-002, FR-013 |
| gender | VARCHAR(10) | NOT NULL, CHECK (gender IN ('Male', 'Female', 'Other')) | Student gender | DB-002, FR-013 |
| contact_number | VARCHAR(15) | NULL | Contact number (optional) | DB-002, FR-013 |
| created_at | TIMESTAMP | DEFAULT NOW() | Record creation timestamp | DB-002 |
| updated_at | TIMESTAMP | DEFAULT NOW() | Record last update timestamp | DB-002 |

**TR-DB-TABLE-005:** CREATE TABLE SQL for students:
```sql
CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    roll_number VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NULL,
    date_of_birth DATE NOT NULL,
    gender VARCHAR(10) NOT NULL CHECK (gender IN ('Male', 'Female', 'Other')),
    contact_number VARCHAR(15) NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

**TR-DB-TABLE-006:** Constraints on students table:
- UNIQUE constraint on roll_number prevents duplicate enrollments
- CHECK constraint on gender ensures only valid values
- NOT NULL on date_of_birth required for result lookup authentication

**TR-DB-TABLE-007:** Composite index for result lookup optimization:
```sql
CREATE INDEX idx_students_lookup ON students(roll_number, date_of_birth);
```

### 7.3 Table: subjects

**TR-DB-TABLE-008:** Subjects table specification:

| Column Name | Data Type | Constraints | Description | PRD Ref |
|-------------|-----------|-------------|-------------|---------|
| id | SERIAL | PRIMARY KEY | Auto-increment subject ID | DB-003 |
| subject_code | VARCHAR(20) | UNIQUE, NOT NULL | Subject code (e.g., MATH101) | DB-003, FR-021 |
| subject_name | VARCHAR(100) | NOT NULL | Subject full name | DB-003, FR-021 |
| max_marks | INTEGER | NOT NULL, CHECK (max_marks > 0) | Maximum marks for subject | DB-003, FR-021 |
| created_at | TIMESTAMP | DEFAULT NOW() | Record creation timestamp | DB-003 |
| updated_at | TIMESTAMP | DEFAULT NOW() | Record last update timestamp | DB-003 |

**TR-DB-TABLE-009:** CREATE TABLE SQL for subjects:
```sql
CREATE TABLE subjects (
    id SERIAL PRIMARY KEY,
    subject_code VARCHAR(20) UNIQUE NOT NULL,
    subject_name VARCHAR(100) NOT NULL,
    max_marks INTEGER NOT NULL CHECK (max_marks > 0),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

**TR-DB-TABLE-010:** Constraints on subjects table:
- UNIQUE constraint on subject_code prevents duplicate subject codes
- CHECK constraint ensures max_marks is always positive
- NOT NULL on all core fields ensures data integrity

### 7.4 Table: marks

**TR-DB-TABLE-011:** Marks table specification:

| Column Name | Data Type | Constraints | Description | PRD Ref |
|-------------|-----------|-------------|-------------|---------|
| id | SERIAL | PRIMARY KEY | Auto-increment marks ID | DB-004 |
| student_id | INTEGER | NOT NULL, FOREIGN KEY → students(id) | Reference to student | DB-004, FR-028 |
| subject_id | INTEGER | NOT NULL, FOREIGN KEY → subjects(id) | Reference to subject | DB-004, FR-028 |
| marks_obtained | INTEGER | NOT NULL, CHECK (marks_obtained >= 0) | Marks scored by student | DB-004, FR-028 |
| is_absent | BOOLEAN | DEFAULT FALSE | Whether student was absent | DB-004, FR-035 |
| created_at | TIMESTAMP | DEFAULT NOW() | Record creation timestamp | DB-004 |
| updated_at | TIMESTAMP | DEFAULT NOW() | Record last update timestamp | DB-004 |

**TR-DB-TABLE-012:** Composite unique constraint on marks:
```sql
CONSTRAINT unique_student_subject UNIQUE (student_id, subject_id)
```

**TR-DB-TABLE-013:** CREATE TABLE SQL for marks:
```sql
CREATE TABLE marks (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL,
    subject_id INTEGER NOT NULL,
    marks_obtained INTEGER NOT NULL CHECK (marks_obtained >= 0),
    is_absent BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT unique_student_subject UNIQUE (student_id, subject_id),
    CONSTRAINT fk_marks_student 
        FOREIGN KEY (student_id) 
        REFERENCES students(id) 
        ON DELETE CASCADE,
    CONSTRAINT fk_marks_subject 
        FOREIGN KEY (subject_id) 
        REFERENCES subjects(id) 
        ON DELETE RESTRICT
);
```

**TR-DB-TABLE-014:** Foreign key constraints:
- CASCADE on student deletion: When a student is deleted, all their marks are automatically deleted
- RESTRICT on subject deletion: Cannot delete a subject if marks records exist for it

### 7.5 Database Relationships

**TR-DB-REL-001:** Entity Relationship Diagram:

```
┌─────────────────┐
│     admins      │
│─────────────────│
│ id (PK)         │
│ username (UQ)   │
│ email (UQ)      │
│ password_hash   │
│ full_name       │
└─────────────────┘
        │
        │ manages (conceptual, no FK)
        │
        ▼
┌─────────────────┐         ┌─────────────────┐
│    students     │         │    subjects     │
│─────────────────│         │─────────────────│
│ id (PK)         │         │ id (PK)         │
│ roll_number (UQ)│         │ subject_code(UQ)│
│ name            │         │ subject_name    │
│ date_of_birth   │         │ max_marks       │
│ gender          │         └─────────────────┘
└─────────────────┘                  │
        │                            │
        │ 1                     1    │
        │                            │
        │      ┌─────────────────┐   │
        └──────┤     marks       ├───┘
            N  │─────────────────│  N
               │ id (PK)         │
               │ student_id (FK) │
               │ subject_id (FK) │
               │ marks_obtained  │
               │ is_absent       │
               └─────────────────┘
               (student_id, subject_id) UNIQUE
```

**TR-DB-REL-002:** Relationship cardinality:
- One Student → Many Marks (1:N)
- One Subject → Many Marks (1:N)
- One Marks → One Student (N:1)
- One Marks → One Subject (N:1)
- Unique constraint prevents duplicate (student, subject) combinations

**TR-DB-REL-003:** Referential integrity rules:
- When student deleted → CASCADE delete all related marks (FR-038)
- When subject deleted → RESTRICT if marks exist (FR-051)
- Cannot insert marks for non-existent student or subject
- marks.marks_obtained must be ≤ subjects.max_marks (enforced at application level)

### 7.6 Data Integrity Constraints

**TR-DB-INTEGRITY-001:** Application-level validation requirements:
- marks.marks_obtained ≤ subjects.max_marks (cannot be enforced by CHECK constraint due to cross-table dependency)
- students.date_of_birth must be in the past
- students.contact_number must be exactly 10 digits if provided
- students.email must be valid email format if provided

**TR-DB-INTEGRITY-002:** Database-level integrity guaranteed by:
- PRIMARY KEY constraints prevent duplicate IDs
- UNIQUE constraints prevent duplicate roll_numbers, subject_codes, and (student_id, subject_id) pairs
- FOREIGN KEY constraints ensure referential integrity
- CHECK constraints enforce value ranges (max_marks > 0, marks_obtained >= 0)
- NOT NULL constraints prevent missing required data

### 7.7 Sample Data Requirements

**TR-DB-SAMPLE-001:** Initial admin account (password to be hashed with bcrypt):
```sql
INSERT INTO admins (username, email, password_hash, full_name)
VALUES ('admin', 'admin@resultportal.com', '$[hashed_password]', 'System Administrator');
```

**TR-DB-SAMPLE-002:** Sample students (at least 15 for demo):
- Varied names, roll numbers 2024001-2024015
- Mixed genders
- DOB around 2005 (18-19 years old)
- Some with email/contact, some without

**TR-DB-SAMPLE-003:** Sample subjects (6 subjects):
- MATH101 - Mathematics - 100 marks
- SCI102 - Science - 100 marks
- ENG103 - English - 100 marks
- CS104 - Computer Science - 100 marks
- SS105 - Social Studies - 100 marks
- PHY106 - Physics - 100 marks

**TR-DB-SAMPLE-004:** Sample marks distribution:
- 4 students with Grade A (85-95 in all subjects)
- 3 students with Grade C (60-74 in all subjects)
- 2 students with Grade D (40-59 in all subjects)
- 2 students failing (below 40 in at least one subject)
- 1 student marked absent in one subject
- 1 student with incomplete marks (only 3/6 subjects)

---

## 8. API / ROUTE SPECIFICATIONS

### 8.1 Route Naming Convention

**TR-API-001:** All routes shall follow RESTful naming conventions where applicable.

**TR-API-002:** Route structure:
- GET /resource - List all resources
- GET /resource/<id> - View specific resource
- GET /resource/add - Display add form
- POST /resource/add - Create new resource
- GET /resource/<id>/edit - Display edit form
- POST /resource/<id>/edit - Update existing resource
- POST /resource/<id>/delete - Delete resource

### 8.2 Authentication Routes

**TR-API-AUTH-001:** Login route (GET /login, POST /login)
```python
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Validate credentials
        # Create session
        # Redirect to dashboard
    return render_template('auth/login.html')
```
**Maps to:** FR-001, FR-002, FR-003, FR-004

**TR-API-AUTH-002:** Logout route (POST /logout)
```python
@bp.route('/logout', methods=['POST'])
@login_required
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
```
**Maps to:** FR-006, FR-007

### 8.3 Dashboard Routes

**TR-API-DASH-001:** Dashboard route (GET /dashboard)
```python
@bp.route('/dashboard')
@login_required
def index():
    # Calculate metrics
    # Fetch top performers
    # Prepare chart data
    return render_template('dashboard/index.html', 
                         metrics=metrics, 
                         charts=charts)
```
**Maps to:** FR-011 through FR-021

### 8.4 Student Management Routes

**TR-API-STU-001:** List students (GET /students)
```python
@bp.route('/students')
@login_required
def list():
    # Fetch all students
    # Apply search/filter if query params exist
    return render_template('students/list.html', students=students)
```
**Maps to:** FR-014, FR-015, FR-016

**TR-API-STU-002:** Add student form (GET /students/add)
```python
@bp.route('/students/add', methods=['GET'])
@login_required
def add_form():
    return render_template('students/add.html')
```

**TR-API-STU-003:** Create student (POST /students/add)
```python
@bp.route('/students/add', methods=['POST'])
@login_required
def add():
    # Validate input
    # Check duplicate roll_number
    # Insert into database
    # Redirect with success message
```
**Maps to:** FR-013, FR-019, FR-020, FR-023

**TR-API-STU-004:** Edit student form (GET /students/<id>/edit)
```python
@bp.route('/students/<int:id>/edit', methods=['GET'])
@login_required
def edit_form(id):
    # Fetch student by ID
    return render_template('students/edit.html', student=student)
```
**Maps to:** FR-031, FR-032

**TR-API-STU-005:** Update student (POST /students/<id>/edit)
```python
@bp.route('/students/<int:id>/edit', methods=['POST'])
@login_required
def edit(id):
    # Validate input
    # Update database
    # Redirect with success message
```
**Maps to:** FR-017, FR-033, FR-034

**TR-API-STU-006:** Delete student (POST /students/<id>/delete)
```python
@bp.route('/students/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    # Check for existing marks
    # If marks exist, confirm with user
    # Delete student (CASCADE deletes marks)
    # Redirect with success message
```
**Maps to:** FR-018, FR-036, FR-037, FR-038

### 8.5 Subject Management Routes

**TR-API-SUB-001:** List subjects (GET /subjects)
**TR-API-SUB-002:** Add subject (GET/POST /subjects/add)
**TR-API-SUB-003:** Edit subject (GET/POST /subjects/<id>/edit)
**TR-API-SUB-004:** Delete subject (POST /subjects/<id>/delete)
**Maps to:** FR-021 through FR-027, FR-039 through FR-051

### 8.6 Marks Management Routes

**TR-API-MARKS-001:** List marks (GET /marks)
**TR-API-MARKS-002:** Add marks (GET/POST /marks/add)
**TR-API-MARKS-003:** Edit marks (GET/POST /marks/<id>/edit)
**TR-API-MARKS-004:** Delete marks (POST /marks/<id>/delete)
**Maps to:** FR-028 through FR-035, FR-052 through FR-071

### 8.7 Results Routes

**TR-API-RES-001:** Admin results list (GET /results)
```python
@bp.route('/results')
@login_required
def list():
    # Calculate results for all students
    # Apply filters if query params
    return render_template('results/admin_list.html', results=results)
```
**Maps to:** FR-081, FR-082, FR-083

**TR-API-RES-002:** Student result lookup form (GET /result-lookup)
```python
@bp.route('/result-lookup', methods=['GET'])
def lookup_form():
    return render_template('results/student_lookup.html')
```
**Maps to:** FR-059

**TR-API-RES-003:** Student result display (POST /result-lookup)
```python
@bp.route('/result-lookup', methods=['POST'])
def lookup():
    roll_number = request.form.get('roll_number')
    dob = request.form.get('date_of_birth')
    
    # Validate both fields provided
    # Query student with roll_number AND dob
    # If not found, show error
    # Fetch marks for student
    # Calculate results
    # Display result page
    return render_template('results/student_result.html', result=result)
```
**Maps to:** FR-060, FR-086 through FR-101

### 8.8 Analysis Routes

**TR-API-ANAL-001:** Analysis dashboard (GET /analysis)
```python
@bp.route('/analysis')
@login_required
def index():
    # Calculate class statistics
    # Calculate subject-wise statistics
    # Identify top performers, weak/strong subjects
    # Prepare chart data
    return render_template('analysis/index.html', 
                         stats=stats, 
                         charts=charts)
```
**Maps to:** FR-102 through FR-117

### 8.9 Reports Routes

**TR-API-REP-001:** Reports menu (GET /reports)
**TR-API-REP-002:** Individual student report (GET /reports/individual?student_id=X)
**TR-API-REP-003:** Class results report (GET /reports/class)
**TR-API-REP-004:** Subject performance report (GET /reports/subjects)
**TR-API-REP-005:** Overall analysis report (GET /reports/analysis)
**Maps to:** FR-118 through FR-128

### 8.10 Request/Response Formats

**TR-API-FORMAT-001:** All POST requests shall use form-encoded data (application/x-www-form-urlencoded).

**TR-API-FORMAT-002:** All responses shall be HTML rendered by Jinja2 templates.

**TR-API-FORMAT-003:** Flash messages shall be used for success/error notifications:
```python
flash('Student added successfully!', 'success')
flash('Invalid credentials', 'error')
```

**TR-API-FORMAT-004:** Form data validation errors shall be passed to template:
```python
return render_template('students/add.html', errors=errors, form_data=request.form)
```

---

## 9. AUTHENTICATION AND AUTHORIZATION

### 9.1 Admin Authentication

**TR-AUTH-001:** Password hashing specification:
```python
import bcrypt

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def check_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
```
**Maps to:** FR-002, SEC-001

**TR-AUTH-002:** Login validation flow:
1. Receive email/username and password from form
2. Query admins table for matching email or username
3. If not found, return "Invalid credentials" (generic message)
4. If found, verify password using bcrypt.checkpw()
5. If password matches, create session and redirect to dashboard
6. If password doesn't match, return "Invalid credentials"
7. Never reveal whether username or password was incorrect
**Maps to:** FR-001, FR-004, FR-005, SEC-008

**TR-AUTH-003:** Session creation:
```python
from flask import session
from datetime import timedelta

def create_admin_session(admin):
    session.clear()
    session['admin_id'] = admin['id']
    session['username'] = admin['username']
    session['email'] = admin['email']
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)
```
**Maps to:** FR-003

**TR-AUTH-004:** Session validation decorator:
```python
from functools import wraps
from flask import session, redirect, url_for

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Please login to access this page', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function
```
**Maps to:** FR-008

### 9.2 Student Authentication

**TR-AUTH-005:** Student result lookup authentication:
```python
def authenticate_student(roll_number: str, dob: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, roll_number, name
        FROM students
        WHERE roll_number = %s AND date_of_birth = %s
    """, (roll_number, dob))
    student = cursor.fetchone()
    cursor.close()
    conn.close()
    return student
```
**Maps to:** FR-060, FR-086, FR-087, FR-088, SEC-011

**TR-AUTH-006:** Student authentication rules:
- Must provide both roll_number AND date_of_birth
- Both must match exactly (case-sensitive for roll_number)
- No session created (stateless lookup)
- Cannot access other students' results (only matching record returned)
**Maps to:** FR-071, SEC-012

### 9.3 Session Management

**TR-AUTH-007:** Session configuration:
```python
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')  # 256-bit random hex string
app.config['SESSION_COOKIE_NAME'] = 'result_system_session'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = True  # Only in production (HTTPS)
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30 minutes in seconds
```
**Maps to:** SEC-003, SEC-004, SEC-005

**TR-AUTH-008:** Session timeout handling:
- Session automatically expires after 30 minutes of inactivity
- Next request after expiry redirects to login page
- Flash message: "Your session has expired. Please login again."
**Maps to:** SEC-006, ERR-002

**TR-AUTH-009:** Logout implementation:
```python
@bp.route('/logout', methods=['POST'])
@login_required
def logout():
    session.clear()
    flash('You have been logged out successfully', 'success')
    return redirect(url_for('auth.login'))
```
**Maps to:** FR-007

### 9.4 Authorization

**TR-AUTH-010:** Route protection:
- All admin routes must use @login_required decorator
- Public routes: /login, /result-lookup (no authentication)
- Student lookup does not grant access to admin routes

**TR-AUTH-011:** Unauthorized access handling:
```python
# In login_required decorator
if 'admin_id' not in session:
    return redirect(url_for('auth.login'))
```
**Maps to:** SEC-009, SEC-010, SEC-013

---

## 10. STUDENT MANAGEMENT TECHNICAL REQUIREMENTS

### 10.1 Create Student

**TR-STU-CREATE-001:** Student creation function:
```python
def create_student(data: dict) -> int:
    # Validate all fields
    errors = validate_student_data(data)
    if errors:
        raise ValidationError(errors)
    
    # Check duplicate roll_number
    if check_duplicate_roll_number(data['roll_number']):
        raise ValidationError({'roll_number': 'Roll number already exists'})
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO students (roll_number, name, email, date_of_birth, gender, contact_number)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (data['roll_number'], data['name'], data.get('email'), 
              data['date_of_birth'], data['gender'], data.get('contact_number')))
        new_id = cursor.fetchone()['id']
        conn.commit()
        return new_id
    except Exception as e:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()
```
**Maps to:** FR-013, FR-019, FR-020, FR-023

### 10.2 Update Student

**TR-STU-UPDATE-001:** Student update function:
```python
def update_student(student_id: int, data: dict) -> bool:
    errors = validate_student_data(data)
    if errors:
        raise ValidationError(errors)
    
    # Check if roll_number changed and not duplicate
    if data['roll_number'] != get_student_roll_number(student_id):
        if check_duplicate_roll_number(data['roll_number']):
            raise ValidationError({'roll_number': 'Roll number already exists'})
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE students
            SET roll_number = %s, name = %s, email = %s, 
                date_of_birth = %s, gender = %s, contact_number = %s,
                updated_at = NOW()
            WHERE id = %s
        """, (data['roll_number'], data['name'], data.get('email'),
              data['date_of_birth'], data['gender'], data.get('contact_number'), 
              student_id))
        
        if cursor.rowcount == 0:
            raise ValueError('Student not found')
        
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()
```
**Maps to:** FR-017, FR-033, FR-034

### 10.3 Delete Student

**TR-STU-DELETE-001:** Student deletion with marks check:
```python
def delete_student(student_id: int, confirmed: bool = False) -> dict:
    # Check for existing marks
    marks_count = get_student_marks_count(student_id)
    
    if marks_count > 0 and not confirmed:
        return {
            'status': 'confirmation_required',
            'message': f'This student has {marks_count} marks records. Deleting will remove all marks. Confirm?',
            'marks_count': marks_count
        }
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # CASCADE delete will automatically remove marks
        cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
        
        if cursor.rowcount == 0:
            raise ValueError('Student not found')
        
        conn.commit()
        return {'status': 'success', 'marks_deleted': marks_count}
    except Exception as e:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()
```
**Maps to:** FR-018, FR-036, FR-037, FR-038

### 10.4 Search and Filter

**TR-STU-SEARCH-001:** Student search implementation:
```python
def search_students(search_term: str = None, gender_filter: str = None):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM students WHERE 1=1"
    params = []
    
    if search_term:
        query += " AND (roll_number ILIKE %s OR name ILIKE %s)"
        params.extend([f'%{search_term}%', f'%{search_term}%'])
    
    if gender_filter and gender_filter != 'All':
        query += " AND gender = %s"
        params.append(gender_filter)
    
    query += " ORDER BY roll_number"
    
    cursor.execute(query, params)
    students = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return students
```
**Maps to:** FR-015, FR-016, FR-029, FR-030

---

## 11. SUBJECT MANAGEMENT TECHNICAL REQUIREMENTS

**TR-SUB-001:** Subject management follows same patterns as student management with these specifics:

- CREATE: Check duplicate subject_code, validate max_marks > 0
- UPDATE: Check duplicate subject_code if changed, validate max_marks
- DELETE: RESTRICT if marks records exist (cannot delete)
- SEARCH: Filter by subject_code or subject_name

**TR-SUB-DELETE-001:** Subject deletion with marks check:
```python
def delete_subject(subject_id: int) -> dict:
    # Check for existing marks
    marks_count = get_subject_marks_count(subject_id)
    
    if marks_count > 0:
        return {
            'status': 'error',
            'message': 'Cannot delete subject. Marks records exist for this subject.'
        }
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM subjects WHERE id = %s", (subject_id,))
        
        if cursor.rowcount == 0:
            raise ValueError('Subject not found')
        
        conn.commit()
        return {'status': 'success'}
    except Exception as e:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()
```
**Maps to:** FR-025, FR-050, FR-051

---

## 12. MARKS MANAGEMENT TECHNICAL REQUIREMENTS

### 12.1 Create Marks

**TR-MARKS-CREATE-001:** Marks creation with validation:
```python
def create_marks(student_id: int, subject_id: int, marks_obtained: int, is_absent: bool = False):
    # Get subject max_marks for validation
    subject = get_subject_by_id(subject_id)
    if not subject:
        raise ValueError('Subject not found')
    
    # Validate marks
    if marks_obtained < 0:
        raise ValidationError('Marks cannot be negative')
    
    if marks_obtained > subject['max_marks']:
        raise ValidationError(f'Marks cannot exceed maximum marks ({subject["max_marks"]})')
    
    # If absent, marks should be 0
    if is_absent:
        marks_obtained = 0
    
    # Check for duplicate
    if check_duplicate_marks(student_id, subject_id):
        raise ValidationError('Marks already exist for this student-subject combination')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO marks (student_id, subject_id, marks_obtained, is_absent)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (student_id, subject_id, marks_obtained, is_absent))
        new_id = cursor.fetchone()['id']
        conn.commit()
        return new_id
    except Exception as e:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()
```
**Maps to:** FR-028, FR-033, FR-034, FR-035, FR-056, FR-057, FR-058, FR-059, FR-060, FR-061, FR-062

### 12.2 Marks Validation

**TR-MARKS-VAL-001:** Marks validation rules:
```python
def validate_marks(marks_obtained: int, max_marks: int, is_absent: bool) -> dict:
    errors = {}
    
    if marks_obtained < 0:
        errors['marks_obtained'] = 'Marks cannot be negative'
    
    if marks_obtained > max_marks:
        errors['marks_obtained'] = f'Marks cannot exceed {max_marks}'
    
    if is_absent and marks_obtained != 0:
        errors['marks_obtained'] = 'Marks must be 0 for absent students'
    
    return errors
```
**Maps to:** FR-033, FR-058, FR-060, VAL-030 through VAL-040

---

## 13. RESULT CALCULATION LOGIC

### 13.1 Result Calculation Functions

**TR-CALC-001:** Calculate total marks:
```python
def calculate_total_marks(student_id: int) -> dict:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            SUM(m.marks_obtained) as total_obtained,
            SUM(s.max_marks) as total_maximum,
            COUNT(*) as subjects_appeared
        FROM marks m
        JOIN subjects s ON m.subject_id = s.id
        WHERE m.student_id = %s
    """, (student_id,))
    
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return {
        'total_obtained': result['total_obtained'] or 0,
        'total_maximum': result['total_maximum'] or 0,
        'subjects_appeared': result['subjects_appeared'] or 0
    }
```
**Maps to:** FR-036, FR-073, FR-074

**TR-CALC-002:** Calculate percentage:
```python
def calculate_percentage(total_obtained: int, total_maximum: int) -> float:
    if total_maximum == 0:
        return 0.0
    percentage = (total_obtained / total_maximum) * 100
    return round(percentage, 2)
```
**Maps to:** FR-037, FR-075

**TR-CALC-003:** Assign grade:
```python
def assign_grade(percentage: float) -> str:
    if percentage >= 90:
        return 'A'
    elif percentage >= 75:
        return 'B'
    elif percentage >= 60:
        return 'C'
    elif percentage >= 40:
        return 'D'
    else:
        return 'F'
```
**Maps to:** FR-038, FR-076

**TR-CALC-004:** Determine pass/fail status:
```python
def determine_pass_fail(student_id: int) -> dict:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if absent in any subject
    cursor.execute("""
        SELECT COUNT(*) as absent_count
        FROM marks
        WHERE student_id = %s AND is_absent = TRUE
    """, (student_id,))
    absent_count = cursor.fetchone()['absent_count']
    
    if absent_count > 0:
        return {'status': 'FAIL', 'reason': 'Absent in one or more subjects'}
    
    # Check each subject for passing marks (40% of max_marks)
    cursor.execute("""
        SELECT 
            s.subject_name,
            m.marks_obtained,
            s.max_marks,
            (s.max_marks * 0.40) as passing_marks
        FROM marks m
        JOIN subjects s ON m.subject_id = s.id
        WHERE m.student_id = %s
    """, (student_id,))
    
    subjects = cursor.fetchall()
    failed_subjects = []
    
    for subject in subjects:
        if subject['marks_obtained'] < subject['passing_marks']:
            failed_subjects.append(subject['subject_name'])
    
    cursor.close()
    conn.close()
    
    if failed_subjects:
        return {
            'status': 'FAIL',
            'reason': f'Failed in: {", ".join(failed_subjects)}'
        }
    
    # Check overall percentage
    totals = calculate_total_marks(student_id)
    percentage = calculate_percentage(totals['total_obtained'], totals['total_maximum'])
    
    if percentage < 40:
        return {'status': 'FAIL', 'reason': 'Overall percentage below 40%'}
    
    return {'status': 'PASS', 'reason': 'Passed all subjects'}
```
**Maps to:** FR-039, FR-077, FR-078, FR-079, FR-080

### 13.2 Complete Result Generation

**TR-CALC-005:** Generate complete result:
```python
def generate_result(student_id: int) -> dict:
    student = get_student_by_id(student_id)
    if not student:
        return None
    
    # Check if all subjects have marks
    total_subjects = get_total_subjects_count()
    marks_count = get_student_marks_count(student_id)
    
    if marks_count < total_subjects:
        return {
            'status': 'incomplete',
            'message': 'Result not yet published',
            'subjects_completed': marks_count,
            'subjects_total': total_subjects
        }
    
    # Calculate results
    totals = calculate_total_marks(student_id)
    percentage = calculate_percentage(totals['total_obtained'], totals['total_maximum'])
    grade = assign_grade(percentage)
    status_info = determine_pass_fail(student_id)
    
    # Fetch subject-wise details
    subject_results = get_subject_wise_results(student_id)
    
    return {
        'student': student,
        'total_obtained': totals['total_obtained'],
        'total_maximum': totals['total_maximum'],
        'percentage': percentage,
        'grade': grade,
        'status': status_info['status'],
        'status_reason': status_info['reason'],
        'subjects': subject_results
    }
```
**Maps to:** FR-072, FR-085, FR-090, FR-091, FR-092

---

## 14. RESULT ANALYSIS AND ANALYTICS

### 14.1 Class Statistics

**TR-ANAL-001:** Calculate class average:
```python
def calculate_class_average() -> float:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT s.id, s.name
        FROM students s
        WHERE (
            SELECT COUNT(*) 
            FROM marks m 
            WHERE m.student_id = s.id
        ) = (SELECT COUNT(*) FROM subjects)
    """)
    
    students_with_complete_results = cursor.fetchall()
    
    if not students_with_complete_results:
        return 0.0
    
    total_percentage = 0
    for student in students_with_complete_results:
        result = generate_result(student['id'])
        total_percentage += result['percentage']
    
    cursor.close()
    conn.close()
    
    return round(total_percentage / len(students_with_complete_results), 2)
```
**Maps to:** FR-042, FR-103, ANAL-001

**TR-ANAL-002:** Calculate pass/fail statistics:
```python
def calculate_pass_fail_stats() -> dict:
    # Get all students with complete results
    students = get_students_with_complete_results()
    
    pass_count = 0
    fail_count = 0
    
    for student in students:
        result = generate_result(student['id'])
        if result['status'] == 'PASS':
            pass_count += 1
        else:
            fail_count += 1
    
    total = pass_count + fail_count
    pass_percentage = (pass_count / total * 100) if total > 0 else 0
    fail_percentage = (fail_count / total * 100) if total > 0 else 0
    
    return {
        'pass_count': pass_count,
        'fail_count': fail_count,
        'total': total,
        'pass_percentage': round(pass_percentage, 2),
        'fail_percentage': round(fail_percentage, 2)
    }
```
**Maps to:** FR-008, FR-009, FR-015, FR-016, ANAL-003

### 14.2 Subject Statistics

**TR-ANAL-003:** Calculate subject-wise average:
```python
def calculate_subject_averages() -> list:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            s.id,
            s.subject_name,
            s.max_marks,
            AVG(m.marks_obtained) as average_marks,
            MAX(m.marks_obtained) as highest_marks,
            MIN(m.marks_obtained) as lowest_marks,
            COUNT(*) as total_students
        FROM subjects s
        JOIN marks m ON s.id = m.subject_id
        GROUP BY s.id, s.subject_name, s.max_marks
        ORDER BY s.subject_name
    """)
    
    subjects = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return subjects
```
**Maps to:** FR-043, FR-104, ANAL-002

### 14.3 Grade Distribution

**TR-ANAL-004:** Calculate grade distribution:
```python
def calculate_grade_distribution() -> dict:
    students = get_students_with_complete_results()
    
    distribution = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
    
    for student in students:
        result = generate_result(student['id'])
        distribution[result['grade']] += 1
    
    return distribution
```
**Maps to:** FR-050, FR-111

### 14.4 Top Performers

**TR-ANAL-005:** Get top performers:
```python
def get_top_performers(limit: int = 10) -> list:
    students = get_students_with_complete_results()
    
    results = []
    for student in students:
        result = generate_result(student['id'])
        results.append({
            'student_id': student['id'],
            'roll_number': student['roll_number'],
            'name': student['name'],
            'percentage': result['percentage'],
            'grade': result['grade']
        })
    
    # Sort by percentage descending
    results.sort(key=lambda x: x['percentage'], reverse=True)
    
    return results[:limit]
```
**Maps to:** FR-011, FR-048, FR-109

---

## 15. VALIDATION RULES

### 15.1 Admin Validation Rules

**TR-VAL-001:** Admin username validation:
- Format: Alphanumeric only, no spaces
- Length: 3-50 characters
- Pattern: `^[a-zA-Z0-9_]+$`
- Required: Yes
- **Maps to:** VAL-001

**TR-VAL-002:** Admin email validation:
- Format: Valid email format
- Length: Max 100 characters
- Pattern: `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`
- Required: Yes
- **Maps to:** VAL-002

**TR-VAL-003:** Admin password validation:
- Length: Minimum 8 characters
- Complexity: At least one uppercase, one lowercase, one digit
- Required: Yes
- **Maps to:** VAL-003, SEC-001

**TR-VAL-004:** Admin full name validation:
- Length: 2-100 characters
- Format: Letters and spaces only
- Pattern: `^[a-zA-Z\s]+$`
- Required: Yes
- **Maps to:** VAL-004

### 15.2 Student Validation Rules

**TR-VAL-005:** Roll number validation:
- Format: Alphanumeric with optional hyphens
- Length: 5-20 characters
- Pattern: `^[A-Z0-9-]+$`
- Required: Yes
- Unique: Yes
- **Maps to:** VAL-005, FR-013

**TR-VAL-006:** Student name validation:
- Length: 2-100 characters
- Format: Letters, spaces, dots, apostrophes only
- Pattern: `^[a-zA-Z\s.'-]+$`
- Required: Yes
- **Maps to:** VAL-006, FR-013

**TR-VAL-007:** Student email validation:
- Format: Valid email format (if provided)
- Length: Max 100 characters
- Pattern: `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`
- Required: No
- **Maps to:** VAL-007, FR-013

**TR-VAL-008:** Date of birth validation:
- Format: YYYY-MM-DD
- Range: Must be between 5 and 100 years ago
- Logic: `today - 100 years <= DOB <= today - 5 years`
- Required: Yes
- **Maps to:** VAL-008, FR-013, FR-079

**TR-VAL-009:** Gender validation:
- Allowed values: 'Male', 'Female', 'Other'
- Case-sensitive: Yes
- Required: Yes
- **Maps to:** VAL-009, FR-013

**TR-VAL-010:** Contact number validation:
- Format: Digits, spaces, hyphens, plus sign only
- Length: 10-15 characters
- Pattern: `^[\+0-9\s-]{10,15}$`
- Required: No
- **Maps to:** VAL-010, FR-013

### 15.3 Subject Validation Rules

**TR-VAL-011:** Subject code validation:
- Format: Uppercase letters and digits
- Length: 3-10 characters
- Pattern: `^[A-Z0-9]+$`
- Required: Yes
- Unique: Yes
- **Maps to:** VAL-011, FR-032

**TR-VAL-012:** Subject name validation:
- Length: 3-100 characters
- Format: Letters, digits, spaces, ampersand
- Pattern: `^[a-zA-Z0-9\s&]+$`
- Required: Yes
- **Maps to:** VAL-012, FR-032

**TR-VAL-013:** Total marks validation:
- Type: Integer
- Range: 1 to 1000
- Default: 100
- Required: Yes
- **Maps to:** VAL-013, FR-032

**TR-VAL-014:** Passing marks validation:
- Type: Integer
- Range: 1 to total_marks
- Logic: `passing_marks < total_marks`
- Required: Yes
- **Maps to:** VAL-014, FR-032

### 15.4 Marks Validation Rules

**TR-VAL-015:** Marks obtained validation:
- Type: Integer or Decimal (up to 2 decimal places)
- Range: 0 to subject.total_marks
- Logic: `0 <= marks_obtained <= subject.total_marks`
- Required: Yes
- **Maps to:** VAL-015, FR-049

**TR-VAL-016:** Student-Subject uniqueness validation:
- Logic: Only one marks entry per (student_id, subject_id) combination
- Enforced by: Database UNIQUE constraint
- **Maps to:** VAL-016, FR-049

**TR-VAL-017:** Student existence validation:
- Logic: student_id must exist in students table
- Enforced by: Foreign key constraint
- **Maps to:** VAL-017, FR-049

**TR-VAL-018:** Subject existence validation:
- Logic: subject_id must exist in subjects table
- Enforced by: Foreign key constraint
- **Maps to:** VAL-018, FR-049

### 15.5 Result Lookup Validation Rules

**TR-VAL-019:** Roll number + DOB combination validation:
- Logic: Both must match a single student record
- Error message: "Invalid credentials" (do not reveal which field is wrong)
- **Maps to:** VAL-019, FR-079, SEC-023

**TR-VAL-020:** DOB format validation for lookup:
- Input format: Accepts YYYY-MM-DD, DD/MM/YYYY, DD-MM-YYYY
- Normalized to: YYYY-MM-DD for database query
- **Maps to:** VAL-020, FR-079

### 15.6 Validation Implementation

**TR-VAL-021:** Frontend validation (JavaScript):
`javascript
function validateRollNumber(rollNumber) {
    const pattern = /^[A-Z0-9-]{5,20}$/;
    if (!rollNumber) return { valid: false, message: 'Roll number is required' };
    if (!pattern.test(rollNumber)) return { valid: false, message: 'Invalid format' };
    return { valid: true };
}

function validateEmail(email) {
    const pattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    if (email && !pattern.test(email)) return { valid: false, message: 'Invalid email' };
    return { valid: true };
}

function validateDateOfBirth(dob) {
    const date = new Date(dob);
    const today = new Date();
    const minDate = new Date(today.getFullYear() - 100, today.getMonth(), today.getDate());
    const maxDate = new Date(today.getFullYear() - 5, today.getMonth(), today.getDate());
    
    if (!dob) return { valid: false, message: 'Date of birth is required' };
    if (date < minDate || date > maxDate) {
        return { valid: false, message: 'Invalid age (must be 5-100 years old)' };
    }
    return { valid: true };
}

function validateMarks(marks, totalMarks) {
    const marksNum = parseFloat(marks);
    if (isNaN(marksNum)) return { valid: false, message: 'Marks must be a number' };
    if (marksNum < 0 || marksNum > totalMarks) {
        return { valid: false, message: `Marks must be between 0 and ${totalMarks}` };
    }
    return { valid: true };
}
`

**TR-VAL-022:** Backend validation (Python):
`python
import re
from datetime import datetime, timedelta

def validate_roll_number(roll_number):
    if not roll_number:
        return False, 'Roll number is required'
    if not re.match(r'^[A-Z0-9-]{5,20}$', roll_number):
        return False, 'Invalid roll number format'
    return True, None

def validate_email(email):
    if email and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return False, 'Invalid email format'
    return True, None

def validate_date_of_birth(dob_str):
    try:
        dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
        today = datetime.now().date()
        min_date = today - timedelta(days=365*100)
        max_date = today - timedelta(days=365*5)
        
        if dob < min_date or dob > max_date:
            return False, 'Invalid age (must be 5-100 years old)'
        return True, None
    except ValueError:
        return False, 'Invalid date format'

def validate_marks(marks, total_marks):
    try:
        marks_num = float(marks)
        if marks_num < 0 or marks_num > total_marks:
            return False, f'Marks must be between 0 and {total_marks}'
        return True, None
    except ValueError:
        return False, 'Marks must be a valid number'

def validate_subject_code(code):
    if not code:
        return False, 'Subject code is required'
    if not re.match(r'^[A-Z0-9]{3,10}$', code):
        return False, 'Invalid subject code format'
    return True, None
`

**TR-VAL-023:** Validation shall occur in the following order:
1. Frontend JavaScript validation (immediate feedback)
2. Backend Python validation (security, cannot be bypassed)
3. Database constraints (final enforcement)

**TR-VAL-024:** Error messages shall be user-friendly and specific to the validation failure.

**TR-VAL-025:** All validation functions shall return tuple: `(is_valid: bool, error_message: str | None)`

---

## 16. ERROR HANDLING

### 16.1 Error Categories

**TR-ERR-001:** Application shall handle four error categories:
1. **Client Errors (4xx):** User input errors, validation failures
2. **Server Errors (5xx):** Application crashes, database failures
3. **Business Logic Errors:** Duplicate entries, referential integrity violations
4. **External Service Errors:** Database connection failures, timeout errors

**Maps to:** ERR-001 through ERR-010

### 16.2 Client Error Handling

**TR-ERR-002:** 400 Bad Request - Invalid form data:
- Trigger: Validation failures, malformed JSON
- Response: HTML form with error messages or JSON `{ "error": "message" }`
- User action: Fix input and resubmit
- **Maps to:** ERR-011, ERR-012

**TR-ERR-003:** 401 Unauthorized - Not logged in:
- Trigger: Accessing protected route without session
- Response: Redirect to /login with message "Please log in to continue"
- User action: Log in
- **Maps to:** ERR-013, SEC-020

**TR-ERR-004:** 403 Forbidden - Insufficient permissions:
- Trigger: Student trying to access admin routes
- Response: "Access denied" page
- User action: Contact administrator
- **Maps to:** ERR-014, SEC-021

**TR-ERR-005:** 404 Not Found - Resource doesn't exist:
- Trigger: Invalid URL, deleted record
- Response: Custom 404 page with navigation links
- User action: Use navigation to find correct page
- **Maps to:** ERR-015

**TR-ERR-006:** 405 Method Not Allowed - Wrong HTTP method:
- Trigger: GET request to POST-only route
- Response: "Method not allowed" message
- User action: Use correct HTTP method
- **Maps to:** ERR-016

### 16.3 Server Error Handling

**TR-ERR-007:** 500 Internal Server Error - Application crash:
- Trigger: Unhandled exceptions, code bugs
- Response: Generic error page "Something went wrong"
- Logging: Full stack trace to application logs
- User action: Try again later, contact support
- **Maps to:** ERR-020, ERR-021

**TR-ERR-008:** 503 Service Unavailable - Database connection failure:
- Trigger: Supabase down, network issues
- Response: "Service temporarily unavailable" page
- Logging: Connection error details
- User action: Wait and retry
- **Maps to:** ERR-022

**TR-ERR-009:** Request timeout handling:
- Timeout: 30 seconds for database queries
- Response: "Request timeout, please try again"
- Logging: Timeout details
- **Maps to:** ERR-023

### 16.4 Business Logic Error Handling

**TR-ERR-010:** Duplicate entry errors:
- Trigger: Inserting duplicate roll number or subject code
- Response: "Roll number already exists" or "Subject code already exists"
- User action: Use different roll number/subject code
- **Maps to:** ERR-030, FR-013, FR-032

**TR-ERR-011:** Foreign key constraint violation:
- Trigger: Deleting subject that has marks entries
- Response: "Cannot delete subject: marks entries exist"
- User action: Delete marks first, then subject
- **Maps to:** ERR-031, DB-007

**TR-ERR-012:** Check constraint violation:
- Trigger: Marks > total_marks, passing_marks >= total_marks
- Response: "Invalid marks: exceeds maximum"
- User action: Enter valid marks
- **Maps to:** ERR-032

**TR-ERR-013:** Record not found errors:
- Trigger: Editing/deleting non-existent record
- Response: "Record not found" with 404 status
- User action: Refresh page, select valid record
- **Maps to:** ERR-033

### 16.5 Error Response Format

**TR-ERR-014:** HTML form errors shall display inline:
`html
<div class="form-group">
    <label for="roll_number">Roll Number</label>
    <input type="text" id="roll_number" name="roll_number" class="{% if errors.roll_number %}error{% endif %}" value="{{ form_data.roll_number }}">
    {% if errors.roll_number %}
        <span class="error-message">{{ errors.roll_number }}</span>
    {% endif %}
</div>
`

**TR-ERR-015:** Flash messages for general errors:
`python
flash('Student added successfully', 'success')
flash('Invalid roll number format', 'error')
flash('Database connection failed', 'error')
`

**TR-ERR-016:** JSON API errors (if applicable):
`json
{
    "error": "Validation failed",
    "details": {
        "roll_number": "Roll number already exists",
        "email": "Invalid email format"
    },
    "status": 400
}
`

### 16.6 Error Logging Strategy

**TR-ERR-017:** Logging levels:
- **DEBUG:** Detailed diagnostic information (dev only)
- **INFO:** General informational messages (successful operations)
- **WARNING:** Unexpected but handled situations
- **ERROR:** Error events (caught exceptions)
- **CRITICAL:** Critical failures (application crash)

**TR-ERR-018:** What to log:
`python
# INFO level
app.logger.info(f'Student {roll_number} added successfully by admin {admin_id}')

# WARNING level
app.logger.warning(f'Login attempt with invalid username: {username}')

# ERROR level
app.logger.error(f'Database error: {str(e)}', exc_info=True)

# CRITICAL level
app.logger.critical(f'Failed to connect to database: {str(e)}')
`

**TR-ERR-019:** Log format:
`
2026-09-01 14:30:45,123 INFO: Student STU001 added by admin 1 [in routes/students.py:45]
2026-09-01 14:31:12,456 ERROR: Database error: connection timeout [in utils/db.py:23]
`

**TR-ERR-020:** Sensitive data exclusion:
- Never log passwords (plain or hashed)
- Never log full credit card numbers
- Log only last 4 digits of sensitive IDs if needed

### 16.7 Error Recovery Mechanisms

**TR-ERR-021:** Database transaction rollback:
`python
try:
    # multiple database operations
    conn.commit()
except Exception as e:
    conn.rollback()
    app.logger.error(f'Transaction failed: {e}')
    flash('Operation failed. Changes not saved.', 'error')
`

**TR-ERR-022:** Connection retry logic:
`python
def get_db_connection_with_retry(max_retries=3):
    for attempt in range(max_retries):
        try:
            return get_db_connection()
        except psycopg2.OperationalError as e:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # exponential backoff
                continue
            raise
`

**TR-ERR-023:** Graceful degradation:
- If analytics queries fail, show cached results or "Data unavailable"
- If Chart.js fails to load, show data in table format
- If database is slow, show loading spinner with timeout

**TR-ERR-024:** User-friendly error pages:
- 404: "Page not found" with link to dashboard
- 500: "Something went wrong" with contact information
- 503: "Service temporarily unavailable" with retry button

---

## 17. SECURITY REQUIREMENTS

### 17.1 Authentication Security

**TR-SEC-001:** Password hashing:
- Algorithm: bcrypt
- Cost factor: 12
- Implementation:
`python
import bcrypt

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12))

def verify_password(password, password_hash):
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
`
- **Maps to:** SEC-001, SEC-010

**TR-SEC-002:** Session security:
- Session cookie flags: HttpOnly=True, Secure=True (production), SameSite=Lax
- Session timeout: 30 minutes of inactivity
- Session regeneration: On login to prevent session fixation
- **Maps to:** SEC-011, SEC-012

**TR-SEC-003:** Login attempt limiting (optional but recommended):
- Max failed attempts: 5 per username per 15 minutes
- Lockout duration: 15 minutes
- Implementation: In-memory counter or database table
- **Maps to:** SEC-013

**TR-SEC-004:** Logout functionality:
- Clear all session data: `session.clear()`
- Redirect to login page
- **Maps to:** SEC-014

### 17.2 Authorization Security

**TR-SEC-005:** Route protection:
- All admin routes require `@login_required` decorator
- Student result lookup does NOT require authentication
- **Maps to:** SEC-020, SEC-021, FR-077

**TR-SEC-006:** Authorization decorator:
`python
from functools import wraps
from flask import session, redirect, url_for

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Please log in to access this page', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

# Usage
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard/index.html')
`
- **Maps to:** SEC-020

**TR-SEC-007:** Role-based access control:
- Only role: Admin (no student login)
- Student access: Public result lookup only (no authentication)
- **Maps to:** SEC-022, FR-001

### 17.3 Input Validation Security

**TR-SEC-008:** SQL injection prevention:
- Use parameterized queries exclusively
- NEVER concatenate user input into SQL strings
- Example:
`python
# Secure
cursor.execute("SELECT * FROM students WHERE roll_number = %s", (roll_number,))

# INSECURE - NEVER DO THIS
cursor.execute(f"SELECT * FROM students WHERE roll_number = '{roll_number}'")
`
- **Maps to:** SEC-030

**TR-SEC-009:** XSS (Cross-Site Scripting) prevention:
- Use Jinja2 auto-escaping (enabled by default)
- Escape user input in HTML: `{{ user_input }}` (auto-escaped)
- Use `{{ user_input|safe }}` only for trusted HTML
- **Maps to:** SEC-031

**TR-SEC-010:** HTML sanitization for form inputs:
`python
from markupsafe import escape

def sanitize_input(user_input):
    return escape(user_input)
`

**TR-SEC-011:** File upload restrictions (if added later):
- Allowed extensions: .pdf, .jpg, .png only
- Max file size: 5 MB
- Validate file content (magic bytes), not just extension
- **Maps to:** SEC-032

### 17.4 Data Protection

**TR-SEC-012:** Sensitive data handling:
- Passwords: Never stored in plain text, always bcrypt hashed
- Date of birth: Used for authentication, not displayed publicly
- Admin sessions: Encrypted with SECRET_KEY
- **Maps to:** SEC-040, SEC-001

**TR-SEC-013:** Database connection security:
- SSL/TLS required: `sslmode='require'`
- Connection string in environment variable (not in code)
- **Maps to:** SEC-041

**TR-SEC-014:** HTTPS enforcement:
- Production: All traffic over HTTPS (Render enforces this)
- Development: HTTP acceptable
- Configuration:
`python
if os.getenv('FLASK_ENV') == 'production':
    app.config['SESSION_COOKIE_SECURE'] = True
`
- **Maps to:** SEC-042

**TR-SEC-015:** Environment variable security:
- Store in .env file (not committed to Git)
- Add .env to .gitignore
- Use .env.example as template (no actual secrets)
- **Maps to:** SEC-043

### 17.5 Error Information Disclosure

**TR-SEC-016:** Production error messages:
- Generic messages only: "An error occurred"
- No stack traces exposed to users
- Detailed errors logged server-side only
- **Maps to:** SEC-050

**TR-SEC-017:** Debug mode:
- Disabled in production: `FLASK_ENV=production` or `FLASK_DEBUG=False`
- Enabled in development only
- **Maps to:** SEC-051

**TR-SEC-018:** Database error messages:
- Do not expose table names, column names, or SQL queries
- Example: "Database error" instead of "Column 'email' violates unique constraint"
- **Maps to:** SEC-052

### 17.6 Additional Security Measures

**TR-SEC-019:** CSRF protection (optional but recommended):
- Use Flask-WTF for CSRF tokens
- Protect all POST requests
- **Maps to:** SEC-060

**TR-SEC-020:** Secure headers (using Flask-Talisman or manual):
`python
@app.after_request
def set_secure_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    if os.getenv('FLASK_ENV') == 'production':
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response
`
- **Maps to:** SEC-061

**TR-SEC-021:** Rate limiting (optional):
- Limit login attempts: 5 per minute per IP
- Limit result lookups: 10 per minute per IP
- Implementation: Flask-Limiter or custom middleware
- **Maps to:** SEC-062

**TR-SEC-022:** Dependency security:
- Regularly update dependencies: `pip list --outdated`
- Review security advisories for Flask, bcrypt, psycopg2
- **Maps to:** SEC-063

---

## 18. PROJECT FOLDER/MODULE RESPONSIBILITIES

### 18.1 Root Structure

**TR-STRUCT-001:** Project root folder structure:
`
Student_Result_Analysis/
├── CODEBASE/
│   ├── BACKEND/                # Flask application code
│   ├── DATABASE/               # Database setup scripts (schema.sql)
│   └── FRONTEND/               # Static assets (CSS, JS, images) and templates
├── DOCS/
│   ├── PRD.md                  # Product Requirements Document
│   └── TRD.md                  # Technical Requirements Document (this file)
├── .gitignore                  # Git ignore file
├── README.md                   # Project documentation
└── requirements.txt            # Python dependencies (root or in BACKEND/)
`

### 18.2 BACKEND/ Folder Structure

**TR-STRUCT-002:** BACKEND/ detailed structure:
`
BACKEND/
├── app.py                      # Flask application entry point, initialization
├── config.py                   # Configuration management (dev/prod settings)
├── models.py                   # Database models (if using ORM) or SQL query functions
│
├── routes/                     # Route handlers (Blueprints)
│   ├── __init__.py
│   ├── auth.py                 # /login, /logout routes
│   ├── dashboard.py            # /dashboard route
│   ├── students.py             # /students/* CRUD routes
│   ├── subjects.py             # /subjects/* CRUD routes
│   ├── marks.py                # /marks/* CRUD routes
│   ├── results.py              # /results/* routes (admin list, student lookup)
│   ├── analysis.py             # /analysis/* routes (analytics dashboard)
│   └── reports.py              # /reports/* routes (PDF generation)
│
├── utils/                      # Utility modules
│   ├── __init__.py
│   ├── db.py                   # Database connection, query helpers
│   ├── validators.py           # Input validation functions
│   ├── calculations.py         # Result calculation logic (grade, percentage, status)
│   ├── helpers.py              # General helper functions (date formatting, etc.)
│   └── decorators.py           # Custom decorators (@login_required)
│
├── static/                     # Static files (served by Flask)
│   ├── css/
│   │   ├── main.css            # Main stylesheet
│   │   └── print.css           # Print-specific styles
│   ├── js/
│   │   ├── main.js             # Common JavaScript utilities
│   │   ├── charts.js           # Chart.js initialization
│   │   └── validation.js       # Frontend validation
│   └── images/
│       └── logo.png            # Application logo
│
├── templates/                  # Jinja2 templates
│   ├── base.html               # Base layout with navigation
│   ├── partials/
│   │   └── navigation.html     # Navigation menu
│   ├── errors/
│   │   ├── 404.html
│   │   └── 500.html
│   ├── auth/
│   │   └── login.html
│   ├── dashboard/
│   │   └── index.html
│   ├── students/
│   │   ├── list.html
│   │   ├── add.html
│   │   └── edit.html
│   ├── subjects/
│   │   ├── list.html
│   │   ├── add.html
│   │   └── edit.html
│   ├── marks/
│   │   ├── list.html
│   │   └── add.html
│   ├── results/
│   │   ├── admin_list.html     # Admin view: all students results
│   │   ├── student_lookup.html # Public result lookup form
│   │   └── student_result.html # Public result display
│   ├── analysis/
│   │   └── index.html          # Analytics dashboard
│   └── reports/
│       ├── index.html          # Reports menu
│       ├── individual.html     # Individual student report
│       └── class.html          # Class report
│
├── requirements.txt            # Python dependencies
├── runtime.txt                 # Python version for Render
├── .env.example                # Environment variable template
└── .gitignore                  # Ignore .env, __pycache__, etc.
`

### 18.3 Module Responsibilities

**TR-STRUCT-003:** app.py responsibilities:
- Initialize Flask application
- Load configuration from environment variables
- Register all Blueprints
- Configure session management
- Set up error handlers
- Configure logging
- Run the application

**TR-STRUCT-004:** config.py responsibilities:
- Define configuration classes (DevelopmentConfig, ProductionConfig)
- Load environment variables
- Set default values
- Provide configuration based on FLASK_ENV

**TR-STRUCT-005:** models.py responsibilities:
- Define SQLAlchemy models (if using ORM)
- OR Define functions for raw SQL queries
- Provide data access layer abstraction

**TR-STRUCT-006:** routes/auth.py responsibilities:
- GET /login: Display login form
- POST /login: Validate credentials, create session
- GET /logout: Clear session, redirect to login
- **Maps to:** FR-001, FR-002, FR-007

**TR-STRUCT-007:** routes/dashboard.py responsibilities:
- GET /dashboard: Display admin dashboard with statistics
- Calculate: Total students, total subjects, average pass rate, recent activities
- **Maps to:** FR-011

**TR-STRUCT-008:** routes/students.py responsibilities:
- GET /students: List all students (with search/filter)
- GET /students/add: Display add student form
- POST /students/add: Validate and insert new student
- GET /students/edit/<id>: Display edit student form
- POST /students/edit/<id>: Validate and update student
- POST /students/delete/<id>: Delete student and associated marks
- **Maps to:** FR-013, FR-014, FR-015, FR-016, FR-018

**TR-STRUCT-009:** routes/subjects.py responsibilities:
- GET /subjects: List all subjects
- GET /subjects/add: Display add subject form
- POST /subjects/add: Validate and insert new subject
- GET /subjects/edit/<id>: Display edit subject form
- POST /subjects/edit/<id>: Validate and update subject
- POST /subjects/delete/<id>: Delete subject (if no marks entries)
- **Maps to:** FR-032, FR-033, FR-034, FR-035, FR-036

**TR-STRUCT-010:** routes/marks.py responsibilities:
- GET /marks: List all marks entries (with filters)
- GET /marks/add: Display add marks form (select student + subject)
- POST /marks/add: Validate and insert marks
- GET /marks/edit/<id>: Display edit marks form
- POST /marks/edit/<id>: Validate and update marks
- POST /marks/delete/<id>: Delete marks entry
- **Maps to:** FR-049, FR-050, FR-051, FR-052, FR-053

**TR-STRUCT-011:** routes/results.py responsibilities:
- GET /results/admin: List all students with calculated results (admin only)
- GET /result-lookup: Display public result lookup form
- POST /result-lookup: Validate roll number + DOB, display result
- **Maps to:** FR-070, FR-071, FR-077, FR-079, FR-080

**TR-STRUCT-012:** routes/analysis.py responsibilities:
- GET /analysis: Display analytics dashboard with charts
- Calculate: Pass/fail distribution, grade distribution, subject-wise performance, top performers
- Render charts using Chart.js
- **Maps to:** FR-109, FR-110, FR-111, FR-112

**TR-STRUCT-013:** routes/reports.py responsibilities:
- GET /reports: Display reports menu
- GET /reports/individual/<student_id>: Generate individual student report
- GET /reports/class: Generate class report with all students
- Provide print-friendly view
- **Maps to:** FR-130, FR-131

**TR-STRUCT-014:** utils/db.py responsibilities:
- Provide `get_db_connection()` function
- Handle connection pooling
- Provide query helper functions (execute_query, fetch_one, fetch_all)
- Handle connection errors

**TR-STRUCT-015:** utils/validators.py responsibilities:
- Implement validation functions for all input types
- Return tuple: `(is_valid: bool, error_message: str | None)`
- Functions: validate_roll_number, validate_email, validate_date_of_birth, validate_marks, etc.

**TR-STRUCT-016:** utils/calculations.py responsibilities:
- Implement result calculation logic
- Functions:
  - `calculate_percentage(total_obtained, total_marks)`
  - `calculate_grade(percentage)`
  - `calculate_status(marks_per_subject, passing_marks_per_subject)`
  - `generate_full_result(student_id)` (returns complete result dict)

**TR-STRUCT-017:** utils/helpers.py responsibilities:
- General helper functions
- Date formatting, string manipulation
- Flash message wrappers
- Pagination helpers

**TR-STRUCT-018:** utils/decorators.py responsibilities:
- Define `@login_required` decorator
- Define other custom decorators (if needed)

### 18.4 DATABASE/ Folder Structure

**TR-STRUCT-019:** DATABASE/ contents:
`
DATABASE/
├── schema.sql                  # Complete database schema (CREATE TABLE statements)
├── seed.sql                    # Sample data for testing (optional)
└── README.md                   # Database setup instructions
`

**TR-STRUCT-020:** schema.sql responsibilities:
- CREATE TABLE statements for: admins, students, subjects, marks
- CREATE INDEX statements for performance
- Initial admin account INSERT statement (hashed password)

### 18.5 Static Files Organization

**TR-STRUCT-021:** static/css/ responsibilities:
- main.css: Global styles, layout, components, forms, tables, buttons
- print.css: Print-specific styles (hide navigation, optimize for paper)

**TR-STRUCT-022:** static/js/ responsibilities:
- main.js: Common utilities (form validation helpers, date formatting, confirmation dialogs)
- charts.js: Chart.js initialization functions (grade chart, pass/fail pie chart, etc.)
- validation.js: Frontend validation functions (called on form submit)

**TR-STRUCT-023:** static/images/ responsibilities:
- logo.png: Application logo (displayed in navigation)
- Other images as needed (icons, placeholders)

### 18.6 Templates Organization

**TR-STRUCT-024:** templates/ structure principles:
- base.html: Master template with navigation, flash messages, footer
- Feature folders: Each feature (students, subjects, marks, etc.) has its own folder
- Consistent naming: list.html, add.html, edit.html

**TR-STRUCT-025:** Template inheritance pattern:
`html
<!-- base.html -->
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}{% endblock %}</title>
    {% block extra_css %}{% endblock %}
</head>
<body>
    {% block content %}{% endblock %}
    {% block extra_js %}{% endblock %}
</body>
</html>

<!-- students/list.html -->
{% extends 'base.html' %}
{% block title %}Students List{% endblock %}
{% block content %}
    <!-- student list content -->
{% endblock %}
`

### 18.7 Configuration Files

**TR-STRUCT-026:** .env.example content:
`
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@host:5432/database
FLASK_ENV=development
FLASK_DEBUG=1
`

**TR-STRUCT-027:** .gitignore content:
`
.env
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.log
*.sqlite3
venv/
.venv/
.DS_Store
.vscode/
.idea/
`

**TR-STRUCT-028:** requirements.txt location:
- Option 1: Root of project
- Option 2: Inside BACKEND/ folder
- Render build command adjusted accordingly

**TR-STRUCT-029:** runtime.txt content:
`
python-3.11.6
`

---

## 19. TESTING REQUIREMENTS

### 19.1 Testing Strategy

**TR-TEST-001:** Testing levels:
1. **Unit Testing:** Test individual functions (validators, calculations)
2. **Integration Testing:** Test route handlers with database
3. **Manual Testing:** Test UI workflows in browser
4. **User Acceptance Testing:** Admin user tests complete workflows

**Maps to:** TEST-001

### 19.2 Unit Testing

**TR-TEST-002:** Unit testing framework: pytest 7.4.0+

**TR-TEST-003:** Unit test coverage:
- utils/validators.py: All validation functions
- utils/calculations.py: All calculation functions
- utils/helpers.py: All helper functions

**TR-TEST-004:** Sample unit tests:
`python
# tests/test_validators.py
import pytest
from utils.validators import validate_roll_number, validate_marks

def test_validate_roll_number_valid():
    is_valid, error = validate_roll_number('STU001')
    assert is_valid is True
    assert error is None

def test_validate_roll_number_invalid_length():
    is_valid, error = validate_roll_number('ST')
    assert is_valid is False
    assert 'format' in error.lower()

def test_validate_marks_valid():
    is_valid, error = validate_marks(85, 100)
    assert is_valid is True
    assert error is None

def test_validate_marks_exceeds_total():
    is_valid, error = validate_marks(110, 100)
    assert is_valid is False
    assert 'between' in error.lower()
`

**TR-TEST-005:** Calculation logic tests:
`python
# tests/test_calculations.py
import pytest
from utils.calculations import calculate_percentage, calculate_grade

def test_calculate_percentage():
    assert calculate_percentage(450, 500) == 90.0
    assert calculate_percentage(0, 100) == 0.0
    assert calculate_percentage(100, 100) == 100.0

def test_calculate_grade():
    assert calculate_grade(95) == 'A'
    assert calculate_grade(85) == 'B'
    assert calculate_grade(75) == 'C'
    assert calculate_grade(65) == 'D'
    assert calculate_grade(45) == 'F'
`

**TR-TEST-006:** Running unit tests:
`ash
pytest tests/ -v
pytest tests/ --cov=utils --cov-report=html
`

**Maps to:** TEST-010, TEST-011, TEST-012

### 19.3 Integration Testing

**TR-TEST-007:** Integration testing approach:
- Use pytest with Flask test client
- Use separate test database or in-memory SQLite
- Test complete request-response cycles

**TR-TEST-008:** Sample integration tests:
`python
# tests/test_routes.py
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_login_page_loads(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data

def test_login_success(client):
    response = client.post('/login', data={
        'username': 'admin',
        'password': 'admin123'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Dashboard' in response.data

def test_dashboard_requires_login(client):
    response = client.get('/dashboard')
    assert response.status_code == 302  # Redirect to login
`

**TR-TEST-009:** Database integration tests:
`python
def test_add_student(client):
    # Log in first
    client.post('/login', data={'username': 'admin', 'password': 'admin123'})
    
    # Add student
    response = client.post('/students/add', data={
        'roll_number': 'TEST001',
        'name': 'Test Student',
        'date_of_birth': '2005-01-01',
        'gender': 'Male'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Student added successfully' in response.data
`

**Maps to:** TEST-020, TEST-021

### 19.4 Manual Testing Checklist

**TR-TEST-010:** Admin authentication testing:
- [ ] Login with valid credentials succeeds
- [ ] Login with invalid credentials fails with error message
- [ ] Logout clears session and redirects to login
- [ ] Accessing protected routes without login redirects to login
- [ ] Session expires after 30 minutes of inactivity

**Maps to:** TEST-030, FR-001, FR-002, FR-007

**TR-TEST-011:** Student management testing:
- [ ] Add student with valid data succeeds
- [ ] Add student with duplicate roll number fails with error
- [ ] Add student with invalid date of birth fails with error
- [ ] Edit student updates data correctly
- [ ] Search/filter students works correctly
- [ ] Delete student removes student and associated marks

**Maps to:** TEST-031, FR-013 through FR-018

**TR-TEST-012:** Subject management testing:
- [ ] Add subject with valid data succeeds
- [ ] Add subject with duplicate subject code fails with error
- [ ] Add subject with passing_marks >= total_marks fails with error
- [ ] Edit subject updates data correctly
- [ ] Delete subject with marks entries fails with error
- [ ] Delete subject without marks entries succeeds

**Maps to:** TEST-032, FR-032 through FR-036

**TR-TEST-013:** Marks management testing:
- [ ] Add marks for student-subject combination succeeds
- [ ] Add marks exceeding total marks fails with error
- [ ] Add marks with negative value fails with error
- [ ] Add duplicate marks for same student-subject fails with error
- [ ] Edit marks updates correctly
- [ ] Delete marks removes entry

**Maps to:** TEST-033, FR-049 through FR-053

**TR-TEST-014:** Result display testing:
- [ ] Admin can view list of all students with results
- [ ] Results show correct total marks, percentage, grade, status
- [ ] Grade is calculated correctly based on percentage
- [ ] Status is "Pass" only if all subjects >= passing marks
- [ ] Results sorted by percentage descending

**Maps to:** TEST-034, FR-070, FR-071, FR-074, FR-075

**TR-TEST-015:** Public result lookup testing:
- [ ] Result lookup form accessible without login
- [ ] Valid roll number + DOB displays correct result
- [ ] Invalid roll number + DOB shows "Invalid credentials"
- [ ] Result displays all subject marks and calculations
- [ ] Result includes student name, roll number, DOB

**Maps to:** TEST-035, FR-077, FR-079, FR-080

**TR-TEST-016:** Analytics testing:
- [ ] Analytics dashboard displays all charts correctly
- [ ] Grade distribution chart shows correct data
- [ ] Pass/fail pie chart shows correct counts
- [ ] Subject-wise average chart shows correct data
- [ ] Top performers list shows correct students (sorted by percentage)

**Maps to:** TEST-036, FR-109 through FR-112

### 19.5 Test Data

**TR-TEST-017:** Test database shall include:
- 1 admin account (username: admin, password: admin123)
- 10-20 sample students with realistic data
- 5-8 subjects with varying total and passing marks
- Marks entries for all students across all subjects
- Mix of passing and failing students

**TR-TEST-018:** Test data SQL (DATABASE/seed.sql):
`sql
-- Sample admin (password: admin123)
INSERT INTO admins (username, email, password_hash, full_name)
VALUES ('admin', 'admin@example.com', '[bcrypt-hash]', 'System Administrator');

-- Sample students
INSERT INTO students (roll_number, name, email, date_of_birth, gender, contact_number) VALUES
('STU001', 'Alice Johnson', 'alice@example.com', '2005-03-15', 'Female', '9876543210'),
('STU002', 'Bob Smith', 'bob@example.com', '2005-07-22', 'Male', '9876543211'),
-- ... more students

-- Sample subjects
INSERT INTO subjects (subject_code, subject_name, total_marks, passing_marks) VALUES
('MATH101', 'Mathematics', 100, 35),
('ENG101', 'English', 100, 35),
('SCI101', 'Science', 100, 35),
-- ... more subjects

-- Sample marks
INSERT INTO marks (student_id, subject_id, marks_obtained) VALUES
(1, 1, 85.0),
(1, 2, 78.0),
(1, 3, 92.0),
-- ... more marks
`

### 19.6 Testing Tools

**TR-TEST-019:** Recommended testing tools:
- **pytest:** Unit and integration testing
- **pytest-cov:** Code coverage measurement
- **pytest-flask:** Flask-specific testing utilities
- **Postman:** API endpoint testing (manual)
- **Browser DevTools:** Frontend debugging and testing

**TR-TEST-020:** Running tests:
`ash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html

# Run specific test file
pytest tests/test_validators.py -v

# Run specific test function
pytest tests/test_validators.py::test_validate_roll_number_valid -v
`

---

## 20. DEPLOYMENT REQUIREMENTS

### 20.1 Deployment Platform

**TR-DEPLOY-001:** Application shall be deployed on Render free tier.

**TR-DEPLOY-002:** Render web service configuration:
- Type: Web Service
- Environment: Python 3.11
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app`
- Auto-deploy: Enabled (deploy on push to main branch)

**TR-DEPLOY-003:** Database shall be hosted on Supabase free tier.

**TR-DEPLOY-004:** Supabase free tier limits:
- Storage: 500 MB (sufficient for text data)
- Bandwidth: 2 GB per month
- Connections: Up to 60 concurrent connections
- No credit card required

**Maps to:** DEP-001, DEP-002, DEP-010

### 20.2 Render Deployment Steps

**TR-DEPLOY-005:** Render deployment procedure:
1. Create GitHub repository and push code
2. Sign up for Render account (free)
3. Create new Web Service
4. Connect GitHub repository
5. Configure build and start commands
6. Add environment variables
7. Deploy

**TR-DEPLOY-006:** Render build settings:
`yaml
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app --bind 0.0.0.0:
Branch: main
Auto-Deploy: Yes
`

**TR-DEPLOY-007:** Render environment variables (set in dashboard):
`
SECRET_KEY=<generate-random-string>
DATABASE_URL=<supabase-connection-string>
FLASK_ENV=production
FLASK_DEBUG=0
`

**TR-DEPLOY-008:** Render health check:
- Health Check Path: / or /health
- Expected Status: 200
- Timeout: 30 seconds

**TR-DEPLOY-009:** Render free tier limitations:
- Instance spins down after 15 minutes of inactivity
- First request after spin-down takes 30-60 seconds (cold start)
- 512 MB RAM
- Shared CPU

**Maps to:** DEP-020, DEP-021

### 20.3 Supabase Setup

**TR-DEPLOY-010:** Supabase project setup:
1. Sign up at supabase.com
2. Create new project
3. Choose region (closest to target users)
4. Set database password
5. Wait for provisioning (2-3 minutes)
6. Get connection string from Settings > Database

**TR-DEPLOY-011:** Supabase connection string format:
`
postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres
`

**TR-DEPLOY-012:** Database schema deployment:
1. Navigate to SQL Editor in Supabase dashboard
2. Copy contents of DATABASE/schema.sql
3. Execute in SQL Editor
4. Verify tables created (check Table Editor)
5. Insert initial admin account

**TR-DEPLOY-013:** Supabase security settings:
- Enable SSL (required by default)
- Enable Row Level Security (optional, not used in this project)
- Disable Realtime subscriptions (not needed)

**Maps to:** DEP-030

### 20.4 Application Configuration for Production

**TR-DEPLOY-014:** Production configuration in app.py:
`python
import os

if os.getenv('FLASK_ENV') == 'production':
    app.config.update(
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax',
        PERMANENT_SESSION_LIFETIME=1800
    )
    app.config['DEBUG'] = False
`

**TR-DEPLOY-015:** Gunicorn configuration (app.py or gunicorn.conf.py):
`python
# gunicorn.conf.py (optional)
bind = "0.0.0.0:8000"
workers = 1  # Free tier limitation
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
errorlog = "-"
accesslog = "-"
loglevel = "info"
`

**TR-DEPLOY-016:** Static file serving:
- Flask serves static files directly (no CDN needed for Diploma project)
- Static folder: BACKEND/static/
- Route: /static/<path>

**TR-DEPLOY-017:** Logging configuration for production:
`python
import logging
import sys

if os.getenv('FLASK_ENV') == 'production':
    app.logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
`

**Maps to:** DEP-040

### 20.5 Deployment Verification

**TR-DEPLOY-018:** Post-deployment checklist:
- [ ] Application loads at Render URL
- [ ] Login page accessible
- [ ] Admin can log in with credentials
- [ ] Dashboard displays without errors
- [ ] Database connection successful
- [ ] Static files (CSS, JS) load correctly
- [ ] Forms submit successfully
- [ ] Charts render correctly (Chart.js loads from CDN)
- [ ] Public result lookup works
- [ ] Session persistence works
- [ ] HTTPS enforced

**TR-DEPLOY-019:** Performance verification:
- [ ] Cold start completes within 60 seconds
- [ ] Warm requests respond within 2 seconds
- [ ] Database queries complete within 500ms
- [ ] Page loads within 3 seconds

**TR-DEPLOY-020:** Error monitoring:
- Check Render logs for errors: Dashboard > Logs
- Monitor Supabase connection count: Dashboard > Database > Connections
- Test error pages (404, 500) display correctly

**Maps to:** DEP-050

### 20.6 Continuous Deployment

**TR-DEPLOY-021:** Auto-deployment workflow:
1. Developer pushes code to GitHub main branch
2. Render detects commit via webhook
3. Render pulls latest code
4. Render runs build command
5. Render restarts service with new code
6. Deployment complete (typically 2-5 minutes)

**TR-DEPLOY-022:** Rollback procedure (if deployment fails):
1. Navigate to Render dashboard
2. Select Web Service
3. Go to "Manual Deploy" section
4. Select previous successful commit
5. Click "Deploy"

**TR-DEPLOY-023:** Database migration strategy (for future schema changes):
- Option 1: Run migration SQL in Supabase SQL Editor
- Option 2: Use Alembic (Flask-Migrate) for versioned migrations
- For Diploma project, manual SQL migrations sufficient

**Maps to:** DEP-060

### 20.7 Domain and HTTPS

**TR-DEPLOY-024:** Default domain:
- Format: `<app-name>.onrender.com`
- HTTPS automatic (Let's Encrypt certificate)
- No custom domain needed for Diploma project

**TR-DEPLOY-025:** Custom domain (optional):
- Render supports custom domains on free tier
- Add DNS CNAME record pointing to Render
- SSL certificate automatically provisioned

**Maps to:** DEP-070

### 20.8 Backup and Recovery

**TR-DEPLOY-026:** Database backup strategy:
- Supabase automatic daily backups (retained 7 days on free tier)
- Manual backup: Export SQL from Supabase dashboard
- Restore: Import SQL in new project

**TR-DEPLOY-027:** Code backup:
- GitHub repository serves as primary backup
- Commit frequently
- Tag releases: `git tag -a v1.0 -m "Release 1.0"`

**Maps to:** DEP-080

---

## 21. ENVIRONMENT CONFIGURATION

### 21.1 Environment Variables

**TR-ENV-001:** Required environment variables:

| Variable Name | Description | Example Value | Required |
|---------------|-------------|---------------|----------|
| SECRET_KEY | Flask session encryption key | random-string-32-chars | Yes |
| DATABASE_URL | PostgreSQL connection string | postgresql://... | Yes |
| FLASK_ENV | Environment (development/production) | production | Yes |
| FLASK_DEBUG | Debug mode (0/1) | 0 | No (default: 0) |

**TR-ENV-002:** SECRET_KEY generation:
`python
import secrets
secret_key = secrets.token_hex(32)
print(secret_key)  # Use this value
`
Or:
`ash
python -c "import secrets; print(secrets.token_hex(32))"
`

**TR-ENV-003:** DATABASE_URL format:
`
postgresql://[user]:[password]@[host]:[port]/[database]?sslmode=require
`

Example:
`
postgresql://postgres:mypassword@db.abc123.supabase.co:5432/postgres?sslmode=require
`

**Maps to:** ENV-001, ENV-002

### 21.2 Development Environment (.env file)

**TR-ENV-004:** .env file for local development:
`env
# Flask Configuration
SECRET_KEY=dev-secret-key-change-in-production
FLASK_ENV=development
FLASK_DEBUG=1

# Database Configuration
DATABASE_URL=postgresql://postgres:password@localhost:5432/student_results

# Optional Settings
LOG_LEVEL=DEBUG
`

**TR-ENV-005:** Loading .env file:
`python
# app.py
from dotenv import load_dotenv
import os

load_dotenv()  # Load .env file

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
# ... other config
`

**TR-ENV-006:** .env.example template (committed to Git):
`env
# Flask Configuration
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
FLASK_DEBUG=1

# Database Configuration
DATABASE_URL=postgresql://user:password@host:5432/database

# Optional Settings
LOG_LEVEL=INFO
`

**Maps to:** ENV-010

### 21.3 Production Environment (Render)

**TR-ENV-007:** Production environment variables (set in Render dashboard):
`
SECRET_KEY=<generate-with-secrets.token_hex(32)>
DATABASE_URL=<supabase-connection-string>
FLASK_ENV=production
FLASK_DEBUG=0
`

**TR-ENV-008:** Setting environment variables in Render:
1. Go to Render dashboard
2. Select your Web Service
3. Navigate to "Environment" tab
4. Click "Add Environment Variable"
5. Enter key-value pairs
6. Save changes (triggers redeployment)

**Maps to:** ENV-020

### 21.4 Configuration Classes

**TR-ENV-009:** config.py implementation:
`python
import os
from datetime import timedelta

class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    FLASK_ENV = 'development'
    SESSION_COOKIE_SECURE = False
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://localhost/student_results')

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    FLASK_ENV = 'production'
    SESSION_COOKIE_SECURE = True
    DATABASE_URL = os.getenv('DATABASE_URL')
    
    # Validate required variables
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL environment variable not set")

# Select configuration based on FLASK_ENV
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
`

**TR-ENV-010:** Using configuration in app.py:
`python
from config import config

app = Flask(__name__)
env = os.getenv('FLASK_ENV', 'development')
app.config.from_object(config[env])
`

**Maps to:** ENV-030

### 21.5 Security Considerations

**TR-ENV-011:** Environment variable security:
- Never commit .env file to Git (add to .gitignore)
- Never hardcode secrets in source code
- Rotate SECRET_KEY if compromised
- Use different DATABASE_URL for development and production

**TR-ENV-012:** .gitignore must include:
`
.env
.env.local
.env.*.local
*.env
`

**TR-ENV-013:** Accessing environment variables in code:
`python
# Correct
database_url = os.getenv('DATABASE_URL')
if not database_url:
    raise ValueError('DATABASE_URL not configured')

# Also acceptable (with default)
log_level = os.getenv('LOG_LEVEL', 'INFO')
`

**Maps to:** ENV-040, SEC-043

---

## 22. PRD → TRD TRACEABILITY MATRIX

### 22.1 Functional Requirements Mapping

| PRD Requirement ID | Requirement Summary | TRD Requirement ID(s) | Section |
|-------------------|---------------------|----------------------|---------|
| FR-001 | Admin login required | TR-AUTH-001, TR-STRUCT-006 | 9, 18 |
| FR-002 | Admin credentials validation | TR-AUTH-002, TR-AUTH-003 | 9 |
| FR-007 | Admin logout | TR-AUTH-009, TR-STRUCT-006 | 9, 18 |
| FR-011 | Admin dashboard with statistics | TR-DASH-001 through TR-DASH-007, TR-STRUCT-007 | 10, 18 |
| FR-013 | Add student | TR-STUDENT-001 through TR-STUDENT-007, TR-VAL-005 through TR-VAL-010 | 10, 15 |
| FR-014 | View students list | TR-STUDENT-008 through TR-STUDENT-010 | 10 |
| FR-015 | Edit student | TR-STUDENT-011 through TR-STUDENT-013 | 10 |
| FR-016 | Delete student | TR-STUDENT-014, TR-STUDENT-015 | 10 |
| FR-018 | Search/filter students | TR-STUDENT-016, TR-STUDENT-017 | 10 |
| FR-032 | Add subject | TR-SUBJECT-001 through TR-SUBJECT-007, TR-VAL-011 through TR-VAL-014 | 11, 15 |
| FR-033 | View subjects list | TR-SUBJECT-008 | 11 |
| FR-034 | Edit subject | TR-SUBJECT-009, TR-SUBJECT-010 | 11 |
| FR-035 | Delete subject (with restrictions) | TR-SUBJECT-011, TR-SUBJECT-012 | 11 |
| FR-036 | Search subjects | TR-SUBJECT-013 | 11 |
| FR-049 | Add marks | TR-MARKS-001 through TR-MARKS-009, TR-VAL-015 through TR-VAL-018 | 12, 15 |
| FR-050 | View marks list | TR-MARKS-010, TR-MARKS-011 | 12 |
| FR-051 | Edit marks | TR-MARKS-012, TR-MARKS-013 | 12 |
| FR-052 | Delete marks | TR-MARKS-014 | 12 |
| FR-053 | Filter marks | TR-MARKS-015 | 12 |
| FR-070 | Admin view all results | TR-RESULT-001 through TR-RESULT-005 | 13 |
| FR-071 | Calculate and display results | TR-RESULT-006 through TR-RESULT-010 | 13 |
| FR-074 | Display total, percentage, grade, status | TR-RESULT-011 through TR-RESULT-015 | 13 |
| FR-075 | Sort results by percentage | TR-RESULT-016 | 13 |
| FR-077 | Public result lookup (no login) | TR-RESULT-017, TR-RESULT-018 | 13 |
| FR-079 | Authenticate with Roll Number + DOB | TR-RESULT-019, TR-RESULT-020, TR-VAL-019, TR-VAL-020 | 13, 15 |
| FR-080 | Display individual result | TR-RESULT-021 through TR-RESULT-025 | 13 |
| FR-109 | Analytics dashboard | TR-ANAL-001, TR-ANAL-002 | 14 |
| FR-110 | Pass/fail distribution | TR-ANAL-003, TR-ANAL-004 | 14 |
| FR-111 | Grade distribution | TR-ANAL-005, TR-ANAL-006 | 14 |
| FR-112 | Subject-wise performance | TR-ANAL-007, TR-ANAL-008 | 14 |
| FR-113 | Top performers | TR-ANAL-009, TR-ANAL-010 | 14 |
| FR-130 | Individual student report (printable) | TR-STRUCT-013 | 18 |
| FR-131 | Class report (printable) | TR-STRUCT-013 | 18 |

### 22.2 Database Requirements Mapping

| PRD Requirement ID | Requirement Summary | TRD Requirement ID(s) | Section |
|-------------------|---------------------|----------------------|---------|
| DB-001 | Admins table | TR-DB-TABLE-001 through TR-DB-TABLE-003 | 7 |
| DB-002 | Students table | TR-DB-TABLE-004 through TR-DB-TABLE-006 | 7 |
| DB-003 | Subjects table | TR-DB-TABLE-007 through TR-DB-TABLE-009 | 7 |
| DB-004 | Marks table | TR-DB-TABLE-010 through TR-DB-TABLE-012 | 7 |
| DB-005 | Foreign key relationships | TR-DB-TABLE-013 through TR-DB-TABLE-015 | 7 |
| DB-006 | Cascade delete for marks | TR-DB-TABLE-016 | 7 |
| DB-007 | Restrict delete for subjects | TR-DB-TABLE-017 | 7 |

### 22.3 Security Requirements Mapping

| PRD Requirement ID | Requirement Summary | TRD Requirement ID(s) | Section |
|-------------------|---------------------|----------------------|---------|
| SEC-001 | Password hashing (bcrypt) | TR-SEC-001, TR-VAL-003 | 17, 15 |
| SEC-010 | Secure password storage | TR-SEC-001 | 17 |
| SEC-011 | Session security | TR-SEC-002 | 17 |
| SEC-012 | Session timeout | TR-SEC-002 | 17 |
| SEC-013 | Login attempt limiting | TR-SEC-003 | 17 |
| SEC-014 | Secure logout | TR-SEC-004 | 17 |
| SEC-020 | Route protection | TR-SEC-005, TR-SEC-006 | 17 |
| SEC-021 | Authorization checks | TR-SEC-006 | 17 |
| SEC-022 | Role-based access | TR-SEC-007 | 17 |
| SEC-023 | Result lookup authentication | TR-VAL-019 | 15 |
| SEC-030 | SQL injection prevention | TR-SEC-008 | 17 |
| SEC-031 | XSS prevention | TR-SEC-009, TR-SEC-010 | 17 |
| SEC-032 | File upload validation | TR-SEC-011 | 17 |
| SEC-040 | Sensitive data protection | TR-SEC-012 | 17 |
| SEC-041 | Database SSL/TLS | TR-SEC-013 | 17 |
| SEC-042 | HTTPS enforcement | TR-SEC-014 | 17 |
| SEC-043 | Environment variable security | TR-SEC-015, TR-ENV-011, TR-ENV-012 | 17, 21 |
| SEC-050 | Error message security | TR-SEC-016, TR-SEC-017, TR-SEC-018 | 17 |
| SEC-051 | Debug mode disabled in production | TR-SEC-017 | 17 |
| SEC-052 | Hide database details in errors | TR-SEC-018 | 17 |
| SEC-060 | CSRF protection | TR-SEC-019 | 17 |
| SEC-061 | Security headers | TR-SEC-020 | 17 |
| SEC-062 | Rate limiting | TR-SEC-021 | 17 |
| SEC-063 | Dependency security | TR-SEC-022 | 17 |

### 22.4 Validation Requirements Mapping

| PRD Requirement ID | Requirement Summary | TRD Requirement ID(s) | Section |
|-------------------|---------------------|----------------------|---------|
| VAL-001 | Admin username format | TR-VAL-001 | 15 |
| VAL-002 | Admin email format | TR-VAL-002 | 15 |
| VAL-003 | Admin password strength | TR-VAL-003 | 15 |
| VAL-004 | Admin full name format | TR-VAL-004 | 15 |
| VAL-005 | Roll number format and uniqueness | TR-VAL-005 | 15 |
| VAL-006 | Student name format | TR-VAL-006 | 15 |
| VAL-007 | Student email format | TR-VAL-007 | 15 |
| VAL-008 | Date of birth validation | TR-VAL-008 | 15 |
| VAL-009 | Gender validation | TR-VAL-009 | 15 |
| VAL-010 | Contact number format | TR-VAL-010 | 15 |
| VAL-011 | Subject code format and uniqueness | TR-VAL-011 | 15 |
| VAL-012 | Subject name format | TR-VAL-012 | 15 |
| VAL-013 | Total marks range | TR-VAL-013 | 15 |
| VAL-014 | Passing marks validation | TR-VAL-014 | 15 |
| VAL-015 | Marks obtained range | TR-VAL-015 | 15 |
| VAL-016 | Student-subject uniqueness | TR-VAL-016 | 15 |
| VAL-017 | Student existence check | TR-VAL-017 | 15 |
| VAL-018 | Subject existence check | TR-VAL-018 | 15 |
| VAL-019 | Roll number + DOB validation | TR-VAL-019 | 15 |
| VAL-020 | DOB format normalization | TR-VAL-020 | 15 |

### 22.5 Technology Stack Mapping

| PRD Requirement ID | Requirement Summary | TRD Requirement ID(s) | Section |
|-------------------|---------------------|----------------------|---------|
| TECH-001 | Backend: Python + Flask | TR-TECH-001, TR-TECH-002 | 3 |
| TECH-002 | Frontend: HTML5 + CSS3 + JavaScript | TR-TECH-009, TR-TECH-010, TR-TECH-011 | 3 |
| TECH-003 | Database: Supabase PostgreSQL | TR-TECH-015, TR-TECH-016 | 3 |
| TECH-004 | Charts: Chart.js | TR-TECH-012, TR-TECH-022 | 3 |
| TECH-005 | Hosting: Render free tier | TR-DEPLOY-001, TR-DEPLOY-002 | 20 |
| TECH-006 | No frontend frameworks | TR-TECH-013, TR-TECH-014 | 3 |
| TECH-007 | Password hashing: bcrypt | TR-TECH-004 | 3 |
| TECH-008 | Session management: Flask sessions | TR-TECH-003 | 3 |
| TECH-009 | Database adapter: psycopg2 | TR-TECH-005 | 3 |
| TECH-010 | Production server: Gunicorn | TR-TECH-007 | 3 |

---

## 23. TECHNICAL DEPENDENCIES

### 23.1 Python Dependencies

**TR-DEP-001:** requirements.txt complete specification:
`	xt
# Web Framework
Flask==3.0.0

# Database
psycopg2-binary==2.9.9

# Authentication & Security
bcrypt==4.1.1

# Configuration
python-dotenv==1.0.0

# Production Server
gunicorn==21.2.0

# Optional: ORM (if using SQLAlchemy)
# Flask-SQLAlchemy==3.1.1
# SQLAlchemy==2.0.23

# Optional: Testing
# pytest==7.4.3
# pytest-flask==1.3.0
# pytest-cov==4.1.0
`

**TR-DEP-002:** Dependency descriptions:

| Package | Version | Purpose | Required |
|---------|---------|---------|----------|
| Flask | 3.0.0+ | Web framework, routing, templates | Yes |
| psycopg2-binary | 2.9.9+ | PostgreSQL database adapter | Yes |
| bcrypt | 4.1.1+ | Password hashing | Yes |
| python-dotenv | 1.0.0+ | Load environment variables from .env | Yes |
| gunicorn | 21.2.0+ | Production WSGI server | Yes |
| Flask-SQLAlchemy | 3.1.1+ | ORM for database abstraction | Optional |
| pytest | 7.4.3+ | Testing framework | Dev only |
| pytest-flask | 1.3.0+ | Flask testing utilities | Dev only |
| pytest-cov | 4.1.0+ | Code coverage measurement | Dev only |

**Maps to:** TECH-001 through TECH-010

### 23.2 Frontend Dependencies

**TR-DEP-003:** Frontend dependencies (CDN-loaded):
`html
<!-- Chart.js for data visualization -->
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
`

**TR-DEP-004:** No npm or frontend build tools required.

**TR-DEP-005:** All CSS and JavaScript are custom-written (no Bootstrap, jQuery, etc.).

**Maps to:** TECH-012, TECH-022

### 23.3 System Dependencies

**TR-DEP-006:** System requirements for development:
- Python 3.11.x
- pip (Python package manager)
- Git 2.x
- PostgreSQL 14+ (optional, for local development)
- Web browser (Chrome, Firefox, Edge, Safari)

**TR-DEP-007:** System requirements for deployment:
- None (Render provides Python runtime)
- Supabase provides managed PostgreSQL

**Maps to:** TECH-001

### 23.4 Development Dependencies

**TR-DEP-008:** requirements-dev.txt (optional):
`	xt
# Include production dependencies
-r requirements.txt

# Development Tools
pytest==7.4.3
pytest-flask==1.3.0
pytest-cov==4.1.0
black==23.12.1           # Code formatter
flake8==7.0.0            # Linter
mypy==1.7.1              # Type checker
`

**TR-DEP-009:** Installing development dependencies:
`ash
pip install -r requirements-dev.txt
`

### 23.5 Dependency Installation

**TR-DEP-010:** Installation commands:
`ash
# Production dependencies
pip install -r requirements.txt

# Development dependencies (if using requirements-dev.txt)
pip install -r requirements-dev.txt

# Or install individually
pip install Flask==3.0.0
pip install psycopg2-binary==2.9.9
pip install bcrypt==4.1.1
pip install python-dotenv==1.0.0
pip install gunicorn==21.2.0
`

**TR-DEP-011:** Virtual environment setup (recommended):
`ash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
`

### 23.6 Dependency Security

**TR-DEP-012:** Checking for security vulnerabilities:
`ash
# Using pip-audit (if installed)
pip install pip-audit
pip-audit

# Using safety (alternative)
pip install safety
safety check
`

**TR-DEP-013:** Updating dependencies:
`ash
# Check outdated packages
pip list --outdated

# Update specific package
pip install --upgrade Flask

# Update all packages (use cautiously)
pip install --upgrade -r requirements.txt
`

**TR-DEP-014:** Pinned versions rationale:
- Using exact versions (==) ensures consistent builds
- Minor version updates (e.g., 3.0.0 → 3.0.1) usually safe for bug fixes
- Major version updates (e.g., 3.0.0 → 4.0.0) may require code changes

**Maps to:** SEC-063

### 23.7 Dependency Licensing

**TR-DEP-015:** All dependencies use permissive open-source licenses:
- Flask: BSD-3-Clause
- psycopg2-binary: LGPL-3.0
- bcrypt: Apache-2.0
- python-dotenv: BSD-3-Clause
- gunicorn: MIT
- Chart.js: MIT

**TR-DEP-016:** No licensing issues for educational/commercial use.

---

## 24. TECHNICAL RISKS AND MITIGATION

### 24.1 Infrastructure Risks

**TR-RISK-001:** Risk: Render free tier cold start delay (30-60 seconds after 15 min inactivity)
- **Impact:** Poor user experience for first visitor after inactivity
- **Likelihood:** High (expected behavior of free tier)
- **Mitigation:**
  1. Display loading message: "Waking up the server, please wait..."
  2. Document this behavior in project documentation
  3. Consider using a cron job to ping the app every 10 minutes (from free service like cron-job.org)
  4. Upgrade to paid tier if budget allows (eliminates cold starts)
- **PRD Ref:** TECH-005

**TR-RISK-002:** Risk: Supabase free tier limits (500 MB storage, 2 GB bandwidth/month)
- **Impact:** Application stops working if limits exceeded
- **Likelihood:** Low (text data is very small)
- **Mitigation:**
  1. Monitor usage in Supabase dashboard
  2. Estimate: 1000 students × 10 subjects × 100 bytes/record ≈ 1 MB (well under 500 MB)
  3. Implement pagination to reduce data transfer
  4. Avoid storing large files (images, PDFs) in database
- **PRD Ref:** TECH-003, DB-008

**TR-RISK-003:** Risk: Render 512 MB RAM limitation
- **Impact:** Application crashes under high concurrent load
- **Likelihood:** Medium (depends on usage)
- **Mitigation:**
  1. Optimize memory usage (close database connections, avoid large in-memory data structures)
  2. Use database queries instead of loading all data into memory
  3. Implement connection pooling
  4. Upgrade to paid tier if needed
- **PRD Ref:** TECH-005

### 24.2 Security Risks

**TR-RISK-004:** Risk: SQL injection if parameterized queries not used consistently
- **Impact:** Critical - database compromise, data theft
- **Likelihood:** Low (if following guidelines)
- **Mitigation:**
  1. Code review: Check all database queries use parameterization
  2. Use ORM (SQLAlchemy) which prevents SQL injection by default
  3. Input validation on all user inputs
  4. Testing: Attempt SQL injection in testing phase
- **PRD Ref:** SEC-030

**TR-RISK-005:** Risk: Session hijacking if HTTPS not enforced
- **Impact:** High - unauthorized admin access
- **Likelihood:** Low (Render enforces HTTPS)
- **Mitigation:**
  1. Verify SESSION_COOKIE_SECURE=True in production
  2. Use HSTS header to force HTTPS
  3. Session timeout after 30 minutes
- **PRD Ref:** SEC-011, SEC-042

**TR-RISK-006:** Risk: Weak passwords chosen by admin users
- **Impact:** Medium - unauthorized access
- **Likelihood:** Medium
- **Mitigation:**
  1. Enforce password complexity requirements (TR-VAL-003)
  2. Minimum 8 characters, uppercase, lowercase, digit
  3. Consider password strength indicator in UI
- **PRD Ref:** SEC-001, VAL-003

**TR-RISK-007:** Risk: Exposed environment variables in Git
- **Impact:** Critical - database credentials leaked
- **Likelihood:** Low (if following guidelines)
- **Mitigation:**
  1. Add .env to .gitignore
  2. Use .env.example template without real secrets
  3. GitHub secret scanning enabled
  4. Rotate credentials if accidentally committed
- **PRD Ref:** SEC-043, ENV-040

### 24.3 Data Integrity Risks

**TR-RISK-008:** Risk: Orphaned marks records if student deleted without cascade
- **Impact:** Low - data inconsistency, storage waste
- **Likelihood:** Very Low (database constraints prevent this)
- **Mitigation:**
  1. Use ON DELETE CASCADE for marks → students foreign key
  2. Database constraints enforce referential integrity
  3. Test delete operations in testing phase
- **PRD Ref:** DB-006

**TR-RISK-009:** Risk: Duplicate roll numbers due to race condition
- **Impact:** Medium - data integrity violation
- **Likelihood:** Very Low (single-user system)
- **Mitigation:**
  1. UNIQUE constraint on students.roll_number (database level)
  2. Handle constraint violation errors gracefully in application
  3. Display error message: "Roll number already exists"
- **PRD Ref:** VAL-005, DB-002

**TR-RISK-010:** Risk: Incorrect grade calculation due to logic error
- **Impact:** High - incorrect results displayed
- **Likelihood:** Low (if tested thoroughly)
- **Mitigation:**
  1. Comprehensive unit tests for calculation functions
  2. Manual verification with sample data
  3. Document expected behavior clearly
  4. Test edge cases (0%, 100%, passing marks boundary)
- **PRD Ref:** FR-074, TEST-011

### 24.4 Performance Risks

**TR-RISK-011:** Risk: Slow queries for analytics with large datasets
- **Impact:** Medium - dashboard loads slowly
- **Likelihood:** Low (Diploma project scale)
- **Mitigation:**
  1. Create indexes on frequently queried columns
  2. Use aggregate queries (COUNT, AVG) instead of loading all data
  3. Implement caching for analytics results (if needed)
  4. Pagination for large lists
- **PRD Ref:** FR-109, DB-013

**TR-RISK-012:** Risk: Database connection exhaustion under load
- **Impact:** High - application stops responding
- **Likelihood:** Low (single-admin system)
- **Mitigation:**
  1. Implement connection pooling (psycopg2 pool or SQLAlchemy)
  2. Always close connections in finally blocks
  3. Monitor active connections in Supabase dashboard
- **PRD Ref:** TR-DB-001, TR-DB-004

### 24.5 Deployment Risks

**TR-RISK-013:** Risk: Deployment fails due to missing environment variables
- **Impact:** High - application won't start
- **Likelihood:** Medium (common deployment issue)
- **Mitigation:**
  1. Checklist: Verify all required env vars set in Render dashboard
  2. Application startup validation: Check for required env vars
  3. Clear error messages if env var missing
  4. Document required env vars in README
- **PRD Ref:** ENV-001, DEP-020

**TR-RISK-014:** Risk: Database schema not created before deployment
- **Impact:** High - application crashes on database queries
- **Likelihood:** Medium (first-time deployment)
- **Mitigation:**
  1. Deployment checklist: Run schema.sql in Supabase before deploying app
  2. Document schema setup steps clearly
  3. Consider migration scripts for future schema changes
- **PRD Ref:** DEP-030

**TR-RISK-015:** Risk: Static files not loading after deployment
- **Impact:** Medium - broken UI, no charts
- **Likelihood:** Low (Flask serves static files by default)
- **Mitigation:**
  1. Verify static folder structure matches Flask defaults
  2. Test static file loading immediately after deployment
  3. Check browser console for 404 errors
- **PRD Ref:** TR-FE-016, DEP-050

### 24.6 Usability Risks

**TR-RISK-016:** Risk: Chart.js CDN fails to load
- **Impact:** Medium - charts don't display
- **Likelihood:** Low (CDN reliability high)
- **Mitigation:**
  1. Use reliable CDN (jsDelivr)
  2. Fallback: Display data in table format if chart fails
  3. Test CDN loading during deployment verification
- **PRD Ref:** TECH-012, FR-109

**TR-RISK-017:** Risk: Poor mobile responsiveness
- **Impact:** Low - poor user experience on mobile devices
- **Likelihood:** Medium (if not tested on mobile)
- **Mitigation:**
  1. Use responsive CSS (media queries)
  2. Test on multiple device sizes
  3. Use viewport meta tag
  4. Ensure forms and tables are mobile-friendly
- **PRD Ref:** TR-FE-005

### 24.7 Risk Summary Table

| Risk ID | Risk Description | Impact | Likelihood | Priority | Mitigation Status |
|---------|------------------|--------|------------|----------|-------------------|
| TR-RISK-001 | Cold start delay | Medium | High | Medium | Documented |
| TR-RISK-002 | Supabase limits | Low | Low | Low | Monitored |
| TR-RISK-003 | RAM limitation | Medium | Medium | Medium | Optimized |
| TR-RISK-004 | SQL injection | Critical | Low | High | Mitigated |
| TR-RISK-005 | Session hijacking | High | Low | High | Mitigated |
| TR-RISK-006 | Weak passwords | Medium | Medium | Medium | Mitigated |
| TR-RISK-007 | Exposed secrets | Critical | Low | High | Mitigated |
| TR-RISK-008 | Orphaned records | Low | Very Low | Low | Mitigated |
| TR-RISK-009 | Duplicate roll numbers | Medium | Very Low | Low | Mitigated |
| TR-RISK-010 | Incorrect calculations | High | Low | High | Tested |
| TR-RISK-011 | Slow queries | Medium | Low | Low | Indexed |
| TR-RISK-012 | Connection exhaustion | High | Low | Medium | Pooled |
| TR-RISK-013 | Missing env vars | High | Medium | High | Documented |
| TR-RISK-014 | Schema not created | High | Medium | High | Documented |
| TR-RISK-015 | Static files missing | Medium | Low | Low | Tested |
| TR-RISK-016 | CDN failure | Medium | Low | Low | Fallback |
| TR-RISK-017 | Poor mobile UX | Low | Medium | Low | Tested |

---

## 25. DEFINITION OF DONE

### 25.1 Development Checklist

**TR-DOD-001:** Backend implementation complete:
- [ ] Flask application structure created as per TR-STRUCT-002
- [ ] All route handlers implemented (auth, dashboard, students, subjects, marks, results, analysis, reports)
- [ ] Database connection and query functions implemented
- [ ] All validation functions implemented (frontend and backend)
- [ ] Result calculation logic implemented and tested
- [ ] Session management and authentication working
- [ ] Error handling implemented for all routes
- [ ] Logging configured

**TR-DOD-002:** Frontend implementation complete:
- [ ] Base template with navigation created
- [ ] All page templates implemented (login, dashboard, CRUD forms, result lookup, analytics)
- [ ] CSS styling complete and responsive
- [ ] JavaScript validation functions implemented
- [ ] Chart.js integration working for all visualizations
- [ ] Search/filter functionality working
- [ ] Print-friendly styles implemented
- [ ] Forms submit correctly with proper validation

**TR-DOD-003:** Database implementation complete:
- [ ] schema.sql created with all tables (admins, students, subjects, marks)
- [ ] All foreign keys and constraints defined
- [ ] Indexes created for performance
- [ ] Initial admin account created (or seed script provided)
- [ ] Sample data available for testing (seed.sql)
- [ ] Database deployed to Supabase
- [ ] Connection verified from application

### 25.2 Testing Checklist

**TR-DOD-004:** Unit testing complete:
- [ ] Validation functions tested (all pass/fail cases)
- [ ] Calculation functions tested (percentage, grade, status)
- [ ] Helper functions tested
- [ ] Test coverage >= 80% for utils/ folder

**TR-DOD-005:** Integration testing complete:
- [ ] All routes tested with Flask test client
- [ ] Database operations tested (CRUD)
- [ ] Authentication flow tested (login, logout, protected routes)
- [ ] Error handling tested (400, 404, 500 errors)

**TR-DOD-006:** Manual testing complete:
- [ ] All admin workflows tested (add/edit/delete students, subjects, marks)
- [ ] Result calculation verified with sample data
- [ ] Public result lookup tested (valid and invalid credentials)
- [ ] Analytics dashboard displays correct data and charts
- [ ] Reports generate correctly (individual and class)
- [ ] Search and filter functions work correctly
- [ ] Session timeout works (30 minutes)
- [ ] Error messages display correctly

**TR-DOD-007:** Cross-browser testing:
- [ ] Tested on Chrome (latest)
- [ ] Tested on Firefox (latest)
- [ ] Tested on Edge (latest)
- [ ] Tested on Safari (latest) - if available
- [ ] Tested on mobile devices (responsive)

### 25.3 Security Checklist

**TR-DOD-008:** Security measures implemented:
- [ ] All passwords hashed with bcrypt (cost 12)
- [ ] SQL injection prevention: All queries use parameterization
- [ ] XSS prevention: Jinja2 auto-escaping enabled
- [ ] Session cookies secure (HttpOnly, Secure in production, SameSite)
- [ ] HTTPS enforced in production
- [ ] Environment variables not committed to Git (.env in .gitignore)
- [ ] Debug mode disabled in production (FLASK_DEBUG=0)
- [ ] Error messages don't expose sensitive information
- [ ] Login rate limiting implemented (optional but recommended)

**TR-DOD-009:** Security testing complete:
- [ ] Attempted SQL injection (all queries safe)
- [ ] Attempted XSS attacks (all inputs escaped)
- [ ] Verified session expiration works
- [ ] Verified protected routes require authentication
- [ ] Verified error pages don't expose stack traces in production

### 25.4 Deployment Checklist

**TR-DOD-010:** Pre-deployment tasks:
- [ ] Code pushed to GitHub repository
- [ ] requirements.txt and runtime.txt created
- [ ] .env.example provided (no real secrets)
- [ ] README.md created with setup instructions
- [ ] .gitignore properly configured

**TR-DOD-011:** Deployment configuration:
- [ ] Render web service created
- [ ] Render build and start commands configured
- [ ] Environment variables set in Render dashboard (SECRET_KEY, DATABASE_URL, FLASK_ENV=production)
- [ ] Supabase project created
- [ ] Database schema deployed to Supabase
- [ ] Initial admin account created in production database
- [ ] Application deployed successfully to Render

**TR-DOD-012:** Post-deployment verification:
- [ ] Application accessible at Render URL
- [ ] HTTPS working (automatic SSL certificate)
- [ ] Login works with admin credentials
- [ ] Dashboard displays correctly
- [ ] CRUD operations work (add, edit, delete)
- [ ] Result lookup works
- [ ] Analytics charts render correctly
- [ ] Static files (CSS, JS, images) load correctly
- [ ] Database connection working
- [ ] No console errors in browser DevTools
- [ ] Cold start handled gracefully (loading message)

### 25.5 Documentation Checklist

**TR-DOD-013:** Project documentation complete:
- [ ] README.md with project overview, features, tech stack
- [ ] Setup instructions for local development
- [ ] Deployment instructions (Render + Supabase)
- [ ] Environment variable documentation
- [ ] Database schema documentation
- [ ] API/route documentation (optional)
- [ ] User guide (admin workflows)
- [ ] Screenshots of key pages (optional)

**TR-DOD-014:** Technical documentation complete:
- [ ] PRD.md (Product Requirements Document) - already provided
- [ ] TRD.md (Technical Requirements Document) - this document
- [ ] Code comments in complex functions
- [ ] Inline documentation for APIs/functions

### 25.6 Code Quality Checklist

**TR-DOD-015:** Code quality standards:
- [ ] Python code follows PEP 8 style guidelines
- [ ] Functions are modular with single responsibility
- [ ] No hardcoded credentials or secrets in code
- [ ] Meaningful variable and function names
- [ ] Error handling comprehensive (try-except blocks)
- [ ] Database connections properly closed (finally blocks)
- [ ] No unused imports or variables
- [ ] Code formatted consistently

**TR-DOD-016:** Code review complete:
- [ ] All validation logic reviewed
- [ ] All database queries reviewed (parameterization verified)
- [ ] All authentication and authorization logic reviewed
- [ ] All calculation logic reviewed for correctness
- [ ] Error handling reviewed

### 25.7 Performance Checklist

**TR-DOD-017:** Performance optimization:
- [ ] Database indexes created for frequently queried columns
- [ ] Pagination implemented for large lists (if applicable)
- [ ] Database connections pooled or properly managed
- [ ] Unnecessary database queries eliminated (N+1 query problem)
- [ ] Static files cacheable (Flask default headers)
- [ ] Charts render within 1 second

**TR-DOD-018:** Performance testing:
- [ ] Dashboard loads within 3 seconds
- [ ] Form submissions respond within 2 seconds
- [ ] Result calculations complete within 1 second
- [ ] Analytics dashboard loads within 5 seconds
- [ ] Cold start completes within 60 seconds

### 25.8 User Acceptance Checklist

**TR-DOD-019:** Admin user acceptance:
- [ ] Admin can log in and access all features
- [ ] Admin can add, edit, delete students without issues
- [ ] Admin can add, edit, delete subjects without issues
- [ ] Admin can add, edit, delete marks without issues
- [ ] Admin can view and search all data
- [ ] Admin can view analytics dashboard
- [ ] Admin can generate reports
- [ ] All features work as expected in real-world usage

**TR-DOD-020:** Student (public) user acceptance:
- [ ] Students can access result lookup without login
- [ ] Students can view their results with correct roll number + DOB
- [ ] Result displays correct marks, percentage, grade, status
- [ ] Result is printable

### 25.9 Final Sign-Off

**TR-DOD-021:** Project completion criteria:
- [ ] All functional requirements from PRD implemented
- [ ] All technical requirements from TRD implemented
- [ ] All testing completed and passed
- [ ] All security measures in place
- [ ] Deployed to production and verified working
- [ ] Documentation complete
- [ ] User acceptance testing passed
- [ ] Project ready for submission/presentation

**TR-DOD-022:** Sign-off approvals:
- [ ] Developer sign-off (self-review)
- [ ] Peer review (if applicable)
- [ ] Supervisor/mentor review (if applicable)
- [ ] Final testing complete
- [ ] Ready for Diploma project submission

---

## DOCUMENT REVISION HISTORY

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-09-01 | Kiro AI | Initial TRD creation based on PRD v1.0 |

---

## APPENDIX A: ACRONYMS AND DEFINITIONS

**API:** Application Programming Interface  
**CDN:** Content Delivery Network  
**CRUD:** Create, Read, Update, Delete  
**CSRF:** Cross-Site Request Forgery  
**CSS:** Cascading Style Sheets  
**DOB:** Date of Birth  
**HTTPS:** HyperText Transfer Protocol Secure  
**HTML:** HyperText Markup Language  
**MVC:** Model-View-Controller  
**ORM:** Object-Relational Mapping  
**PRD:** Product Requirements Document  
**SQL:** Structured Query Language  
**SSL/TLS:** Secure Sockets Layer / Transport Layer Security  
**TRD:** Technical Requirements Document  
**UI:** User Interface  
**UX:** User Experience  
**WSGI:** Web Server Gateway Interface  
**XSS:** Cross-Site Scripting

---

## APPENDIX B: REFERENCES

1. **Flask Documentation:** https://flask.palletsprojects.com/
2. **PostgreSQL Documentation:** https://www.postgresql.org/docs/
3. **Supabase Documentation:** https://supabase.com/docs
4. **Render Documentation:** https://render.com/docs
5. **Chart.js Documentation:** https://www.chartjs.org/docs/
6. **bcrypt Documentation:** https://pypi.org/project/bcrypt/
7. **psycopg2 Documentation:** https://www.psycopg.org/docs/
8. **PEP 8 Style Guide:** https://pep8.org/
9. **OWASP Top 10:** https://owasp.org/www-project-top-ten/
10. **PRD v1.0:** DOCS/PRD.md (single source of truth)

---

## DOCUMENT END

**Total Sections:** 25  
**Total Technical Requirements:** 500+  
**Last Updated:** 2026-09-01  
**Status:** Complete - Ready for Implementation  

**Next Steps:**
1. Review this TRD with supervisor/mentor
2. Set up development environment (Python, Git, IDE)
3. Create GitHub repository
4. Set up Supabase database project
5. Begin implementation following TRD specifications
6. Use PRD + TRD as single source of truth during development

**Important Notes:**
- Do NOT modify PRD.md
- All implementation decisions have been made in this TRD
- Follow folder structure exactly as specified in Section 18
- Refer to traceability matrix (Section 22) to map PRD requirements to TRD requirements
- Use Definition of Done (Section 25) to verify completion

---

**END OF TECHNICAL REQUIREMENTS DOCUMENT**
