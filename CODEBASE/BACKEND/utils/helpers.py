from datetime import datetime


def format_date(date_obj):
    """Format date object to DD/MM/YYYY string"""
    if date_obj:
        return date_obj.strftime('%d/%m/%Y')
    return ''


def format_datetime(dt_obj):
    """Format datetime to DD/MM/YYYY HH:MM"""
    if dt_obj:
        return dt_obj.strftime('%d/%m/%Y %H:%M')
    return ''


def get_current_datetime():
    """Get current datetime object"""
    return datetime.now()


def get_current_date():
    """Get current date object"""
    return datetime.now().date()
