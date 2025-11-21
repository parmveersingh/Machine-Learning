// DOM elements
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
    
    // Database input event listeners
    databaseInput.addEventListener('focus', function() {
        console.log('Database input focused');
        this.removeAttribute('readonly');
        this.placeholder = 'Start typing to search...';
        // Clear selection if invalid
        if (this.value && !allDatabases.includes(this.value)) {
            this.value = '';
            resetTableSelection();
            resetS3Location();
        }
    });
    
    databaseInput.addEventListener('blur', function() {
        console.log('Database input blurred');
        // Set back to readonly after a delay to allow selection
        setTimeout(() => {
            if (this.value && allDatabases.includes(this.value)) {
                this.setAttribute('readonly', 'true');
                this.placeholder = this.value;
            } else if (!this.value) {
                this.setAttribute('readonly', 'true');
                this.placeholder = 'Click to select database...';
            }
        }, 200);
    });
    
    databaseInput.addEventListener('input', function() {
        const databaseName = this.value.trim();
        console.log('Database input:', databaseName);
        
        // Check if the input matches a valid database
        if (databaseName && allDatabases.includes(databaseName)) {
            console.log('Valid database selected:', databaseName);
            this.setAttribute('readonly', 'true');
            this.placeholder = databaseName;
            loadTables(databaseName);
        }
    });
    
    // Table input event listeners
    tableInput.addEventListener('focus', function() {
        if (!this.disabled) {
            console.log('Table input focused');
            this.removeAttribute('readonly');
            this.placeholder = 'Start typing to search...';
            // Clear selection if invalid
            const currentTable = this.value;
            if (currentTable && !allTables.find(table => table.name === currentTable)) {
                this.value = '';
                resetS3Location();
            }
        }
    });
    
    tableInput.addEventListener('blur', function() {
        if (!this.disabled) {
            console.log('Table input blurred');
            setTimeout(() => {
                if (this.value && allTables.find(table => table.name === this.value)) {
                    this.setAttribute('readonly', 'true');
                    this.placeholder = this.value;
                } else if (!this.value) {
                    this.setAttribute('readonly', 'true');
                    this.placeholder = 'Click to select table...';
                }
            }, 200);
        }
    });
    
    tableInput.addEventListener('input', function() {
        if (!this.disabled) {
            const tableName = this.value.trim();
            console.log('Table input:', tableName);
            
            // Find the selected table and its location
            const selectedTable = allTables.find(table => table.name === tableName);
            if (selectedTable) {
                this.setAttribute('readonly', 'true');
                this.placeholder = tableName;
                currentS3Path = selectedTable.location;
                s3LocationDiv.textContent = currentS3Path;
                s3LocationDiv.style.color = '#000';
                downloadBtn.disabled = false;
                console.log('Table selected, S3 path:', currentS3Path);
            }
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
            
            if (data.error) {
                showError(databaseError, data.error);
                databaseInput.placeholder = 'Error loading databases';
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
            tableInput.placeholder = 'Click to select table...';
            
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
    tableInput.setAttribute('readonly', 'true');
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

// ... rest of the functions remain the same (downloadFiles, showElement, hideElement, showError)