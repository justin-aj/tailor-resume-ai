// Job URLs Management
let jobs = [];
let jobIdCounter = 1;

// Load jobs from localStorage on page load
document.addEventListener('DOMContentLoaded', function() {
    loadJobsFromStorage();
    renderJobsTable();
    
    // Handle Enter key in URL input
    const jobUrlInput = document.getElementById('jobUrl');
    if (jobUrlInput) {
        jobUrlInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                addJobUrl();
            }
        });
    }
});

// Load jobs from localStorage
function loadJobsFromStorage() {
    const stored = localStorage.getItem('scraperJobs');
    if (stored) {
        try {
            const data = JSON.parse(stored);
            jobs = (data.jobs || []).map(job => ({
                applied: false,
                ...job
            }));
            jobIdCounter = data.counter || 1;
        } catch (e) {
            console.error('Error loading jobs:', e);
            jobs = [];
        }
    }
}

// Save jobs to localStorage
function saveJobsToStorage() {
    localStorage.setItem('scraperJobs', JSON.stringify({
        jobs: jobs,
        counter: jobIdCounter
    }));
}

// Add job URL
function addJobUrl() {
    console.log('addJobUrl called'); // Debug
    const urlInput = document.getElementById('jobUrl');
    
    if (!urlInput) {
        console.error('URL input element not found!');
        showToast('Error: URL input not found', 'danger');
        return;
    }
    
    const url = urlInput.value.trim();
    console.log('URL entered:', url); // Debug
    
    if (!url) {
        showToast('Please enter a URL', 'warning');
        return;
    }
    
    // Basic URL validation
    try {
        new URL(url);
    } catch (e) {
        console.error('Invalid URL:', e);
        showToast('Please enter a valid URL', 'danger');
        return;
    }
    
    // Check for duplicates
    if (jobs.some(job => job.url === url)) {
        showToast('This URL is already in the list', 'warning');
        return;
    }
    
    // Add job
    const job = {
        id: jobIdCounter++,
        url: url,
        title: null,
        description: null,
        dateAdded: new Date().toISOString(),
        status: 'pending', // pending, scraping, scraped, error
        applied: false
    };
    
    console.log('Adding job:', job); // Debug
    jobs.unshift(job); // Add to beginning
    saveJobsToStorage();
    renderJobsTable();
    
    // Clear input
    urlInput.value = '';
    
    showToast('URL added successfully', 'success');
}

// Render jobs table
function renderJobsTable() {
    const tbody = document.getElementById('jobsTableBody');
    const emptyRow = document.getElementById('emptyRow');
    
    if (jobs.length === 0) {
        emptyRow.style.display = '';
        return;
    }
    
    emptyRow.style.display = 'none';
    
    // Clear existing rows (except empty row)
    Array.from(tbody.children).forEach(row => {
        if (row.id !== 'emptyRow') {
            row.remove();
        }
    });
    
    // Add job rows
    jobs.forEach((job, index) => {
        const row = createJobRow(job, index);
        tbody.insertBefore(row, emptyRow);
    });
}

