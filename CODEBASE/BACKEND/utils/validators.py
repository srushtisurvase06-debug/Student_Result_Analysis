"""Student validation utilities.

All validation functions return a tuple (is_valid: bool, error_message: str | None).
"""

import re
from datetime import datetime


def validate_roll_number(roll_number: str) -> tuple[bool, str | None]:
    """Validate student roll number.
    
    Rules:
    - Required field
    - Alphanumeric only
    - Length 5-20 characters
    - Pattern: ^[A-Z0-9-]+$
    
    Returns:
        (True, None) if valid
        (False, error_message) if invalid
    """
    if not roll_number or not roll_number.strip():
        return False, 'Roll number is required'
    
    roll_number = roll_number.strip()
    
    if len(roll_number) < 5 or len(roll_number) > 20:
        return False, 'Roll number must be 5-20 characters'
    
    if not re.match(r'^[A-Z0-9-]+$', roll_number):
        return False, 'Roll number must be alphanumeric (A-Z, 0-9, hyphens only)'
    
    return True, None


def validate_name(name: str) -> tuple[bool, str | None]:
    """Validate student name.
    
    Rules:
    - Required field
    - Length 2-100 characters
    - Letters, spaces, apostrophes, hyphens only
    
    Returns:
        (True, None) if valid
        (False, error_message) if invalid
    """
    if not name or not name.strip():
        return False, 'Name is required'
    
    name = name.strip()
    
    if len(name) < 2 or len(name) > 100:
        return False, 'Name must be 2-100 characters'
    
    if not re.match(r"^[a-zA-Z\s.'-]+$", name):
        return False, 'Name must contain only letters, spaces, apostrophes, and hyphens'
    
    return True, None


def validate_email(email: str) -> tuple[bool, str | None]:
    """Validate student email (optional field).
    
    Rules:
    - If provided, must be valid email format
    - Pattern: r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\. [a-zA-Z]{2,}$'
    
    Returns:
        (True, None) if valid or empty
        (False, error_message) if invalid
    """
    if not email or not email.strip():
        # Email is optional
        return True, None
    
    email = email.strip()
    
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return False, 'Invalid email format'
    
    return True, None


def validate_date_of_birth(dob: str) -> tuple[bool, str | None]:
    """Validate student date of birth.
    
    Rules:
    - Required field
    - Format: YYYY-MM-DD
    - Must be in the past
    - Age between 5 and 100 years
    
    Returns:
        (True, None) if valid
        (False, error_message) if invalid
    """
    if not dob or not dob.strip():
        return False, 'Date of birth is required'
    
    try:
        dob_date = datetime.strptime(dob.strip(), '%Y-%m-%d').date()
    except ValueError:
        return False, 'Invalid date format (use YYYY-MM-DD)'
    
    today = datetime.now().date()
    
    if dob_date >= today:
        return False, 'Date of birth must be in the past'
    
    # Calculate age
    age = today.year - dob_date.year
    if (today.month, today.day) < (dob_date.month, dob_date.day):
        age -= 1
    
    if age < 5 or age > 100:
        return False, 'Age must be between 5 and 100 years'
    
    return True, None


def validate_gender(gender: str) -> tuple[bool, str | None]:
    """Validate student gender.
    
    Rules:
    - Required field
    - Must be one of: 'Male', 'Female', 'Other'
    
    Returns:
        (True, None) if valid
        (False, error_message) if invalid
    """
    if not gender or not gender.strip():
        return False, 'Gender is required'
    
    gender = gender.strip()
    
    if gender not in ('Male', 'Female', 'Other'):
        return False, 'Gender must be Male, Female, or Other'
    
    return True, None


def validate_contact_number(contact: str) -> tuple[bool, str | None]:
    """Validate student contact number (optional field).
    
    Rules:
    - If provided, must be 10-15 digits (can include spaces, dashes, plus)
    - Pattern: r'^[+\\s0-9]{10,15}$'
    
    Returns:
        (True, None) if valid or empty
        (False, error_message) if invalid
    """
    if not contact or not contact.strip():
        # Contact is optional
        return True, None
    
    contact = contact.strip()
    
    if not re.match(r'^[\+\s0-9]{10,15}$', contact):
        return False, 'Contact number must be 10-15 digits (spaces, dashes, + allowed)'
    
    # Check that at least 10 digits exist
    digit_count = sum(c.isdigit() for c in contact)
    if digit_count < 10:
        return False, 'Contact number must contain at least 10 digits'
    
    return True, None


def validate_student_data(data: dict) -> dict:
    """Validate all student fields at once.
    
    Args:
        data: Dictionary with student fields
        
    Returns:
        Dictionary of field_name -> error_message for all validation errors
    """
    errors = {}
    
    is_valid, error = validate_roll_number(data.get('roll_number', ''))
    if not is_valid:
        errors['roll_number'] = error
    
    is_valid, error = validate_name(data.get('name', ''))
    if not is_valid:
        errors['name'] = error
    
    is_valid, error = validate_email(data.get('email', ''))
    if not is_valid:
        errors['email'] = error
    
    is_valid, error = validate_date_of_birth(data.get('date_of_birth', ''))
    if not is_valid:
        errors['date_of_birth'] = error
    
    is_valid, error = validate_gender(data.get('gender', ''))
    if not is_valid:
        errors['gender'] = error
    
    is_valid, error = validate_contact_number(data.get('contact_number', ''))
    if not is_valid:
        errors['contact_number'] = error
    
    return errors


