// Upload Section DOM Elements
const zipFileInput = document.getElementById('zipFile');
const fileDisplay = document.getElementById('fileDisplay');
const fileError = document.getElementById('fileError');

const uploadDatabaseDropdown = document.getElementById('uploadDatabaseDropdown');
const uploadDatabaseText = document.getElementById('uploadDatabaseText');
const uploadDatabaseSearch = document.getElementById('uploadDatabaseSearch');
const uploadDatabaseList = document.getElementById('uploadDatabaseList');
const uploadDatabaseLoading = document.getElementById('uploadDatabaseLoading');
const uploadDatabaseError = document.getElementById('uploadDatabaseError');

const uploadTableDropdown = document.getElementById('uploadTableDropdown');
const uploadTableText = document.getElementById('uploadTableText');
const uploadTableSearch = document.getElementById('uploadTableSearch');
const uploadTableList = document.getElementById('uploadTableList');
const uploadTableLoading = document.getElementById('uploadTableLoading');
const uploadTableError = document.getElementById('uploadTableError');

const uploadS3LocationDiv = document.getElementById('uploadS3Location');
const customS3PathInput = document.getElementById('customS3Path');
const uploadBtn = document.getElementById('uploadBtn');
const uploadLoading = document.getElementById('uploadLoading');
const uploadError = document.getElementById('uploadError');
const uploadSuccess = document.getElementById('uploadSuccess');

// Upload Section State
let uploadAllDatabases = [];
let uploadAllTables = [];
let uploadSelectedDatabase = '';
let uploadSelectedTableName = '';
let uploadSelectedTableLocation = '';
let selectedZipFile = null;

// Initialize Upload Section
function initializeUploadSection() {
    loadUploadDatabases();
    
    // File input events
    zipFileInput.addEventListener('change', handleFileSelect);
    
    // Drag and drop for file input
    fileDisplay.addEventListener('dragover', function(e) {
        e.preventDefault();
        this.style.backgroundColor = '#e9ecef';
    });
    
    fileDisplay.addEventListener('dragleave', function(e) {
        e.preventDefault();
        this.style.backgroundColor = '#f8f9fa';
    });
    
    fileDisplay.addEventListener('drop', function(e) {
        e.preventDefault();
        this.style.backgroundColor = '#f8f9fa';
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
    if (file) {
        if (file.name.toLowerCase().endsWith('.zip')) {
            selectedZipFile = file;
            fileDisplay.textContent = `Selected: ${file.name} (${(file.size / 1024 / 1024).toFixed(2)} MB)`;
            fileDisplay.style.borderColor = '#198754';
            hideElement(fileError);
            updateUploadButtonState();
        } else {
            showError(fileError, 'Please select a ZIP file');
            resetFileSelection();
        }
    } else {
        resetFileSelection();
    }
}

function resetFileSelection() {
    selectedZipFile = null;
    fileDisplay.textContent = 'Click to select ZIP file or drag and drop here';
    fileDisplay.style.borderColor = '#ced4da';
    updateUploadButtonState();
}

function loadUploadDatabases() {
    console.log('Loading databases for upload section...');
    
    uploadDatabaseDropdown.disabled = true;
    uploadDatabaseText.textContent = 'Loading databases...';
    showElement(uploadDatabaseLoading);
    hideElement(uploadDatabaseError);
    
    fetch('/api/databases')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            hideElement(uploadDatabaseLoading);
            uploadDatabaseDropdown.disabled = false;
            
            if (data.error) {
                showError(uploadDatabaseError, data.error);
                uploadDatabaseText.textContent = 'Error loading databases';
                return;
            }
            
            uploadAllDatabases = data.databases || [];
            populateUploadDropdown('database', uploadAllDatabases);
            console.log(`Loaded ${uploadAllDatabases.length} databases for upload section`);
        })
        .catch(error => {
            hideElement(uploadDatabaseLoading);
            uploadDatabaseDropdown.disabled = false;
            uploadDatabaseText.textContent = 'Error loading databases';
            showError(uploadDatabaseError, `Failed to load databases: ${error.message}`);
        });
}

