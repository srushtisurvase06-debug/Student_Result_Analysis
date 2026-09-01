# PRODUCT REQUIREMENTS DOCUMENT (PRD)

## Online Student Result Analysis System

**Version:** 1.0  
**Date:** September 1, 2026  
**Project Type:** Diploma Final-Year Project  
**Document Owner:** Product Requirements  

---

## TABLE OF CONTENTS

1. [Project Overview](#1-project-overview)
2. [User Roles](#2-user-roles)
3. [Core Features](#3-core-features)
4. [Result Calculation Logic](#4-result-calculation-logic)
5. [Functional Requirements](#5-functional-requirements)
6. [Database Requirements](#6-database-requirements)
7. [Security Requirements](#7-security-requirements)
8. [UI/UX Requirements](#8-uiux-requirements)
9. [Dashboard Requirements](#9-dashboard-requirements)
10. [Search, Filter, and Sort](#10-search-filter-and-sort)
11. [Validation Rules](#11-validation-rules)
12. [Error Handling](#12-error-handling)
13. [Reporting & Analytics](#13-reporting--analytics)
14. [Non-Functional Requirements](#14-non-functional-requirements)
15. [Deployment Requirements](#15-deployment-requirements)
16. [Testing Requirements](#16-testing-requirements)
17. [Demo / Viva Requirements](#17-demo--viva-requirements)
18. [Sample Data Requirements](#18-sample-data-requirements)
19. [Future Enhancements](#19-future-enhancements)
20. [MVP Definition](#20-mvp-definition)
21. [Acceptance Criteria](#21-acceptance-criteria)
22. [Final Project Summary](#22-final-project-summary)
23. [PRD Approval Checklist](#23-prd-approval-checklist)

---

## 1. PROJECT OVERVIEW

### 1.1 Project Name
**Online Student Result Analysis System**

### 1.2 Problem Statement
Educational institutions manually manage student results using spreadsheets or paper-based systems, leading to:
- Time-consuming manual calculation of grades and percentages
- High risk of human errors in result computation
- Difficulty in analyzing class performance trends
- Inefficient result distribution to students
- Lack of instant performance insights for administrators and faculty

### 1.3 Proposed Solution
A web-based result management system that:
- Automates result calculation (total, percentage, grade, pass/fail)
- Provides instant performance analysis and visualization
- Enables secure online result access for students
- Generates comprehensive reports for administrators
- Maintains centralized database of all academic records

### 1.4 Project Vision
To create a reliable, user-friendly, and fully functional academic result management system suitable for demonstration in a diploma final-year project viva, showcasing practical software engineering skills and deployment capabilities.

### 1.5 Project Objectives
1. Automate student result calculation and grade assignment
2. Provide real-time performance analysis and insights
3. Enable secure access control for different user roles
4. Generate professional result reports
5. Demonstrate full-stack development skills using Python Flask
6. Successfully deploy to production environment (Render + Supabase)
7. Create a system that can be demonstrated live in 5-10 minutes

### 1.6 Target Users

| User Role | Count (Typical) | Primary Need |
|-----------|----------------|--------------|
| Administrator | 1-5 | Complete system management and analysis |
| Students | 50-500 | View personal results securely |

**Note:** Teacher/Faculty role is excluded from MVP (see Section 1.8 for rationale)

### 1.7 Target Institution
- Diploma-level educational institutions
- Polytechnic colleges
- Technical training centers
- Small to medium-sized departments (50-500 students)

### 1.8 Expected Benefits

**For Institution:**
- Reduced administrative workload by 70%
- Elimination of manual calculation errors
- Instant result generation
- Centralized data management
- Easy performance tracking

**For Students:**
- 24/7 result access
- Clear performance breakdown
- Instant grade information
- No dependency on physical result cards

**For Project Demonstration:**
- Complete end-to-end workflow
- Visual analytics for impressive viva presentation
- Real-world applicable system
- Demonstrates database design, backend logic, frontend development, and deployment skills

### 1.9 Project Scope

**IN SCOPE:**
- Admin authentication and dashboard
- Student registration and management (CRUD)
- Subject management (CRUD)
- Marks entry and management
- Automatic result calculation (total, percentage, grade, pass/fail)
- Performance analysis dashboard with key metrics
- Visual charts (bar charts, pie charts)
- Individual student result view
- Class-wide reports
- Subject-wise performance analysis
- Search and filter functionality
- Responsive web design (desktop and mobile)
- Input validation (frontend and backend)
- Secure database operations
- Production deployment on free tier services

**OUT OF SCOPE:**
- Teacher/Faculty separate role (Admin performs all management tasks)
- Student self-registration (Admin creates all student accounts)
- Email/SMS notifications
- Parent login portal
- Attendance integration
- Fee management
- Library management
- Multiple departments/branches
- Multiple institutions (single institution only)
- PDF generation (unless trivially implementable)
- Advanced AI/ML predictions
- Mobile native apps
- Offline mode
- Real-time collaboration features
- Exam schedule management
- Question paper management

### 1.10 Assumptions
1. One institution with one admin managing the system
2. Single academic year/semester focus (can add year field if needed)
3. All subjects have equal maximum marks (e.g., 100) - configurable
4. Simple grading system (A, B, C, D, F)
5. Students access results via Roll Number + Date of Birth (no student login in MVP)
6. Admin has basic computer literacy
7. Internet connectivity available during result access
8. Desktop browser is primary access method (mobile responsive as secondary)

---

## 2. USER ROLES

### 2.1 Role: Administrator

**Purpose:**  
Complete system management including student data, subjects, marks entry, result generation, and performance analysis.

**Authentication:**
- Login with email/username and password
- Session-based authentication
- Secure logout

**Permissions:**

| Action | Students | Subjects | Marks | Results | Reports | Settings |
|--------|----------|----------|-------|---------|---------|----------|
| Create | ✅ | ✅ | ✅ | Auto-generated | ✅ | N/A |
| Read | ✅ | ✅ | ✅ | ✅ | ✅ | N/A |
| Update | ✅ | ✅ | ✅ | Auto-updated | N/A | N/A |
| Delete | ✅ | ✅ | ✅ | ✅ | N/A | N/A |

**Can Access:**
- Admin dashboard with analytics
- Complete student database
- All subjects
- All marks records
- All calculated results
- Performance analysis charts
- Class reports
- Search/filter across all data

**Cannot Access:**
- Other admin accounts (single admin system)
- System configuration beyond application scope
- Database direct access (only through application)

### 2.2 Role: Student

**Purpose:**  
View personal academic results and performance summary.

**Authentication:**
- Public result lookup page
- Authenticate using Roll Number + Date of Birth
- No persistent login session (stateless lookup)

**Permissions:**

| Action | Own Results | Other Student Results | Marks Entry | Reports |
|--------|-------------|----------------------|-------------|---------|
| Read | ✅ | ❌ | ❌ | ❌ |
| Create | ❌ | ❌ | ❌ | ❌ |
| Update | ❌ | ❌ | ❌ | ❌ |
| Delete | ❌ | ❌ | ❌ | ❌ |

**Can Access:**
- Personal result page showing:
  - Subject-wise marks
  - Total marks
  - Percentage
  - Grade
  - Pass/Fail status
  - Individual subject status

**Cannot Access:**
- Other students' results
- Class average or comparison data
- Admin dashboard
- Marks entry system
- Analytics and reports
- Any modification capabilities

### 2.3 Role: Teacher/Faculty (EXCLUDED FROM MVP)

**Rationale for Exclusion:**
1. Adds complexity without substantial demo value
2. Admin can perform marks entry efficiently for diploma project scale
3. Separate role requires additional authentication and authorization logic
4. Not essential for demonstrating core result analysis functionality
5. Can be listed as "Future Enhancement"
6. Simplifies the system for viva demonstration

---

## 3. CORE FEATURES

### 3.1 Admin Features

#### 3.1.1 Authentication
- **FR-001:** Secure admin login with email and password
- **FR-002:** Session management with automatic timeout (30 minutes)
- **FR-003:** Secure logout functionality
- **FR-004:** Password stored as hash (never plaintext)

#### 3.1.2 Dashboard
- **FR-005:** Display total number of students
- **FR-006:** Display total number of subjects
- **FR-007:** Display total results generated
- **FR-008:** Calculate and display overall pass percentage
- **FR-009:** Calculate and display overall fail percentage
- **FR-010:** Calculate and display class average percentage
- **FR-011:** Display top 5 performing students
- **FR-012:** Display visual charts (bar chart for grade distribution, pie chart for pass/fail ratio)

#### 3.1.3 Student Management
- **FR-013:** Add new student with: Roll Number, Name, Email, Date of Birth, Gender, Contact
- **FR-014:** View all students in tabular format
- **FR-015:** Search students by Roll Number or Name
- **FR-016:** Filter students by Gender
- **FR-017:** Edit student information
- **FR-018:** Delete student (with confirmation)
- **FR-019:** Prevent duplicate Roll Numbers
- **FR-020:** Validate all student input fields

#### 3.1.4 Subject Management
- **FR-021:** Add new subject with: Subject Code, Subject Name, Maximum Marks
- **FR-022:** View all subjects in tabular format
- **FR-023:** Search subjects by Code or Name
- **FR-024:** Edit subject information
- **FR-025:** Delete subject (with confirmation and dependency check)
- **FR-026:** Prevent duplicate Subject Codes
- **FR-027:** Validate maximum marks (must be positive integer)

#### 3.1.5 Marks Management
- **FR-028:** Enter marks for a student across all subjects
- **FR-029:** View all marks records
- **FR-030:** Search marks by Roll Number or Subject
- **FR-031:** Edit marks (with validation)
- **FR-032:** Delete marks record (with confirmation)
- **FR-033:** Validate marks: 0 ≤ marks ≤ maximum marks
- **FR-034:** Prevent duplicate marks entry (one record per student per subject)
- **FR-035:** Allow marking student as "Absent" (special designation)

#### 3.1.6 Result Generation
- **FR-036:** Automatically calculate total marks for each student
- **FR-037:** Automatically calculate percentage
- **FR-038:** Automatically assign grade based on percentage
- **FR-039:** Automatically determine Pass/Fail status
- **FR-040:** Display calculated results in admin panel
- **FR-041:** Allow result regeneration/refresh after marks update

#### 3.1.7 Performance Analysis
- **FR-042:** Display class average across all subjects
- **FR-043:** Display subject-wise average marks
- **FR-044:** Display highest marks per subject
- **FR-045:** Display lowest marks per subject
- **FR-046:** Calculate pass percentage per subject
- **FR-047:** Calculate fail percentage per subject
- **FR-048:** Identify top 10 performers
- **FR-049:** Identify students below class average
- **FR-050:** Display grade distribution (A, B, C, D, F counts)
- **FR-051:** Identify weak subjects (lowest average)
- **FR-052:** Identify strong subjects (highest average)

#### 3.1.8 Reports
- **FR-053:** Generate individual student report showing all details
- **FR-054:** Generate class result report (all students summary)
- **FR-055:** Generate subject performance report
- **FR-056:** Generate overall analysis report
- **FR-057:** Make reports printable (print-friendly CSS)
- **FR-058:** Display reports in clean tabular format

### 3.2 Student Features

#### 3.2.1 Result Lookup
- **FR-059:** Public result lookup page (no login required)
- **FR-060:** Authenticate using Roll Number + Date of Birth
- **FR-061:** Display personal result page upon successful authentication
- **FR-062:** Show subject-wise marks in table format
- **FR-063:** Display obtained marks and maximum marks per subject
- **FR-064:** Display total marks obtained
- **FR-065:** Display total maximum marks
- **FR-066:** Display calculated percentage
- **FR-067:** Display assigned grade
- **FR-068:** Display Pass/Fail status with color coding
- **FR-069:** Display individual subject status (Pass/Fail per subject)
- **FR-070:** Show "No result available" message if marks not entered
- **FR-071:** Prevent access to other students' results
- **FR-072:** Make result page printable

---

## 4. RESULT CALCULATION LOGIC

### 4.1 Calculation Formulas

#### 4.1.1 Total Marks
```
Total Marks Obtained = Sum of marks obtained in all subjects
Total Maximum Marks = Sum of maximum marks for all subjects
```

**Example:**
- Math: 85/100
- Science: 78/100
- English: 92/100
- Total: 255/300

#### 4.1.2 Percentage
```
Percentage = (Total Marks Obtained / Total Maximum Marks) × 100
Round to 2 decimal places
```

**Example:**
- Percentage = (255 / 300) × 100 = 85.00%

#### 4.1.3 Grade Assignment

**Default Grading Scale (Configurable):**

| Percentage Range | Grade | Description |
|-----------------|-------|-------------|
| 90 - 100 | A | Outstanding |
| 75 - 89 | B | Excellent |
| 60 - 74 | C | Good |
| 40 - 59 | D | Pass |
| 0 - 39 | F | Fail |

**Configuration:**
- Store grading scale in application constants or configuration file
- Easy to modify for different institutions

#### 4.1.4 Overall Pass/Fail Status

**Rules:**
1. **Pass:** Student must score ≥ 40% in EACH subject AND overall percentage ≥ 40%
2. **Fail:** Student fails if:
   - Any subject marks < 40% of that subject's maximum marks, OR
   - Overall percentage < 40%

**Passing Criteria:**
```
For each subject:
  Subject Passing Marks = Maximum Marks × 0.40

Overall Pass = (All subjects passed) AND (Overall percentage ≥ 40%)
```

**Examples:**

| Scenario | Math | Science | English | Total | Percentage | Status |
|----------|------|---------|---------|-------|------------|--------|
| Pass All | 85/100 | 78/100 | 92/100 | 255/300 | 85.00% | PASS |
| Fail One Subject | 85/100 | 35/100 | 92/100 | 212/300 | 70.67% | FAIL (Science < 40) |
| Fail Overall | 42/100 | 41/100 | 38/100 | 121/300 | 40.33% | FAIL (English < 40) |

### 4.2 Edge Cases and Special Scenarios

#### 4.2.1 Absent Students
- **Rule:** If a student is marked "Absent" for any subject, marks = 0 for that subject
- **Status:** Automatically FAIL overall
- **Display:** Show "Absent" indicator on result

#### 4.2.2 Missing Marks
- **Rule:** If marks not entered for a student in any subject
- **Status:** Result not generated / Result status = "Incomplete"
- **Display:** "Result not available yet" message to student
- **Admin View:** Show "Incomplete" status with indication of missing subjects

#### 4.2.3 Zero Marks
- **Rule:** Zero is a valid marks value
- **Calculation:** Include in calculations normally
- **Status:** Will likely result in FAIL status

#### 4.2.4 Full Marks
- **Rule:** Student can score maximum marks
- **Validation:** Marks = Maximum marks is valid

#### 4.2.5 Invalid Marks Entry
- **Prevention:** Frontend and backend validation
- **Rules:**
  - Marks must be numeric
  - Marks cannot be negative
  - Marks cannot exceed subject maximum marks
  - Marks should be integers (no decimals)

#### 4.2.6 Duplicate Marks Entry
- **Prevention:** Database unique constraint on (student_id, subject_id)
- **Handling:** Show error message "Marks already exist for this student-subject combination"
- **Solution:** User must update existing record, not create duplicate

#### 4.2.7 Different Maximum Marks per Subject
- **Support:** YES - each subject can have different maximum marks
- **Storage:** Maximum marks stored in subjects table
- **Calculation:** Use subject-specific maximum marks for percentage calculation

#### 4.2.8 Subject Deletion with Existing Marks
- **Prevention:** Check for existing marks before allowing subject deletion
- **Handling:** Show error "Cannot delete subject with existing marks records"
- **Solution:** Admin must delete marks records first, then delete subject

#### 4.2.9 Student Deletion with Existing Marks
- **Prevention:** Check for existing marks before allowing student deletion
- **Handling:** Show warning "This will delete all marks and results for this student"
- **Solution:** Require explicit confirmation before cascading delete

---

## 5. FUNCTIONAL REQUIREMENTS

### 5.1 Authentication & Authorization

**FR-001:** The system shall provide a secure login page for administrators with email/username and password fields.

**FR-002:** The system shall hash passwords using a secure hashing algorithm (bcrypt or similar) before storing in database.

**FR-003:** The system shall create a session upon successful admin login with 30-minute timeout.

**FR-004:** The system shall validate admin credentials against the admins table in database.

**FR-005:** The system shall display appropriate error messages for invalid login attempts.

**FR-006:** The system shall provide a logout button accessible from all admin pages.

**FR-007:** The system shall destroy the session and redirect to login page upon logout.

**FR-008:** The system shall protect all admin routes and redirect unauthorized access to login page.

**FR-009:** The system shall provide a public result lookup page accessible without authentication.

**FR-010:** The system shall validate student result lookup using Roll Number and Date of Birth.

### 5.2 Admin Dashboard

**FR-011:** The system shall display a dashboard immediately after admin login.

**FR-012:** The dashboard shall show the total count of students registered in the system.

**FR-013:** The dashboard shall show the total count of subjects in the system.

**FR-014:** The dashboard shall show the total count of students with complete results.

**FR-015:** The dashboard shall calculate and display the overall class pass percentage.

**FR-016:** The dashboard shall calculate and display the overall class fail percentage.

**FR-017:** The dashboard shall calculate and display the class average percentage.

**FR-018:** The dashboard shall display the top 5 students ranked by percentage.

**FR-019:** The dashboard shall display a bar chart showing grade distribution (count of A, B, C, D, F).

**FR-020:** The dashboard shall display a pie chart showing pass vs fail ratio.

**FR-021:** The dashboard shall provide navigation links to all major sections (Students, Subjects, Marks, Reports, Analysis).

### 5.3 Student Management

**FR-022:** The system shall provide an "Add Student" form with fields: Roll Number, Name, Email, Date of Birth, Gender, Contact Number.

**FR-023:** The system shall validate that Roll Number is unique before creating a student record.

**FR-024:** The system shall validate that Email format is valid.

**FR-025:** The system shall validate that Date of Birth is in the past.

**FR-026:** The system shall validate that Contact Number contains only digits and is 10 characters.

**FR-027:** The system shall require all student fields except Email and Contact to be mandatory.

**FR-028:** The system shall display all students in a paginated table showing Roll Number, Name, Email, DOB, Gender, Contact.

**FR-029:** The system shall provide a search box to filter students by Roll Number or Name (partial match).

**FR-030:** The system shall provide a dropdown to filter students by Gender.

**FR-031:** The system shall provide an "Edit" button for each student in the table.

**FR-032:** The system shall populate the edit form with existing student data.

**FR-033:** The system shall validate edited data with same rules as create.

**FR-034:** The system shall update student record in database upon successful validation.

**FR-035:** The system shall provide a "Delete" button for each student with confirmation dialog.

**FR-036:** The system shall check for existing marks records before deleting a student.

**FR-037:** The system shall warn admin that deleting student will delete associated marks and results.

**FR-038:** The system shall cascade delete marks records when student is deleted after confirmation.

### 5.4 Subject Management

**FR-039:** The system shall provide an "Add Subject" form with fields: Subject Code, Subject Name, Maximum Marks.

**FR-040:** The system shall validate that Subject Code is unique.

**FR-041:** The system shall validate that Maximum Marks is a positive integer greater than 0.

**FR-042:** The system shall require all subject fields to be mandatory.

**FR-043:** The system shall display all subjects in a table showing Subject Code, Name, Maximum Marks.

**FR-044:** The system shall provide a search box to filter subjects by Code or Name.

**FR-045:** The system shall provide an "Edit" button for each subject.

**FR-046:** The system shall populate the edit form with existing subject data.

**FR-047:** The system shall validate edited data with same rules as create.

**FR-048:** The system shall update subject record in database upon successful validation.

**FR-049:** The system shall provide a "Delete" button for each subject with confirmation dialog.

**FR-050:** The system shall check for existing marks records before deleting a subject.

**FR-051:** The system shall prevent subject deletion if marks records exist and display appropriate error message.

### 5.5 Marks Management

**FR-052:** The system shall provide a marks entry form with dropdowns for Student and Subject selection.

**FR-053:** The system shall display student Roll Number and Name in the student dropdown.

**FR-054:** The system shall display Subject Code and Name in the subject dropdown.

**FR-055:** The system shall provide an input field for Marks Obtained.

**FR-056:** The system shall provide a checkbox to mark student as "Absent".

**FR-057:** The system shall automatically set marks to 0 when "Absent" is checked.

**FR-058:** The system shall validate that marks is a non-negative integer.

**FR-059:** The system shall retrieve the maximum marks for the selected subject from database.

**FR-060:** The system shall validate that marks obtained does not exceed maximum marks for the subject.

**FR-061:** The system shall check for duplicate marks entry (student-subject combination).

**FR-062:** The system shall prevent duplicate marks creation and display error message.

**FR-063:** The system shall insert marks record into database upon successful validation.

**FR-064:** The system shall display all marks records in a table showing Roll Number, Student Name, Subject, Marks Obtained, Maximum Marks, Absent status.

**FR-065:** The system shall provide search functionality to filter marks by Student Roll Number or Subject.

**FR-066:** The system shall provide an "Edit" button for each marks record.

**FR-067:** The system shall populate the edit form with existing marks data.

**FR-068:** The system shall validate edited marks with same rules as create.

**FR-069:** The system shall update marks record in database upon successful validation.

**FR-070:** The system shall provide a "Delete" button for each marks record with confirmation.

**FR-071:** The system shall delete marks record from database after confirmation.

---

### 5.6 Result Calculation & Display

**FR-072:** The system shall automatically calculate results when all marks for a student are entered.

**FR-073:** The system shall calculate total marks obtained by summing marks across all subjects for a student.

**FR-074:** The system shall calculate total maximum marks by summing maximum marks of all subjects.

**FR-075:** The system shall calculate percentage as (total obtained / total maximum) × 100, rounded to 2 decimal places.

**FR-076:** The system shall assign grade based on percentage using the defined grading scale.

**FR-077:** The system shall determine pass/fail status by checking if student passed all subjects individually and overall percentage ≥ 40%.

**FR-078:** The system shall consider a subject passed if marks ≥ 40% of maximum marks for that subject.

**FR-079:** The system shall mark overall status as FAIL if any subject is failed, regardless of overall percentage.

**FR-080:** The system shall mark overall status as FAIL if student is marked Absent in any subject.

**FR-081:** The system shall provide a "Results" section in admin panel showing all calculated results.

**FR-082:** The system shall display results table with columns: Roll Number, Name, Total Marks, Percentage, Grade, Status.

**FR-083:** The system shall provide search/filter for results by Roll Number or Status.

**FR-084:** The system shall allow admin to view detailed subject-wise results for any student.

**FR-085:** The system shall recalculate results automatically when marks are updated.

### 5.7 Student Result Lookup

**FR-086:** The system shall provide a public result lookup page with fields: Roll Number, Date of Birth.

**FR-087:** The system shall validate that both fields are provided before querying database.

**FR-088:** The system shall query database for student matching both Roll Number and Date of Birth.

**FR-089:** The system shall display "Invalid credentials" message if no matching student found.

**FR-090:** The system shall check if result exists (all marks entered) for the matched student.

**FR-091:** The system shall display "Result not yet published" message if marks incomplete.

**FR-092:** The system shall display complete result page if student and result found.

**FR-093:** The result page shall show student information: Roll Number, Name.

**FR-094:** The result page shall show subject-wise marks in table format with columns: Subject Name, Marks Obtained, Maximum Marks, Status (Pass/Fail).

**FR-095:** The result page shall calculate and display subject pass/fail status individually.

**FR-096:** The result page shall display total marks obtained and total maximum marks.

**FR-097:** The result page shall display calculated percentage.

**FR-098:** The result page shall display assigned grade with color coding.

**FR-099:** The result page shall display overall status (PASS/FAIL) with prominent color coding (green for pass, red for fail).

**FR-100:** The result page shall indicate "Absent" for subjects where student was marked absent.

**FR-101:** The result page shall be printable with clean print-friendly CSS.

### 5.8 Performance Analysis

**FR-102:** The system shall provide a dedicated "Analysis" section accessible from admin navigation.

**FR-103:** The system shall calculate and display class average percentage across all students.

**FR-104:** The system shall calculate and display subject-wise average marks for each subject.

**FR-105:** The system shall identify and display the highest marks scored in each subject with student name.

**FR-106:** The system shall identify and display the lowest marks scored in each subject with student name.

**FR-107:** The system shall calculate and display pass percentage for each subject.

**FR-108:** The system shall calculate and display fail percentage for each subject.

**FR-109:** The system shall identify and display top 10 performing students based on percentage.

**FR-110:** The system shall identify students scoring below class average and display count.

**FR-111:** The system shall calculate grade distribution showing count of students in each grade (A, B, C, D, F).

**FR-112:** The system shall identify weak subjects (subjects with lowest average marks).

**FR-113:** The system shall identify strong subjects (subjects with highest average marks).

**FR-114:** The system shall display a bar chart for subject-wise average comparison.

**FR-115:** The system shall display a bar chart for grade distribution.

**FR-116:** The system shall display a pie chart for pass/fail ratio.

**FR-117:** The system shall display a bar chart for subject-wise pass percentage.

### 5.9 Reports

**FR-118:** The system shall provide a "Reports" section accessible from admin navigation.

**FR-119:** The system shall allow admin to select report type from: Individual Student, Class Results, Subject Performance, Overall Analysis.

**FR-120:** For Individual Student Report, system shall provide dropdown to select student by Roll Number.

**FR-121:** Individual Student Report shall display complete student information and subject-wise marks in tabular format.

**FR-122:** For Class Results Report, system shall display all students with their results in summary format.

**FR-123:** Class Results Report shall include columns: Roll Number, Name, Total Marks, Percentage, Grade, Status.

**FR-124:** For Subject Performance Report, system shall display subject-wise statistics: Average, Highest, Lowest, Pass %, Fail %.

**FR-125:** For Overall Analysis Report, system shall display comprehensive analytics: Total Students, Pass Count, Fail Count, Class Average, Grade Distribution.

**FR-126:** All reports shall include report generation date and time.

**FR-127:** All reports shall be printable with clean print-friendly CSS.

**FR-128:** Reports shall be displayed in professional tabular format with proper headings and formatting.

### 5.10 Search & Filter

**FR-129:** The system shall provide search functionality on student management page to filter by Roll Number or Name.

**FR-130:** The system shall provide filter dropdown on student management page to filter by Gender.

**FR-131:** The system shall provide search functionality on subject management page to filter by Subject Code or Name.

**FR-132:** The system shall provide search functionality on marks management page to filter by Student Roll Number or Subject Code.

**FR-133:** The system shall provide filter functionality on results page to filter by Status (Pass/Fail/All).

**FR-134:** Search shall work with partial matches (case-insensitive).

**FR-135:** Filters shall update the displayed table in real-time without page reload.

---

## 6. DATABASE REQUIREMENTS

### 6.1 Existing Database Review

**Current Tables:**
1. `admins` - For administrator authentication
2. `students` - Student master data
3. `subjects` - Subject master data
4. `marks` - Student marks records

**Assessment:** The existing four-table structure is appropriate for the MVP scope. No additional tables are required.

### 6.2 Recommended Database Schema

#### 6.2.1 Table: admins

**DB-001:** Table for administrator authentication

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | Auto-increment ID |
| username | VARCHAR(50) | UNIQUE, NOT NULL | Admin username |
| email | VARCHAR(100) | UNIQUE, NOT NULL | Admin email |
| password_hash | VARCHAR(255) | NOT NULL | Hashed password |
| full_name | VARCHAR(100) | NOT NULL | Admin full name |
| created_at | TIMESTAMP | DEFAULT NOW() | Account creation timestamp |
| last_login | TIMESTAMP | NULL | Last login timestamp |

**Indexes:**
- Primary key on `id`
- Unique index on `username`
- Unique index on `email`

**Initial Data:**
- One default admin account with username: `admin`, email: `admin@result.com`, password: `Admin@123` (to be hashed)

#### 6.2.2 Table: students

**DB-002:** Table for student master data

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | Auto-increment ID |
| roll_number | VARCHAR(20) | UNIQUE, NOT NULL | Student roll number |
| name | VARCHAR(100) | NOT NULL | Student full name |
| email | VARCHAR(100) | NULL | Student email (optional) |
| date_of_birth | DATE | NOT NULL | Date of birth (for result lookup) |
| gender | VARCHAR(10) | NOT NULL | Gender (Male/Female/Other) |
| contact_number | VARCHAR(15) | NULL | Contact number (optional) |
| created_at | TIMESTAMP | DEFAULT NOW() | Record creation timestamp |
| updated_at | TIMESTAMP | DEFAULT NOW() | Record update timestamp |

**Indexes:**
- Primary key on `id`
- Unique index on `roll_number`
- Index on `roll_number, date_of_birth` (for result lookup query optimization)

**Validation Rules:**
- `roll_number`: Alphanumeric, max 20 characters
- `name`: Non-empty string
- `date_of_birth`: Must be in the past
- `gender`: Must be one of ('Male', 'Female', 'Other')
- `contact_number`: Digits only, 10 characters if provided

#### 6.2.3 Table: subjects

**DB-003:** Table for subject master data

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | Auto-increment ID |
| subject_code | VARCHAR(20) | UNIQUE, NOT NULL | Subject code |
| subject_name | VARCHAR(100) | NOT NULL | Subject name |
| max_marks | INTEGER | NOT NULL, CHECK (max_marks > 0) | Maximum marks for subject |
| created_at | TIMESTAMP | DEFAULT NOW() | Record creation timestamp |
| updated_at | TIMESTAMP | DEFAULT NOW() | Record update timestamp |

**Indexes:**
- Primary key on `id`
- Unique index on `subject_code`

**Validation Rules:**
- `subject_code`: Alphanumeric, max 20 characters, unique
- `subject_name`: Non-empty string
- `max_marks`: Positive integer > 0

#### 6.2.4 Table: marks

**DB-004:** Table for student marks records

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | Auto-increment ID |
| student_id | INTEGER | NOT NULL, FOREIGN KEY → students(id) | Reference to student |
| subject_id | INTEGER | NOT NULL, FOREIGN KEY → subjects(id) | Reference to subject |
| marks_obtained | INTEGER | NOT NULL, CHECK (marks_obtained >= 0) | Marks obtained |
| is_absent | BOOLEAN | DEFAULT FALSE | Absent status |
| created_at | TIMESTAMP | DEFAULT NOW() | Record creation timestamp |
| updated_at | TIMESTAMP | DEFAULT NOW() | Record update timestamp |
| UNIQUE (student_id, subject_id) | | CONSTRAINT | Prevent duplicate marks entry |

**Indexes:**
- Primary key on `id`
- Unique composite index on `(student_id, subject_id)`
- Foreign key index on `student_id`
- Foreign key index on `subject_id`

**Foreign Key Constraints:**
- `student_id` REFERENCES `students(id)` ON DELETE CASCADE
- `subject_id` REFERENCES `subjects(id)` ON DELETE RESTRICT

**Validation Rules:**
- `marks_obtained`: Non-negative integer
- `marks_obtained` must be ≤ corresponding `subjects.max_marks` (application-level validation)
- If `is_absent` = TRUE, `marks_obtained` should be 0

**Delete Behavior:**
- If student deleted: CASCADE delete all marks records
- If subject deleted: RESTRICT (prevent deletion if marks exist)

### 6.3 Database Modifications Required

**No structural modifications required** to the existing four tables, but ensure the following columns and constraints exist:

#### 6.3.1 Modifications to `admins` table (if needed)

| Current State | Required Change | Reason |
|---------------|----------------|---------|
| May not have `last_login` | ADD COLUMN `last_login TIMESTAMP NULL` | Track admin activity |
| May not have `full_name` | ADD COLUMN `full_name VARCHAR(100)` | Display admin name |

#### 6.3.2 Modifications to `students` table (if needed)

| Current State | Required Change | Reason |
|---------------|----------------|---------|
| May not have unique constraint on `roll_number` | ALTER TABLE students ADD CONSTRAINT unique_roll_number UNIQUE (roll_number) | Prevent duplicates |
| May not have `updated_at` | ADD COLUMN `updated_at TIMESTAMP DEFAULT NOW()` | Track updates |
| May not have index on lookup fields | CREATE INDEX idx_student_lookup ON students(roll_number, date_of_birth) | Optimize result lookup query |

#### 6.3.3 Modifications to `subjects` table (if needed)

| Current State | Required Change | Reason |
|---------------|----------------|---------|
| May not have `max_marks` constraint | ALTER TABLE subjects ADD CHECK (max_marks > 0) | Ensure valid max marks |
| May not have unique constraint on `subject_code` | ALTER TABLE subjects ADD CONSTRAINT unique_subject_code UNIQUE (subject_code) | Prevent duplicates |

#### 6.3.4 Modifications to `marks` table (if needed)

| Current State | Required Change | Reason |
|---------------|----------------|---------|
| May not have unique constraint | ALTER TABLE marks ADD CONSTRAINT unique_student_subject UNIQUE (student_id, subject_id) | Prevent duplicate marks |
| May not have `is_absent` column | ADD COLUMN `is_absent BOOLEAN DEFAULT FALSE` | Track absent students |
| May not have check constraint | ALTER TABLE marks ADD CHECK (marks_obtained >= 0) | Prevent negative marks |
| Foreign key may not have CASCADE | ALTER FOREIGN KEY student_id ON DELETE CASCADE | Auto-delete marks when student deleted |

### 6.4 Database Relationships

```
admins (1) -------- (manages) -------- (many) students
admins (1) -------- (manages) -------- (many) subjects
students (1) -------- (has) -------- (many) marks
subjects (1) -------- (has) -------- (many) marks
marks (many) -------- (belongs to) -------- (1) student
marks (many) -------- (belongs to) -------- (1) subject
```

**Relationship Details:**

| Relationship | Type | Foreign Key | Delete Behavior |
|--------------|------|-------------|-----------------|
| students → marks | One-to-Many | marks.student_id | CASCADE |
| subjects → marks | One-to-Many | marks.subject_id | RESTRICT |

### 6.5 Sample Data Requirements

#### 6.5.1 Admin Data
- 1 admin account for testing

#### 6.5.2 Student Data
- 10-15 sample students with varied Roll Numbers
- Mix of Male/Female genders
- Realistic names and dates of birth

#### 6.5.3 Subject Data
- 5-6 subjects (e.g., Mathematics, Science, English, Computer Science, Social Studies)
- Subject codes like MATH101, SCI102, ENG103, CS104, SS105
- Varied maximum marks (e.g., 100, 80, 50) to test calculation logic

#### 6.5.4 Marks Data
- Complete marks for 8-10 students (for result demonstration)
- 2-3 students with incomplete marks
- 1-2 students marked absent in at least one subject
- 1-2 students failing in one or more subjects
- 3-4 students passing with distinction (>75%)
- Varied marks to demonstrate grade distribution

---

## 7. SECURITY REQUIREMENTS

### 7.1 Authentication & Session Security

**SEC-001:** All admin passwords must be hashed using bcrypt with minimum cost factor of 12 before storing in database.

**SEC-002:** Plain text passwords must never be stored in database or logged.

**SEC-003:** Session cookies must have HttpOnly flag set to prevent JavaScript access.

**SEC-004:** Session cookies must have Secure flag set in production (HTTPS only).

**SEC-005:** Sessions must expire after 30 minutes of inactivity.

**SEC-006:** Admin must be redirected to login page when session expires.

**SEC-007:** Login page must implement rate limiting (max 5 failed attempts per IP per 15 minutes) to prevent brute force attacks.

**SEC-008:** Failed login attempts must not reveal whether username or password was incorrect (use generic message).

### 7.2 Authorization & Access Control

**SEC-009:** All admin routes must check for valid session before allowing access.

**SEC-010:** Unauthorized access attempts must redirect to login page with appropriate message.

**SEC-011:** Student result lookup must validate both Roll Number AND Date of Birth (two-factor lookup).

**SEC-012:** Student result lookup must only return data for the matching student (no access to other students' data).

**SEC-013:** Direct URL access to admin pages without authentication must be prevented.

**SEC-014:** API endpoints must validate authentication before processing requests.

### 7.3 Input Validation & Sanitization

**SEC-015:** All user inputs must be validated on both frontend (JavaScript) and backend (Python).

**SEC-016:** Email inputs must be validated against proper email format regex.

**SEC-017:** Numeric inputs (marks, max_marks) must be validated to ensure they are integers.

**SEC-018:** Marks inputs must be validated to ensure they are within valid range (0 to max_marks).

**SEC-019:** Date inputs must be validated to ensure proper date format and logical values.

**SEC-020:** All string inputs must be sanitized to remove potentially malicious characters before processing.

**SEC-021:** HTML special characters in user inputs must be escaped before rendering to prevent XSS attacks.

### 7.4 SQL Injection Prevention

**SEC-022:** All database queries must use parameterized queries or ORM methods (SQLAlchemy or similar).

**SEC-023:** Direct string concatenation for SQL queries must be strictly prohibited.

**SEC-024:** User inputs must never be directly interpolated into SQL query strings.

**SEC-025:** Database error messages must not be displayed to end users (log internally only).

### 7.5 Environment Variables & Secrets Management

**SEC-026:** Database connection URL must be stored in environment variable (SUPABASE_URL, SUPABASE_KEY).

**SEC-027:** Secret key for session management must be stored in environment variable (SECRET_KEY).

**SEC-028:** All sensitive configuration must be loaded from environment variables, never hardcoded.

**SEC-029:** `.env` file must be included in `.gitignore` to prevent committing secrets to version control.

**SEC-030:** Production environment must use strong, randomly generated SECRET_KEY.

**SEC-031:** Environment variables must be configured in Render dashboard for production deployment.

**SEC-032:** `.env.example` file should be provided with placeholder values for documentation.

### 7.6 Error Handling & Information Disclosure

**SEC-033:** Generic error messages must be shown to users (e.g., "An error occurred. Please try again.").

**SEC-034:** Detailed error information must be logged server-side only, never displayed to users.

**SEC-035:** Stack traces must never be displayed in production environment.

**SEC-036:** Database connection errors must show generic message to users.

**SEC-037:** 404 errors for admin pages must not reveal whether the page exists (redirect to login or show generic 404).

### 7.7 Production Security

**SEC-038:** Flask debug mode must be disabled in production (`DEBUG=False`).

**SEC-039:** HTTPS must be enforced in production (Render provides this by default).

**SEC-040:** CORS policy must be configured appropriately if API endpoints are exposed.

**SEC-041:** Security headers must be set: `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `X-XSS-Protection: 1; mode=block`.

**SEC-042:** Production logs must not contain sensitive information (passwords, session tokens, personal data).

### 7.8 Database Security

**SEC-043:** Database connection must use SSL/TLS (Supabase provides this by default).

**SEC-044:** Database credentials must never be committed to version control.

**SEC-045:** Principle of least privilege: application database user should only have necessary permissions (SELECT, INSERT, UPDATE, DELETE on required tables).

**SEC-046:** Database backups should be configured in Supabase dashboard.

**SEC-047:** Row-level security policies in Supabase can be configured for additional protection (optional but recommended).

### 7.9 Password Policy

**SEC-048:** Admin passwords must be minimum 8 characters long.

**SEC-049:** Admin passwords should contain at least one uppercase, one lowercase, one digit, and one special character (enforced during admin creation).

**SEC-050:** Password change functionality should be implemented (future enhancement, but consider in design).

---

## 8. UI/UX REQUIREMENTS

### 8.1 Overall Design Direction

**UI-001:** Professional, clean, and modern interface suitable for educational institution.

**UI-002:** Consistent color scheme throughout the application.

**UI-003:** Intuitive navigation with clear visual hierarchy.

**UI-004:** Fast page loads with minimal JavaScript overhead.

**UI-005:** Accessible design following basic WCAG guidelines (proper contrast, semantic HTML).

### 8.2 Color Scheme & Branding

**Recommended Color Palette:**

| Element | Color | Usage |
|---------|-------|-------|
| Primary | #2563eb (Blue) | Headers, buttons, links |
| Success | #16a34a (Green) | Pass status, success messages |
| Danger | #dc2626 (Red) | Fail status, error messages, delete actions |
| Warning | #ea580c (Orange) | Warnings, absent status |
| Info | #0891b2 (Cyan) | Information messages |
| Background | #f8fafc (Light Gray) | Page background |
| Card Background | #ffffff (White) | Cards, tables, forms |
| Text Primary | #1e293b (Dark Gray) | Body text |
| Text Secondary | #64748b (Medium Gray) | Subtitles, labels |
| Border | #e2e8f0 (Light Gray) | Borders, dividers |

### 8.3 Typography

**UI-006:** Use web-safe fonts: Primary font: `'Segoe UI', Arial, sans-serif`.

**UI-007:** Font sizes:
- H1: 2rem (32px) - Page titles
- H2: 1.5rem (24px) - Section headers
- H3: 1.25rem (20px) - Card titles
- Body: 1rem (16px) - Regular text
- Small: 0.875rem (14px) - Secondary text

**UI-008:** Line height: 1.5 for body text, 1.2 for headings.

### 8.4 Layout & Navigation

**UI-009:** Admin panel shall use a two-column layout:
- Left sidebar: Navigation menu (fixed position)
- Right content area: Main content

**UI-010:** Navigation menu shall include:
- Dashboard (home icon)
- Students (users icon)
- Subjects (book icon)
- Marks (edit icon)
- Results (chart icon)
- Analysis (bar-chart icon)
- Reports (document icon)
- Logout (logout icon)

**UI-011:** Active navigation item shall be highlighted with background color.

**UI-012:** Top header bar shall display:
- Application logo/name
- Admin name
- Logout button

**UI-013:** Mobile view (< 768px) shall use hamburger menu for navigation.

**UI-014:** Public pages (login, result lookup) shall use centered single-column layout.

### 8.5 Responsive Design

**UI-015:** Application must be fully responsive across devices:
- Desktop: ≥ 1024px (primary target)
- Tablet: 768px - 1023px
- Mobile: < 768px

**UI-016:** Tables shall be horizontally scrollable on mobile devices.

**UI-017:** Forms shall stack vertically on mobile devices.

**UI-018:** Navigation sidebar shall collapse to hamburger menu on mobile.

**UI-019:** Charts shall resize appropriately for smaller screens.

**UI-020:** Buttons shall be adequately sized for touch interaction (minimum 44x44px tap target).

### 8.6 Page-Specific UI Requirements

#### 8.6.1 Login Page

**UI-021:** Centered card-style login form with:
- Application logo/title
- Email/Username field
- Password field with show/hide toggle
- "Login" button (full width)
- Error message area (hidden until error occurs)

**UI-022:** Clean background with subtle gradient or pattern.

**UI-023:** Form validation errors displayed inline below respective fields.

#### 8.6.2 Admin Dashboard

**UI-024:** Grid of stat cards showing key metrics:
- Total Students (icon + number)
- Total Subjects (icon + number)
- Total Results (icon + number)
- Pass Percentage (icon + percentage + color)

**UI-025:** Charts section with:
- Grade Distribution Bar Chart
- Pass/Fail Ratio Pie Chart
- Subject-wise Performance Bar Chart

**UI-026:** Top Performers table showing top 5 students.

**UI-027:** Quick action buttons for common tasks (Add Student, Add Subject, Enter Marks).

#### 8.6.3 Student Management Page

**UI-028:** Page header with "Students" title and "Add New Student" button.

**UI-029:** Search bar and filter dropdowns above table.

**UI-030:** Data table with columns: Roll Number, Name, Email, DOB, Gender, Contact, Actions.

**UI-031:** Action buttons per row: Edit (blue), Delete (red).

**UI-032:** Add/Edit form as modal overlay or separate section with fields in grid layout.

**UI-033:** Form validation with inline error messages.

**UI-034:** Success notification after add/edit/delete operations.

#### 8.6.4 Subject Management Page

**UI-035:** Similar layout to Student Management with table showing: Subject Code, Subject Name, Max Marks, Actions.

**UI-036:** Add/Edit form with fields: Subject Code, Subject Name, Maximum Marks.

#### 8.6.5 Marks Management Page

**UI-037:** Marks entry form with:
- Student dropdown (searchable)
- Subject dropdown
- Marks Obtained input
- Absent checkbox
- Submit button

**UI-038:** Display maximum marks for selected subject dynamically.

**UI-039:** Marks table showing: Roll Number, Student Name, Subject, Marks, Max Marks, Status, Actions.

**UI-040:** Color-coded status indicators (green for pass, red for fail, orange for absent).

#### 8.6.6 Results Page

**UI-041:** Filter options: All Students / Pass / Fail.

**UI-042:** Results table: Roll Number, Name, Total Marks, Percentage, Grade, Status, View Details.

**UI-043:** "View Details" button opens detailed subject-wise result in modal or new page.

**UI-044:** Grade badges with color coding:
- A: Green
- B: Light Green
- C: Yellow
- D: Orange
- F: Red

#### 8.6.7 Analysis Dashboard

**UI-045:** Metrics cards for class statistics.

**UI-046:** Multiple charts in grid layout:
- Subject-wise average comparison
- Grade distribution
- Pass/fail ratio
- Top performers list

**UI-047:** Subject performance table with statistics.

#### 8.6.8 Reports Page

**UI-048:** Report type selector (radio buttons or dropdown).

**UI-049:** Report parameters (e.g., select student for individual report).

**UI-050:** "Generate Report" button.

**UI-051:** Report display area with print button.

**UI-052:** Clean print CSS hiding navigation and unnecessary elements.

#### 8.6.9 Student Result Lookup Page

**UI-053:** Centered card with:
- Application title
- Roll Number input
- Date of Birth date picker
- "View Result" button
- Link to institution homepage (optional)

**UI-054:** Result display page with:
- Student information header
- Subject-wise marks table with pass/fail indicators
- Summary card showing Total, Percentage, Grade, Overall Status
- Print button

**UI-055:** Pass/Fail status displayed prominently with large text and color.

### 8.7 Form Design

**UI-056:** All form fields shall have clear labels.

**UI-057:** Required fields shall be indicated with asterisk (*).

**UI-058:** Input fields shall have placeholder text for guidance.

**UI-059:** Submit buttons shall be positioned at bottom-right of forms.

**UI-060:** Cancel/Close buttons shall be positioned next to submit buttons.

**UI-061:** Form validation errors shall be displayed inline below fields in red text.

**UI-062:** Successful form submission shall show success notification (toast or alert).

### 8.8 Tables

**UI-063:** Tables shall have alternating row colors (zebra striping) for readability.

**UI-064:** Table headers shall have darker background.

**UI-065:** Table rows shall have hover effect (light background color change).

**UI-066:** Action buttons in table cells shall be icon buttons or small text buttons.

**UI-067:** Empty table state shall display "No data available" message.

**UI-068:** Tables shall be horizontally scrollable on mobile with sticky first column.

### 8.9 Buttons & Interactive Elements

**UI-069:** Primary action buttons: Blue background with white text.

**UI-070:** Delete/Danger buttons: Red background with white text.

**UI-071:** Secondary buttons: White background with border and primary color text.

**UI-072:** Buttons shall have hover state (slightly darker shade).

**UI-073:** Buttons shall have active/pressed state (darker shade + slight shadow).

**UI-074:** Disabled buttons shall have gray background and reduced opacity.

**UI-075:** Loading state: Show spinner on button during async operations.

### 8.10 Notifications & Feedback

**UI-076:** Success messages: Green background toast notification.

**UI-077:** Error messages: Red background toast notification.

**UI-078:** Info messages: Blue background toast notification.

**UI-079:** Warning messages: Orange background toast notification.

**UI-080:** Notifications shall auto-dismiss after 5 seconds.

**UI-081:** Confirmation dialogs shall be modal overlays with clear action buttons.

**UI-082:** Loading spinners shall be displayed during database operations.

### 8.11 Charts & Data Visualization

**UI-083:** Use Chart.js library for creating charts (lightweight and simple).

**UI-084:** Charts shall be responsive and resize with container.

**UI-085:** Bar charts for comparing multiple items (grade distribution, subject averages).

**UI-086:** Pie charts for part-to-whole relationships (pass/fail ratio).

**UI-087:** Chart colors shall match the application color scheme.

**UI-088:** Charts shall display data labels for clarity.

**UI-089:** Charts shall have legends where appropriate.

### 8.12 Accessibility

**UI-090:** Use semantic HTML elements (header, nav, main, section, article).

**UI-091:** All images shall have descriptive alt text.

**UI-092:** Form inputs shall have associated labels.

**UI-093:** Color contrast ratio shall meet WCAG AA standards (4.5:1 for text).

**UI-094:** Focus indicators shall be visible on interactive elements.

**UI-095:** Keyboard navigation shall be fully supported.

### 8.13 Performance

**UI-096:** CSS shall be minified in production.

**UI-097:** JavaScript shall be minified in production.

**UI-098:** Images shall be optimized and compressed.

**UI-099:** Use CSS for animations instead of JavaScript where possible.

**UI-100:** Limit external dependencies to essential libraries only.

---

## 9. DASHBOARD REQUIREMENTS

### 9.1 Admin Dashboard

**DASH-001:** Admin dashboard shall be the first page after successful login.

**DASH-002:** Dashboard shall load and display within 2 seconds.

#### 9.1.1 Key Metrics Cards

**DASH-003:** Display "Total Students" card showing count of all registered students.

**DASH-004:** Display "Total Subjects" card showing count of all subjects.

**DASH-005:** Display "Results Published" card showing count of students with complete results.

**DASH-006:** Display "Class Average" card showing average percentage across all students with results.

**DASH-007:** Each metric card shall have:
- Icon representing the metric
- Large number display
- Descriptive label
- Background color for visual distinction

#### 9.1.2 Pass/Fail Statistics

**DASH-008:** Display pass count and percentage (e.g., "45 students (75%)").

**DASH-009:** Display fail count and percentage (e.g., "15 students (25%)").

**DASH-010:** Use color coding: Green for pass, Red for fail.

#### 9.1.3 Top Performers Section

**DASH-011:** Display top 5 students ranked by percentage in descending order.

**DASH-012:** Show for each top performer:
- Rank position
- Roll Number
- Student Name
- Percentage
- Grade

**DASH-013:** Display as a table or list with clear formatting.

#### 9.1.4 Grade Distribution Chart

**DASH-014:** Display bar chart showing count of students in each grade (A, B, C, D, F).

**DASH-015:** X-axis: Grades (A, B, C, D, F).

**DASH-016:** Y-axis: Number of students.

**DASH-017:** Use consistent color scheme for grade bars.

**DASH-018:** Display count value on top of each bar.

#### 9.1.5 Pass/Fail Ratio Chart

**DASH-019:** Display pie chart showing pass vs fail distribution.

**DASH-020:** Two segments: Pass (green), Fail (red).

**DASH-021:** Display percentage on each segment.

**DASH-022:** Include legend identifying segments.

#### 9.1.6 Subject-wise Performance Chart

**DASH-023:** Display bar chart showing average marks for each subject.

**DASH-024:** X-axis: Subject names.

**DASH-025:** Y-axis: Average marks.

**DASH-026:** Identify highest performing subject with different color.

**DASH-027:** Identify lowest performing subject with different color.

#### 9.1.7 Quick Actions

**DASH-028:** Provide quick action buttons:
- "Add New Student" → redirects to student management
- "Enter Marks" → redirects to marks entry
- "View Reports" → redirects to reports section

**DASH-029:** Quick action buttons shall be visually prominent (larger size, primary color).

### 9.2 Student Result Summary (for student view)

**DASH-032:** After successful result lookup, display summary card showing:
- Roll Number
- Name
- Total Marks (obtained / maximum)
- Percentage
- Grade with color-coded badge
- Overall Status (PASS/FAIL) with prominent display

**DASH-033:** Display visual indicator:
- Green checkmark icon for PASS
- Red cross icon for FAIL

**DASH-034:** Subject-wise performance section showing each subject with:
- Subject name
- Marks obtained / Maximum marks
- Pass/Fail status for that subject

**DASH-035:** Use progress bar or percentage bar for visual representation of marks per subject.

**DASH-036:** Highlight failed subjects in red.

### 9.3 Dashboard Data Refresh

**DASH-037:** Dashboard data shall be fetched fresh on each page load (no stale cached data).

**DASH-038:** Display loading spinner while dashboard data is being fetched.

**DASH-039:** If data fetching fails, display error message with retry option.

---

## 10. SEARCH, FILTER, AND SORT

### 10.1 Student Management Search & Filter

**SEARCH-001:** Provide search input field above student table labeled "Search by Roll Number or Name".

**SEARCH-002:** Search shall filter students where Roll Number or Name contains search term (case-insensitive).

**SEARCH-003:** Search shall work with partial matches (e.g., searching "john" matches "John Doe").

**SEARCH-004:** Search shall update results in real-time as user types (with debounce of 300ms).

**SEARCH-005:** Provide filter dropdown labeled "Filter by Gender" with options: All, Male, Female, Other.

**SEARCH-006:** Filter shall update table to show only students matching selected gender.

**SEARCH-007:** Search and filter shall work together (combined filtering).

**SEARCH-008:** Display "No students found" message when search/filter returns no results.

**SEARCH-009:** Provide "Clear" or "Reset" button to clear search and filters.

### 10.2 Subject Management Search

**SEARCH-010:** Provide search input field above subject table labeled "Search by Subject Code or Name".

**SEARCH-011:** Search shall filter subjects where Code or Name contains search term (case-insensitive).

**SEARCH-012:** Search shall work with partial matches.

**SEARCH-013:** Display "No subjects found" when search returns no results.

### 10.3 Marks Management Search & Filter

**SEARCH-014:** Provide search field labeled "Search by Roll Number or Subject".

**SEARCH-015:** Search shall filter marks records where student Roll Number or Subject Name contains search term.

**SEARCH-016:** Provide filter dropdown "Filter by Status" with options: All, Pass, Fail, Absent.

**SEARCH-017:** Filter shall show only marks records matching selected status.

**SEARCH-018:** Display "No marks records found" when search/filter returns no results.

### 10.4 Results Page Filter

**SEARCH-019:** Provide filter buttons/tabs: "All", "Pass", "Fail".

**SEARCH-020:** "All" shall display all students with calculated results.

**SEARCH-021:** "Pass" shall display only students with overall Pass status.

**SEARCH-022:** "Fail" shall display only students with overall Fail status.

**SEARCH-023:** Active filter button shall be visually highlighted.

**SEARCH-024:** Provide search field to search results by Roll Number or Name.

### 10.5 Sort Functionality (Nice to Have)

**SEARCH-025:** Allow sorting student table by clicking column headers (Roll Number, Name).

**SEARCH-026:** Allow sorting results table by Percentage (highest to lowest, lowest to highest).

**SEARCH-027:** Display sort direction indicator (up/down arrow) on sorted column header.

### 10.6 Performance Considerations

**SEARCH-028:** For tables with >100 records, implement client-side pagination (10-20 records per page).

**SEARCH-029:** Search should be performed on already-loaded data (client-side filtering) for responsiveness.

**SEARCH-030:** For very large datasets (>500 records), consider server-side search and pagination (future enhancement).

---

## 11. VALIDATION RULES

### 11.1 Admin Login Validation

**VAL-001:** Email/Username field is required (frontend and backend).

**VAL-002:** Password field is required (frontend and backend).

**VAL-003:** Email format validation using regex pattern (if email is used).

**VAL-004:** Display error "Email/Username is required" if empty.

**VAL-005:** Display error "Password is required" if empty.

**VAL-006:** Backend shall verify credentials against database hashed password.

**VAL-007:** Display generic error "Invalid credentials" on authentication failure (never specify which field was wrong).

### 11.2 Student Management Validation

**VAL-008:** Roll Number is required (frontend and backend).

**VAL-009:** Roll Number must be alphanumeric, max 20 characters.

**VAL-010:** Roll Number must be unique (check database before insert/update).

**VAL-011:** Name is required, min 2 characters, max 100 characters.

**VAL-012:** Name should contain only letters and spaces (no numbers or special characters).

**VAL-013:** Email format validation using regex if provided (email is optional).

**VAL-014:** Date of Birth is required.

**VAL-015:** Date of Birth must be a valid date in the past.

**VAL-016:** Date of Birth should be reasonable (e.g., between 10 and 50 years ago for diploma students).

**VAL-017:** Gender is required and must be one of: Male, Female, Other.

**VAL-018:** Contact Number is optional; if provided, must be exactly 10 digits.

**VAL-019:** Contact Number must contain only digits (no spaces, dashes, or special characters).

**VAL-020:** Display specific error messages for each validation failure inline below the field.

**VAL-021:** Prevent form submission if any validation error exists.

### 11.3 Subject Management Validation

**VAL-022:** Subject Code is required (frontend and backend).

**VAL-023:** Subject Code must be alphanumeric, max 20 characters.

**VAL-024:** Subject Code must be unique (check database before insert/update).

**VAL-025:** Subject Name is required, min 2 characters, max 100 characters.

**VAL-026:** Maximum Marks is required.

**VAL-027:** Maximum Marks must be a positive integer greater than 0.

**VAL-028:** Maximum Marks should have reasonable upper limit (e.g., ≤ 500).

**VAL-029:** Display error messages inline for validation failures.

### 11.4 Marks Management Validation

**VAL-030:** Student selection is required.

**VAL-031:** Subject selection is required.

**VAL-032:** Marks Obtained is required (unless Absent is checked).

**VAL-033:** Marks Obtained must be a non-negative integer (≥ 0).

**VAL-034:** Marks Obtained cannot exceed Maximum Marks for the selected subject.

**VAL-035:** Fetch Maximum Marks dynamically based on selected subject.

**VAL-036:** If "Absent" checkbox is checked, set Marks to 0 and disable marks input field.

**VAL-037:** Check for duplicate marks entry (student + subject combination) before insert.

**VAL-038:** Display error "Marks already exist for this student in this subject" if duplicate detected.

**VAL-039:** Display error "Marks cannot exceed maximum marks (X)" if validation fails.

**VAL-040:** Display error messages inline for validation failures.

### 11.5 Result Lookup Validation

**VAL-041:** Roll Number is required for result lookup.

**VAL-042:** Date of Birth is required for result lookup.

**VAL-043:** Date of Birth must be valid date format.

**VAL-044:** Display error "Please enter both Roll Number and Date of Birth" if any field is empty.

**VAL-045:** Display error "Invalid credentials or result not available" if no matching student found.

**VAL-046:** Display error "Result not yet published" if student exists but marks incomplete.

### 11.6 General Validation Rules

**VAL-047:** All required field validations must be performed on both frontend (JavaScript) and backend (Python).

**VAL-048:** Frontend validation provides immediate user feedback.

**VAL-049:** Backend validation prevents malicious requests bypassing frontend.

**VAL-050:** Trim whitespace from all text inputs before validation and saving.

**VAL-051:** Sanitize inputs to prevent XSS attacks (escape HTML special characters).

**VAL-052:** Validate data types: ensure numeric fields receive numbers, date fields receive dates, etc.

**VAL-053:** Display validation errors in red text below the respective input field.

**VAL-054:** Clear previous validation errors when user starts correcting the field.

**VAL-055:** Submit button should be disabled until all required fields are valid (optional but good UX).

---

## 12. ERROR HANDLING

### 12.1 Authentication Errors

**ERR-001:** Invalid login credentials → Display: "Invalid email/username or password. Please try again."

**ERR-002:** Session expired → Redirect to login page with message: "Your session has expired. Please login again."

**ERR-003:** Unauthorized access attempt → Redirect to login page with message: "Please login to access this page."

**ERR-004:** Too many login attempts (rate limiting) → Display: "Too many failed attempts. Please try again after 15 minutes."

### 12.2 Database Errors

**ERR-005:** Database connection failure → Display: "Unable to connect to database. Please try again later."

**ERR-006:** Query execution error → Display: "An error occurred while processing your request. Please try again."

**ERR-007:** Duplicate key error (unique constraint violation) → Display: "Record with this identifier already exists."

**ERR-008:** Foreign key constraint error → Display: "Cannot delete this record as it is referenced by other data."

**ERR-009:** Data not found error → Display: "Requested record not found."

### 12.3 Student Management Errors

**ERR-010:** Duplicate Roll Number → Display: "A student with this Roll Number already exists."

**ERR-011:** Student not found → Display: "Student not found. Please check the Roll Number."

**ERR-012:** Cannot delete student with marks → Display: "Cannot delete student. Please delete associated marks first." OR show warning: "Deleting this student will also delete all their marks. Continue?"

### 12.4 Subject Management Errors

**ERR-013:** Duplicate Subject Code → Display: "A subject with this Subject Code already exists."

**ERR-014:** Subject not found → Display: "Subject not found."

**ERR-015:** Cannot delete subject with marks → Display: "Cannot delete subject. Marks records exist for this subject."

### 12.5 Marks Management Errors

**ERR-016:** Duplicate marks entry → Display: "Marks already exist for this student in this subject. Please edit the existing record."

**ERR-017:** Marks exceed maximum → Display: "Marks obtained (X) cannot exceed maximum marks (Y) for this subject."

**ERR-018:** Negative marks → Display: "Marks cannot be negative."

**ERR-019:** Invalid marks format → Display: "Please enter a valid number for marks."

**ERR-020:** Student not found → Display: "Selected student not found in database."

**ERR-021:** Subject not found → Display: "Selected subject not found in database."

### 12.6 Result Lookup Errors

**ERR-022:** Invalid result lookup credentials → Display: "Invalid Roll Number or Date of Birth. Please check and try again."

**ERR-023:** Student exists but result not available → Display: "Result not yet published for this student. Please check back later."

**ERR-024:** No student found → Display: "No student found with the provided credentials."

### 12.7 Network & Server Errors

**ERR-025:** Network request timeout → Display: "Request timeout. Please check your internet connection and try again."

**ERR-026:** Server error (500) → Display: "Server error occurred. Please try again later."

**ERR-027:** Service unavailable (503) → Display: "Service temporarily unavailable. Please try again later."

**ERR-028:** Bad request (400) → Display: "Invalid request. Please check your input and try again."

### 12.8 Form Validation Errors

**ERR-029:** Required field empty → Display: "[Field name] is required."

**ERR-030:** Invalid email format → Display: "Please enter a valid email address."

**ERR-031:** Invalid date format → Display: "Please enter a valid date."

**ERR-032:** Date in future when past required → Display: "Date cannot be in the future."

**ERR-033:** Invalid number format → Display: "Please enter a valid number."

**ERR-034:** Value below minimum → Display: "[Field name] must be at least [min value]."

**ERR-035:** Value above maximum → Display: "[Field name] cannot exceed [max value]."

### 12.9 General Error Handling Principles

**ERR-036:** Never expose technical error details (stack traces, SQL errors) to end users.

**ERR-037:** Log detailed errors server-side for debugging.

**ERR-038:** Display user-friendly error messages that explain what went wrong and suggest action.

**ERR-039:** Use consistent error message format throughout the application.

**ERR-040:** Error messages should be displayed prominently (toast notification or alert box).

**ERR-041:** Provide "Try Again" or "Retry" option where appropriate.

**ERR-042:** For critical errors, provide contact information or support link (optional).

**ERR-043:** Errors should be dismissible by user (close button on notifications).

**ERR-044:** Auto-dismiss non-critical error messages after 8-10 seconds.

**ERR-045:** Critical errors (blocking errors) should remain visible until user dismisses or takes action.

### 12.10 Error Logging

**ERR-046:** Log all errors with timestamp, user context, and request details server-side.

**ERR-047:** Use appropriate log levels: ERROR for exceptions, WARNING for validation failures, INFO for normal operations.

**ERR-048:** Error logs should be written to file or logging service (not just console in production).

**ERR-049:** Sensitive information (passwords, tokens) should never be logged.

**ERR-050:** Error logs should include enough context to debug issues without exposing security risks.

---

## 13. REPORTING & ANALYTICS

### 13.1 Report Types

#### 13.1.1 Individual Student Report

**REP-001:** Allow admin to select a student from dropdown (searchable by Roll Number or Name).

**REP-002:** Generate detailed report for selected student containing:
- Student information: Roll Number, Name, DOB, Gender
- Subject-wise marks table: Subject Code, Subject Name, Marks Obtained, Maximum Marks, Percentage, Status (Pass/Fail)
- Summary: Total Marks, Overall Percentage, Grade, Overall Status
- Report generation date and time

**REP-003:** Display in clean tabular format with proper headings.

**REP-004:** Provide "Print" button to print the report.

**REP-005:** Print CSS should hide navigation, buttons, and show only report content.

#### 13.1.2 Class Results Report

**REP-006:** Generate report showing all students with results in a summary table.

**REP-007:** Table columns: Sr. No., Roll Number, Name, Total Marks, Percentage, Grade, Status.

**REP-008:** Sort by Roll Number or Percentage (selectable).

**REP-009:** Include summary statistics at bottom:
- Total Students
- Pass Count & Percentage
- Fail Count & Percentage
- Class Average Percentage
- Highest Percentage (student name)
- Lowest Percentage (student name)

**REP-010:** Provide "Print" button with print-friendly formatting.

#### 13.1.3 Subject Performance Report

**REP-011:** Generate report for each subject containing:
- Subject Code, Subject Name, Maximum Marks
- Number of students who appeared
- Number of students passed
- Number of students failed
- Pass Percentage
- Average marks
- Highest marks (with student name)
- Lowest marks (with student name)
- Standard deviation (optional, nice to have)

**REP-012:** Display all subjects in tabular format.

**REP-013:** Highlight subject with highest and lowest pass percentage.

**REP-014:** Provide "Print" button.

#### 13.1.4 Overall Analysis Report

**REP-015:** Comprehensive analytics report containing:
- Total Students Registered
- Total Students with Results
- Total Subjects
- Overall Pass Percentage
- Overall Fail Percentage
- Class Average Percentage
- Grade Distribution (count and percentage for A, B, C, D, F)
- Top 10 Performers (Roll Number, Name, Percentage)
- Subject-wise average comparison
- Weak subjects identification (bottom 3 by average)
- Strong subjects identification (top 3 by average)

**REP-016:** Include visual charts in the report (optional for print version).

**REP-017:** Provide "Print" button.

### 13.2 Analytics Calculations

#### 13.2.1 Basic Metrics

**ANAL-001:** Class Average Percentage:
```
Class Average = (Sum of all students' percentages) / (Total students with results)
```

**ANAL-002:** Subject Average Marks:
```
Subject Average = (Sum of marks obtained by all students in subject) / (Number of students who appeared)
```

**ANAL-003:** Pass Percentage:
```
Pass Percentage = (Number of students passed / Total students with results) × 100
```

**ANAL-004:** Subject Pass Percentage:
```
Subject Pass % = (Number of students passed in subject / Total students appeared) × 100
```

#### 13.2.2 Advanced Metrics (Nice to Have)

**ANAL-005:** Standard Deviation for subject marks (shows marks spread):
```
σ = sqrt(Σ(xi - μ)² / N)
where xi = individual marks, μ = mean, N = count
```

**ANAL-006:** Percentile Rank for a student:
```
Percentile = (Number of students below this student / Total students) × 100
```

**ANAL-007:** Subject Difficulty Index:
```
Difficulty Index = Average Marks / Maximum Marks
Higher value = Easier subject
```

### 13.3 Charts & Visualizations

#### 13.3.1 Grade Distribution Chart

**CHART-001:** Type: Bar Chart (vertical bars).

**CHART-002:** X-axis: Grades (A, B, C, D, F).

**CHART-003:** Y-axis: Number of Students.

**CHART-004:** Display count on top of each bar.

**CHART-005:** Color code bars: Green (A), Light Green (B), Yellow (C), Orange (D), Red (F).

**CHART-006:** Title: "Grade Distribution".

**Viva Value:** Demonstrates clear visualization of performance distribution.

#### 13.3.2 Pass/Fail Ratio Chart

**CHART-007:** Type: Pie Chart (2 segments).

**CHART-008:** Segments: Pass (green), Fail (red).

**CHART-009:** Display percentage on each segment.

**CHART-010:** Include legend.

**CHART-011:** Title: "Pass/Fail Ratio".

**Viva Value:** Quick visual insight into overall class performance.

#### 13.3.3 Subject-wise Average Comparison

**CHART-012:** Type: Bar Chart (horizontal or vertical).

**CHART-013:** X-axis: Subject Names.

**CHART-014:** Y-axis: Average Marks.

**CHART-015:** Highlight highest performing subject in green.

**CHART-016:** Highlight lowest performing subject in red.

**CHART-017:** Display average value on each bar.

**CHART-018:** Title: "Subject-wise Average Marks".

**Viva Value:** Shows which subjects students find easy/difficult.

#### 13.3.4 Subject-wise Pass Percentage Chart

**CHART-019:** Type: Bar Chart.

**CHART-020:** X-axis: Subject Names.

**CHART-021:** Y-axis: Pass Percentage.

**CHART-022:** Color code bars based on pass percentage: >75% green, 50-75% yellow, <50% red.

**CHART-023:** Display percentage on each bar.

**CHART-024:** Title: "Subject-wise Pass Percentage".

**Viva Value:** Identifies subjects where students struggle most.

#### 13.3.5 Top Performers Chart (Optional)

**CHART-025:** Type: Horizontal bar chart showing top 10 students.

**CHART-026:** Y-axis: Student Names (Roll Number).

**CHART-027:** X-axis: Percentage.

**CHART-028:** Title: "Top 10 Performers".

**Viva Value:** Quick identification of best students.

### 13.4 Performance Insights

**INSIGHT-001:** Identify "Weak Subjects" - subjects with lowest average marks or lowest pass percentage.

**INSIGHT-002:** Identify "Strong Subjects" - subjects with highest average marks or highest pass percentage.

**INSIGHT-003:** Identify "At-Risk Students" - students with percentage between 40-50% (barely passing).

**INSIGHT-004:** Identify "Students Below Average" - count of students scoring below class average.

**INSIGHT-005:** Display insights as cards or highlighted sections in Analysis dashboard.

### 13.5 Export Functionality (Optional - Future Enhancement)

**EXPORT-001:** Export Individual Student Report as PDF (using library like ReportLab or weasyprint).

**EXPORT-002:** Export Class Results as CSV for Excel analysis.

**EXPORT-003:** Export Subject Performance Report as PDF.

**Note:** PDF export is optional for MVP. Print-to-PDF via browser is acceptable for diploma project.

### 13.6 Viva Demonstration Value

**For impressive viva demonstration, prioritize:**

1. **Grade Distribution Chart** - Shows clear understanding of data visualization
2. **Pass/Fail Pie Chart** - Simple but effective visual
3. **Subject-wise Average Comparison** - Shows analytical thinking
4. **Top Performers List** - Practical and useful feature
5. **Individual Student Report** - Demonstrates complete workflow

**These features showcase:**
- Database querying and aggregation
- Data visualization skills
- Business logic implementation
- Practical application value
- Professional UI/UX

---

## 14. NON-FUNCTIONAL REQUIREMENTS

### 14.1 Performance Requirements

**NFR-001:** Admin dashboard shall load within 2 seconds on standard broadband connection (10 Mbps).

**NFR-002:** Page navigation shall respond within 1 second.

**NFR-003:** Form submission shall provide feedback within 2 seconds.

**NFR-004:** Database queries shall execute within 500ms for datasets up to 500 students.

**NFR-005:** Search/filter operations shall update results within 300ms (client-side filtering).

**NFR-006:** Charts shall render within 1 second of data load.

**NFR-007:** Student result lookup shall return result within 1.5 seconds.

**NFR-008:** Report generation shall complete within 3 seconds for individual reports, 5 seconds for class reports.

### 14.2 Reliability Requirements

**NFR-009:** System shall have 95% uptime during demonstration period (acceptable for student project).

**NFR-010:** Database connections shall be properly closed after each operation to prevent connection leaks.

**NFR-011:** System shall gracefully handle database connection failures with user-friendly error messages.

**NFR-012:** Session timeout shall be handled gracefully without data loss for ongoing form entries (warn before timeout).

**NFR-013:** Failed transactions shall be rolled back properly to maintain data integrity.

### 14.3 Scalability Requirements

**NFR-014:** System shall efficiently handle up to 500 students without performance degradation.

**NFR-015:** System shall handle up to 20 subjects without performance issues.

**NFR-016:** System shall handle up to 10,000 marks records (500 students × 20 subjects) efficiently.

**NFR-017:** Database queries shall use proper indexing to maintain performance as data grows.

**NFR-018:** Pagination shall be implemented for tables displaying more than 50 records (client-side for MVP).

**Note:** For diploma project, 100-200 students is a realistic demonstration dataset.

### 14.4 Security Requirements

**NFR-019:** All passwords shall be hashed using bcrypt with cost factor ≥ 12.

**NFR-020:** Session cookies shall be httpOnly and secure (in production).

**NFR-021:** All database queries shall use parameterized queries to prevent SQL injection.

**NFR-022:** All user inputs shall be validated and sanitized before processing.

**NFR-023:** Admin routes shall be protected with session authentication middleware.

**NFR-024:** Sensitive configuration (database URL, secret key) shall be stored in environment variables.

**NFR-025:** Production environment shall have DEBUG mode disabled.

**NFR-026:** HTTPS shall be enforced in production deployment.

**NFR-027:** Error messages shall not expose sensitive system information.

### 14.5 Maintainability Requirements

**NFR-028:** Code shall follow PEP 8 style guidelines for Python.

**NFR-029:** Functions shall have descriptive names and be limited to single responsibility.

**NFR-030:** Database schema shall be documented with column descriptions.

**NFR-031:** Complex business logic (result calculation) shall be modularized in separate functions.

**NFR-032:** Configuration values shall be centralized (not hardcoded throughout the code).

**NFR-033:** Code comments shall be provided for complex logic sections.

**NFR-034:** API routes shall follow RESTful conventions where applicable.

**NFR-035:** Clear separation between routes (controllers), business logic, and database operations (models).

### 14.6 Usability Requirements

**NFR-036:** User interface shall be intuitive enough for first-time admin users to navigate without training.

**NFR-037:** Form fields shall have clear labels and placeholder text.

**NFR-038:** Error messages shall be clear and actionable.

**NFR-039:** Success operations shall provide clear confirmation feedback.

**NFR-040:** Navigation menu shall be consistent across all pages.

**NFR-041:** Active page shall be clearly indicated in navigation.

**NFR-042:** Buttons shall be clearly labeled with action verbs (Add, Update, Delete, Cancel).

**NFR-043:** Destructive actions (Delete) shall require confirmation.

**NFR-044:** Color coding shall be consistent (Green=Success/Pass, Red=Error/Fail, Yellow=Warning).

### 14.7 Compatibility Requirements

**NFR-045:** Application shall work on modern web browsers:
- Google Chrome (latest 2 versions)
- Mozilla Firefox (latest 2 versions)
- Microsoft Edge (latest 2 versions)
- Safari (latest 2 versions)

**NFR-046:** Application shall be responsive and functional on screen sizes from 320px to 1920px width.

**NFR-047:** Core functionality shall work with JavaScript enabled (no no-JS fallback required for student project).

**NFR-048:** Application shall work on devices:
- Desktop/Laptop (primary target)
- Tablet (iPad, Android tablets)
- Mobile phones (secondary target, view-only features acceptable)

### 14.8 Responsive Design Requirements

**NFR-049:** Layout shall adapt to three breakpoints:
- Mobile: < 768px
- Tablet: 768px - 1023px
- Desktop: ≥ 1024px

**NFR-050:** Navigation menu shall collapse to hamburger menu on mobile devices.

**NFR-051:** Tables shall be horizontally scrollable on mobile devices.

**NFR-052:** Form fields shall stack vertically on mobile devices.

**NFR-053:** Touch targets (buttons, links) shall be minimum 44×44 pixels for mobile usability.

**NFR-054:** Charts shall be responsive and readable on all screen sizes.

### 14.9 Accessibility Requirements (Basic)

**NFR-055:** All images and icons shall have descriptive alt text.

**NFR-056:** Form inputs shall have associated labels.

**NFR-057:** Color shall not be the only means of conveying information (use text + color).

**NFR-058:** Text color contrast shall meet WCAG AA standards (4.5:1 for normal text).

**NFR-059:** Focus states shall be visible on interactive elements for keyboard navigation.

**NFR-060:** Semantic HTML elements shall be used (header, nav, main, section, article, footer).

**Note:** Full WCAG compliance is not required for diploma project, but basic accessibility is good practice.

### 14.10 Browser Storage Requirements

**NFR-061:** Session data shall be stored server-side (not in browser localStorage).

**NFR-062:** Sensitive data shall never be stored in browser localStorage or cookies.

**NFR-063:** localStorage can be used for non-sensitive UI preferences (e.g., sidebar collapsed state) - optional.

### 14.11 Deployment Requirements

**NFR-064:** Application shall be deployable on Render free tier without modification.

**NFR-065:** Database shall be hostable on Supabase free tier.

**NFR-066:** Environment variables shall be configurable through Render dashboard.

**NFR-067:** Application startup shall complete within 60 seconds on Render.

**NFR-068:** Application shall automatically reconnect to database after temporary connection loss.

**NFR-069:** Static files (CSS, JS, images) shall be served efficiently.

**NFR-070:** Application shall handle Render's automatic sleep and wake-up (free tier limitation).

---

## 15. DEPLOYMENT REQUIREMENTS

### 15.1 Production Environment

**DEPLOY-001:** Backend and Frontend shall be deployed together on **Render Free Tier**.

**DEPLOY-002:** Database shall be hosted on **Supabase PostgreSQL Free Tier**.

**DEPLOY-003:** No paid services or subscriptions shall be required.

**DEPLOY-004:** Deployment shall be achievable by a diploma student with basic technical knowledge.

### 15.2 Technology Stack Confirmation

| Component | Technology | Version | Justification |
|-----------|-----------|---------|---------------|
| Backend | Python Flask | 3.0+ | Lightweight, easy to learn, suitable for project |
| Frontend | HTML, CSS, JavaScript | Standard | Native web technologies, no build step required |
| Database | Supabase PostgreSQL | Latest | Free tier, managed, no server setup |
| Hosting | Render | Free tier | Easy deployment, free tier available |
| Charts | Chart.js | 4.x | Lightweight, easy to use, no backend dependency |

### 15.3 Environment Variables

**DEPLOY-005:** Application shall use environment variables for configuration:

| Variable Name | Description | Example Value | Required |
|---------------|-------------|---------------|----------|
| `DATABASE_URL` or `SUPABASE_URL` | Supabase PostgreSQL connection string | `postgresql://user:pass@host:5432/db` | Yes |
| `SUPABASE_KEY` | Supabase API key (if using Supabase client) | `eyJhbGc...` | Optional |
| `SECRET_KEY` | Flask session secret key | `random-256-bit-hex-string` | Yes |
| `FLASK_ENV` | Environment (production/development) | `production` | Yes |
| `DEBUG` | Debug mode flag | `False` | Yes |

**DEPLOY-006:** Environment variables shall be set in Render dashboard under service settings.

**DEPLOY-007:** A `.env.example` file shall be provided in repository with placeholder values:
```
DATABASE_URL=your_supabase_connection_url
SECRET_KEY=your_secret_key_here
FLASK_ENV=production
DEBUG=False
```

**DEPLOY-008:** Actual `.env` file shall be included in `.gitignore` to prevent committing secrets.

### 15.4 Python Dependencies

**DEPLOY-009:** All Python dependencies shall be listed in `requirements.txt`:
```
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
python-dotenv==1.0.0
bcrypt==4.1.1
psycopg2-binary==2.9.9
gunicorn==21.2.0
```

**DEPLOY-010:** Dependency versions shall be pinned to ensure consistent deployment.

**DEPLOY-011:** Only essential dependencies shall be included (avoid bloat).

### 15.5 Application Structure

**DEPLOY-012:** Application shall follow a standard Flask project structure:
```
/
├── app.py (main application file)
├── models.py (database models)
├── routes.py (or blueprints)
├── config.py (configuration)
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── /static
│   ├── /css
│   ├── /js
│   └── /images
└── /templates
    ├── base.html
    ├── login.html
    ├── dashboard.html
    └── ...
```

**DEPLOY-013:** Static files (CSS, JS, images) shall be served from `/static` directory.

**DEPLOY-014:** HTML templates shall be in `/templates` directory using Jinja2 templating.

### 15.6 Database Connection

**DEPLOY-015:** Database connection shall be established using connection string from environment variable.

**DEPLOY-016:** Connection pooling shall be configured appropriately for Flask application.

**DEPLOY-017:** Database connection errors shall be handled gracefully with retry logic.

**DEPLOY-018:** Application shall use Supabase's provided PostgreSQL connection string.

**DEPLOY-019:** SSL mode shall be enabled for database connection (required by Supabase).

### 15.7 Render Deployment Configuration

**DEPLOY-020:** Render service type: **Web Service**.

**DEPLOY-021:** Build Command: `pip install -r requirements.txt`

**DEPLOY-022:** Start Command: `gunicorn app:app` (assuming main file is `app.py` and Flask app instance is `app`)

**DEPLOY-023:** Python version: **3.11** (specify in Render dashboard or use `runtime.txt` file)

**DEPLOY-024:** Auto-deploy shall be enabled from GitHub repository (optional but recommended).

**DEPLOY-025:** Health check path: `/` or `/health` (implement simple health check endpoint).

### 15.8 Static File Serving

**DEPLOY-026:** Flask shall serve static files using `url_for('static', filename='...')` in templates.

**DEPLOY-027:** Static file caching shall be configured for performance (Flask default is acceptable).

**DEPLOY-028:** CSS and JS files shall be minified for production (optional for MVP, but good practice).

### 15.9 Database Initialization

**DEPLOY-029:** Database tables shall be created either:
- Option A: Manually using Supabase SQL editor
- Option B: Using Flask-Migrate or Alembic migrations
- Option C: Using initialization script run once after deployment

**DEPLOY-030:** Sample/seed data shall be insertable via SQL script or admin interface.

**DEPLOY-031:** Database schema documentation shall be provided for manual setup.

### 15.10 Logging

**DEPLOY-032:** Application shall log to stdout/stderr (captured by Render logs).

**DEPLOY-033:** Log level shall be configurable via environment variable (default: INFO in production).

**DEPLOY-034:** Errors shall be logged with sufficient detail for debugging without exposing sensitive data.

**DEPLOY-035:** Render logs shall be accessible via dashboard for troubleshooting.

### 15.11 Production Security Checklist

**DEPLOY-036:** `DEBUG=False` in production environment.

**DEPLOY-037:** `FLASK_ENV=production` in production environment.

**DEPLOY-038:** Strong random `SECRET_KEY` generated and set.

**DEPLOY-039:** Database credentials not hardcoded in source code.

**DEPLOY-040:** `.env` file excluded from git via `.gitignore`.

**DEPLOY-041:** HTTPS enforced (Render provides this automatically).

**DEPLOY-042:** Security headers configured (can use Flask-Talisman or manual headers).

### 15.12 Deployment Testing

**DEPLOY-043:** Test deployment on local machine first using production-like settings.

**DEPLOY-044:** Test database connectivity from local environment to Supabase.

**DEPLOY-045:** Test all critical features after production deployment:
- Admin login
- Student CRUD operations
- Marks entry
- Result calculation
- Result lookup
- Dashboard charts

**DEPLOY-046:** Verify responsive design on actual mobile devices after deployment.

**DEPLOY-047:** Test print functionality on deployed application.

### 15.13 Free Tier Limitations & Considerations

**Render Free Tier Limitations:**
- **DEPLOY-048:** Service sleeps after 15 minutes of inactivity (first request after sleep may take 30-60 seconds to wake up).
- **DEPLOY-049:** 750 hours/month free runtime (sufficient for demo project).
- **DEPLOY-050:** Application should handle cold start gracefully with loading indicator.

**Supabase Free Tier Limitations:**
- **DEPLOY-051:** 500 MB database storage (more than sufficient for student result project).
- **DEPLOY-052:** Project pauses after 1 week of inactivity (can be resumed easily).
- **DEPLOY-053:** 2 GB bandwidth/month (sufficient for demo purposes).

**Considerations:**
- **DEPLOY-054:** Warn viva examiners about potential 30-second initial load time if service was sleeping.
- **DEPLOY-055:** Consider waking up service 5 minutes before viva/demo.
- **DEPLOY-056:** Have backup plan: local demonstration if production deployment has issues.

### 15.14 GitHub Workflow (Recommended)

**DEPLOY-057:** Create GitHub repository for the project.

**DEPLOY-058:** Connect Render to GitHub repository for automatic deployments.

**DEPLOY-059:** Push to `main` branch triggers automatic redeployment.

**DEPLOY-060:** Include comprehensive `README.md` with:
- Project description
- Technology stack
- Local setup instructions
- Deployment instructions
- Environment variables documentation
- Database setup guide

### 15.15 Backup & Recovery

**DEPLOY-061:** Supabase provides automatic backups (check free tier policy).

**DEPLOY-062:** Periodically export database using Supabase dashboard or `pg_dump` for safety.

**DEPLOY-063:** Keep local copy of sample data SQL script for quick recovery.

**DEPLOY-064:** Document database recovery procedure in README.

---

## 16. TESTING REQUIREMENTS

### 16.1 Unit Testing (Backend)

**TEST-001:** Test user authentication functions:
- Valid login credentials → successful authentication
- Invalid login credentials → authentication failure
- Password hashing and verification

**TEST-002:** Test student CRUD operations:
- Create student with valid data → success
- Create student with duplicate Roll Number → error
- Update student with valid data → success
- Delete student without marks → success
- Delete student with marks → warning/confirmation

**TEST-003:** Test subject CRUD operations:
- Create subject with valid data → success
- Create subject with duplicate Subject Code → error
- Update subject → success
- Delete subject without marks → success
- Delete subject with marks → error (prevented)

**TEST-004:** Test marks CRUD operations:
- Create marks with valid data → success
- Create duplicate marks (same student-subject) → error
- Update marks → success
- Validate marks ≤ maximum marks

**TEST-005:** Test result calculation logic:
- Calculate total marks correctly
- Calculate percentage correctly (rounded to 2 decimals)
- Assign correct grade based on percentage
- Determine pass/fail status correctly
- Handle absent students (marks=0, status=FAIL)
- Handle subject-wise pass/fail correctly

**TEST-006:** Test analysis calculations:
- Class average calculation
- Subject average calculation
- Pass percentage calculation
- Grade distribution counts

### 16.2 Integration Testing

**TEST-007:** Test complete user workflows:
- Admin login → Dashboard → Add Student → Add Subject → Enter Marks → View Result
- Student lookup → Enter credentials → View result

**TEST-008:** Test database interactions:
- Create record → verify in database
- Update record → verify changes persisted
- Delete record → verify removed from database
- Foreign key constraints work correctly

**TEST-009:** Test session management:
- Login creates session
- Session persists across pages
- Session expires after timeout
- Logout destroys session

**TEST-010:** Test form submissions:
- Valid form data → success response
- Invalid form data → validation errors shown
- Server-side validation catches bypassed frontend validation

### 16.3 Frontend Testing

**TEST-011:** Test form validations:
- Required field empty → error message shown
- Invalid email format → error message shown
- Marks exceed maximum → error message shown
- Validation errors clear when corrected

**TEST-012:** Test search and filter functionality:
- Search students by name → filtered results shown
- Search students by roll number → filtered results shown
- Filter by gender → correct subset shown
- Combined search + filter works

**TEST-013:** Test navigation:
- All navigation links work
- Active page highlighted in menu
- Unauthorized access redirected to login
- Logout redirects to login page

**TEST-014:** Test responsive design:
- Test on desktop resolution (1920×1080, 1366×768)
- Test on tablet resolution (768×1024)
- Test on mobile resolution (375×667)
- Navigation collapses to hamburger on mobile
- Tables are scrollable on mobile

**TEST-015:** Test charts rendering:
- Grade distribution chart displays correctly
- Pass/fail pie chart displays correctly
- Subject-wise bar chart displays correctly
- Charts resize on window resize

### 16.4 Security Testing

**TEST-016:** Test authentication security:
- Direct URL access to admin pages without login → redirected
- Invalid session token → redirected to login
- Session hijacking protection

**TEST-017:** Test SQL injection prevention:
- Enter SQL injection patterns in input fields → safely handled
- Verify parameterized queries used throughout

**TEST-018:** Test XSS prevention:
- Enter `<script>alert('XSS')</script>` in text fields → escaped/sanitized
- Verify HTML special characters escaped in output

**TEST-019:** Test authorization:
- Student cannot access admin routes
- Student can only view own result (not others')

**TEST-020:** Test password security:
- Password stored as hash in database (never plaintext)
- Bcrypt used with appropriate cost factor

### 16.5 Validation Testing

**TEST-021:** Test input validation for all forms:
- Student form: Roll Number, Name, Email, DOB, Gender, Contact
- Subject form: Subject Code, Subject Name, Max Marks
- Marks form: Student, Subject, Marks, Absent
- Login form: Email/Username, Password
- Result lookup form: Roll Number, DOB

**TEST-022:** Test edge cases:
- Empty strings
- Very long strings (> max length)
- Special characters
- Unicode characters
- Negative numbers where not allowed
- Zero values
- Extremely large numbers

### 16.6 Error Handling Testing

**TEST-023:** Test error scenarios:
- Database connection failure → error message shown
- Duplicate record creation → appropriate error shown
- Record not found → appropriate error shown
- Network timeout → error message with retry option

**TEST-024:** Verify error messages:
- User-friendly messages shown (not technical details)
- Stack traces not exposed to users
- Errors logged server-side

### 16.7 Performance Testing (Basic)

**TEST-025:** Test page load times:
- Dashboard loads within 2 seconds
- Student list page loads within 2 seconds
- Result lookup completes within 1.5 seconds

**TEST-026:** Test with realistic data volume:
- 200 students
- 10 subjects
- 2000 marks records (200 × 10)
- Verify no significant performance degradation

**TEST-027:** Test search performance:
- Search responds within 300ms with 200 students

### 16.8 Browser Compatibility Testing

**TEST-028:** Test on multiple browsers:
- Google Chrome (latest)
- Mozilla Firefox (latest)
- Microsoft Edge (latest)
- Safari (latest) - if Mac available

**TEST-029:** Verify consistent appearance and functionality across browsers.

**TEST-030:** Test on different operating systems:
- Windows
- macOS (if available)
- Linux (optional)

### 16.9 Deployment Testing

**TEST-031:** Test local deployment:
- Application runs locally with `.env` configuration
- Database connectivity works
- All features functional

**TEST-032:** Test production deployment on Render:
- Application deploys successfully
- Environment variables configured correctly
- Database connectivity works from Render to Supabase
- HTTPS enforced
- All features functional in production

**TEST-033:** Test cold start (after service sleep):
- Service wakes up successfully
- First request completes (may take 30-60 seconds)
- Subsequent requests are fast

### 16.10 User Acceptance Testing (UAT)

**TEST-034:** Simulate complete admin workflow:
1. Login as admin
2. View dashboard statistics
3. Add 5 students
4. Add 5 subjects
5. Enter marks for all students
6. View results
7. View analysis dashboard with charts
8. Generate individual report
9. Generate class report
10. Logout

**TEST-035:** Simulate student workflow:
1. Open result lookup page
2. Enter Roll Number and DOB
3. View personal result
4. Verify subject-wise marks displayed correctly
5. Verify overall status shown correctly
6. Print result

**TEST-036:** Verify all acceptance criteria met (see Section 21).

### 16.11 Test Data Preparation

**TEST-037:** Create comprehensive test dataset:
- 10-15 students with varied details
- 6-8 subjects
- Complete marks for all students
- Include edge cases: 1 student absent, 2 students failing, 3 students distinction

**TEST-038:** Create test SQL script for quick database population.

**TEST-039:** Document test user credentials (admin login).

### 16.12 Testing Checklist

**Create a practical test checklist for viva preparation:**

| # | Test Item | Expected Result | Status |
|---|-----------|----------------|--------|
| 1 | Admin login with valid credentials | Redirect to dashboard | ☐ |
| 2 | Admin login with invalid credentials | Error message shown | ☐ |
| 3 | Add new student | Student created successfully | ☐ |
| 4 | Add duplicate Roll Number | Error message shown | ☐ |
| 5 | Edit student | Changes saved successfully | ☐ |
| 6 | Delete student | Student deleted (or warning shown) | ☐ |
| 7 | Add new subject | Subject created successfully | ☐ |
| 8 | Enter marks | Marks saved successfully | ☐ |
| 9 | Enter marks exceeding maximum | Error message shown | ☐ |
| 10 | View results | Results displayed correctly | ☐ |
| 11 | Dashboard charts | Charts render correctly | ☐ |
| 12 | Student result lookup | Result displayed correctly | ☐ |
| 13 | Student result lookup (wrong credentials) | Error message shown | ☐ |
| 14 | Generate individual report | Report displayed correctly | ☐ |
| 15 | Print report | Print preview clean | ☐ |
| 16 | Search students | Filtered results shown | ☐ |
| 17 | Responsive design (mobile) | Layout adapts correctly | ☐ |
| 18 | Session timeout | Redirect to login | ☐ |
| 19 | Logout | Session destroyed, redirect to login | ☐ |
| 20 | Production deployment | Application accessible via URL | ☐ |

---

## 17. DEMO / VIVA REQUIREMENTS

### 17.1 Viva Demonstration Flow (5-10 minutes)

**Recommended Demo Sequence:**

#### Stage 1: Introduction (30 seconds)
**DEMO-001:** Briefly introduce the project:
- "Online Student Result Analysis System"
- "Web-based application for managing and analyzing student academic results"
- "Built using Python Flask, HTML/CSS/JavaScript, and Supabase PostgreSQL"

#### Stage 2: Admin Login (30 seconds)
**DEMO-002:** Demonstrate admin authentication:
- Open application URL
- Show login page
- Enter admin credentials
- Successfully login and redirect to dashboard

#### Stage 3: Dashboard Overview (1 minute)
**DEMO-003:** Highlight dashboard features:
- Point out key metrics (Total Students, Total Subjects, Pass %, Class Average)
- Show top performers list
- Demonstrate charts (Grade Distribution, Pass/Fail Ratio)
- Explain what insights these provide

#### Stage 4: Student Management (1.5 minutes)
**DEMO-004:** Demonstrate student operations:
- Navigate to Students section
- Show existing students table
- Add a new student (fill form, submit)
- Show success notification
- Demonstrate search functionality (search by name or roll number)
- Optionally: Edit a student, show delete confirmation

#### Stage 5: Subject Management (1 minute)
**DEMO-005:** Demonstrate subject operations:
- Navigate to Subjects section
- Show existing subjects table
- Add a new subject (or just show existing ones)
- Highlight maximum marks configuration

#### Stage 6: Marks Entry (1.5 minutes)
**DEMO-006:** Demonstrate marks entry process:
- Navigate to Marks section
- Select a student from dropdown
- Select a subject
- Enter marks
- Submit and show success
- Show validation: Try entering marks greater than maximum → error shown
- Demonstrate marks table with existing records

#### Stage 7: Results & Calculation (1.5 minutes)
**DEMO-007:** Demonstrate result generation and calculation:
- Navigate to Results section
- Show results table with calculated percentages, grades, pass/fail status
- Click to view detailed result for one student
- Explain calculation: "Total marks, percentage calculated automatically, grade assigned based on percentage, pass/fail determined by subject-wise and overall criteria"
- Point out color coding (green for pass, red for fail)

#### Stage 8: Performance Analysis (1.5 minutes)
**DEMO-008:** Demonstrate analytics features:
- Navigate to Analysis section
- Show subject-wise average comparison chart
- Show grade distribution
- Highlight weak and strong subjects identification
- Explain practical value: "Teachers can identify which subjects students struggle with"

#### Stage 9: Reports (1 minute)
**DEMO-009:** Demonstrate report generation:
- Navigate to Reports section
- Generate individual student report
- Show print preview (clean formatted report)
- Briefly mention class report and subject performance report options

#### Stage 10: Student Result Lookup (1 minute)
**DEMO-010:** Demonstrate student-facing feature:
- Open new browser tab (or logout and go to result lookup)
- Show public result lookup page
- Enter Roll Number and Date of Birth for a test student
- Show personal result page with subject-wise marks, percentage, grade, status
- Highlight security: "Student can only see their own result using Roll Number + DOB authentication"

#### Stage 11: Responsive Design (30 seconds)
**DEMO-011:** Demonstrate responsive design:
- Resize browser window to mobile size (or open on mobile device if available)
- Show navigation collapses to hamburger menu
- Show table becomes scrollable
- Show layout adapts

#### Stage 12: Conclusion (30 seconds)
**DEMO-012:** Summarize key features:
- "Complete result management system"
- "Automated calculation and analysis"
- "Visual analytics with charts"
- "Secure role-based access"
- "Deployed on cloud (Render + Supabase)"
- "Responsive and production-ready"

### 17.2 Questions You Should Be Prepared to Answer

**Technical Questions:**

**Q1: Why did you choose Flask over Django?**
**A:** Flask is lightweight, easier to learn and implement for a focused project like this. Django would be overkill with unnecessary features. Flask gives me better understanding of core concepts.

**Q2: How do you ensure password security?**
**A:** Passwords are hashed using bcrypt with cost factor 12 before storing in database. Plaintext passwords are never stored. Session-based authentication with httpOnly cookies.

**Q3: Explain the result calculation logic.**
**A:** Total marks = sum of marks in all subjects. Percentage = (total obtained / total maximum) × 100. Grade assigned based on percentage ranges. Pass/Fail determined by: student must score ≥40% in each subject AND overall ≥40%.

**Q4: How do you prevent SQL injection?**
**A:** All database queries use parameterized queries (with SQLAlchemy or psycopg2). User inputs are never directly concatenated into SQL strings. Backend validation sanitizes all inputs.

**Q5: What is the database schema?**
**A:** Four tables: admins (authentication), students (master data), subjects (master data), marks (student-subject marks with foreign keys). Marks table has composite unique constraint on (student_id, subject_id) to prevent duplicates.

**Q6: How do you handle duplicate marks entry?**
**A:** Database unique constraint on (student_id, subject_id). Backend checks for existing record before insert. If duplicate detected, show error message to user.

**Q7: Explain your deployment architecture.**
**A:** Flask application deployed on Render free tier as web service. Database hosted on Supabase PostgreSQL free tier. Environment variables configured in Render dashboard. Auto-deployment from GitHub repository.

**Q8: How do you handle marks for absent students?**
**A:** Marks table has `is_absent` boolean field. If marked absent, marks set to 0 and overall status becomes FAIL.

**Q9: What happens if a student fails in one subject but has high overall percentage?**
**A:** Student still fails overall. Our logic requires passing each subject individually (≥40% per subject) AND overall percentage ≥40%. Failing any subject results in overall FAIL status.

**Q10: How do you ensure data consistency?**
**A:** Foreign key constraints in database. Cascade delete for student→marks. Restrict delete for subject→marks. Backend validation before all operations. Database transactions for multi-step operations.

**Functional Questions:**

**Q11: Can a teacher add marks?**
**A:** In MVP, only admin adds marks. Teacher role excluded for simplicity. Can be added as future enhancement.

**Q12: Can students change their marks?**
**A:** No. Students have read-only access to their own results. No modification capabilities.

**Q13: How do students know their Roll Number and DOB if they forgot?**
**A:** In real implementation, this information would be provided during admission. For demo, assume students have this information.

**Q14: What if marks need correction after result published?**
**A:** Admin can edit marks. Result will be automatically recalculated upon marks update.

**Q15: Can you export results to Excel?**
**A:** Currently, reports can be printed to PDF via browser. CSV export can be added as future enhancement.

### 17.3 Features That Provide Strongest Demo Value

**Priority for Demonstration:**

1. **Auto-calculation and result generation** - Shows core business logic implementation
2. **Visual charts and analytics** - Impressive visual element, shows data visualization skills
3. **Student result lookup with DOB authentication** - Shows security awareness
4. **Responsive design** - Shows modern web development practices
5. **Form validation (try entering invalid data)** - Shows attention to user experience and data integrity
6. **Print-friendly reports** - Shows practical usability
7. **Search and filter** - Shows interactive UI capabilities
8. **Production deployment** - Shows end-to-end project completion

### 17.4 Demo Preparation Checklist

**PREP-001:** Ensure production deployment is working 1 day before viva.

**PREP-002:** Test complete demo flow at least 3 times before viva.

**PREP-003:** Prepare test data: 10-15 students, 6 subjects, complete marks, varied results (pass/fail/distinction).

**PREP-004:** Wake up Render service 5 minutes before demo (to avoid cold start delay).

**PREP-005:** Have admin credentials ready (written down).

**PREP-006:** Have 2-3 student Roll Number + DOB combinations ready for result lookup demo.

**PREP-007:** Prepare backup: Have application running locally in case of internet/deployment issues.

**PREP-008:** Prepare system architecture diagram (simple: Browser → Flask → Database).

**PREP-009:** Prepare database schema diagram (ER diagram showing 4 tables and relationships).

**PREP-010:** Test on the laptop/system you'll use for demo.

**PREP-011:** Ensure stable internet connection or have mobile hotspot backup.

**PREP-012:** Prepare 1-2 slides (optional): Project title, Tech stack, Features overview.

### 17.5 Confidence Boosters

**DEMO-013:** Practice explaining technical decisions confidently.

**DEMO-014:** Know your code: Be able to show specific files/functions if asked.

**DEMO-015:** Emphasize practical value: "This system can be used by real educational institutions."

**DEMO-016:** Highlight automation: "Manual calculation eliminated, reduces errors and saves time."

**DEMO-017:** Mention security: "Role-based access, password hashing, SQL injection prevention."

**DEMO-018:** Mention scalability awareness: "Current design handles 500 students efficiently, can be scaled further with optimization."

**DEMO-019:** Be honest about limitations: "PDF export not implemented in MVP, but can be added. Free tier has cold start delay."

**DEMO-020:** Show enthusiasm: "I learned a lot implementing this project, especially database design, backend logic, and deployment."

---

## 18. SAMPLE DATA REQUIREMENTS

### 18.1 Admin Sample Data

**SAMPLE-001:** One default admin account for testing and demo:

| Field | Value |
|-------|-------|
| Username | admin |
| Email | admin@resultportal.com |
| Password (plaintext for reference only) | Admin@123 |
| Password Hash | (to be generated using bcrypt) |
| Full Name | System Administrator |

### 18.2 Student Sample Data

**SAMPLE-002:** 15 sample students with varied profiles:

| Roll No | Name | Email | DOB | Gender | Contact |
|---------|------|-------|-----|--------|---------|
| 2024001 | Rahul Sharma | rahul.sharma@email.com | 2005-03-15 | Male | 9876543210 |
| 2024002 | Priya Patel | priya.patel@email.com | 2005-07-22 | Female | 9876543211 |
| 2024003 | Amit Kumar | amit.kumar@email.com | 2005-01-10 | Male | 9876543212 |
| 2024004 | Sneha Singh | sneha.singh@email.com | 2005-09-05 | Female | 9876543213 |
| 2024005 | Rohan Verma | rohan.verma@email.com | 2005-11-18 | Male | 9876543214 |
| 2024006 | Anjali Gupta | anjali.gupta@email.com | 2005-04-25 | Female | 9876543215 |
| 2024007 | Vikram Reddy | vikram.reddy@email.com | 2005-06-12 | Male | 9876543216 |
| 2024008 | Pooja Desai | pooja.desai@email.com | 2005-08-30 | Female | 9876543217 |
| 2024009 | Karan Joshi | karan.joshi@email.com | 2005-02-14 | Male | 9876543218 |
| 2024010 | Neha Mehta | neha.mehta@email.com | 2005-10-08 | Female | 9876543219 |
| 2024011 | Sanjay Rao | sanjay.rao@email.com | 2005-05-20 | Male | 9876543220 |
| 2024012 | Divya Nair | divya.nair@email.com | 2005-12-03 | Female | 9876543221 |
| 2024013 | Arjun Iyer | arjun.iyer@email.com | 2005-03-28 | Male | 9876543222 |
| 2024014 | Kavita Pillai | kavita.pillai@email.com | 2005-07-16 | Female | 9876543223 |
| 2024015 | Manish Kulkarni | manish.kulkarni@email.com | 2005-09-22 | Male | 9876543224 |

**Note:** Date of Birth values are important for result lookup authentication.

### 18.3 Subject Sample Data

**SAMPLE-003:** 6 subjects covering typical diploma curriculum:

| Subject Code | Subject Name | Max Marks |
|--------------|--------------|-----------|
| MATH101 | Mathematics | 100 |
| SCI102 | Science | 100 |
| ENG103 | English | 100 |
| CS104 | Computer Science | 100 |
| SS105 | Social Studies | 100 |
| PHY106 | Physics | 100 |

### 18.4 Marks Sample Data Strategy

**SAMPLE-004:** Create marks data with the following distribution to demonstrate all scenarios:

**High Performers (>75% - Grade A or B):**
- Roll No 2024001: All subjects 85-95 (will get A grade)
- Roll No 2024002: All subjects 80-90 (will get A grade)
- Roll No 2024003: All subjects 76-82 (will get B grade)
- Roll No 2024006: All subjects 78-88 (will get B grade)

**Average Performers (60-74% - Grade C):**
- Roll No 2024004: All subjects 65-72 (will get C grade)
- Roll No 2024007: All subjects 60-68 (will get C grade)
- Roll No 2024010: All subjects 62-70 (will get C grade)

**Below Average but Passing (40-59% - Grade D):**
- Roll No 2024008: All subjects 42-55 (will get D grade)
- Roll No 2024011: All subjects 45-52 (will get D grade)

**Failing Students (demonstrating different fail scenarios):**
- Roll No 2024009: Failed in one subject (e.g., Math: 35, others: 60+) → Overall FAIL
- Roll No 2024012: Failed in two subjects (e.g., Math: 32, Science: 38, others: 55+) → Overall FAIL

**Absent Student:**
- Roll No 2024013: Marked absent in one subject (e.g., Math: Absent/0, others: 70+) → Overall FAIL

**Borderline Student:**
- Roll No 2024014: All subjects exactly 40-42 (barely passing) → PASS with Grade D

**Incomplete (for demonstrating "Result not published"):**
- Roll No 2024015: Only 3 subjects have marks entered, 3 missing → Result not available

**Detailed Example for 2024001 (Top Performer):**

| Subject | Marks Obtained | Max Marks | Status |
|---------|----------------|-----------|--------|
| MATH101 | 92 | 100 | Pass |
| SCI102 | 88 | 100 | Pass |
| ENG103 | 95 | 100 | Pass |
| CS104 | 90 | 100 | Pass |
| SS105 | 85 | 100 | Pass |
| PHY106 | 87 | 100 | Pass |
| **Total** | **537** | **600** | **PASS** |
| **Percentage** | **89.50%** | | |
| **Grade** | **A** | | |

### 18.5 Sample Data Goals

**SAMPLE-005:** Sample data should demonstrate:
- Grade distribution: At least 1-2 students in each grade (A, B, C, D, F)
- Pass/Fail ratio: Approximately 70-80% pass rate (realistic)
- Subject variation: Some subjects with higher averages, some lower
- All validation scenarios: Duplicate prevention, marks validation, absent handling
- Incomplete results: At least 1 student with incomplete marks
- Top performers: Clear top 5 for dashboard display
- Analytics accuracy: Data should produce meaningful charts and statistics

### 18.6 Data Insertion Approach

**SAMPLE-006:** Create SQL script file (`sample_data.sql`) with INSERT statements for easy database population.

**SAMPLE-007:** Alternatively, provide CSV files for bulk import via Supabase dashboard.

**SAMPLE-008:** Ensure admin account is created first, then students, then subjects, then marks (respecting foreign keys).

**SAMPLE-009:** Document sample student credentials (Roll No + DOB) for result lookup demo in README or separate file.

---

## 19. FUTURE ENHANCEMENTS

These features are OUT OF SCOPE for the MVP but can be mentioned during viva as potential improvements:

### 19.1 User Management Enhancements

**FE-001:** Teacher/Faculty Role - Separate role for teachers with limited permissions (marks entry only, no student management).

**FE-002:** Multiple Admin Accounts - Support for multiple administrators with role hierarchy.

**FE-003:** Parent Portal - Separate login for parents to view their child's results.

**FE-004:** Student Login - Full login capability for students instead of Roll No + DOB lookup.

**FE-005:** User Profile Management - Allow users to update their own profiles, change passwords.

### 19.2 Academic Structure Enhancements

**FE-006:** Multiple Departments/Branches - Support different departments (Computer, Mechanical, etc.) within institution.

**FE-007:** Multiple Semesters/Years - Track results across multiple academic periods.

**FE-008:** Different Exam Types - Separate marks for Internal, Mid-term, Final exams.

**FE-009:** Subject Categories - Classify subjects as Core, Elective, Lab, Theory.

**FE-010:** Credit System - Assign credits to subjects and calculate CGPA.

**FE-011:** Grading Scales per Subject - Different subjects can have different grading scales.

### 19.3 Notification Enhancements

**FE-012:** Email Notifications - Send result via email when published.

**FE-013:** SMS Notifications - Send result summary via SMS.

**FE-014:** Parent Notifications - Notify parents when result is published.

**FE-015:** Alert for Low Performance - Automatic alerts for students scoring below threshold.

### 19.4 Reporting Enhancements

**FE-016:** PDF Export - Generate results as downloadable PDF using libraries like ReportLab.

**FE-017:** Excel Export - Export class results to Excel format.

**FE-018:** Bulk Result Cards - Generate printable result cards for all students at once.

**FE-019:** Marksheet Generation - Official marksheet format with institution logo and seal.

**FE-020:** Historical Reports - Compare performance across semesters/years.

**FE-021:** Custom Report Builder - Admin can create custom reports with selected fields.

### 19.5 Analytics Enhancements

**FE-022:** Trend Analysis - Performance trends over multiple semesters.

**FE-023:** Predictive Analytics - Predict student performance based on historical data (ML).

**FE-024:** Subject Correlation Analysis - Identify which subjects students tend to perform similarly in.

**FE-025:** Improvement Tracking - Track individual student improvement over time.

**FE-026:** Comparative Analysis - Compare performance across different classes/departments.

**FE-027:** Advanced Visualizations - More chart types (radar charts, heatmaps, etc.).

### 19.6 Integration Enhancements

**FE-028:** Attendance Integration - Link attendance data with results.

**FE-029:** Fee Management - Prevent result access if fees unpaid.

**FE-030:** Library Integration - Show library due status on result page.

**FE-031:** Digital Certificate - Generate digital certificates for passed students.

**FE-032:** Government Portal Integration - Export data to government education portals.

### 19.7 System Enhancements

**FE-033:** Multi-Institution Support - One system managing multiple institutions.

**FE-034:** Advanced Search - Fuzzy search, search across all fields.

**FE-035:** Audit Logs - Track all changes (who changed what when).

**FE-036:** Data Import - Import students/marks from Excel/CSV.

**FE-037:** Batch Operations - Bulk update, bulk delete with filters.

**FE-038:** Offline Mode - Progressive Web App with offline capabilities.

**FE-039:** Mobile Native App - Android/iOS apps for students and admins.

**FE-040:** API for Third-Party Integration - RESTful API for external systems.

### 19.8 UI/UX Enhancements

**FE-041:** Dark Mode - Theme switcher for dark/light mode.

**FE-042:** Customizable Dashboard - Admin can rearrange dashboard widgets.

**FE-043:** Data Visualization Builder - Drag-and-drop chart builder.

**FE-044:** Multi-Language Support - Interface in multiple languages.

**FE-045:** Accessibility Improvements - Full WCAG AAA compliance.

### 19.9 Security Enhancements

**FE-046:** Two-Factor Authentication - 2FA for admin login.

**FE-047:** Biometric Authentication - Fingerprint/face recognition for mobile app.

**FE-048:** Role-Based Permissions - Granular permissions system.

**FE-049:** Data Encryption - Encrypt sensitive data at rest.

**FE-050:** Regular Security Audits - Automated security scanning.

---

## 20. MVP DEFINITION

### 20.1 MUST HAVE (Absolutely Required)

These features are essential for the project to be considered complete and demonstrable:

**MUST-001:** Admin authentication (login/logout)

**MUST-002:** Admin dashboard with key metrics and charts

**MUST-003:** Student CRUD operations (Create, Read, Update, Delete)

**MUST-004:** Subject CRUD operations

**MUST-005:** Marks entry and management

**MUST-006:** Automatic result calculation (total, percentage, grade, pass/fail)

**MUST-007:** Result viewing for admin

**MUST-008:** Student result lookup (public, using Roll No + DOB)

**MUST-009:** Personal result page for students

**MUST-010:** Performance analysis with key statistics

**MUST-011:** Visual charts (grade distribution, pass/fail ratio, subject-wise performance)

**MUST-012:** Basic reports (individual student, class results)

**MUST-013:** Search functionality (students, subjects, marks)

**MUST-014:** Form validation (frontend and backend)

**MUST-015:** Responsive design (desktop and mobile friendly)

**MUST-016:** Error handling with user-friendly messages

**MUST-017:** Database with proper relationships and constraints

**MUST-018:** Security (password hashing, SQL injection prevention, session management)

**MUST-019:** Production deployment on Render + Supabase

**MUST-020:** Sample data for demonstration

### 20.2 SHOULD HAVE (Important but Not Blocking)

These features add significant value and should be included if time permits:

**SHOULD-001:** Filter functionality (students by gender, results by pass/fail status)

**SHOULD-002:** Subject performance report

**SHOULD-003:** Overall analysis report

**SHOULD-004:** Top performers list on dashboard

**SHOULD-005:** Print-friendly CSS for reports

**SHOULD-006:** Loading indicators during async operations

**SHOULD-007:** Success/error toast notifications

**SHOULD-008:** Confirmation dialogs for delete operations

**SHOULD-009:** Absent student handling

**SHOULD-010:** Marks edit functionality

**SHOULD-011:** Data validation for reasonable value ranges (e.g., DOB not in future)

**SHOULD-012:** Session timeout handling

**SHOULD-013:** Search with partial matching

**SHOULD-014:** Sort functionality on tables (nice to have)

**SHOULD-015:** Weak/strong subject identification

### 20.3 NICE TO HAVE (Optional Enhancements)

These features are good additions but not required for project acceptance:

**NICE-001:** PDF export for reports

**NICE-002:** CSV export for results

**NICE-003:** Advanced charts (radar charts, line charts)

**NICE-004:** Standard deviation calculations

**NICE-005:** Percentile rank for students

**NICE-006:** Subject difficulty index

**NICE-007:** At-risk students identification

**NICE-008:** Recent activity log on dashboard

**NICE-009:** Pagination for large tables

**NICE-010:** Dark mode theme

**NICE-011:** Password change functionality

**NICE-012:** Rate limiting for login attempts

**NICE-013:** Email validation with verification

**NICE-014:** Bulk marks entry (upload via CSV)

**NICE-015:** Custom grading scale configuration

### 20.4 MVP Boundary Summary

**For Diploma Final-Year Project Acceptance:**

✅ **Include:** All MUST HAVE features (20 items)  
✅ **Include:** At least 10 SHOULD HAVE features  
⚠️ **Optional:** NICE TO HAVE features only if time permits  

**Minimum Viable Product = MUST HAVE features fully functional**

**Recommended MVP = MUST HAVE + Most SHOULD HAVE features**

---

## 21. ACCEPTANCE CRITERIA

The project shall be considered **COMPLETE and READY FOR SUBMISSION** when all the following criteria are met:

### 21.1 Functional Completeness

**AC-001:** Admin can successfully login with valid credentials and logout.

**AC-002:** Admin dashboard displays all key metrics (student count, subject count, pass %, class average) correctly.

**AC-003:** Admin dashboard displays at least 2 charts (grade distribution, pass/fail ratio).

**AC-004:** Admin can create, view, edit, and delete students with proper validation.

**AC-005:** System prevents duplicate Roll Numbers.

**AC-006:** Admin can create, view, edit, and delete subjects with proper validation.

**AC-007:** System prevents duplicate Subject Codes.

**AC-008:** System prevents subject deletion when marks records exist.

**AC-009:** Admin can enter marks for students with validation (marks ≤ max marks).

**AC-010:** System prevents duplicate marks entry (same student-subject combination).

**AC-011:** System correctly calculates total marks, percentage (2 decimals), grade, and pass/fail status.

**AC-012:** Pass/fail logic works correctly: student must pass all subjects (≥40%) AND overall (≥40%).

**AC-013:** Absent students are handled correctly (marks=0, status=FAIL).

**AC-014:** Admin can view all calculated results in results section.

**AC-015:** Student can lookup their result using Roll Number + Date of Birth.

**AC-016:** Student result page displays subject-wise marks, total, percentage, grade, and status correctly.

**AC-017:** Student cannot access other students' results.

**AC-018:** Analysis section displays class average, subject averages, and identifies weak/strong subjects.

**AC-019:** Individual student report can be generated and printed.

**AC-020:** Class results report can be generated showing all students.

### 21.2 Validation & Error Handling

**AC-021:** All forms have frontend validation with inline error messages.

**AC-022:** All forms have backend validation that catches bypassed frontend validation.

**AC-023:** User-friendly error messages are displayed (no technical details exposed).

**AC-024:** Database errors are handled gracefully without crashing the application.

**AC-025:** Invalid login shows appropriate error message.

### 21.3 Security

**AC-026:** Admin passwords are stored as bcrypt hashes (never plaintext).

**AC-027:** All admin routes are protected and redirect to login if not authenticated.

**AC-028:** Sessions expire after timeout (30 minutes).

**AC-029:** SQL injection attempts are prevented (parameterized queries used).

**AC-030:** XSS attempts are prevented (input sanitization and output escaping).

### 21.4 Database

**AC-031:** All four tables (admins, students, subjects, marks) exist with correct schema.

**AC-032:** Foreign key constraints work correctly (student→marks, subject→marks).

**AC-033:** Unique constraints prevent duplicate entries (Roll Number, Subject Code, student-subject marks).

**AC-034:** Cascade delete works: deleting student also deletes their marks.

**AC-035:** Restrict delete works: cannot delete subject if marks exist.

### 21.5 UI/UX

**AC-036:** Application has consistent navigation across all pages.

**AC-037:** Active page is highlighted in navigation menu.

**AC-038:** Application is responsive and usable on desktop (1920×1080, 1366×768).

**AC-039:** Application is responsive and usable on tablet (768×1024).

**AC-040:** Application is functional on mobile (375×667) with acceptable UX.

**AC-041:** All tables are readable and usable (scrollable on mobile if needed).

**AC-042:** Forms are properly formatted with labels, placeholders, and validation.

**AC-043:** Color coding is consistent (Green=Pass, Red=Fail, Blue=Primary actions).

**AC-044:** Charts render correctly and are readable.

**AC-045:** Reports are printable with clean print CSS (no navigation/buttons in print).

### 21.6 Performance

**AC-046:** Dashboard loads within 3 seconds (acceptable for free tier).

**AC-047:** Page navigation responds within 2 seconds.

**AC-048:** Form submissions provide feedback within 2 seconds.

**AC-049:** Search/filter operations update within 500ms.

**AC-050:** Charts render within 2 seconds.

### 21.7 Deployment

**AC-051:** Application is successfully deployed on Render free tier.

**AC-052:** Database is successfully hosted on Supabase free tier.

**AC-053:** Application is accessible via public URL.

**AC-054:** All features work correctly in production environment.

**AC-055:** HTTPS is enforced (provided by Render).

**AC-056:** Environment variables are properly configured (no hardcoded secrets).

**AC-057:** Application handles cold start gracefully (Render free tier limitation).

### 21.8 Documentation

**AC-058:** README.md contains project description, tech stack, and setup instructions.

**AC-059:** Database schema is documented.

**AC-060:** Sample data is provided for testing.

**AC-061:** Admin test credentials are documented.

**AC-062:** Student test credentials (Roll No + DOB) are documented for demo.

### 21.9 Demo Readiness

**AC-063:** Complete demo can be performed in 5-10 minutes.

**AC-064:** All demo scenarios work without errors.

**AC-065:** Sample data demonstrates all grade types (A, B, C, D, F).

**AC-066:** Sample data includes pass and fail scenarios.

**AC-067:** Charts display meaningful data.

**AC-068:** At least one student has incomplete result for demonstration.

### 21.10 Code Quality

**AC-069:** Code follows consistent formatting and naming conventions.

**AC-070:** No critical bugs or errors in logs.

**AC-071:** No console errors in browser developer tools.

**AC-072:** No SQL errors or warnings in database logs.

**AC-073:** Code is reasonably modular and maintainable.

---

## 22. FINAL PROJECT SUMMARY

### A. Final Feature List

**Core Features:**
1. Admin Authentication & Authorization
2. Admin Dashboard with Metrics & Charts
3. Student Management (CRUD)
4. Subject Management (CRUD)
5. Marks Management (CRUD)
6. Automated Result Calculation
7. Student Result Lookup (Public)
8. Performance Analysis Dashboard
9. Report Generation (Individual, Class, Subject)
10. Search & Filter Functionality
11. Responsive Web Design
12. Print-Friendly Reports

### B. Final User-Role Matrix

| Role | Authentication | Can Create | Can Read | Can Update | Can Delete | Key Features |
|------|---------------|------------|----------|------------|------------|--------------|
| **Administrator** | Email + Password (Session-based) | Students, Subjects, Marks | All Data | Students, Subjects, Marks | Students, Subjects, Marks | Dashboard, Analytics, Reports |
| **Student** | Roll No + DOB (Stateless lookup) | None | Own Result Only | None | None | Result Lookup |

### C. Final Database Table List

| Table | Purpose | Key Columns | Constraints |
|-------|---------|-------------|-------------|
| `admins` | Admin authentication | username, email, password_hash | UNIQUE on username, email |
| `students` | Student master data | roll_number, name, dob, gender | UNIQUE on roll_number |
| `subjects` | Subject master data | subject_code, subject_name, max_marks | UNIQUE on subject_code |
| `marks` | Student marks records | student_id, subject_id, marks_obtained, is_absent | UNIQUE on (student_id, subject_id), FKs with CASCADE/RESTRICT |

### D. Final Technology Stack

**Backend:**
- Python 3.11
- Flask 3.0+
- psycopg2-binary (PostgreSQL driver)
- bcrypt (password hashing)
- python-dotenv (environment variables)
- gunicorn (production server)

**Frontend:**
- HTML5 (semantic markup)
- CSS3 (responsive design, flexbox/grid)
- Vanilla JavaScript (DOM manipulation, form validation)
- Chart.js 4.x (data visualization)

**Database:**
- Supabase PostgreSQL (free tier)

**Deployment:**
- Render (free tier for backend + frontend)
- GitHub (version control & auto-deploy)

### E. MVP Boundary

**MUST HAVE (Core MVP):**
- All authentication, CRUD operations, result calculation, charts, reports
- 20 essential features fully implemented

**SHOULD HAVE (Enhanced MVP):**
- Filters, print CSS, toast notifications, absent handling, weak/strong subject identification
- 10-15 additional features for better UX

**NICE TO HAVE (Future):**
- PDF export, CSV export, advanced analytics, dark mode
- Can be mentioned as future enhancements in viva

### F. Major Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Render Free Tier Cold Start** | 30-60 sec initial load delay | Wake service 5 mins before demo; have local backup |
| **Supabase Inactivity Pause** | Database unavailable after 1 week | Keep project active; resume before demo |
| **Internet Connection Failure** | Cannot access deployed app | Have local development server ready as backup |
| **Browser Compatibility Issues** | Features not working in some browsers | Test on Chrome, Firefox, Edge during development |
| **Data Loss During Development** | Lost sample data or code | Regular git commits; backup database export |

### G. Recommended Development Order

**Phase 1: Foundation (Week 1-2)**
1. Setup project structure (Flask app, folders, files)
2. Setup Supabase database and create tables
3. Implement admin authentication (login/logout)
4. Create base HTML template with navigation

**Phase 2: Core CRUD (Week 3-4)**
5. Implement student management (add, view, edit, delete)
6. Implement subject management (add, view, edit, delete)
7. Implement marks entry and management
8. Add form validations (frontend + backend)

**Phase 3: Business Logic (Week 5)**
9. Implement result calculation logic
10. Create results display page for admin
11. Implement student result lookup functionality
12. Test all calculation scenarios

**Phase 4: Analytics & Visualization (Week 6)**
13. Create admin dashboard with metrics
14. Implement Chart.js visualizations
15. Create performance analysis page
16. Implement report generation

**Phase 5: Polish & Features (Week 7)**
17. Add search and filter functionality
18. Implement responsive design (mobile/tablet)
19. Add print-friendly CSS for reports
20. Enhance UI/UX (colors, spacing, feedback)

**Phase 6: Testing & Deployment (Week 8)**
21. Create comprehensive sample data
22. Test all features thoroughly
23. Deploy to Render + Supabase
24. Perform end-to-end testing in production
25. Prepare demo script and practice

---

## 23. PRD APPROVAL CHECKLIST

### Document Completeness

- [x] Project overview with clear problem statement
- [x] User roles defined with permissions matrix
- [x] Core features enumerated (72 functional requirements)
- [x] Result calculation logic with formulas and examples
- [x] Complete functional requirements (FR-001 to FR-135)
- [x] Database schema with all 4 tables documented
- [x] Security requirements (50 security specifications)
- [x] UI/UX requirements (100 UI specifications)
- [x] Dashboard requirements with chart specifications
- [x] Search, filter, and sort requirements
- [x] Validation rules (55 validation specs)
- [x] Error handling (50 error scenarios)
- [x] Reporting & analytics with chart types
- [x] Non-functional requirements (70 NFRs)
- [x] Deployment requirements with tech stack
- [x] Testing requirements with test checklist
- [x] Demo/viva requirements with Q&A preparation
- [x] Sample data requirements with examples
- [x] Future enhancements list
- [x] MVP definition (MUST/SHOULD/NICE TO HAVE)
- [x] Acceptance criteria (73 criteria)
- [x] Final project summary

### Clarity & Implementation Readiness

- [x] All requirements are specific and testable
- [x] Technology stack is clearly defined
- [x] Database schema is complete and normalized
- [x] Security measures are comprehensive
- [x] UI mockup descriptions are detailed
- [x] Deployment process is documented
- [x] No ambiguous or vague requirements
- [x] All assumptions are documented
- [x] Edge cases are identified and handled
- [x] Sample data strategy is clear

### Project Feasibility

- [x] Scope is appropriate for diploma final-year project
- [x] Timeline is realistic (8 weeks recommended)
- [x] Technology choices are beginner-friendly
- [x] Deployment is achievable on free tier
- [x] Features are demonstrable in 5-10 minute viva
- [x] No unnecessary complexity or over-engineering
- [x] MVP is clearly separated from nice-to-haves

### Viva Preparation

- [x] Demo flow is clearly defined (12 stages)
- [x] Technical questions are anticipated with answers
- [x] Functional questions are covered
- [x] Confidence boosters are included
- [x] Demo preparation checklist provided
- [x] Backup plans for common issues documented

---

## END OF PRODUCT REQUIREMENTS DOCUMENT

**Document Status:** ✅ COMPLETE  
**Next Step:** Technical Requirements Document (TRD) & Implementation  
**Prepared By:** Product Requirements Team  
**Date:** September 1, 2026  

**This PRD is ready for:**
1. Technical team review and approval
2. TRD creation based on these requirements
3. Development phase initiation
4. Project implementation by AI coding agent

---
