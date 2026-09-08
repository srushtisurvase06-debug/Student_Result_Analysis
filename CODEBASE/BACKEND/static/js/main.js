/**
 * main.js - Phase 5 JavaScript utilities + Phase 6 Dashboard charts
 *
 * Scope:
 * - Phase 5: hamburger/mobile navigation toggle, flash-message auto-dismiss (~5 seconds)
 * - Phase 6: Dashboard chart initialization via initDashboardCharts()
 */

// ------------------------------------------------------------------ flash message --

/**
 * Auto-dismiss flash messages after 5 seconds (TR-FE-007).
 * Removes .alert elements from the DOM after the timeout.
 */
function autoDismissFlashMessages() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.style.transition = 'opacity 0.5s ease';
            alert.style.opacity = '0';
            setTimeout(function() {
                alert.parentNode.removeChild(alert);
            }, 500);
        }, 5000);
    });
}

// ------------------------------------------------------------------ mobile nav --

/**
 * Toggle mobile navigation menu visibility.
 * Hamburger icon triggers menu expand/collapse on mobile.
 */
function initMobileNavigation() {
    var navbar = document.querySelector('.navbar');
    if (!navbar) return;

    var menuButton = document.createElement('button');
    menuButton.className = 'navbar__menu-button';
    menuButton.setAttribute('aria-label', 'Toggle navigation menu');
    menuButton.setAttribute('aria-expanded', 'false');
    menuButton.innerHTML = '<span class="navbar__hamburger"></span>';

    var menu = navbar.querySelector('.navbar__menu');
    if (!menu) return;

    menuButton.addEventListener('click', function() {
        var expanded = menuButton.getAttribute('aria-expanded') === 'true';
        menuButton.setAttribute('aria-expanded', !expanded);
        menu.classList.toggle('navbar__menu--open');
    });

    navbar.insertBefore(menuButton, menu);

    // Close menu when clicking outside on mobile
    document.addEventListener('click', function(event) {
        var isClickInside = navbar.contains(event.target);
        var isMenuOpen = menuButton.getAttribute('aria-expanded') === 'true';

        if (!isClickInside && isMenuOpen) {
            menuButton.setAttribute('aria-expanded', 'false');
            menu.classList.remove('navbar__menu--open');
        }
    });
}

// -------------------------------------------------------------------- charts --

/**
 * Initialize Chart.js charts for dashboard (Phase 6).
 * Called from dashboard/index.html template after Chart.js loads.
 */
function initDashboardCharts() {
    console.log('Dashboard charts initialized');

    // Grade distribution chart
    var gradeCtx = document.getElementById('gradeChart');
    if (gradeCtx) {
        new Chart(gradeCtx.getContext('2d'), {
            type: 'bar',
            data: {
                labels: ['A', 'B', 'C', 'D', 'F'],
                datasets: [{
                    label: 'Number of Students',
                    data: gradeChartConfig.data,
                    backgroundColor: gradeChartConfig.colors
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { display: false } },
                scales: {
                    y: { beginAtZero: true, ticks: { stepSize: 1, precision: 0 } }
                }
            }
        });
    }

    // Pass/Fail pie chart
    var passFailCtx = document.getElementById('passFailChart');
    if (passFailCtx) {
        new Chart(passFailCtx.getContext('2d'), {
            type: 'pie',
            data: {
                labels: ['Pass', 'Fail'],
                datasets: [{
                    data: [passFailChartConfig.pass, passFailChartConfig.fail],
                    backgroundColor: ['#16a34a', '#dc2626']
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { position: 'bottom' } }
            }
        });
    }
}

// -------------------------------------------------------------------- search --

/**
 * Initialize search functionality with real-time filtering.
 */
function initSearch() {
    const searchInputs = document.querySelectorAll('.search-bar__input');
    
    searchInputs.forEach(function(input) {
        const searchButton = input.nextElementSibling;
        
        // Handle search button click
        if (searchButton && searchButton.classList.contains('search-bar__btn')) {
            searchButton.addEventListener('click', function(e) {
                e.preventDefault();
                performSearch(input);
            });
        }
        
        // Handle Enter key in search input
        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                performSearch(input);
            }
        });
        
        // Real-time search as user types (with debounce)
        let searchTimeout;
        input.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(function() {
                performSearch(input);
            }, 300); // Wait 300ms after user stops typing
        });
    });
}

/**
 * Perform search by filtering table rows.
 */
function performSearch(searchInput) {
    const searchTerm = searchInput.value.toLowerCase().trim();
    const table = searchInput.closest('.page-content').querySelector('.data-table');
    
    if (!table) return;
    
    const rows = table.querySelectorAll('tbody .data-table__row');
    let visibleCount = 0;
    
    rows.forEach(function(row) {
        const text = row.textContent.toLowerCase();
        
        if (text.includes(searchTerm)) {
            row.style.display = '';
            visibleCount++;
        } else {
            row.style.display = 'none';
        }
    });
    
    // Show/hide empty state
    const tbody = table.querySelector('tbody');
    let emptyRow = tbody.querySelector('.empty-state-row');
    
    if (visibleCount === 0 && searchTerm !== '') {
        if (!emptyRow) {
            emptyRow = document.createElement('tr');
            emptyRow.className = 'empty-state-row';
            const colspan = table.querySelectorAll('thead th').length;
            emptyRow.innerHTML = '<td class="data-table__cell" colspan="' + colspan + '"><div class="empty-state"><p>No results found for "' + searchInput.value + '"</p></div></td>';
            tbody.appendChild(emptyRow);
        }
    } else if (emptyRow) {
        emptyRow.remove();
    }
}

// ------------------------------------------------------------------ delete confirmation --

/**
 * Initialize delete button confirmation dialogs.
 */
function initDeleteButtons() {
    const deleteButtons = document.querySelectorAll('[data-delete-url]');
    
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            const deleteUrl = button.getAttribute('data-delete-url');
            const deleteName = button.getAttribute('data-delete-name');
            
            const confirmMessage = deleteName 
                ? 'Are you sure you want to delete "' + deleteName + '"? This action cannot be undone.'
                : 'Are you sure you want to delete this item? This action cannot be undone.';
            
            if (confirm(confirmMessage)) {
                // Create and submit a form for DELETE request
                const form = document.createElement('form');
                form.method = 'POST';
                form.action = deleteUrl;
                
                // Add CSRF token if available
                const csrfToken = document.querySelector('input[name="csrf_token"]');
                if (csrfToken) {
                    const tokenInput = document.createElement('input');
                    tokenInput.type = 'hidden';
                    tokenInput.name = 'csrf_token';
                    tokenInput.value = csrfToken.value;
                    form.appendChild(tokenInput);
                }
                
                document.body.appendChild(form);
                form.submit();
            }
        });
    });
}

// ----------------------------------------------------------------- initialization --

/**
 * Initialize all Phase 5 utilities on DOM ready.
 */
function initPhase5() {
    console.log('Phase 5 utilities initialized');

    // Auto-dismiss flash messages after 5 seconds
    autoDismissFlashMessages();

    // Initialize mobile navigation toggle
    initMobileNavigation();
    
    // Initialize search functionality
    initSearch();
    
    // Initialize delete button confirmations
    initDeleteButtons();
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initPhase5);
} else {
    initPhase5();
}
