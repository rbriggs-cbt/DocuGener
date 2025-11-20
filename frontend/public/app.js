/**
 * Frontend JavaScript for DocuGener.
 * Handles fetching captures, updating context, pause/resume, and export.
 */

const API_BASE = '/api';

let captures = [];
let isPaused = false;
let focusedTextareaId = null;
let focusedTextareaSelection = null;
let isUserTyping = false;
let currentProjectId = null;
let currentProjectName = null;

// DOM Elements
const controlPanel = document.getElementById('controlPanel');
const minimizedBar = document.getElementById('minimizedBar');
const minimizeBtn = document.getElementById('minimizeBtn');
const restoreBtn = document.getElementById('restoreBtn');
const pauseBtn = document.getElementById('pauseBtn');
const statusDot = document.getElementById('statusDot');
const statusText = document.getElementById('statusText');
const clearBtn = document.getElementById('clearBtn');
const projectsBtn = document.getElementById('projectsBtn');
const exportBtn = document.getElementById('exportBtn');
const exportModal = document.getElementById('exportModal');
const cancelExportBtn = document.getElementById('cancelExportBtn');
const confirmExportBtn = document.getElementById('confirmExportBtn');
const projectsModal = document.getElementById('projectsModal');
const closeProjectsBtn = document.getElementById('closeProjectsBtn');
const newProjectBtn = document.getElementById('newProjectBtn');
const newProjectModal = document.getElementById('newProjectModal');
const cancelNewProjectBtn = document.getElementById('cancelNewProjectBtn');
const createProjectBtn = document.getElementById('createProjectBtn');
const projectsList = document.getElementById('projectsList');
const capturesContainer = document.getElementById('capturesContainer');
const currentProjectNameEl = document.getElementById('currentProjectName');
const projectNameDisplay = document.getElementById('projectNameDisplay');

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
    clearBtn.addEventListener('click', handleClearAll);
    projectsBtn.addEventListener('click', showProjectsModal);
    closeProjectsBtn.addEventListener('click', hideProjectsModal);
    newProjectBtn.addEventListener('click', showNewProjectModal);
    cancelNewProjectBtn.addEventListener('click', hideNewProjectModal);
    createProjectBtn.addEventListener('click', handleCreateProject);
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
        
        // Only re-render if captures have actually changed AND user is not typing
        const currentIds = captures.map(c => c.id).sort().join(',');
        const newIds = data.map(c => c.id).sort().join(',');
        
        if (currentIds !== newIds && !isUserTyping) {
            captures = data;
            renderCaptures();
        } else {
            // Update captures data but don't re-render to preserve focus
            captures = data;
        }
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
        const captureId = textarea.dataset.id;
        
        // Restore focus and selection if this was the focused textarea
        if (focusedTextareaId === captureId) {
            textarea.focus();
            if (focusedTextareaSelection) {
                textarea.setSelectionRange(focusedTextareaSelection.start, focusedTextareaSelection.end);
            }
        }
        
        // Track focus
        textarea.addEventListener('focus', () => {
            focusedTextareaId = captureId;
            isUserTyping = true;
        });
        
        textarea.addEventListener('blur', () => {
            if (focusedTextareaId === captureId) {
                focusedTextareaId = null;
                focusedTextareaSelection = {
                    start: textarea.selectionStart,
                    end: textarea.selectionEnd
                };
                // Small delay before allowing re-render
                setTimeout(() => {
                    isUserTyping = false;
                }, 500);
            }
        });
        
        let timeout;
        textarea.addEventListener('input', () => {
            isUserTyping = true;
            clearTimeout(timeout);
            timeout = setTimeout(() => {
                updateContext(captureId, textarea.value);
                isUserTyping = false;
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

function updateProjectDisplay() {
    if (currentProjectName) {
        projectNameDisplay.textContent = currentProjectName;
        currentProjectNameEl.style.display = 'block';
    } else {
        currentProjectNameEl.style.display = 'none';
    }
}

async function handleClearAll(skipConfirmation = false) {
    if (!skipConfirmation && !confirm('Are you sure you want to clear all captures? This cannot be undone.')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/clear-all`, {
            method: 'POST'
        });
        
        if (response.ok) {
            captures = [];
            renderCaptures();
            if (!skipConfirmation) {
                alert('All captures cleared successfully.');
            }
        } else {
            if (!skipConfirmation) {
                alert('Error clearing captures. Please try again.');
            }
        }
    } catch (error) {
        console.error('Error clearing captures:', error);
        if (!skipConfirmation) {
            alert('Error clearing captures. Please try again.');
        }
    }
}

function showProjectsModal() {
    projectsModal.style.display = 'flex';
    loadProjects();
}

function hideProjectsModal() {
    projectsModal.style.display = 'none';
}

function showNewProjectModal() {
    newProjectModal.style.display = 'flex';
    document.getElementById('projectName').value = '';
    document.getElementById('projectDescription').value = '';
}

function hideNewProjectModal() {
    newProjectModal.style.display = 'none';
}

async function loadProjects() {
    try {
        const response = await fetch(`${API_BASE}/projects`);
        if (!response.ok) return;
        
        const projects = await response.json();
        renderProjectsList(projects);
    } catch (error) {
        console.error('Error loading projects:', error);
    }
}

function renderProjectsList(projects) {
    if (projects.length === 0) {
        projectsList.innerHTML = '<p class="empty-message">No saved projects. Create one to get started!</p>';
        return;
    }
    
    projectsList.innerHTML = projects.map(project => `
        <div class="project-item" data-id="${project.id}">
            <div class="project-info">
                <div class="project-name">${escapeHtml(project.name)}</div>
                ${project.description ? `<div class="project-description">${escapeHtml(project.description)}</div>` : ''}
                <div class="project-meta">
                    <span>Updated: ${formatTimestamp(project.updated_at)}</span>
                </div>
            </div>
            <div class="project-actions">
                <button class="load-project-btn" data-id="${project.id}">Load</button>
                <button class="save-project-btn" data-id="${project.id}">Save</button>
                <button class="delete-project-btn" data-id="${project.id}">Delete</button>
            </div>
        </div>
    `).join('');
    
    // Add event listeners
    document.querySelectorAll('.load-project-btn').forEach(btn => {
        btn.addEventListener('click', () => handleLoadProject(btn.dataset.id));
    });
    
    document.querySelectorAll('.save-project-btn').forEach(btn => {
        btn.addEventListener('click', () => handleSaveProject(btn.dataset.id));
    });
    
    document.querySelectorAll('.delete-project-btn').forEach(btn => {
        btn.addEventListener('click', () => handleDeleteProject(btn.dataset.id));
    });
}

async function handleCreateProject() {
    const name = document.getElementById('projectName').value.trim();
    const description = document.getElementById('projectDescription').value.trim();
    
    if (!name) {
        alert('Please enter a project name.');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/projects`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name, description })
        });
        
        if (response.ok) {
            const data = await response.json();
            currentProjectId = data.id;
            currentProjectName = name;
            updateProjectDisplay();
            
            // Auto-clear all captures when creating a new project
            await handleClearAll(true); // Pass true to skip confirmation
            
            hideNewProjectModal();
            loadProjects();
            alert('Project created successfully!');
        } else {
            const data = await response.json();
            alert(data.error || 'Error creating project. Please try again.');
        }
    } catch (error) {
        console.error('Error creating project:', error);
        alert('Error creating project. Please try again.');
    }
}

