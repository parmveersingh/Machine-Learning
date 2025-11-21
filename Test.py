// Fix the upload section initialization
function initializeUploadSection() {
    console.log('Initializing upload section...');
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
    
    // Upload database dropdown events - FIXED
    uploadDatabaseSearch.addEventListener('input', function() {
        console.log('Upload database search:', this.value);
        filterUploadDropdown('database', this.value);
    });
    
    // Upload table dropdown events - FIXED
    uploadTableSearch.addEventListener('input', function() {
        console.log('Upload table search:', this.value);
        filterUploadDropdown('table', this.value);
    });
    
    // Custom S3 path input event
    customS3PathInput.addEventListener('input', function() {
        updateUploadButtonState();
    });
    
    // Upload button event
    uploadBtn.addEventListener('click', handleUpload);
}

// Fix the loadUploadTables function
function loadUploadTables(databaseName) {
    uploadSelectedDatabase = databaseName;
    
    // Reset table selection
    resetUploadTableSelection();
    uploadTableDropdown.disabled = true;
    uploadTableText.textContent = 'Loading tables...';
    
    console.log(`Loading tables for upload database: ${databaseName}`);
    showElement(uploadTableLoading);
    hideElement(uploadTableError);
    
    fetch(`/api/tables/${encodeURIComponent(databaseName)}`)
        .then(response => {
            console.log('Upload Tables API response status:', response.status);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Upload Tables API response data:', data);
            hideElement(uploadTableLoading);
            uploadTableDropdown.disabled = false;
            
            if (data.error) {
                showError(uploadTableError, data.error);
                uploadTableText.textContent = 'Error loading tables';
                return;
            }
            
            // Store all tables and populate dropdown - FIXED
            uploadAllTables = data.tables || [];
            console.log('Upload tables stored:', uploadAllTables);
            
            // Populate the dropdown with table names
            populateUploadDropdown('table', uploadAllTables);
            console.log(`Loaded ${uploadAllTables.length} tables for upload section`);
        })
        .catch(error => {
            hideElement(uploadTableLoading);
            uploadTableDropdown.disabled = false;
            uploadTableText.textContent = 'Error loading tables';
            const errorMsg = `Failed to load tables: ${error.message}`;
            showError(uploadTableError, errorMsg);
            console.error('Upload Tables fetch error:', error);
        });
}

// Fix the populateUploadDropdown function for tables
function populateUploadDropdown(type, items) {
    console.log(`Populating upload ${type} dropdown with:`, items);
    
    let listElement, displayItems;
    
    if (type === 'database') {
        listElement = uploadDatabaseList;
        displayItems = items; // items are database names (strings)
        uploadAllDatabases = items || [];
    } else if (type === 'table') {
        listElement = uploadTableList;
        // items are table objects, extract names for display
        uploadAllTables = items || [];
        displayItems = uploadAllTables.map(table => table.name);
        console.log('Upload table names for display:', displayItems);
    }
    
    // Clear existing items
    listElement.innerHTML = '';
    
    if (!displayItems || displayItems.length === 0) {
        const noResults = document.createElement('div');
        noResults.className = 'no-results';
        noResults.textContent = 'No items found';
        listElement.appendChild(noResults);
        return;
    }
    
    // Add items to dropdown
    displayItems.forEach((item, index) => {
        const itemElement = document.createElement('div');
        itemElement.className = 'dropdown-item';
        itemElement.textContent = item;
        itemElement.title = item;
        
        // Store the actual table object reference if it's a table
        if (type === 'table') {
            itemElement.dataset.tableIndex = index;
        }
        
        itemElement.addEventListener('click', function() {
            console.log(`Upload ${type} selected:`, item);
            
            if (type === 'database') {
                handleUploadDropdownSelection(type, item);
            } else if (type === 'table') {
                // For tables, get the full table object
                const tableIndex = this.dataset.tableIndex;
                const tableObject = uploadAllTables[tableIndex];
                handleUploadDropdownSelection(type, tableObject);
            }
            
            const dropdown = type === 'database' ? uploadDatabaseDropdown : uploadTableDropdown;
            const bsDropdown = bootstrap.Dropdown.getInstance(dropdown);
            if (bsDropdown) bsDropdown.hide();
            
            if (type === 'database') {
                uploadDatabaseSearch.value = '';
            } else {
                uploadTableSearch.value = '';
            }
        });
        
        listElement.appendChild(itemElement);
    });
    
    if (type === 'database') {
        uploadDatabaseSearch.value = '';
    } else {
        uploadTableSearch.value = '';
    }
}

