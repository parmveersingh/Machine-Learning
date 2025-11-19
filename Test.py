// DOM elements
const databaseSelect = document.getElementById('databaseSelect');
const tableSelect = document.getElementById('tableSelect');
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

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    console.log('Page loaded, initializing database dropdown...');
    loadDatabases();
    
    // Event listeners
    databaseSelect.addEventListener('change', function() {
        const databaseName = this.value;
        console.log('Database selected:', databaseName);
        if (databaseName) {
            loadTables(databaseName);
        } else {
            resetTableSelection();
            resetS3Location();
        }
    });
    
    tableSelect.addEventListener('change', function() {
        const selectedOption = this.options[this.selectedIndex];
        if (selectedOption && selectedOption.dataset.location) {
            currentS3Path = selectedOption.dataset.location;
            s3LocationDiv.textContent = currentS3Path;
            s3LocationDiv.style.color = '#000';
            downloadBtn.disabled = false;
            console.log('Table selected, S3 path:', currentS3Path);
        } else {
            resetS3Location();
        }
    });
    
    downloadBtn.addEventListener('click', function() {
        if (currentS3Path) {
            console.log('Download initiated for:', currentS3Path);
            downloadFiles(currentS3Path);
        }
    });
});

function loadDatabases() {
    console.log('Loading databases...');
    showElement(databaseLoading);
    hideElement(databaseError);
    databaseSelect.disabled = true;
    
    fetch('/api/databases')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            hideElement(databaseLoading);
            databaseSelect.disabled = false;
            
            if (data.error) {
                showError(databaseError, data.error);
                console.error('Database API error:', data.error);
                return;
            }
            
            // Populate database dropdown
            databaseSelect.innerHTML = '<option value="">-- Select a Database --</option>';
            if (data.databases && data.databases.length > 0) {
                data.databases.forEach(db => {
                    const option = document.createElement('option');
                    option.value = db;
                    option.textContent = db;
                    databaseSelect.appendChild(option);
                });
                console.log(`Loaded ${data.databases.length} databases`);
            } else {
                console.warn('No databases found');
                const option = document.createElement('option');
                option.value = '';
                option.textContent = 'No databases found';
                databaseSelect.appendChild(option);
            }
        })
        .catch(error => {
            hideElement(databaseLoading);
            databaseSelect.disabled = false;
            showError(databaseError, `Failed to load databases: ${error.message}`);
            console.error('Database fetch error:', error);
        });
}

function loadTables(databaseName) {
    // Reset table selection
    resetTableSelection();
    tableSelect.disabled = true;
    
    console.log(`Loading tables for database: ${databaseName}`);
    showElement(tableLoading);
    hideElement(tableError);
    
    fetch(`/api/tables/${encodeURIComponent(databaseName)}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            hideElement(tableLoading);
            tableSelect.disabled = false;
            
            if (data.error) {
                showError(tableError, data.error);
                console.error('Tables API error:', data.error);
                return;
            }
            
            // Populate table dropdown
            tableSelect.innerHTML = '<option value="">-- Select a Table --</option>';
            if (data.tables && data.tables.length > 0) {
                data.tables.forEach(table => {
                    const option = document.createElement('option');
                    option.value = table.name;
                    option.textContent = table.name;
                    option.dataset.location = table.location;
                    tableSelect.appendChild(option);
                });
                console.log(`Loaded ${data.tables.length} tables`);
            } else {
                console.warn('No tables found in database:', databaseName);
                const option = document.createElement('option');
                option.value = '';
                option.textContent = 'No tables found';
                tableSelect.appendChild(option);
            }
        })
        .catch(error => {
            hideElement(tableLoading);
            tableSelect.disabled = false;
            showError(tableError, `Failed to load tables: ${error.message}`);
            console.error('Tables fetch error:', error);
        });
}

// ... rest of the functions remain the same (downloadFiles, resetTableSelection, etc.)