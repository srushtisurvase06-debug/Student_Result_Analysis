# Database Schema

This folder contains the database schema and seed data for the Online Student Result Analysis System.

## Deployment

### Prerequisites

- Supabase account and project created
- DATABASE_URL configured in .env file
- psycopg2 or psql installed (optional, for command-line deployment)

### Deploying to Supabase

#### Method 1: Using Supabase SQL Editor (Recommended)

1. Sign in to your Supabase Dashboard
2. Navigate to **SQL Editor**
3. Copy the entire contents of `schema.sql`
4. Paste into the SQL Editor
5. Click **Run**
6. Verify all tables appear in **Table Editor**
7. Copy the entire contents of `seed.sql`
8. Paste into the SQL Editor
9. Click **Run**
10. Verify data appears in tables

#### Method 2: Using psql (Command Line)

```bash
# Set DATABASE_URL environment variable first
export DATABASE_URL="postgresql://postgres:password@host:5432/database"

# Deploy schema
psql $DATABASE_URL -f schema.sql

# Deploy seed data
psql $DATABASE_URL -f seed.sql
```

### Verifying Deployment

```sql
-- Check tables exist
SELECT table_name FROM information_schema.tables
WHERE table_schema = 'public';

-- Count records
SELECT COUNT(*) FROM admins;
SELECT COUNT(*) FROM students;
SELECT COUNT(*) FROM subjects;
SELECT COUNT(*) FROM marks;

-- Verify admin exists
SELECT id, username, email, full_name FROM admins;
```

## Resetting Database

To reset the database to initial state:

```sql
-- Drop all tables (in correct order due to foreign keys)
DROP TABLE IF EXISTS marks CASCADE;
DROP TABLE IF EXISTS subjects CASCADE;
DROP TABLE IF EXISTS students CASCADE;
DROP TABLE IF EXISTS admins CASCADE;

-- Re-run schema.sql and seed.sql
```

## Schema Diagram

```
┌─────────────────┐
│     admins      │
├─────────────────┤
│ id (PK)         │
│ username (UN)   │
│ email (UN)      │
│ password_hash   │
│ full_name       │
│ created_at      │
│ last_login      │
└─────────────────┘

┌─────────────────┐
│     students    │
├─────────────────┤
│ id (PK)         │
│ roll_number (UN)│
│ name            │
│ email           │
│ date_of_birth   │
│ gender          │
│ contact_number  │
│ created_at      │
│ updated_at      │
└─────────────────┘
         │
         │ 1:N
         │
         ▼
┌─────────────────┐
│     marks       │
├─────────────────┤
│ id (PK)         │
│ student_id (FK) │───► students(id) ON DELETE CASCADE
│ subject_id (FK) │───► subjects(id) ON DELETE RESTRICT
│ marks_obtained  │
│ is_absent       │
│ created_at      │
│ updated_at      │
└─────────────────┘

┌─────────────────┐
│    subjects     │
├─────────────────┤
│ id (PK)         │
│ subject_code (UN)│
│ subject_name    │
│ max_marks       │
│ created_at      │
│ updated_at      │
└─────────────────┘
```

## Table Specifications

### admins
- Stores administrator credentials
- Passwords are bcrypt hashed (cost factor 12)
- Initial admin account: username=`admin`, password=`admin123`

### students
- Student master data
- roll_number is unique identifier
- date_of_birth required for result lookup authentication

### subjects
- Subject master data
- max_marks: Maximum possible marks for the subject
- Each subject has unique subject_code

### marks
- Student-subject marks records
- Composite unique constraint on (student_id, subject_id)
- is_absent flag for absent students
- Foreign key to students: ON DELETE CASCADE (marks deleted if student deleted)
- Foreign key to subjects: ON DELETE RESTRICT (cannot delete subject if marks exist)

## Environment Variables

The DATABASE_URL must be set before running SQL:

```
DATABASE_URL=postgresql://postgres:password@host:5432/database
```

## Notes

- This schema uses PostgreSQL features (SERIAL, TIMESTAMP, CHECK constraints, FOREIGN KEY)
- All connections use SSL (sslmode='require')
- No credentials are stored in these files
- Run `seed.sql` only after `schema.sql` completes successfully
