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
    loadDatabases();

    // Event listeners
    databaseSelect.addEventListener('change', function() {
        const databaseName = this.value;
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
        } else {
            resetS3Location();
        }
    });

    downloadBtn.addEventListener('click', function() {
        if (currentS3Path) {
            downloadFiles(currentS3Path);
        }
    });
});

function loadDatabases() {
    showElement(databaseLoading);
    hideElement(databaseError);

    fetch('/api/databases')
        .then(response => response.json())
        .then(data => {
            hideElement(databaseLoading);

            if (data.error) {
                showError(databaseError, data.error);
                return;
            }

            // Populate database dropdown
            databaseSelect.innerHTML = '<option value="">-- Select a Database --</option>';
            data.databases.forEach(db => {
                const option = document.createElement('option');
                option.value = db;
                option.textContent = db;
                databaseSelect.appendChild(option);
            });
        })
        .catch(error => {
            hideElement(databaseLoading);
            showError(databaseError, `Failed to load databases: ${error.message}`);
        });
}

function loadTables(databaseName) {
    // Reset table selection
    resetTableSelection();
    tableSelect.disabled = true;

    showElement(tableLoading);
    hideElement(tableError);

    fetch(`/api/tables/${encodeURIComponent(databaseName)}`)
        .then(response => response.json())
        .then(data => {
            hideElement(tableLoading);
            tableSelect.disabled = false;

            if (data.error) {
                showError(tableError, data.error);
                return;
            }

            // Populate table dropdown
            tableSelect.innerHTML = '<option value="">-- Select a Table --</option>';
            data.tables.forEach(table => {
                const option = document.createElement('option');
                option.value = table.name;
                option.textContent = table.name;
                option.dataset.location = table.location;
                tableSelect.appendChild(option);
            });
        })
        .catch(error => {
            hideElement(tableLoading);
            tableSelect.disabled = false;
            showError(tableError, `Failed to load tables: ${error.message}`);
        });
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

function resetTableSelection() {
    tableSelect.innerHTML = '<option value="">-- First select a database --</option>';
    tableSelect.disabled = true;
    resetS3Location();
}

function resetS3Location() {
    s3LocationDiv.textContent = 'No table selected';
    s3LocationDiv.style.color = '#6c757d';
    downloadBtn.disabled = true;
    currentS3Path = '';
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
