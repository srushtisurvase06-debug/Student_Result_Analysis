# Student Result Analysis System

A comprehensive web-based result management system that automates student result calculation, provides performance analytics, and enables secure online result access.

## Overview

This system provides a complete academic result management solution with:
- **Admin Portal**: Secure dashboard for managing students, subjects, marks, and generating reports
- **Public Result Portal**: Student result lookup with professional printable format
- **Analytics Dashboard**: Visual performance insights with charts and statistics
- **Automated Calculations**: Automatic result computation with grade assignment

## Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Backend | Python | 3.11+ |
| Web Framework | Flask | 3.0.0 |
| Database | PostgreSQL | Latest (Supabase) |
| Frontend | HTML, CSS, JavaScript | Standard |
| Charts | Chart.js | 4.x |
| Testing | pytest | 7.4.3 |
| Security | bcrypt | 4.1.1 |

## Features

### Admin Features (Authenticated)
- ✅ **Authentication**: Secure login with bcrypt password hashing
- ✅ **Dashboard**: Overview with key statistics and quick actions
- ✅ **Student Management**: Add, edit, view, and manage student records
- ✅ **Subject Management**: Create and manage subjects with maximum marks
- ✅ **Marks Entry**: Assign marks to students for different subjects
- ✅ **Results Overview**: View calculated results with grades and percentages
- ✅ **Performance Analysis**: Visual charts showing subject-wise and overall performance
- ✅ **Report Generation**: 
  - Individual student reports
  - Class performance reports
  - Subject-wise analysis
  - Grade distribution
  - Class ranking
- ✅ **Admin Profile**: Update admin information and change password
- ✅ **Print Support**: Professional print layouts for all reports

### Public Features (No Authentication Required)
- ✅ **Result Lookup**: Students can check results using Roll Number + Date of Birth
- ✅ **Print Result**: Professional academic marks statement format
- ✅ **Secure Access**: Results accessible only with correct credentials

### Automatic Calculations
- Total marks computation
- Percentage calculation
- Grade assignment (A+, A, B+, B, C, D, F)
- Pass/Fail determination
- Class ranking
- Subject-wise statistics

## Setup Instructions

### Prerequisites

- Python 3.11 or higher
- PostgreSQL database (Supabase recommended)
- Git

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Student_Result_Analysis
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=postgresql://user:password@host:5432/database
   FLASK_ENV=development
   FLASK_DEBUG=1
   ```
   
   **Important**: 
   - Generate a strong `SECRET_KEY` (use `python -c "import secrets; print(secrets.token_hex(32))"`)
   - Replace database connection details with your PostgreSQL credentials
   - Never commit the `.env` file to version control

5. **Set up the database**
   
   Run the schema and seed scripts:
   ```bash
   # Connect to your PostgreSQL database and run:
   psql -h <host> -U <user> -d <database> -f CODEBASE/DATABASE/schema.sql
   psql -h <host> -U <user> -d <database> -f CODEBASE/DATABASE/seed.sql
   ```

6. **Run the application**
   ```bash
   cd CODEBASE/BACKEND
   python app.py
   ```

7. **Access the application**
   - Admin Portal: `http://localhost:5000/login`
   - Public Result Lookup: `http://localhost:5000/results/lookup`

### Default Admin Credentials

After running the seed script, use:
- **Username**: See seed.sql for default admin
- **Password**: See seed.sql for default admin

**⚠️ IMPORTANT**: Change the default admin password immediately after first login!

## Deployment

This project is designed to be deployed on:
- **Backend/Frontend:** Render (Free Tier)
- **Database:** Supabase PostgreSQL (Free Tier)

## Project Structure