async function handleLoadProject(projectId) {
    if (!confirm('Loading this project will replace all current captures. Continue?')) {
        return;
    }
    
    try {
        // Get project info first
        const projectResponse = await fetch(`${API_BASE}/projects/${projectId}`);
        if (!projectResponse.ok) {
            throw new Error('Failed to get project info');
        }
        const projectData = await projectResponse.json();
        
        const response = await fetch(`${API_BASE}/projects/${projectId}/load`, {
            method: 'POST'
        });
        
        if (response.ok) {
            const data = await response.json();
            
            // Update current project
            currentProjectId = projectId;
            currentProjectName = projectData.name;
            updateProjectDisplay();
            
            // Force reload captures from server
            // Use a small delay to ensure backend has finished processing
            setTimeout(() => {
                loadCaptures();
            }, 100);
            
            hideProjectsModal();
            alert('Project loaded successfully!');
        } else {
            const errorData = await response.json();
            alert(errorData.error || 'Error loading project. Please try again.');
        }
    } catch (error) {
        console.error('Error loading project:', error);
        alert('Error loading project. Please try again.');
    }
}

async function handleSaveProject(projectId) {
    try {
        const response = await fetch(`${API_BASE}/projects/${projectId}/save`, {
            method: 'POST'
        });
        
        if (response.ok) {
            // Update current project if saving to the active project
            if (projectId === currentProjectId) {
                // Project name should already be set, just refresh display
                updateProjectDisplay();
            } else {
                // Get project info to update display
                const projectResponse = await fetch(`${API_BASE}/projects/${projectId}`);
                if (projectResponse.ok) {
                    const projectData = await projectResponse.json();
                    currentProjectId = projectId;
                    currentProjectName = projectData.name;
                    updateProjectDisplay();
                }
            }
            
            loadProjects();
            alert('Project saved successfully!');
        } else {
            alert('Error saving project. Please try again.');
        }
    } catch (error) {
        console.error('Error saving project:', error);
        alert('Error saving project. Please try again.');
    }
}

async function handleDeleteProject(projectId) {
    if (!confirm('Are you sure you want to delete this project? This cannot be undone.')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/projects/${projectId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            loadProjects();
            alert('Project deleted successfully!');
        } else {
            alert('Error deleting project. Please try again.');
        }
    } catch (error) {
        console.error('Error deleting project:', error);
        alert('Error deleting project. Please try again.');
    }
}

