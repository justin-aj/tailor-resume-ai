// JavaScript for Resume Tailor AI

// Global variables
let validationTimeout;

// DOM Ready
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips if Bootstrap is available
    if (typeof bootstrap !== 'undefined') {
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
    
    // Add real-time character counting for LaTeX textarea
    const latexTextarea = document.getElementById('latex_resume');
    if (latexTextarea) {
        setupRealTimeValidation(latexTextarea);
    }
    
    // Setup update buttons
    setupUpdateButtons();
});

// Setup update buttons functionality
function setupUpdateButtons() {
    const updateLatexBtn = document.getElementById('updateLatexBtn');
    const updateResumeBtn = document.getElementById('updateResumeBtn');
    const saveLatexBtn = document.getElementById('saveLatexBtn');
    const saveResumeBtn = document.getElementById('saveResumeBtn');
    
    if (updateLatexBtn) {
        updateLatexBtn.addEventListener('click', function() {
            updateFieldFromFile('latex_resume', '/update-latex-resume', this);
        });
    }
    
    if (updateResumeBtn) {
        updateResumeBtn.addEventListener('click', function() {
            updateFieldFromFile('additional_info', '/update-resume-txt', this);
        });
    }
    
    if (saveLatexBtn) {
        saveLatexBtn.addEventListener('click', function() {
            saveFieldToFile('latex_resume', '/save-latex-resume', this, 'data_science_resume.tex');
        });
    }
    
    if (saveResumeBtn) {
        saveResumeBtn.addEventListener('click', function() {
            saveFieldToFile('additional_info', '/save-resume-txt', this, 'resume.txt');
        });
    }
}

// Update field content from file
function updateFieldFromFile(fieldId, endpoint, buttonElement) {
    const field = document.getElementById(fieldId);
    if (!field) return;
    
    // Show loading state
    const originalText = buttonElement.innerHTML;
    buttonElement.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Loading...';
    buttonElement.disabled = true;
    
    fetch(endpoint)
        .then(response => response.json())
        .then(data => {
            field.value = data.content;
            // Update character count if it's the LaTeX field
            if (fieldId === 'latex_resume') {
                updateCharacterCount(field);
            }
            showUpdateFeedback(buttonElement, true, 'Loaded!');
        })
        .catch(error => {
            console.error('Update error:', error);
            showUpdateFeedback(buttonElement, false, 'Load Failed');
        })
        .finally(() => {
            buttonElement.innerHTML = originalText;
            buttonElement.disabled = false;
        });
}

// Save field content to file
function saveFieldToFile(fieldId, endpoint, buttonElement, fileName) {
    const field = document.getElementById(fieldId);
    if (!field) return;
    
    const content = field.value;
    if (!content.trim()) {
        showUpdateFeedback(buttonElement, false, 'Empty Content');
        return;
    }
    
    // Show loading state
    const originalText = buttonElement.innerHTML;
    buttonElement.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Saving...';
    buttonElement.disabled = true;
    
    fetch(endpoint, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ content: content })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showUpdateFeedback(buttonElement, true, 'Saved!');
                if (typeof showToast !== 'undefined') {
                    showToast(`Content saved to ${fileName}`, 'success');
                }
            } else {
                showUpdateFeedback(buttonElement, false, 'Save Failed');
                if (typeof showToast !== 'undefined') {
                    showToast(`Failed to save: ${data.message}`, 'danger');
                }
            }
        })
        .catch(error => {
            console.error('Save error:', error);
            showUpdateFeedback(buttonElement, false, 'Save Failed');
            if (typeof showToast !== 'undefined') {
                showToast('Network error while saving', 'danger');
            }
        })
        .finally(() => {
            buttonElement.innerHTML = originalText;
            buttonElement.disabled = false;
        });
}

// Show update feedback
function showUpdateFeedback(button, success, customMessage = null) {
    const originalText = button.innerHTML;
    const originalClass = button.className;
    
    let message, newClass;
    if (success) {
        message = customMessage || 'Updated!';
        newClass = originalClass.replace('btn-outline-secondary', 'btn-success').replace('btn-outline-primary', 'btn-success');
    } else {
        message = customMessage || 'Failed';
        newClass = originalClass.replace('btn-outline-secondary', 'btn-danger').replace('btn-outline-primary', 'btn-danger');
    }
    
    button.innerHTML = `<i class="fas fa-${success ? 'check' : 'times'} me-1"></i>${message}`;
    button.className = newClass;
    
    setTimeout(() => {
        button.innerHTML = originalText;
        button.className = originalClass;
    }, 2000);
}

// Real-time validation for LaTeX input
function setupRealTimeValidation(textarea) {
    // Create character counter display
    const counterDiv = document.createElement('div');
    counterDiv.className = 'form-text mt-1';
    counterDiv.id = 'characterCounter';
    textarea.parentNode.insertBefore(counterDiv, textarea.nextSibling);
    
    // Add input listener
    textarea.addEventListener('input', function() {
        updateCharacterCount(this);
        
        // Debounced validation
        clearTimeout(validationTimeout);
        validationTimeout = setTimeout(() => {
            validateLatexRealTime(this.value);
        }, 1000);
    });
    
    // Initial count
    updateCharacterCount(textarea);
}