function loadUploadTables(databaseName) {
    uploadSelectedDatabase = databaseName;
    
    resetUploadTableSelection();
    uploadTableDropdown.disabled = true;
    uploadTableText.textContent = 'Loading tables...';
    
    console.log(`Loading tables for upload database: ${databaseName}`);
    showElement(uploadTableLoading);
    hideElement(uploadTableError);
    
    fetch(`/api/tables/${encodeURIComponent(databaseName)}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            hideElement(uploadTableLoading);
            uploadTableDropdown.disabled = false;
            
            if (data.error) {
                showError(uploadTableError, data.error);
                uploadTableText.textContent = 'Error loading tables';
                return;
            }
            
            uploadAllTables = data.tables || [];
            const tableNames = uploadAllTables.map(table => table.name);
            populateUploadDropdown('table', tableNames);
            console.log(`Loaded ${uploadAllTables.length} tables for upload section`);
        })
        .catch(error => {
            hideElement(uploadTableLoading);
            uploadTableDropdown.disabled = false;
            uploadTableText.textContent = 'Error loading tables';
            showError(uploadTableError, `Failed to load tables: ${error.message}`);
        });
}

function populateUploadDropdown(type, items) {
    const listElement = type === 'database' ? uploadDatabaseList : uploadTableList;
    const searchElement = type === 'database' ? uploadDatabaseSearch : uploadTableSearch;
    
    listElement.innerHTML = '';
    
    if (items.length === 0) {
        const noResults = document.createElement('div');
        noResults.className = 'no-results';
        noResults.textContent = 'No items found';
        listElement.appendChild(noResults);
        return;
    }
    
    items.forEach(item => {
        const itemElement = document.createElement('div');
        itemElement.className = 'dropdown-item';
        itemElement.textContent = item;
        itemElement.addEventListener('click', function() {
            handleUploadDropdownSelection(type, item);
            const dropdown = type === 'database' ? uploadDatabaseDropdown : uploadTableDropdown;
            const bsDropdown = bootstrap.Dropdown.getInstance(dropdown);
            if (bsDropdown) bsDropdown.hide();
        });
        listElement.appendChild(itemElement);
    });
    
    searchElement.value = '';
}

function filterUploadDropdown(type, searchTerm) {
    const listElement = type === 'database' ? uploadDatabaseList : uploadTableList;
    const items = type === 'database' ? uploadAllDatabases : uploadAllTables.map(table => table.name);
    
    listElement.innerHTML = '';
    
    const filteredItems = items.filter(item => 
        item.toLowerCase().includes(searchTerm.toLowerCase())
    );
    
    if (filteredItems.length === 0) {
        const noResults = document.createElement('div');
        noResults.className = 'no-results';
        noResults.textContent = 'No matching items found';
        listElement.appendChild(noResults);
        return;
    }
    
    filteredItems.forEach(item => {
        const itemElement = document.createElement('div');
        itemElement.className = 'dropdown-item';
        itemElement.textContent = item;
        itemElement.addEventListener('click', function() {
            handleUploadDropdownSelection(type, item);
            const dropdown = type === 'database' ? uploadDatabaseDropdown : uploadTableDropdown;
            const bsDropdown = bootstrap.Dropdown.getInstance(dropdown);
            if (bsDropdown) bsDropdown.hide();
        });
        listElement.appendChild(itemElement);
    });
}

function handleUploadDropdownSelection(type, selectedValue) {
    if (type === 'database') {
        uploadDatabaseText.textContent = selectedValue;
        loadUploadTables(selectedValue);
    } else if (type === 'table') {
        uploadTableText.textContent = selectedValue;
        uploadSelectedTableName = selectedValue;
        
        const selectedTable = uploadAllTables.find(table => table.name === selectedValue);
        if (selectedTable) {
            uploadSelectedTableLocation = selectedTable.location;
            uploadS3LocationDiv.textContent = uploadSelectedTableLocation;
            uploadS3LocationDiv.style.color = '#000';
        }
    }
    updateUploadButtonState();
}

function resetUploadTableSelection() {
    uploadTableText.textContent = 'Select table...';
    uploadTableDropdown.disabled = true;
    uploadTableList.innerHTML = '';
    uploadTableSearch.value = '';
    uploadAllTables = [];
    uploadSelectedTableName = '';
    uploadSelectedTableLocation = '';
    uploadS3LocationDiv.textContent = 'No table selected';
    uploadS3LocationDiv.style.color = '#6c757d';
    updateUploadButtonState();
}

function updateUploadButtonState() {
    const hasFile = selectedZipFile !== null;
    const hasS3Path = customS3PathInput.value.trim() !== '' || uploadSelectedTableLocation !== '';
    
    uploadBtn.disabled = !(hasFile && hasS3Path);
}

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
        hideElement(uploadLoading);
        
        if (data.error) {
            showError(uploadError, data.error);
        } else {
            showElement(uploadSuccess);
            uploadSuccess.textContent = data.message || 'Files uploaded successfully!';
            setTimeout(() => hideElement(uploadSuccess), 5000);
            console.log(`Upload successful: ${data.file_count} files uploaded`);
        }
    })
    .catch(error => {
        hideElement(uploadLoading);
        showError(uploadError, `Upload failed: ${error.message}`);
    });
}

// Initialize both sections when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('Page loaded, initializing application...');
    loadDatabases(); // Existing download section
    initializeUploadSection(); // New upload section
    
    // Your existing download section event listeners remain the same
    // ...
});