# ============================================================================
# Subject Validators (Phase 8)
# ============================================================================


def validate_subject_code(subject_code: str) -> tuple[bool, str | None]:
    """Validate subject code.
    
    Rules (TRD TR-VAL-011):
    - Required field
    - Uppercase letters and digits only
    - Length 3-10 characters
    - Pattern: ^[A-Z0-9]+$
    
    Returns:
        (True, None) if valid
        (False, error_message) if invalid
    """
    if not subject_code or not subject_code.strip():
        return False, 'Subject code is required'
    
    subject_code = subject_code.strip()
    
    if len(subject_code) < 3 or len(subject_code) > 10:
        return False, 'Subject code must be 3-10 characters'
    
    if not re.match(r'^[A-Z0-9]+$', subject_code):
        return False, 'Subject code must be uppercase letters and digits only'
    
    return True, None


def validate_subject_name(subject_name: str) -> tuple[bool, str | None]:
    """Validate subject name.
    
    Rules (TRD TR-VAL-012):
    - Required field
    - Length 3-100 characters
    - Letters, digits, spaces, and ampersand allowed
    - Pattern: r'^[a-zA-Z0-9\\s&]+$'
    
    Returns:
        (True, None) if valid
        (False, error_message) if invalid
    """
    if not subject_name or not subject_name.strip():
        return False, 'Subject name is required'
    
    subject_name = subject_name.strip()
    
    if len(subject_name) < 3 or len(subject_name) > 100:
        return False, 'Subject name must be 3-100 characters'
    
    if not re.match(r'^[a-zA-Z0-9\s&]+$', subject_name):
        return False, 'Subject name must contain only letters, digits, spaces, and ampersand'
    
    return True, None


def validate_max_marks(max_marks: str) -> tuple[bool, str | None]:
    """Validate maximum marks.
    
    Rules (PRD VAL-027, VAL-028; TRD TR-VAL-013):
    - Required field
    - Must be a valid integer
    - Range: 1 to 500
    
    Returns:
        (True, None) if valid
        (False, error_message) if invalid
    """
    if not max_marks or not str(max_marks).strip():
        return False, 'Maximum marks is required'
    
    max_marks_str = str(max_marks).strip()
    
    try:
        max_marks_int = int(max_marks_str)
    except ValueError:
        return False, 'Maximum marks must be a valid integer'
    
    if max_marks_int < 1:
        return False, 'Maximum marks must be at least 1'
    
    if max_marks_int > 500:
        return False, 'Maximum marks cannot exceed 500'
    
    return True, None


def validate_subject_data(data: dict) -> dict:
    """Validate all subject fields at once.
    
    Args:
        data: Dictionary with subject fields
        
    Returns:
        Dictionary of field_name -> error_message for all validation errors
    """
    errors = {}
    
    is_valid, error = validate_subject_code(data.get('subject_code', ''))
    if not is_valid:
        errors['subject_code'] = error
    
    is_valid, error = validate_subject_name(data.get('subject_name', ''))
    if not is_valid:
        errors['subject_name'] = error
    
    is_valid, error = validate_max_marks(data.get('max_marks', ''))
    if not is_valid:
        errors['max_marks'] = error
    
    return errors


# ============================================================================
# Marks Validators (Phase 9)
# ============================================================================


def validate_marks_obtained(marks_obtained: str, max_marks: int, is_absent: bool) -> tuple[bool, str | None]:
    """Validate marks obtained value.
    
    Rules (TRD TR-MARKS-VAL-001):
    - Must be a valid integer
    - Cannot be negative
    - Cannot exceed subject's max_marks
    - If absent, must be 0
    
    Args:
        marks_obtained: String value from form
        max_marks: Maximum marks for the subject
        is_absent: Whether student is marked absent
        
    Returns:
        (True, None) if valid
        (False, error_message) if invalid
    """
    if not marks_obtained or not str(marks_obtained).strip():
        return False, 'Marks obtained is required'
    
    try:
        marks_int = int(str(marks_obtained).strip())
    except ValueError:
        return False, 'Marks obtained must be a valid integer'
    
    if marks_int < 0:
        return False, 'Marks cannot be negative'
    
    if marks_int > max_marks:
        return False, f'Marks cannot exceed {max_marks}'
    
    if is_absent and marks_int != 0:
        return False, 'Marks must be 0 for absent students'
    
    return True, None


def validate_marks_data(data: dict) -> dict:
    """Validate all marks fields at once.
    
    Args:
        data: Dictionary with marks fields including student_id, subject_id,
              marks_obtained, is_absent, and max_marks
            
    Returns:
        Dictionary of field_name -> error_message for all validation errors
    """
    errors = {}
    
    # Validate marks_obtained
    marks_obtained = str(data.get('marks_obtained', '')).strip()
    max_marks = data.get('max_marks', 100)
    is_absent = data.get('is_absent', False)
    
    is_valid, error = validate_marks_obtained(marks_obtained, max_marks, is_absent)
    if not is_valid:
        errors['marks_obtained'] = error
    
    return errors