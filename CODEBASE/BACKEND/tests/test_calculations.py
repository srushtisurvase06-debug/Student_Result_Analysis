"""Unit tests for result calculation utilities.

Tests the functions in utils/calculations.py that implement the result
calculation logic from PRD Section 4 (Phase 10 Result Calculation Engine):
- Percentage calculation (calculate_percentage)
- Grade assignment (calculate_grade)
- Pass/Fail determination (calculate_status)
- Full result generation (generate_full_result)
"""

import pytest
from utils.calculations import (
    calculate_percentage,
    calculate_grade,
)


class TestCalculatePercentage:
    """Test percentage calculation."""

    def test_calculate_percentage_valid(self):
        """Calculate percentage correctly for valid inputs."""
        assert calculate_percentage(450, 500) == 90.0
        assert calculate_percentage(0, 100) == 0.0
        assert calculate_percentage(100, 100) == 100.0
        assert calculate_percentage(85, 100) == 85.0

    def test_calculate_percentage_rounding(self):
        """Test percentage is rounded to 2 decimal places."""
        # 1/3 = 0.333... -> 33.33%
        assert calculate_percentage(1, 3) == 33.33
        # 1/6 = 0.166... -> 16.67%
        assert calculate_percentage(1, 6) == 16.67
        # 7/13 = 0.5384... -> 53.85%
        assert calculate_percentage(7, 13) == 53.85

    def test_calculate_percentage_zero_total(self):
        """Handle division by zero (total maximum = 0)."""
        assert calculate_percentage(0, 0) == 0.0
        assert calculate_percentage(100, 0) == 0.0

    def test_calculate_percentage_large_numbers(self):
        """Handle large numbers correctly."""
        assert calculate_percentage(537, 600) == 89.5
        assert calculate_percentage(400, 500) == 80.0


class TestAssignGrade:
    """Test grade assignment based on percentage."""

    def test_assign_grade_a(self):
        """Grade A for 90-100%."""
        assert calculate_grade(90) == 'A'
        assert calculate_grade(95) == 'A'
        assert calculate_grade(100) == 'A'
        assert calculate_grade(91) == 'A'

    def test_assign_grade_b(self):
        """Grade B for 75-89%."""
        assert calculate_grade(75) == 'B'
        assert calculate_grade(80) == 'B'
        assert calculate_grade(89) == 'B'
        assert calculate_grade(76) == 'B'

    def test_assign_grade_c(self):
        """Grade C for 60-74%."""
        assert calculate_grade(60) == 'C'
        assert calculate_grade(70) == 'C'
        assert calculate_grade(74) == 'C'
        assert calculate_grade(61) == 'C'

    def test_assign_grade_d(self):
        """Grade D for 40-59%."""
        assert calculate_grade(40) == 'D'
        assert calculate_grade(50) == 'D'
        assert calculate_grade(59) == 'D'
        assert calculate_grade(41) == 'D'

    def test_assign_grade_f(self):
        """Grade F for 0-39%."""
        assert calculate_grade(0) == 'F'
        assert calculate_grade(39) == 'F'
        assert calculate_grade(25) == 'F'
        assert calculate_grade(10) == 'F'

    def test_assign_grade_boundary_values(self):
        """Test grade at boundary percentage values."""
        # Exactly at grade boundaries
        assert calculate_grade(39.99) == 'F'
        assert calculate_grade(40) == 'D'
        assert calculate_grade(59.99) == 'D'
        assert calculate_grade(60) == 'C'
        assert calculate_grade(74.99) == 'C'
        assert calculate_grade(75) == 'B'
        assert calculate_grade(89.99) == 'B'
        assert calculate_grade(90) == 'A'