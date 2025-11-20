/**
 * Frontend JavaScript for DocuGener.
 * Handles fetching captures, updating context, pause/resume, and export.
 */

const API_BASE = '/api';

let captures = [];
let isPaused = false;

// DOM Elements
const controlPanel = document.getElementById('controlPanel');
const minimizedBar = document.getElementById('minimizedBar');
const minimizeBtn = document.getElementById('minimizeBtn');
const restoreBtn = document.getElementById('restoreBtn');
const pauseBtn = document.getElementById('pauseBtn');
const statusDot = document.getElementById('statusDot');
const statusText = document.getElementById('statusText');
const exportBtn = document.getElementById('exportBtn');
const exportModal = document.getElementById('exportModal');
const cancelExportBtn = document.getElementById('cancelExportBtn');
const confirmExportBtn = document.getElementById('confirmExportBtn');
const capturesContainer = document.getElementById('capturesContainer');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadCaptures();
    loadStatus();
    setupEventListeners();
    
    // Auto-refresh captures every 2 seconds
    setInterval(loadCaptures, 2000);
});

function setupEventListeners() {
    minimizeBtn.addEventListener('click', minimizeControl);
    restoreBtn.addEventListener('click', restoreControl);
    pauseBtn.addEventListener('click', togglePause);
    exportBtn.addEventListener('click', showExportModal);
    cancelExportBtn.addEventListener('click', hideExportModal);
    confirmExportBtn.addEventListener('click', handleExport);
}

async function loadCaptures() {
    try {
        const response = await fetch(`${API_BASE}/captures`);
        if (!response.ok) {
            console.error(`Failed to load captures: ${response.status} ${response.statusText}`);
            return;
        }
        const data = await response.json();
        captures = data;
        renderCaptures();
    } catch (error) {
        console.error('Error loading captures:', error);
        console.error('Make sure you are accessing http://localhost:5100 (not port 5000)');
    }
}

async function loadStatus() {
    try {
        const response = await fetch(`${API_BASE}/status`);
        const data = await response.json();
        isPaused = data.paused;
        updatePauseButton();
    } catch (error) {
        console.error('Error loading status:', error);
    }
}

async function togglePause() {
    try {
        isPaused = !isPaused;
        const response = await fetch(`${API_BASE}/pause`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ paused: isPaused })
        });
        
        if (response.ok) {
            updatePauseButton();
        } else {
            isPaused = !isPaused; // Revert on error
        }
    } catch (error) {
        console.error('Error toggling pause:', error);
        isPaused = !isPaused; // Revert on error
    }
}

function updatePauseButton() {
    if (isPaused) {
        pauseBtn.textContent = 'Resume';
        pauseBtn.classList.add('paused');
        statusDot.classList.add('paused');
        statusText.textContent = 'Paused';
    } else {
        pauseBtn.textContent = 'Pause';
        pauseBtn.classList.remove('paused');
        statusDot.classList.remove('paused');
        statusText.textContent = 'Recording';
    }
}

function minimizeControl() {
    controlPanel.style.display = 'none';
    minimizedBar.style.display = 'flex';
}

function restoreControl() {
    minimizedBar.style.display = 'none';
    controlPanel.style.display = 'block';
}

function showExportModal() {
    exportModal.style.display = 'flex';
}

function hideExportModal() {
    exportModal.style.display = 'none';
}

async function handleExport() {
    const format = document.querySelector('input[name="exportFormat"]:checked').value;
    const captureIds = captures.map(c => c.id);
    
    try {
        const response = await fetch(`${API_BASE}/export`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                format: format,
                capture_ids: captureIds
            })
        });
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `docugener_export.${format}`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
            hideExportModal();
        } else {
            alert('Error exporting. Please try again.');
        }
    } catch (error) {
        console.error('Error exporting:', error);
        alert('Error exporting. Please try again.');
    }
}

function renderCaptures() {
    if (captures.length === 0) {
        capturesContainer.innerHTML = '<p class="empty-message">No captures yet. Start clicking to capture screenshots!</p>';
        return;
    }
    
    // Sort by timestamp (oldest first)
    const sortedCaptures = [...captures].sort((a, b) => 
        new Date(a.timestamp) - new Date(b.timestamp)
    );
    
    capturesContainer.innerHTML = sortedCaptures.map(capture => `
        <div class="capture-item" data-id="${capture.id}">
            <div class="capture-header">
                <div class="capture-title-wrapper">
                    <div class="capture-title">${escapeHtml(capture.window_title || 'Unknown Window')}</div>
                    ${capture.url ? `<a href="${escapeHtml(capture.url)}" target="_blank" class="capture-url">${escapeHtml(capture.url)}</a>` : ''}
                </div>
                <button class="delete-btn" data-id="${capture.id}" title="Delete this capture">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                        <line x1="10" y1="11" x2="10" y2="17"></line>
                        <line x1="14" y1="11" x2="14" y2="17"></line>
                    </svg>
                </button>
            </div>
            <img src="${API_BASE}/captures/${capture.id}" alt="Capture" class="capture-image" />
            <textarea 
                class="capture-context" 
                placeholder="Add context or description for this capture..."
                data-id="${capture.id}"
            >${escapeHtml(capture.context || '')}</textarea>
            <div class="capture-timestamp">${formatTimestamp(capture.timestamp)}</div>
        </div>
    `).join('');
    
    // Add event listeners for context updates
    document.querySelectorAll('.capture-context').forEach(textarea => {
        let timeout;
        textarea.addEventListener('input', () => {
            clearTimeout(timeout);
            timeout = setTimeout(() => {
                updateContext(textarea.dataset.id, textarea.value);
            }, 1000); // Debounce: update 1 second after user stops typing
        });
    });
    
    // Add event listeners for delete buttons
    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            if (confirm('Are you sure you want to delete this capture?')) {
                deleteCapture(btn.dataset.id);
            }
        });
    });
}

async function updateContext(captureId, context) {
    try {
        const response = await fetch(`${API_BASE}/captures/${captureId}/context`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ context })
        });
        
        if (!response.ok) {
            console.error('Error updating context');
        }
    } catch (error) {
        console.error('Error updating context:', error);
    }
}

async function deleteCapture(captureId) {
    try {
        const response = await fetch(`${API_BASE}/captures/${captureId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            // Remove from local array and reload
            captures = captures.filter(c => c.id !== captureId);
            renderCaptures();
        } else {
            alert('Error deleting capture. Please try again.');
        }
    } catch (error) {
        console.error('Error deleting capture:', error);
        alert('Error deleting capture. Please try again.');
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatTimestamp(timestamp) {
    if (!timestamp) return '';
    const date = new Date(timestamp);
    return date.toLocaleString();
}

