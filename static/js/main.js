// Main JavaScript for College Management System

// Confirm delete/destructive actions
function confirmAction(message) {
    return confirm(message || 'Are you sure you want to perform this action?');
}

// Show loading spinner
function showLoading() {
    let overlay = document.querySelector('.spinner-overlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.className = 'spinner-overlay';
        overlay.innerHTML = '<div class="spinner-border text-light" role="status"><span class="visually-hidden">Loading...</span></div>';
        document.body.appendChild(overlay);
    }
    overlay.classList.add('show');
}

// Hide loading spinner
function hideLoading() {
    const overlay = document.querySelector('.spinner-overlay');
    if (overlay) {
        overlay.classList.remove('show');
    }
}

// Show toast notification
function showToast(message, type = 'info') {
    const toastContainer = document.getElementById('toast-container') || createToastContainer();

    const toastEl = document.createElement('div');
    toastEl.className = `toast align-items-center text-white bg-${type} border-0`;
    toastEl.setAttribute('role', 'alert');
    toastEl.setAttribute('aria-live', 'assertive');
    toastEl.setAttribute('aria-atomic', 'true');

    toastEl.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;

    toastContainer.appendChild(toastEl);

    const toast = new bootstrap.Toast(toastEl, {
        autohide: true,
        delay: 5000
    });
    toast.show();

    toastEl.addEventListener('hidden.bs.toast', function() {
        toastEl.remove();
    });
}

// Create toast container if it doesn't exist
function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
    container.style.zIndex = '11';
    document.body.appendChild(container);
    return container;
}

// Form validation
document.addEventListener('DOMContentLoaded', function() {
    // Add Bootstrap validation to all forms
    const forms = document.querySelectorAll('.needs-validation');

    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Auto-submit form loading indicator
    const submitButtons = document.querySelectorAll('button[type="submit"]');
    submitButtons.forEach(button => {
        button.addEventListener('click', function() {
            const form = this.closest('form');
            if (form && form.checkValidity()) {
                setTimeout(() => {
                    this.disabled = true;
                    this.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Loading...';
                }, 100);
            }
        });
    });
});

// Smooth scroll to top
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// Show/hide password toggle
function togglePasswordVisibility(inputId) {
    const input = document.getElementById(inputId);
    if (input.type === 'password') {
        input.type = 'text';
        return 'Hide';
    } else {
        input.type = 'password';
        return 'Show';
    }
}

// Character counter for text fields
function updateCharacterCount(textareaId, counterId, maxLength) {
    const textarea = document.getElementById(textareaId);
    const counter = document.getElementById(counterId);

    if (textarea && counter) {
        const remaining = maxLength - textarea.value.length;
        counter.textContent = `${remaining} characters remaining`;

        if (remaining < 0) {
            counter.classList.add('text-danger');
        } else {
            counter.classList.remove('text-danger');
        }
    }
}

// Filter table rows
function filterTable(inputId, tableId) {
    const input = document.getElementById(inputId);
    const filter = input.value.toUpperCase();
    const table = document.getElementById(tableId);
    const tr = table.getElementsByTagName('tr');

    for (let i = 1; i < tr.length; i++) {
        const row = tr[i];
        let txtValue = row.textContent || row.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    }
}

// Export table to CSV
function exportTableToCSV(tableId, filename) {
    const table = document.getElementById(tableId);
    let csv = [];
    const rows = table.querySelectorAll('tr');

    for (const row of rows) {
        const cols = row.querySelectorAll('td, th');
        const csvRow = [];
        for (const col of cols) {
            csvRow.push(col.innerText);
        }
        csv.push(csvRow.join(','));
    }

    downloadCSV(csv.join('\n'), filename);
}

function downloadCSV(csv, filename) {
    const csvFile = new Blob([csv], { type: 'text/csv' });
    const downloadLink = document.createElement('a');
    downloadLink.download = filename;
    downloadLink.href = window.URL.createObjectURL(csvFile);
    downloadLink.style.display = 'none';
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
}

// Print page
function printPage() {
    window.print();
}

// Select all checkboxes
function selectAll(source, checkboxClass) {
    const checkboxes = document.querySelectorAll(`.${checkboxClass}`);
    checkboxes.forEach(checkbox => {
        checkbox.checked = source.checked;
    });
}

// Mark all as present (for attendance marking)
function markAllPresent() {
    const presentRadios = document.querySelectorAll('input[type="radio"][value="Present"]');
    presentRadios.forEach(radio => {
        radio.checked = true;
    });
}

// Mark all as absent (for attendance marking)
function markAllAbsent() {
    const absentRadios = document.querySelectorAll('input[type="radio"][value="Absent"]');
    absentRadios.forEach(radio => {
        radio.checked = true;
    });
}

// Real-time clock
function updateClock() {
    const now = new Date();
    const timeString = now.toLocaleTimeString();
    const dateString = now.toLocaleDateString();

    const clockElement = document.getElementById('live-clock');
    if (clockElement) {
        clockElement.innerHTML = `${dateString} ${timeString}`;
    }
}

// Update clock every second
setInterval(updateClock, 1000);

// Auto-refresh dashboard (every 30 seconds)
function enableAutoRefresh(seconds = 30) {
    if (document.getElementById('auto-refresh-toggle')) {
        const toggle = document.getElementById('auto-refresh-toggle');
        if (toggle.checked) {
            setTimeout(() => {
                location.reload();
            }, seconds * 1000);
        }
    }
}

// AJAX form submission
function submitFormAjax(formId, successCallback, errorCallback) {
    const form = document.getElementById(formId);
    if (!form) return;

    form.addEventListener('submit', function(e) {
        e.preventDefault();

        const formData = new FormData(form);
        const url = form.action;

        showLoading();

        fetch(url, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            hideLoading();
            if (data.success) {
                if (successCallback) successCallback(data);
                showToast(data.message || 'Success!', 'success');
            } else {
                if (errorCallback) errorCallback(data);
                showToast(data.message || 'Error occurred', 'danger');
            }
        })
        .catch(error => {
            hideLoading();
            console.error('Error:', error);
            showToast('An error occurred', 'danger');
            if (errorCallback) errorCallback(error);
        });
    });
}
