// Update the file upload area handling
function initializeUploadSection() {
    loadUploadDatabases();
    
    // File input events
    const fileUploadArea = document.getElementById('fileUploadArea');
    const zipFileInput = document.getElementById('zipFile');
    
    fileUploadArea.addEventListener('click', function() {
        zipFileInput.click();
    });
    
    zipFileInput.addEventListener('change', handleFileSelect);
    
    // Enhanced drag and drop
    fileUploadArea.addEventListener('dragover', function(e) {
        e.preventDefault();
        this.classList.add('dragover');
    });
    
    fileUploadArea.addEventListener('dragleave', function(e) {
        e.preventDefault();
        this.classList.remove('dragover');
    });
    
    fileUploadArea.addEventListener('drop', function(e) {
        e.preventDefault();
        this.classList.remove('dragover');
        if (e.dataTransfer.files.length > 0) {
            zipFileInput.files = e.dataTransfer.files;
            handleFileSelect();
        }
    });
    
    // Upload database dropdown events
    uploadDatabaseSearch.addEventListener('input', function() {
        filterUploadDropdown('database', this.value);
    });
    
    // Upload table dropdown events
    uploadTableSearch.addEventListener('input', function() {
        filterUploadDropdown('table', this.value);
    });
    
    // Custom S3 path input event
    customS3PathInput.addEventListener('input', function() {
        updateUploadButtonState();
    });
    
    // Upload button event
    uploadBtn.addEventListener('click', handleUpload);
}

function handleFileSelect() {
    const file = zipFileInput.files[0];
    const fileDisplay = document.getElementById('fileDisplay');
    
    if (file) {
        if (file.name.toLowerCase().endsWith('.zip')) {
            selectedZipFile = file;
            const fileSize = (file.size / 1024 / 1024).toFixed(2);
            fileDisplay.innerHTML = `<i class="fas fa-file-archive"></i> ${file.name} (${fileSize} MB)`;
            fileDisplay.style.color = '#27ae60';
            hideElement(fileError);
            updateUploadButtonState();
        } else {
            showError(fileError, 'Please select a valid ZIP file');
            resetFileSelection();
        }
    } else {
        resetFileSelection();
    }
}

function resetFileSelection() {
    selectedZipFile = null;
    const fileDisplay = document.getElementById('fileDisplay');
    fileDisplay.innerHTML = '<i class="fas fa-cloud-upload-alt"></i> No file selected';
    fileDisplay.style.color = '#6c757d';
    updateUploadButtonState();
}

// Update the showError and showSuccess functions for new styling
function showError(element, message) {
    element.innerHTML = `<i class="fas fa-exclamation-circle me-2"></i>${message}`;
    element.style.display = 'block';
}

function showSuccess(element, message) {
    element.innerHTML = `<i class="fas fa-check-circle me-2"></i>${message}`;
    element.style.display = 'block';
}

// Add smooth loading states for buttons
function setButtonLoading(button, isLoading) {
    if (isLoading) {
        button.disabled = true;
        const originalText = button.innerHTML;
        button.setAttribute('data-original-text', originalText);
        button.innerHTML = '<div class="spinner-border spinner-border-sm me-2" role="status"></div>Processing...';
    } else {
        const originalText = button.getAttribute('data-original-text');
        if (originalText) {
            button.innerHTML = originalText;
        }
        button.disabled = false;
    }
}

// Update downloadFiles function with loading state
function downloadFiles(s3Path, tableName) {
    setButtonLoading(downloadBtn, true);
    showElement(downloadLoading);
    hideElement(downloadError);
    hideElement(downloadSuccess);
    
    console.log('Sending download request - Table:', tableName, 'Path:', s3Path);
    
    fetch('/api/download_files', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
            s3_path: s3Path,
            table_name: tableName
        })
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(data => {
                throw new Error(data.error || 'Download failed');
            });
        }
        return response.blob();
    })
    .then(blob => {
        setButtonLoading(downloadBtn, false);
        hideElement(downloadLoading);
        
        // Create download link
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        showSuccess(downloadSuccess, 'Download started successfully!');
        setTimeout(() => hideElement(downloadSuccess), 5000);
    })
    .catch(error => {
        setButtonLoading(downloadBtn, false);
        hideElement(downloadLoading);
        showError(downloadError, `Download failed: ${error.message}`);
    });
}

// Update handleUpload function with loading state
function handleUpload() {
    if (!selectedZipFile) {
        showError(uploadError, 'Please select a ZIP file');
        return;
    }
    
    const customPath = customS3PathInput.value.trim();
    const s3Path = customPath || uploadSelectedTableLocation;
    
    if (!s3Path) {
        showError(uploadError, 'Please select a target S3 path');
        return;
    }
    
    setButtonLoading(uploadBtn, true);
    showElement(uploadLoading);
    hideElement(uploadError);
    hideElement(uploadSuccess);
    
    const formData = new FormData();
    formData.append('zip_file', selectedZipFile);
    formData.append('s3_path', s3Path);
    
    fetch('/api/upload_files', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        setButtonLoading(uploadBtn, false);
        hideElement(uploadLoading);
        
        if (data.error) {
            showError(uploadError, data.error);
        } else {
            showSuccess(uploadSuccess, data.message || 'Files extracted and uploaded successfully!');
            setTimeout(() => hideElement(uploadSuccess), 5000);
            console.log(`Upload successful: ${data.file_count} files uploaded`);
        }
    })
    .catch(error => {
        setButtonLoading(uploadBtn, false);
        hideElement(uploadLoading);
        showError(uploadError, `Upload failed: ${error.message}`);
    });
}

// Initialize both sections when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('Initializing AWS Glue Catalog Manager...');
    loadDatabases(); // Existing download section
    initializeUploadSection(); // New upload section
    
    // Your existing download section event listeners remain
    // ...
});