"""Unit tests for marks validators (Phase 9)."""

import pytest

from utils.validators import validate_marks_obtained, validate_marks_data


class TestValidateMarksObtained:
    """Tests for validate_marks_obtained function."""

    def test_valid_marks_within_range(self):
        """Valid marks within 0 to max_marks should pass."""
        is_valid, error = validate_marks_obtained('50', 100, False)
        assert is_valid is True
        assert error is None

    def test_valid_marks_at_zero(self):
        """Zero marks should be valid."""
        is_valid, error = validate_marks_obtained('0', 100, False)
        assert is_valid is True
        assert error is None

    def test_valid_marks_at_max(self):
        """Marks equal to max_marks should be valid."""
        is_valid, error = validate_marks_obtained('100', 100, False)
        assert is_valid is True
        assert error is None

    def test_invalid_negative_marks(self):
        """Negative marks should fail."""
        is_valid, error = validate_marks_obtained('-5', 100, False)
        assert is_valid is False
        assert 'cannot be negative' in error

    def test_invalid_marks_exceeds_max(self):
        """Marks exceeding max_marks should fail."""
        is_valid, error = validate_marks_obtained('150', 100, False)
        assert is_valid is False
        assert 'cannot exceed' in error

    def test_invalid_empty_string(self):
        """Empty marks should fail."""
        is_valid, error = validate_marks_obtained('', 100, False)
        assert is_valid is False
        assert 'is required' in error

    def test_invalid_non_integer(self):
        """Non-integer marks should fail."""
        is_valid, error = validate_marks_obtained('abc', 100, False)
        assert is_valid is False
        assert 'must be a valid integer' in error

    def test_absent_student_must_have_zero_marks(self):
        """If absent is True, marks must be 0."""
        is_valid, error = validate_marks_obtained('50', 100, True)
        assert is_valid is False
        assert 'must be 0 for absent students' in error

    def test_absent_student_with_zero_marks(self):
        """If absent is True and marks is 0, should pass."""
        is_valid, error = validate_marks_obtained('0', 100, True)
        assert is_valid is True
        assert error is None


class TestValidateMarksData:
    """Tests for validate_marks_data function."""

    def test_valid_marks_data(self):
        """Valid marks data should pass."""
        data = {
            'marks_obtained': '75',
            'max_marks': 100,
            'is_absent': False
        }
        errors = validate_marks_data(data)
        assert errors == {}

    def test_invalid_negative_marks(self):
        """Negative marks should produce error."""
        data = {
            'marks_obtained': '-5',
            'max_marks': 100,
            'is_absent': False
        }
        errors = validate_marks_data(data)
        assert 'marks_obtained' in errors

    def test_invalid_exceeds_max(self):
        """Marks exceeding max should produce error."""
        data = {
            'marks_obtained': '150',
            'max_marks': 100,
            'is_absent': False
        }
        errors = validate_marks_data(data)
        assert 'marks_obtained' in errors

    def test_absent_with_nonzero_marks(self):
        """Absent with nonzero marks should produce error."""
        data = {
            'marks_obtained': '50',
            'max_marks': 100,
            'is_absent': True
        }
        errors = validate_marks_data(data)
        assert 'marks_obtained' in errors

    def test_absent_with_zero_marks(self):
        """Absent with zero marks should pass."""
        data = {
            'marks_obtained': '0',
            'max_marks': 100,
            'is_absent': True
        }
        errors = validate_marks_data(data)
        assert errors == {}