// Create job table row
function createJobRow(job, index) {
    const row = document.createElement('tr');
    row.id = `job-${job.id}`;
    row.className = 'hover:bg-gray-50 transition-colors';
    
    console.log('Creating row for job:', job.id, 'Status:', job.status); // Debug log
    
    // Format date
    const date = new Date(job.dateAdded);
    const dateStr = date.toLocaleDateString('en-US', { 
        month: 'short', 
        day: 'numeric',
        year: 'numeric'
    });
    
    // Get domain from URL
    let domain = '';
    try {
        const urlObj = new URL(job.url);
        domain = urlObj.hostname.replace('www.', '');
    } catch (e) {
        domain = job.url;
    }
    
    // Status badge
    let statusHtml = '';
    switch (job.status) {
        case 'pending':
            statusHtml = '<span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-800">Pending</span>';
            break;
        case 'scraping':
            statusHtml = '<span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800"><i class="fas fa-spinner fa-spin mr-1"></i>Scraping</span>';
            break;
        case 'scraped':
            statusHtml = '<span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800"><i class="fas fa-check mr-1"></i>Scraped</span>';
            break;
        case 'error':
            statusHtml = '<span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800"><i class="fas fa-times mr-1"></i>Error</span>';
            break;
    }
    
    row.innerHTML = `
        <td class="px-4 py-3 text-center">
            <div class="text-sm font-semibold text-gray-700">${index + 1}</div>
        </td>
        <td class="px-4 py-3">
            <a href="${job.url}" target="_blank" class="text-blue-600 hover:text-blue-800 text-sm truncate block max-w-md" title="${job.url}">${domain}</a>
        </td>
        <td class="px-4 py-3">
            <div class="text-sm ${!job.title ? 'text-gray-400 italic' : 'text-gray-900'}">${job.title || 'Not scraped yet'}</div>
        </td>
        <td class="px-4 py-3">
            <div class="text-sm text-gray-600">${dateStr}</div>
        </td>
        <td class="px-4 py-3 text-center">
            ${statusHtml}
        </td>
        <td class="px-4 py-3 text-center">
            ${job.prompt ? `<button class=\"p-2 text-indigo-600 hover:bg-indigo-50 rounded-lg transition-all\" onclick=\"copyPromptForJob(${job.id})\" title=\"Copy Prompt\"><i class=\"fas fa-copy\"></i></button>` : `<span class=\"text-xs text-gray-400\">-</span>`}
        </td>
        <td class="px-4 py-3 text-center">
            <label class="inline-flex items-center cursor-pointer select-none">
                <input type="checkbox" class="sr-only" ${job.applied ? 'checked' : ''} onchange="setAppliedStatus(${job.id}, this.checked)">
                <div class="w-11 h-6 ${job.applied ? 'bg-green-500' : 'bg-gray-200'} rounded-full relative transition-colors">
                    <div class="absolute top-1 left-1 w-4 h-4 bg-white rounded-full transition-transform ${job.applied ? 'translate-x-5' : ''}"></div>
                </div>
                <span class="ml-3 text-xs font-semibold ${job.applied ? 'text-green-700' : 'text-gray-500'}">${job.applied ? 'Applied' : 'Not applied'}</span>
            </label>
        </td>
        <td class="px-4 py-3 text-center">
            <div class="flex items-center justify-center space-x-2">
                ${job.status === 'scraped' ? 
                    `<button class="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-all" onclick="viewJob(${job.id})" title="View"><i class="fas fa-eye"></i></button><button class="p-2 text-green-600 hover:bg-green-50 rounded-lg transition-all" onclick="generatePromptForJob(${job.id})" title="Generate Prompt"><i class="fas fa-magic"></i></button>` : 
                    `<button class="p-2 text-indigo-600 hover:bg-indigo-50 rounded-lg transition-all" onclick="scrapeJob(${job.id})" title="Scrape"><i class="fas fa-spider"></i></button>`
                }
                <button class="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-all" onclick="deleteJob(${job.id})" title="Delete">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        </td>
    `;
    
    return row;
}

// Scrape single job
async function scrapeJob(jobId) {
    const job = jobs.find(j => j.id === jobId);
    if (!job) return;
    
    // Update status
    job.status = 'scraping';
    saveJobsToStorage();
    renderJobsTable();
    
    showLoadingToast('Scraping job description...');
    
    try {
        const response = await fetch('/api/scrape-job', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url: job.url })
        });
        
        const data = await response.json();
        
        if (data.success) {
            job.status = 'scraped';
            job.title = data.title || 'Job Posting';
            job.description = data.description;
            showToast('Job scraped successfully!', 'success');
        } else {
            job.status = 'error';
            showToast('Failed to scrape job: ' + (data.error || 'Unknown error'), 'danger');
        }
    } catch (error) {
        job.status = 'error';
        showToast('Error scraping job: ' + error.message, 'danger');
    } finally {
        hideLoadingToast();
        saveJobsToStorage();
        renderJobsTable();
    }
}

// Scrape all pending jobs
async function scrapeAllJobs() {
    const pendingJobs = jobs.filter(j => j.status === 'pending' || j.status === 'error');
    
    if (pendingJobs.length === 0) {
        showToast('No jobs to scrape', 'info');
        return;
    }
    
    const scrapeAllBtn = document.getElementById('scrapeAllBtn');
    scrapeAllBtn.disabled = true;
    scrapeAllBtn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Scraping...';
    
    for (const job of pendingJobs) {
        await scrapeJob(job.id);
        // Add delay between requests
        await new Promise(resolve => setTimeout(resolve, 1000));
    }
    
    scrapeAllBtn.disabled = false;
    scrapeAllBtn.innerHTML = '<i class="fas fa-spider mr-2"></i>Scrape All';
    
    showToast(`Scraped ${pendingJobs.length} job(s)`, 'success');
}

// View job details
function viewJob(jobId) {
    const job = jobs.find(j => j.id === jobId);
    if (!job || job.status !== 'scraped') return;
    
    document.getElementById('modalJobTitle').textContent = job.title || 'N/A';
    document.getElementById('modalJobUrl').innerHTML = `<a href="${job.url}" target="_blank" class="text-blue-600 hover:text-blue-800">${job.url}</a>`;
    document.getElementById('modalJobDescription').textContent = job.description || 'No description available';
    
    // Set current modal job ID for other operations
    window.currentModalJobId = jobId;
    
    // Show modal (Tailwind style)
    document.getElementById('jobDetailModal').classList.remove('hidden');
}

// Delete job
function deleteJob(jobId) {
    if (!confirm('Are you sure you want to delete this job URL?')) return;
    
    jobs = jobs.filter(j => j.id !== jobId);
    saveJobsToStorage();
    renderJobsTable();
    showToast('Job URL deleted', 'success');
}

// Clear all jobs
function clearAllJobs() {
    if (!confirm('Are you sure you want to clear all job URLs?')) return;
    
    jobs = [];
    saveJobsToStorage();
    renderJobsTable();
    showToast('All job URLs cleared', 'success');
}

// Copy description to clipboard
function copyToClipboard() {
    const description = document.getElementById('modalJobDescription').textContent;
    
    navigator.clipboard.writeText(description).then(() => {
        showToast('Job description copied to clipboard!', 'success');
    }).catch(err => {
        showToast('Failed to copy: ' + err, 'danger');
    });
}

// Use job description in resume tailor
function useJobDescription() {
    const description = document.getElementById('modalJobDescription').textContent;
    
    // Store in sessionStorage
    sessionStorage.setItem('jobDescription', description);
    
    // Redirect to home page
    window.location.href = '/';
}

// Toast notifications (Tailwind style)
function showToast(message, type = 'info') {
    const colors = {
        'success': 'bg-green-50 border-green-200 text-green-800',
        'danger': 'bg-red-50 border-red-200 text-red-800',
        'warning': 'bg-yellow-50 border-yellow-200 text-yellow-800',
        'info': 'bg-blue-50 border-blue-200 text-blue-800'
    };
    
    const icons = {
        'success': 'fa-check-circle',
        'danger': 'fa-exclamation-circle',
        'warning': 'fa-exclamation-triangle',
        'info': 'fa-info-circle'
    };
    
    const alertDiv = document.createElement('div');
    alertDiv.className = `fixed top-4 right-4 ${colors[type]} border px-6 py-3 rounded-lg shadow-lg z-50 flex items-center space-x-3`;
    alertDiv.innerHTML = `
        <i class="fas ${icons[type]}"></i>
        <span>${message}</span>
        <button onclick="this.parentElement.remove()" class="ml-4 text-xl">&times;</button>
    `;
    document.body.appendChild(alertDiv);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 3000);
}

// Loading toast (Tailwind style)
function showLoadingToast(message = 'Scraping...') {
    const toast = document.getElementById('loadingToast');
    toast.classList.remove('hidden');
}

function hideLoadingToast() {
    const toast = document.getElementById('loadingToast');
    toast.classList.add('hidden');
}

// Generate prompt for a scraped job
async function generatePromptForJob(jobId, options = {}) {
    const { showModal = false, showToastMessage = true, showLoading = true } = options;
    const job = jobs.find(j => j.id === jobId);
    if (!job || job.status !== 'scraped' || !job.description) {
        if (showToastMessage) {
            showToast('Please scrape the job first before generating a prompt', 'warning');
        }
        return { success: false };
    }
    
    if (showLoading) {
        showLoadingToast('Generating prompt...');
    }
    
    try {
        const response = await fetch('/api/generate-prompt', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                job_description: job.description 
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            job.prompt = data.prompt;
            job.promptWordCount = data.word_count;
            job.promptCharCount = data.char_count;
            saveJobsToStorage();
            renderJobsTable();
            
            if (showModal) {
                showPromptModal(job.title, data.prompt, data.word_count, data.char_count);
            }
            if (showToastMessage) {
                showToast('Prompt ready to copy', 'success');
            }
            
            return {
                success: true,
                prompt: data.prompt,
                wordCount: data.word_count,
                charCount: data.char_count
            };
        }
        
        if (showToastMessage) {
            showToast('Failed to generate prompt: ' + (data.error || 'Unknown error'), 'danger');
        }
        return { success: false };
    } catch (error) {
        if (showToastMessage) {
            showToast('Error generating prompt: ' + error.message, 'danger');
        }
        return { success: false };
    } finally {
        if (showLoading) {
            hideLoadingToast();
        }
    }
}

// Generate prompts for all scraped jobs
async function generatePromptsForAllScraped() {
    const scrapedJobs = jobs.filter(j => j.status === 'scraped' && j.description);
    if (scrapedJobs.length === 0) {
        showToast('No scraped jobs available', 'info');
        return;
    }
    
    const generateAllBtn = document.getElementById('generateAllPromptsBtn');
    if (generateAllBtn) {
        generateAllBtn.disabled = true;
        generateAllBtn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Generating...';
    }
    
    showLoadingToast('Generating prompts...');
    
    try {
        const results = [];
        for (const job of scrapedJobs) {
            const result = await generatePromptForJob(job.id, { showModal: false, showToastMessage: false, showLoading: false });
            results.push({ job, result });
            await new Promise(resolve => setTimeout(resolve, 300));
        }
        const successCount = results.filter(item => item.result && item.result.success).length;
        showToast(`Generated ${successCount} prompt(s)`, 'success');
    } finally {
        hideLoadingToast();
        if (generateAllBtn) {
            generateAllBtn.disabled = false;
            generateAllBtn.innerHTML = '<i class="fas fa-magic mr-2"></i>Generate Prompts';
        }
    }
}

// Show prompt modal
function showPromptModal(jobTitle, prompt, wordCount, charCount) {
    // Create modal if it doesn't exist
    let modal = document.getElementById('promptModal');
    if (!modal) {
        modal = document.createElement('div');
        modal.id = 'promptModal';
        modal.className = 'hidden fixed inset-0 bg-black bg-opacity-50 z-50 overflow-y-auto';
        modal.innerHTML = `
            <div class="flex items-center justify-center min-h-screen px-4 py-8">
                <div class="bg-white rounded-2xl shadow-2xl max-w-6xl w-full max-h-[90vh] overflow-hidden">
                    <div class="bg-gradient-to-r from-green-500 to-emerald-500 px-6 py-4 flex justify-between items-center">
                        <h3 class="text-xl font-bold text-white flex items-center">
                            <i class="fas fa-magic mr-2"></i><span id="promptModalTitle">Generated Prompt</span>
                        </h3>
                        <button onclick="closePromptModal()" class="text-white hover:text-gray-200 transition-colors">
                            <i class="fas fa-times text-2xl"></i>
                        </button>
                    </div>
                    <div class="p-6 overflow-y-auto" style="max-height: calc(90vh - 180px);">
                        <div class="mb-4">
                            <textarea id="promptTextArea" 
                                     class="w-full px-4 py-3 border border-gray-300 rounded-lg font-mono text-sm resize-none focus:outline-none focus:ring-2 focus:ring-green-500" 
                                     rows="20" 
                                     readonly></textarea>
                        </div>
                        <div class="flex items-center justify-between text-sm text-gray-600">
                            <div class="flex space-x-4">
                                <span>Words: <strong id="promptWordCount">0</strong></span>
                                <span class="text-gray-400">|</span>
                                <span>Characters: <strong id="promptCharCount">0</strong></span>
                            </div>
                            <span class="text-green-600 font-semibold">
                                <i class="fas fa-check-circle mr-1"></i>Ready to paste
                            </span>
                        </div>
                    </div>
                    <div class="bg-gray-50 px-6 py-4 flex justify-end space-x-3">
                        <button onclick="closePromptModal()" class="px-4 py-2 bg-gray-200 hover:bg-gray-300 text-gray-700 rounded-lg transition-all duration-200">
                            Close
                        </button>
                        <button onclick="copyPromptToClipboard()" class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-all duration-200 flex items-center">
                            <i class="fas fa-copy mr-2"></i>Copy Prompt
                        </button>
                        <button onclick="openChatGPT()" class="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-all duration-200 flex items-center">
                            <i class="fas fa-external-link-alt mr-2"></i>Open ChatGPT
                        </button>
                    </div>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
        
        // Close on background click
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                closePromptModal();
            }
        });
    }
    
    // Update modal content
    document.getElementById('promptModalTitle').textContent = `Prompt for: ${jobTitle}`;
    document.getElementById('promptTextArea').value = prompt;
    document.getElementById('promptWordCount').textContent = wordCount;
    document.getElementById('promptCharCount').textContent = charCount;
    
    // Show modal
    modal.classList.remove('hidden');
}