// Update character count display
function updateCharacterCount(textarea) {
    const content = textarea.value;
    const lines = content.split('\n');
    const totalLines = lines.length;
    const totalChars = content.length;
    
    // Check for long lines
    const longLines = lines.filter(line => line.length > 95).length;
    
    const counter = document.getElementById('characterCounter');
    if (counter) {
        counter.innerHTML = `
            <span class="badge bg-secondary">Lines: ${totalLines}</span>
            <span class="badge bg-secondary">Characters: ${totalChars}</span>
            ${longLines > 0 ? `<span class="badge bg-warning">Long lines: ${longLines}</span>` : ''}
        `;
    }
}

// Real-time LaTeX validation
function validateLatexRealTime(content) {
    if (!content.trim()) return;
    
    fetch('/validate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({latex_content: content})
    })
    .then(response => response.json())
    .then(data => {
        showValidationResults(data, 'validationResults');
    })
    .catch(error => {
        console.error('Validation error:', error);
    });
}

// Manual validation trigger
function validateLatex() {
    const textarea = document.getElementById('latex_resume');
    const btn = document.getElementById('validateBtn');
    const originalText = btn.innerHTML;
    
    if (!textarea.value.trim()) {
        showValidationResults({
            success: false,
            errors: ['Please enter LaTeX content to validate']
        }, 'validationResults');
        return;
    }
    
    // Show loading state
    btn.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Validating...';
    btn.disabled = true;
    
    fetch('/validate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({latex_content: textarea.value})
    })
    .then(response => response.json())
    .then(data => {
        showValidationResults(data, 'validationResults');
    })
    .catch(error => {
        showValidationResults({
            success: false,
            errors: [`Validation request failed: ${error.message}`]
        }, 'validationResults');
    })
    .finally(() => {
        btn.innerHTML = originalText;
        btn.disabled = false;
    });
}

// Show validation results
function showValidationResults(data, containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    if (data.success) {
        container.innerHTML = `
            <div class="alert alert-success alert-sm">
                <i class="fas fa-check-circle me-2"></i>
                <strong>Validation Passed!</strong> 
                Your LaTeX code meets all requirements.
                <small class="d-block mt-1">
                    Lines: ${data.line_count || 'N/A'} | Characters: ${data.char_count || 'N/A'}
                </small>
            </div>
        `;
    } else {
        const errorList = (data.errors || []).map(error => `<li>${escapeHtml(error)}</li>`).join('');
        container.innerHTML = `
            <div class="alert alert-warning alert-sm">
                <i class="fas fa-exclamation-triangle me-2"></i>
                <strong>Validation Issues:</strong>
                <ul class="mt-2 mb-0 small">${errorList}</ul>
            </div>
        `;
    }
}

// Utility function to escape HTML
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, function(m) { return map[m]; });
}

// Form submission with validation
function submitForm() {
    const form = document.getElementById('resumeForm');
    const submitBtn = document.getElementById('submitBtn');
    
    if (!form.checkValidity()) {
        form.reportValidity();
        return false;
    }
    
    // Show loading state
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing Resume...';
    submitBtn.disabled = true;
    
    return true;
}

// Add event listener to form if it exists
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('resumeForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            if (!submitForm()) {
                e.preventDefault();
            }
        });
    }
});

// Copy to clipboard functionality (enhanced)
function copyToClipboard(elementId, buttonElement) {
    const element = document.getElementById(elementId || 'tailoredLatex');
    if (!element) return false;
    
    // Select and copy
    element.select();
    element.setSelectionRange(0, 99999);
    
    try {
        navigator.clipboard.writeText(element.value).then(() => {
            showCopyFeedback(buttonElement, true);
        }).catch(() => {
            // Fallback for older browsers
            document.execCommand('copy');
            showCopyFeedback(buttonElement, true);
        });
    } catch (error) {
        showCopyFeedback(buttonElement, false);
    }
}

// Show copy feedback
function showCopyFeedback(button, success) {
    if (!button) button = event.target.closest('button');
    
    const originalText = button.innerHTML;
    const originalClass = button.className;
    
    if (success) {
        button.innerHTML = '<i class="fas fa-check me-1"></i>Copied!';
        button.className = button.className.replace('btn-outline-secondary', 'btn-success');
    } else {
        button.innerHTML = '<i class="fas fa-times me-1"></i>Failed';
        button.className = button.className.replace('btn-outline-secondary', 'btn-danger');
    }
    
    setTimeout(() => {
        button.innerHTML = originalText;
        button.className = originalClass;
    }, 2000);
}

// Utility: Format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Utility: Show toast notification (if Bootstrap is available)
function showToast(message, type = 'info') {
    if (typeof bootstrap === 'undefined') return;
    
    // Create toast container if it doesn't exist
    let toastContainer = document.getElementById('toastContainer');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toastContainer';
        toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
        toastContainer.style.zIndex = '1055';
        document.body.appendChild(toastContainer);
    }
    
    // Create toast
    const toastId = 'toast_' + Date.now();
    const toast = document.createElement('div');
    toast.id = toastId;
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    toastContainer.appendChild(toast);
    
    // Show toast
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    // Remove after hidden
    toast.addEventListener('hidden.bs.toast', () => {
        toast.remove();
    });
}