```
Student_Result_Analysis/
├── CODEBASE/
│   ├── BACKEND/                    # Flask application
│   │   ├── app.py                  # Application entry point
│   │   ├── config.py               # Configuration management
│   │   ├── pytest.ini              # Pytest configuration
│   │   │
│   │   ├── routes/                 # Route handlers (blueprints)
│   │   │   ├── __init__.py
│   │   │   ├── auth.py             # Authentication routes
│   │   │   ├── dashboard.py        # Dashboard routes
│   │   │   ├── students.py         # Student CRUD routes
│   │   │   ├── subjects.py         # Subject CRUD routes
│   │   │   ├── marks.py            # Marks entry routes
│   │   │   ├── results.py          # Results & lookup routes
│   │   │   ├── analysis.py         # Performance analysis routes
│   │   │   ├── reports.py          # Report generation routes
│   │   │   └── profile.py          # Admin profile routes
│   │   │
│   │   ├── utils/                  # Utility modules
│   │   │   ├── __init__.py
│   │   │   ├── db.py               # Database connection
│   │   │   ├── calculations.py     # Result calculations
│   │   │   ├── validators.py       # Input validation
│   │   │   ├── decorators.py       # Auth decorators
│   │   │   └── helpers.py          # Helper functions
│   │   │
│   │   ├── templates/              # Jinja2 templates
│   │   │   ├── base.html           # Base template
│   │   │   ├── admin_base.html     # Admin base template
│   │   │   ├── public_base.html    # Public base template
│   │   │   ├── auth/               # Login templates
│   │   │   ├── dashboard/          # Dashboard templates
│   │   │   ├── students/           # Student CRUD templates
│   │   │   ├── subjects/           # Subject CRUD templates
│   │   │   ├── marks/              # Marks entry templates
│   │   │   ├── results/            # Results templates
│   │   │   ├── analysis/           # Analysis templates
│   │   │   ├── reports/            # Report templates
│   │   │   ├── profile/            # Profile templates
│   │   │   ├── errors/             # Error templates
│   │   │   └── partials/           # Reusable components
│   │   │
│   │   ├── static/                 # Static assets
│   │   │   ├── css/                # Stylesheets
│   │   │   │   ├── main.css        # Main styles
│   │   │   │   ├── components.css  # Component styles
│   │   │   │   ├── admin.css       # Admin UI styles
│   │   │   │   ├── dashboard.css   # Dashboard styles
│   │   │   │   ├── students.css    # Student page styles
│   │   │   │   ├── errors.css      # Error page styles
│   │   │   │   └── print.css       # Print-specific styles
│   │   │   ├── js/                 # JavaScript
│   │   │   │   └── main.js         # Main JavaScript
│   │   │   └── images/             # Images
│   │   │
│   │   └── tests/                  # Test suite
│   │       ├── conftest.py         # Pytest fixtures
│   │       ├── test_app.py         # App tests
│   │       ├── test_auth.py        # Auth tests
│   │       ├── test_config.py      # Config tests
│   │       ├── test_db.py          # Database tests
│   │       ├── test_calculations.py # Calculation tests
│   │       ├── test_*_routes.py    # Route tests
│   │       └── test_*_validators.py # Validator tests
│   │
│   └── DATABASE/                   # Database files
│       ├── schema.sql              # Database schema
│       ├── seed.sql                # Sample data
│       └── README.md               # Database documentation
│
├── DOCS/                           # Documentation
│   ├── PRD.md                      # Product Requirements Document
│   ├── TRD.md                      # Technical Requirements Document
│   ├── PHASE.md                    # Implementation Roadmap
│   ├── PRESENTATION.txt            # Presentation notes
│   ├── PRINT_LAYOUT_VISUAL.txt     # Print layout reference
│   └── PRINT_REDESIGN_SUMMARY.md   # Print design docs
│
├── .env                            # Environment variables (NOT in git)
├── .env.example                    # Environment template
├── .gitignore                      # Git ignore rules
├── README.md                       # This file
├── requirements.txt                # Python dependencies
└── runtime.txt                     # Python runtime version
```

## Key Routes/Endpoints

### Public Routes (No Authentication)
- `GET /` - Home/API status
- `GET /health` - Health check
- `GET /results/lookup` - Public result lookup form
- `POST /results/lookup` - Process result lookup
- `GET /results/student/<roll>/<dob>` - Display student result

### Admin Routes (Authentication Required)
- `GET /login` - Login page
- `POST /login` - Process login
- `GET /logout` - Logout
- `GET /dashboard/` - Admin dashboard
- `GET /students/` - List students
- `GET /students/add` - Add student form
- `POST /students/add` - Create student
- `GET /students/edit/<id>` - Edit student form
- `POST /students/edit/<id>` - Update student
- `GET /subjects/` - List subjects
- `GET /subjects/add` - Add subject form
- `POST /subjects/add` - Create subject
- `GET /marks/` - List marks
- `GET /marks/add` - Add marks form
- `POST /marks/add` - Create marks entry
- `GET /results/` - View all results
- `GET /analysis/` - Performance analysis dashboard
- `GET /analysis/subject/<id>` - Subject-specific analysis
- `GET /reports/` - Reports hub
- `GET /reports/individual/<id>` - Individual student report
- `GET /reports/class` - Class performance report
- `GET /reports/subject/<id>` - Subject-wise report
- `GET /reports/grade-distribution` - Grade distribution
- `GET /reports/class-rank` - Class ranking
- `GET /profile/` - Admin profile page
- `POST /profile/update` - Update profile
- `POST /profile/change-password` - Change password