// Close prompt modal
function closePromptModal() {
    const modal = document.getElementById('promptModal');
    if (modal) {
        modal.classList.add('hidden');
    }
}

// Copy prompt to clipboard from modal
function copyPromptToClipboard() {
    const textarea = document.getElementById('promptTextArea');
    textarea.select();
    navigator.clipboard.writeText(textarea.value).then(() => {
        showToast('Prompt copied to clipboard!', 'success');
    }).catch(err => {
        showToast('Failed to copy: ' + err, 'danger');
    });
}

// Copy the generated prompt for the current job from the details modal
function copyPromptFromModal() {
    const jobId = window.currentModalJobId;
    const job = jobs.find(j => j.id === jobId);
    if (!job || !job.prompt) {
        showToast('Generate a prompt first', 'warning');
        return;
    }
    
    navigator.clipboard.writeText(job.prompt).then(() => {
        showToast('Prompt copied to clipboard!', 'success');
    }).catch(err => {
        showToast('Failed to copy: ' + err, 'danger');
    });
}

// Copy the generated prompt for a specific job from the table
function copyPromptForJob(jobId) {
    const job = jobs.find(j => j.id === jobId);
    if (!job || !job.prompt) {
        showToast('Generate a prompt first', 'warning');
        return;
    }
    
    navigator.clipboard.writeText(job.prompt).then(() => {
        showToast('Prompt copied to clipboard!', 'success');
    }).catch(err => {
        showToast('Failed to copy: ' + err, 'danger');
    });
}

// Open ChatGPT
function openChatGPT() {
    window.open('https://chat.openai.com/', '_blank');
    showToast('Copy the prompt and paste it into ChatGPT', 'info');
}

// Update applied status
function setAppliedStatus(jobId, isApplied) {
    const job = jobs.find(j => j.id === jobId);
    if (!job) return;

    job.applied = isApplied;
    saveJobsToStorage();
    renderJobsTable();
}