// Fix the filterUploadDropdown function
function filterUploadDropdown(type, searchTerm) {
    console.log(`Filtering upload ${type} with: "${searchTerm}"`);
    
    let listElement, items, displayItems;
    
    if (type === 'database') {
        listElement = uploadDatabaseList;
        items = uploadAllDatabases;
        displayItems = items;
    } else if (type === 'table') {
        listElement = uploadTableList;
        items = uploadAllTables;
        // For tables, filter based on table names but keep the objects
        displayItems = items ? items.map(table => table.name) : [];
    }
    
    console.log(`Total upload ${type}s:`, displayItems.length);
    
    // Clear existing items
    listElement.innerHTML = '';
    
    if (!displayItems || displayItems.length === 0) {
        const noResults = document.createElement('div');
        noResults.className = 'no-results';
        noResults.textContent = 'No items found';
        listElement.appendChild(noResults);
        return;
    }
    
    // Filter items based on search term
    const filteredItems = items.filter((item, index) => {
        const displayName = type === 'table' ? item.name : item;
        if (!searchTerm || searchTerm.trim() === '') {
            return true; // Show all items when search is empty
        }
        return displayName.toLowerCase().includes(searchTerm.toLowerCase());
    });
    
    const filteredDisplayNames = filteredItems.map(item => 
        type === 'table' ? item.name : item
    );
    
    console.log(`Filtered upload ${type}s:`, filteredDisplayNames.length);
    
    if (filteredItems.length === 0) {
        const noResults = document.createElement('div');
        noResults.className = 'no-results';
        noResults.textContent = `No ${type}s match "${searchTerm}"`;
        listElement.appendChild(noResults);
        return;
    }
    
    // Add filtered items to dropdown
    filteredItems.forEach((item, index) => {
        const displayName = type === 'table' ? item.name : item;
        const itemElement = document.createElement('div');
        itemElement.className = 'dropdown-item';
        itemElement.textContent = displayName;
        itemElement.title = displayName;
        
        // Store the actual table object reference if it's a table
        if (type === 'table') {
            itemElement.dataset.tableIndex = uploadAllTables.indexOf(item);
        }
        
        itemElement.addEventListener('click', function() {
            console.log(`Upload ${type} selected:`, displayName);
            
            if (type === 'database') {
                handleUploadDropdownSelection(type, item);
            } else if (type === 'table') {
                handleUploadDropdownSelection(type, item);
            }
            
            const dropdown = type === 'database' ? uploadDatabaseDropdown : uploadTableDropdown;
            const bsDropdown = bootstrap.Dropdown.getInstance(dropdown);
            if (bsDropdown) bsDropdown.hide();
            
            if (type === 'database') {
                uploadDatabaseSearch.value = '';
            } else {
                uploadTableSearch.value = '';
            }
        });
        
        listElement.appendChild(itemElement);
    });
}

// Fix the handleUploadDropdownSelection function for tables
function handleUploadDropdownSelection(type, selectedItem) {
    if (type === 'database') {
        uploadDatabaseText.textContent = selectedItem;
        loadUploadTables(selectedItem);
    } else if (type === 'table') {
        // selectedItem is the table object
        uploadTableText.textContent = selectedItem.name;
        uploadSelectedTableName = selectedItem.name;
        
        uploadSelectedTableLocation = selectedItem.location;
        uploadS3LocationDiv.textContent = uploadSelectedTableLocation;
        uploadS3LocationDiv.style.color = '#000';
        console.log('Upload table selected:', uploadSelectedTableName, 'S3 path:', uploadSelectedTableLocation);
    }
    updateUploadButtonState();
}

// Add debug function to check upload table data
function debugUploadTableData() {
    console.log('=== DEBUG UPLOAD TABLE DATA ===');
    console.log('uploadAllTables:', uploadAllTables);
    console.log('uploadDatabaseText:', uploadDatabaseText.textContent);
    console.log('uploadTableText:', uploadTableText.textContent);
    
    if (uploadAllTables && uploadAllTables.length > 0) {
        console.log('First upload table object:', uploadAllTables[0]);
        console.log('Upload table name:', uploadAllTables[0].name);
        console.log('Upload table location:', uploadAllTables[0].location);
    } else {
        console.log('No upload tables loaded');
    }
}

// Update the DOMContentLoaded to ensure both sections work
document.addEventListener('DOMContentLoaded', function() {
    console.log('Initializing AWS Glue Catalog Manager...');
    
    // Initialize all dropdowns
    const dropdownElementList = [].slice.call(document.querySelectorAll('.dropdown-toggle'));
    const dropdownList = dropdownElementList.map(function (dropdownToggleEl) {
        return new bootstrap.Dropdown(dropdownToggleEl);
    });
    
    // Prevent dropdown from closing when clicking inside
    document.querySelectorAll('.dropdown-menu').forEach(function (dropdown) {
        dropdown.addEventListener('click', function (e) {
            e.stopPropagation();
        });
    });
    
    // Initialize dropdown search functionality
    initializeDropdownSearch();
    
    // Download section event listeners
    databaseSearch.addEventListener('input', function() {
        console.log('Database search input:', this.value);
        filterDropdown('database', this.value);
    });
    
    tableSearch.addEventListener('input', function() {
        console.log('Table search input:', this.value);
        filterDropdown('table', this.value);
    });
    
    // Download button event
    downloadBtn.addEventListener('click', function() {
        if (currentS3Path && selectedTableName) {
            console.log('Download initiated - Table:', selectedTableName, 'Path:', currentS3Path);
            downloadFiles(currentS3Path, selectedTableName);
        } else {
            showError(downloadError, 'Please select a table first');
        }
    });
    
    loadDatabases(); // Load databases for download section
    initializeUploadSection(); // Initialize upload section
    
    // Debug after a short delay to see if both sections are working
    setTimeout(() => {
        console.log('=== INITIALIZATION COMPLETE ===');
        console.log('Download databases loaded:', allDatabases.length);
        console.log('Upload databases loaded:', uploadAllDatabases.length);
    }, 2000);
});