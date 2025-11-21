// DOM elements - updated for datalist
const databaseInput = document.getElementById('databaseInput');
const databaseOptions = document.getElementById('databaseOptions');
const tableInput = document.getElementById('tableInput');
const tableOptions = document.getElementById('tableOptions');
const s3LocationDiv = document.getElementById('s3Location');
const downloadBtn = document.getElementById('downloadBtn');

// Loading and error elements
const databaseLoading = document.getElementById('databaseLoading');
const databaseError = document.getElementById('databaseError');
const tableLoading = document.getElementById('tableLoading');
const tableError = document.getElementById('tableError');
const downloadLoading = document.getElementById('downloadLoading');
const downloadError = document.getElementById('downloadError');
const downloadSuccess = document.getElementById('downloadSuccess');

// Current state
let currentS3Path = '';
let allDatabases = [];
let allTables = [];

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    console.log('Page loaded, initializing application...');
    loadDatabases();
    
    // Event listeners for database input
    databaseInput.addEventListener('input', function() {
        const databaseName = this.value.trim();
        console.log('Database input:', databaseName);
        
        // Check if the input matches a valid database
        if (databaseName && allDatabases.includes(databaseName)) {
            console.log('Valid database selected:', databaseName);
            loadTables(databaseName);
        } else {
            resetTableSelection();
            resetS3Location();
        }
    });
    
    databaseInput.addEventListener('focus', function() {
        // Clear any previous selection when focusing
        if (this.value && !allDatabases.includes(this.value)) {
            this.value = '';
            resetTableSelection();
            resetS3Location();
        }
    });
    
    // Event listeners for table input
    tableInput.addEventListener('input', function() {
        const tableName = this.value.trim();
        console.log('Table input:', tableName);
        
        // Find the selected table and its location
        const selectedTable = allTables.find(table => table.name === tableName);
        if (selectedTable) {
            currentS3Path = selectedTable.location;
            s3LocationDiv.textContent = currentS3Path;
            s3LocationDiv.style.color = '#000';
            downloadBtn.disabled = false;
            console.log('Table selected, S3 path:', currentS3Path);
        } else {
            resetS3Location();
        }
    });
    
    tableInput.addEventListener('focus', function() {
        // Clear any previous selection when focusing
        if (this.value && !allTables.find(table => table.name === this.value)) {
            this.value = '';
            resetS3Location();
        }
    });
    
    // Download button
    downloadBtn.addEventListener('click', function() {
        if (currentS3Path) {
            console.log('Download initiated for:', currentS3Path);
            downloadFiles(currentS3Path);
        }
    });
});

function loadDatabases() {
    console.log('Loading databases from API...');
    
    databaseInput.placeholder = 'Loading databases...';
    databaseInput.disabled = true;
    showElement(databaseLoading);
    hideElement(databaseError);
    
    fetch('/api/databases')
        .then(response => {
            console.log('Database API response status:', response.status);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Database API response data:', data);
            hideElement(databaseLoading);
            databaseInput.disabled = false;
            databaseInput.placeholder = 'Type to search databases...';
            
            if (data.error) {
                showError(databaseError, data.error);
                return;
            }
            
            // Store all databases and populate datalist
            allDatabases = data.databases || [];
            populateDatalist(databaseOptions, allDatabases);
            console.log(`Loaded ${allDatabases.length} databases`);
        })
        .catch(error => {
            hideElement(databaseLoading);
            databaseInput.disabled = false;
            databaseInput.placeholder = 'Error loading databases';
            const errorMsg = `Failed to load databases: ${error.message}`;
            showError(databaseError, errorMsg);
            console.error('Database fetch error:', error);
        });
}

function loadTables(databaseName) {
    // Reset table selection
    resetTableSelection();
    tableInput.disabled = true;
    tableInput.placeholder = 'Loading tables...';
    
    console.log(`Loading tables for database: ${databaseName}`);
    showElement(tableLoading);
    hideElement(tableError);
    
    fetch(`/api/tables/${encodeURIComponent(databaseName)}`)
        .then(response => {
            console.log('Tables API response status:', response.status);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Tables API response data:', data);
            hideElement(tableLoading);
            tableInput.disabled = false;
            tableInput.placeholder = 'Type to search tables...';
            
            if (data.error) {
                showError(tableError, data.error);
                return;
            }
            
            // Store all tables and populate datalist
            allTables = data.tables || [];
            const tableNames = allTables.map(table => table.name);
            populateDatalist(tableOptions, tableNames);
            console.log(`Loaded ${allTables.length} tables`);
        })
        .catch(error => {
            hideElement(tableLoading);
            tableInput.disabled = false;
            tableInput.placeholder = 'Error loading tables';
            const errorMsg = `Failed to load tables: ${error.message}`;
            showError(tableError, errorMsg);
            console.error('Tables fetch error:', error);
        });
}

function populateDatalist(datalistElement, items) {
    // Clear existing options
    datalistElement.innerHTML = '';
    
    // Add new options
    items.forEach(item => {
        const option = document.createElement('option');
        option.value = item;
        datalistElement.appendChild(option);
    });
}

function resetTableSelection() {
    tableInput.value = '';
    tableInput.disabled = true;
    tableInput.placeholder = 'First select a database';
    tableOptions.innerHTML = '';
    allTables = [];
    resetS3Location();
}

function resetS3Location() {
    s3LocationDiv.textContent = 'No table selected';
    s3LocationDiv.style.color = '#6c757d';
    downloadBtn.disabled = true;
    currentS3Path = '';
}

function downloadFiles(s3Path) {
    showElement(downloadLoading);
    hideElement(downloadError);
    hideElement(downloadSuccess);
    
    fetch('/api/download_files', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ s3_path: s3Path })
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
        hideElement(downloadLoading);
        
        // Create download link
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = 's3_files.zip';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        showElement(downloadSuccess);
        setTimeout(() => hideElement(downloadSuccess), 3000);
    })
    .catch(error => {
        hideElement(downloadLoading);
        showError(downloadError, `Download failed: ${error.message}`);
    });
}

function showElement(element) {
    element.style.display = 'block';
}

function hideElement(element) {
    element.style.display = 'none';
}

function showError(element, message) {
    element.textContent = message;
    element.style.display = 'block';
}