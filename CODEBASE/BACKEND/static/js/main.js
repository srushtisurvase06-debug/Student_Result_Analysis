/**
 * main.js - Phase 5 JavaScript utilities
 *
 * Scope: Common validation helpers, date formatting, and UI utilities.
 * Component-specific logic will be in feature-level files in later phases.
 */

// ----------------------------------------------------------------------- form --

/**
 * Validate email format using regex.
 * @param {string} email - Email address to validate
 * @returns {boolean} true if valid format, false otherwise
 */
function validateEmail(email) {
    const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return emailPattern.test(email);
}

/**
 * Validate date of birth (must be in the past, reasonable range).
 * @param {string} dob - Date string in YYYY-MM-DD format
 * @returns {object} { valid: boolean, error: string | null }
 */
function validateDateOfBirth(dob) {
    if (!dob) {
        return { valid: false, error: 'Date of birth is required' };
    }

    const dobDate = new Date(dob);
    const today = new Date();

    // Minimum age: 5 years old
    const minDate = new Date(today.getFullYear() - 100, today.getMonth(), today.getDate());
    const maxDate = new Date(today.getFullYear() - 5, today.getMonth(), today.getDate());

    if (dobDate < minDate || dobDate > maxDate) {
        return { valid: false, error: 'Invalid age (must be 5-100 years old)' };
    }

    if (dobDate > today) {
        return { valid: false, error: 'Date of birth cannot be in the future' };
    }

    return { valid: true, error: null };
}

/**
 * Validate marks (must be numeric, within range).
 * @param {string|number} marks - Marks value
 * @param {number} maxMarks - Maximum possible marks
 * @returns {object} { valid: boolean, error: string | null }
 */
function validateMarks(marks, maxMarks) {
    const marksNum = parseFloat(marks);

    if (isNaN(marksNum)) {
        return { valid: false, error: 'Marks must be a valid number' };
    }

    if (marksNum < 0) {
        return { valid: false, error: 'Marks cannot be negative' };
    }

    if (marksNum > maxMarks) {
        return { valid: false, error: `Marks cannot exceed ${maxMarks}` };
    }

    return { valid: true, error: null };
}

/**
 * Format date to human-readable string (DD/MM/YYYY).
 * @param {string|Date} date - Date to format
 * @returns {string} Formatted date string
 */
function formatDate(date) {
    if (!date) return '';

    const dateObj = date instanceof Date ? date : new Date(date);
    const day = String(dateObj.getDate()).padStart(2, '0');
    const month = String(dateObj.getMonth() + 1).padStart(2, '0');
    const year = dateObj.getFullYear();

    return `${day}/${month}/${year}`;
}

/**
 * Show toast notification.
 * @param {string} message - Notification message
 * @param {string} type - 'success', 'error', 'info', or 'warning'
 */
function showToast(message, type = 'info') {
    // Toast implementation placeholder for Phase 5
    // Full toast system will be implemented in Phase 20 (UI/UX polish)
    console.log(`[${type.toUpperCase()}] ${message}`);
}

/**
 * Confirm delete action.
 * @param {string} message - Custom confirmation message
 * @returns {boolean} true if confirmed, false if cancelled
 */
function confirmDelete(message = 'Are you sure you want to delete this item?') {
    return window.confirm(message);
}

// ------------------------------------------------------------------------ search --

/**
 * Filter table rows based on search term.
 * @param {string} searchTerm - Search term to match
 * @param {string} tableId - Table element ID
 * @param {number} columnIndex - Column index to search (0-based)
 */
function filterTable(searchTerm, tableId, columnIndex) {
    const table = document.getElementById(tableId);
    if (!table) return;

    const rows = table.getElementsByTagName('tr');
    const term = searchTerm.toLowerCase().trim();

    for (let i = 1; i < rows.length; i++) {
        const cell = rows[i].getElementsByTagName('td')[columnIndex];
        if (cell) {
            const text = cell.textContent.toLowerCase();
            if (text.includes(term)) {
                rows[i].style.display = '';
            } else {
                rows[i].style.display = 'none';
            }
        }
    }
}

// ----------------------------------------------------------------- date utils --

/**
 * Get today's date in YYYY-MM-DD format.
 * @returns {string} Today's date as string
 */
function getTodayDate() {
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const day = String(today.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

// ----------------------------------------------------------------- event handlers --

/**
 * Debounce function to limit rapid firing of events.
 * @param {Function} func - Function to debounce
 * @param {number} wait - Wait time in milliseconds
 * @returns {Function} Debounced function
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// ----------------------------------------------------------------- initialization --

/**
 * Initialize all Phase 5 utilities on DOM ready.
 */
function initPhase5() {
    console.log('Phase 5 utilities initialized');

    // Add any initialization logic here
    // For now, utilities are available for import by feature modules
}

// Export for use in other modules (if using ES6 modules later)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        validateEmail,
        validateDateOfBirth,
        validateMarks,
        formatDate,
        showToast,
        confirmDelete,
        filterTable,
        getTodayDate,
        debounce
    };
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initPhase5);
} else {
    initPhase5();
}