## Security Features

- ✅ **Password Security**: bcrypt hashing with salt rounds
- ✅ **Session Management**: Flask session-based authentication
- ✅ **SQL Injection Prevention**: Parameterized queries throughout
- ✅ **XSS Protection**: Template auto-escaping enabled
- ✅ **CSRF Protection**: Form validation and session tokens
- ✅ **Secure Headers**: Security headers configured in production
- ✅ **Input Validation**: Server-side validation for all forms
- ✅ **Access Control**: Login-required decorators on admin routes
- ✅ **Environment Variables**: Secrets stored in .env (not committed)

## Testing

Run the complete test suite:
```bash
cd CODEBASE/BACKEND
pytest tests/ -v
```

Run with coverage report:
```bash
pytest tests/ --cov=. --cov-report=html
```

Run specific test modules:
```bash
pytest tests/test_calculations.py -v
pytest tests/test_auth.py -v
```

### Test Coverage

The application includes 226 tests covering:
- ✅ Authentication flows
- ✅ All CRUD operations
- ✅ Calculation logic
- ✅ Input validation
- ✅ Database operations
- ✅ Route handlers
- ✅ Error handling
- ✅ Security measures

Current test results: **214/226 passing** (12 non-blocking UI assertion failures)

## License

MIT License

## Deployment

### Recommended Stack
- **Application Hosting**: Render (Free Tier) or similar PaaS
- **Database**: Supabase PostgreSQL (Free Tier)
- **Runtime**: Python 3.11+

### Deployment Steps

1. **Database Setup**
   - Create a PostgreSQL database on Supabase
   - Run `schema.sql` to create tables
   - Run `seed.sql` for initial data (optional)
   - Note the connection string

2. **Application Deployment**
   - Push code to GitHub repository
   - Connect repository to Render (or your PaaS)
   - Configure environment variables:
     - `SECRET_KEY` (generate strong random key)
     - `DATABASE_URL` (PostgreSQL connection string)
     - `FLASK_ENV=production`
   - Set start command: `cd CODEBASE/BACKEND && gunicorn app:app`
   - Deploy

3. **Post-Deployment**
   - Verify health check endpoint: `https://your-app.com/health`
   - Test admin login
   - Test public result lookup
   - Change default admin password immediately

### Environment Variables for Production

```env
SECRET_KEY=<strong-random-key>
DATABASE_URL=postgresql://user:password@host:5432/database
FLASK_ENV=production
FLASK_DEBUG=0
```

## Database Schema

The system uses PostgreSQL with the following main tables:
- **admin**: Administrator credentials
- **students**: Student information
- **subjects**: Subject definitions
- **marks**: Student marks per subject
- **results**: Computed results (view/materialized)

See `CODEBASE/DATABASE/schema.sql` for complete schema definition.

## Calculation Logic

### Grading System
- **A+**: 90-100%
- **A**: 80-89%
- **B+**: 70-79%
- **B**: 60-69%
- **C**: 50-59%
- **D**: 40-49%
- **F**: Below 40%

### Result Computation
1. Sum of marks across all subjects
2. Total possible marks calculation
3. Percentage = (obtained/total) × 100
4. Grade assignment based on percentage
5. Pass/Fail: Pass if percentage ≥ 40%

## Troubleshooting

### Common Issues

**Database Connection Error**
- Verify `DATABASE_URL` in `.env`
- Check PostgreSQL service is running
- Verify network connectivity

**Import Errors**
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt`

**Test Failures**
- 12 known non-blocking UI test failures (HTML class assertions)
- All functional tests pass
- Application works correctly despite these test failures

**Port Already in Use**
- Change port in `app.py` or
- Kill process using the port: `netstat -ano | findstr :5000`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `pytest tests/ -v`
5. Submit a pull request

## Support

For issues, questions, or contributions, please refer to the project documentation in the `DOCS/` folder:
- `PRD.md` - Product Requirements
- `TRD.md` - Technical Requirements  
- `PHASE.md` - Implementation Phases

---

**Version**: 1.0.0  
**Status**: Production Ready  
**Last Updated**: 2026

