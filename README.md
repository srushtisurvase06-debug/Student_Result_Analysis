# Online Student Result Analysis System

A web-based result management system that automates student result calculation, provides performance analytics, and enables secure online result access.

## Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Backend | Python | 3.11+ |
| Web Framework | Flask | 3.0.0 |
| Database | PostgreSQL | Latest (Supabase) |
| Frontend | HTML, CSS, JavaScript | Standard |
| Charts | Chart.js | 4.x |

## Features

- Admin authentication and dashboard
- Student management (CRUD)
- Subject management (CRUD)
- Marks entry and management
- Automatic result calculation
- Performance analysis with visual charts
- Student result lookup (public page)
- Printable reports

## Setup Instructions

### Prerequisites

- Python 3.11 or higher
- PostgreSQL database (Supabase recommended)
- Git

### Local Development

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory:
   ```
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=postgresql://user:password@host:5432/database
   FLASK_ENV=development
   FLASK_DEBUG=1
   ```

4. Run the application:
   ```bash
   cd CODEBASE/BACKEND
   python app.py
   ```

5. Access the application at `http://localhost:5000`

## Deployment

This project is designed to be deployed on:
- **Backend/Frontend:** Render (Free Tier)
- **Database:** Supabase PostgreSQL (Free Tier)

## Project Structure

```
Student_Result_Analysis/
├── CODEBASE/
│   ├── BACKEND/
│   │   ├── app.py              # Flask application entry point
│   │   ├── config.py           # Configuration management
│   │   ├── routes/             # Route handlers
│   │   ├── utils/              # Utility modules
│   │   ├── static/             # Static files (CSS, JS, images)
│   │   └── templates/          # Jinja2 templates
│   ├── DATABASE/               # Database schema and scripts
│   └── FRONTEND/               # Frontend assets (if separate)
├── DOCS/
│   ├── PRD.md                  # Product Requirements Document
│   ├── TRD.md                  # Technical Requirements Document
│   └── PHASE.md                # Implementation Roadmap
└── requirements.txt
```

## API/Endpoints

- `GET /` - API status
- `GET /health` - Health check
- `POST /login` - Admin login (to be implemented)
- `POST /logout` - Admin logout (to be implemented)

## Security Features

- Password hashing with bcrypt
- Session-based authentication
- SQL injection prevention
- XSS protection
- HTTPS enforcement in production

## Testing

```bash
pytest tests/ -v
pytest tests/ --cov=. --cov-report=html
```

## License

MIT License
