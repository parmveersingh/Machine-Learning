// DOM elements
const databaseDropdown = document.getElementById('databaseDropdown');
const databaseText = document.getElementById('databaseText');
const databaseSearch = document.getElementById('databaseSearch');
const databaseList = document.getElementById('databaseList');
const tableDropdown = document.getElementById('tableDropdown');
const tableText = document.getElementById('tableText');
const tableSearch = document.getElementById('tableSearch');
const tableList = document.getElementById('tableList');
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
let selectedDatabase = '';

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    console.log('Page loaded, initializing application...');
    loadDatabases();
    
    // Database dropdown events
    databaseSearch.addEventListener('input', function() {
        filterDropdown('database', this.value);
    });
    
    // Table dropdown events
    tableSearch.addEventListener('input', function() {
        filterDropdown('table', this.value);
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
    
    databaseDropdown.disabled = true;
    databaseText.textContent = 'Loading databases...';
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
            databaseDropdown.disabled = false;
            
            if (data.error) {
                showError(databaseError, data.error);
                databaseText.textContent = 'Error loading databases';
                return;
            }
            
            // Store all databases and populate dropdown
            allDatabases = data.databases || [];
            populateDropdown('database', allDatabases);
            console.log(`Loaded ${allDatabases.length} databases`);
        })
        .catch(error => {
            hideElement(databaseLoading);
            databaseDropdown.disabled = false;
            databaseText.textContent = 'Error loading databases';
            const errorMsg = `Failed to load databases: ${error.message}`;
            showError(databaseError, errorMsg);
            console.error('Database fetch error:', error);
        });
}

function loadTables(databaseName) {
    selectedDatabase = databaseName;
    
    // Reset table selection
    resetTableSelection();
    tableDropdown.disabled = true;
    tableText.textContent = 'Loading tables...';
    
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
            tableDropdown.disabled = false;
            
            if (data.error) {
                showError(tableError, data.error);
                tableText.textContent = 'Error loading tables';
                return;
            }
            
            // Store all tables and populate dropdown
            allTables = data.tables || [];
            const tableNames = allTables.map(table => table.name);
            populateDropdown('table', tableNames);
            console.log(`Loaded ${allTables.length} tables`);
        })
        .catch(error => {
            hideElement(tableLoading);
            tableDropdown.disabled = false;
            tableText.textContent = 'Error loading tables';
            const errorMsg = `Failed to load tables: ${error.message}`;
            showError(tableError, errorMsg);
            console.error('Tables fetch error:', error);
        });
}

function populateDropdown(type, items) {
    const listElement = type === 'database' ? databaseList : tableList;
    const searchElement = type === 'database' ? databaseSearch : tableSearch;
    
    // Clear existing items
    listElement.innerHTML = '';
    
    if (items.length === 0) {
        const noResults = document.createElement('div');
        noResults.className = 'no-results';
        noResults.textContent = 'No items found';
        listElement.appendChild(noResults);
        return;
    }
    
    // Add items to dropdown
    items.forEach(item => {
        const itemElement = document.createElement('div');
        itemElement.className = 'dropdown-item';
        itemElement.textContent = item;
        itemElement.addEventListener('click', function() {
            handleDropdownSelection(type, item);
            // Hide the dropdown
            const dropdown = type === 'database' ? databaseDropdown : tableDropdown;
            const bsDropdown = bootstrap.Dropdown.getInstance(dropdown);
            if (bsDropdown) {
                bsDropdown.hide();
            }
        });
        listElement.appendChild(itemElement);
    });
    
    // Reset search
    searchElement.value = '';
}

function filterDropdown(type, searchTerm) {
    const listElement = type === 'database' ? databaseList : tableList;
    const items = type === 'database' ? allDatabases : allTables.map(table => table.name);
    
    // Clear existing items
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
    
    // Add filtered items
    filteredItems.forEach(item => {
        const itemElement = document.createElement('div');
        itemElement.className = 'dropdown-item';
        itemElement.textContent = item;
        itemElement.addEventListener('click', function() {
            handleDropdownSelection(type, item);
            // Hide the dropdown
            const dropdown = type === 'database' ? databaseDropdown : tableDropdown;
            const bsDropdown = bootstrap.Dropdown.getInstance(dropdown);
            if (bsDropdown) {
                bsDropdown.hide();
            }
        });
        listElement.appendChild(itemElement);
    });
}

function handleDropdownSelection(type, selectedValue) {
    if (type === 'database') {
        databaseText.textContent = selectedValue;
        loadTables(selectedValue);
    } else if (type === 'table') {
        tableText.textContent = selectedValue;
        
        // Find the selected table and set S3 location
        const selectedTable = allTables.find(table => table.name === selectedValue);
        if (selectedTable) {
            currentS3Path = selectedTable.location;
            s3LocationDiv.textContent = currentS3Path;
            s3LocationDiv.style.color = '#000';
            downloadBtn.disabled = false;
            console.log('Table selected, S3 path:', currentS3Path);
        }
    }
}

function resetTableSelection() {
    tableText.textContent = 'Select table...';
    tableDropdown.disabled = true;
    tableList.innerHTML = '';
    tableSearch.value = '';
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