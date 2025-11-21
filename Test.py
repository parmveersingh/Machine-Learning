// Update the DOMContentLoaded event listener for download section
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
});

// Fix the filterDropdown function
function filterDropdown(type, searchTerm) {
    console.log(`Filtering ${type} with: "${searchTerm}"`);
    
    let listElement, items;
    
    if (type === 'database') {
        listElement = databaseList;
        items = allDatabases;
    } else if (type === 'table') {
        listElement = tableList;
        items = allTables.map(table => table.name);
    } else {
        console.error('Unknown filter type:', type);
        return;
    }
    
    console.log(`Total ${type}s:`, items.length);
    
    // Clear existing items
    listElement.innerHTML = '';
    
    if (!items || items.length === 0) {
        const noResults = document.createElement('div');
        noResults.className = 'no-results';
        noResults.textContent = 'No items found';
        listElement.appendChild(noResults);
        return;
    }
    
    // Filter items based on search term
    const filteredItems = items.filter(item => {
        if (!searchTerm || searchTerm.trim() === '') {
            return true; // Show all items when search is empty
        }
        return item.toLowerCase().includes(searchTerm.toLowerCase());
    });
    
    console.log(`Filtered ${type}s:`, filteredItems.length);
    
    if (filteredItems.length === 0) {
        const noResults = document.createElement('div');
        noResults.className = 'no-results';
        noResults.textContent = `No ${type}s match "${searchTerm}"`;
        listElement.appendChild(noResults);
        return;
    }
    
    // Add filtered items to dropdown
    filteredItems.forEach(item => {
        const itemElement = document.createElement('div');
        itemElement.className = 'dropdown-item';
        itemElement.textContent = item;
        itemElement.title = item;
        itemElement.addEventListener('click', function() {
            console.log(`${type} selected:`, item);
            handleDropdownSelection(type, item);
            
            // Hide the dropdown after selection
            const dropdown = type === 'database' ? databaseDropdown : tableDropdown;
            const bsDropdown = bootstrap.Dropdown.getInstance(dropdown);
            if (bsDropdown) {
                bsDropdown.hide();
            }
            
            // Clear search term after selection
            if (type === 'database') {
                databaseSearch.value = '';
            } else {
                tableSearch.value = '';
            }
        });
        listElement.appendChild(itemElement);
    });
}

// Fix the filterUploadDropdown function
function filterUploadDropdown(type, searchTerm) {
    console.log(`Filtering upload ${type} with: "${searchTerm}"`);
    
    let listElement, items;
    
    if (type === 'database') {
        listElement = uploadDatabaseList;
        items = uploadAllDatabases;
    } else if (type === 'table') {
        listElement = uploadTableList;
        items = uploadAllTables.map(table => table.name);
    } else {
        console.error('Unknown filter type:', type);
        return;
    }
    
    console.log(`Total upload ${type}s:`, items.length);
    
    // Clear existing items
    listElement.innerHTML = '';
    
    if (!items || items.length === 0) {
        const noResults = document.createElement('div');
        noResults.className = 'no-results';
        noResults.textContent = 'No items found';
        listElement.appendChild(noResults);
        return;
    }
    
    // Filter items based on search term
    const filteredItems = items.filter(item => {
        if (!searchTerm || searchTerm.trim() === '') {
            return true; // Show all items when search is empty
        }
        return item.toLowerCase().includes(searchTerm.toLowerCase());
    });
    
    console.log(`Filtered upload ${type}s:`, filteredItems.length);
    
    if (filteredItems.length === 0) {
        const noResults = document.createElement('div');
        noResults.className = 'no-results';
        noResults.textContent = `No ${type}s match "${searchTerm}"`;
        listElement.appendChild(noResults);
        return;
    }
    
    // Add filtered items to dropdown
    filteredItems.forEach(item => {
        const itemElement = document.createElement('div');
        itemElement.className = 'dropdown-item';
        itemElement.textContent = item;
        itemElement.title = item;
        itemElement.addEventListener('click', function() {
            console.log(`Upload ${type} selected:`, item);
            handleUploadDropdownSelection(type, item);
            
            // Hide the dropdown after selection
            const dropdown = type === 'database' ? uploadDatabaseDropdown : uploadTableDropdown;
            const bsDropdown = bootstrap.Dropdown.getInstance(dropdown);
            if (bsDropdown) {
                bsDropdown.hide();
            }
            
            // Clear search term after selection
            if (type === 'database') {
                uploadDatabaseSearch.value = '';
            } else {
                uploadTableSearch.value = '';
            }
        });
        listElement.appendChild(itemElement);
    });
}

// Update the populateDropdown function to use filter functionality
function populateDropdown(type, items) {
    console.log(`Populating ${type} dropdown with ${items.length} items`);
    
    // Just call filterDropdown with empty search term to show all items
    if (type === 'database') {
        allDatabases = items || [];
        filterDropdown('database', '');
    } else if (type === 'table') {
        allTables = items || [];
        filterDropdown('table', '');
    }
}

// Update the populateUploadDropdown function similarly
function populateUploadDropdown(type, items) {
    console.log(`Populating upload ${type} dropdown with ${items.length} items`);
    
    // Just call filterUploadDropdown with empty search term to show all items
    if (type === 'database') {
        uploadAllDatabases = items || [];
        filterUploadDropdown('database', '');
    } else if (type === 'table') {
        uploadAllTables = items || [];
        filterUploadDropdown('table', '');
    }
}

// Add function to clear search when dropdown is shown
function initializeDropdownSearch() {
    // Clear search when dropdown is shown
    const dropdowns = [
        { toggle: databaseDropdown, search: databaseSearch, type: 'database' },
        { toggle: tableDropdown, search: tableSearch, type: 'table' },
        { toggle: uploadDatabaseDropdown, search: uploadDatabaseSearch, type: 'database' },
        { toggle: uploadTableDropdown, search: uploadTableSearch, type: 'table' }
    ];
    
    dropdowns.forEach(({ toggle, search, type }) => {
        toggle.addEventListener('show.bs.dropdown', function() {
            console.log(`${type} dropdown shown, clearing search`);
            search.value = '';
            if (type === 'database') {
                if (toggle.id === 'databaseDropdown') {
                    filterDropdown('database', '');
                } else {
                    filterUploadDropdown('database', '');
                }
            } else {
                if (toggle.id === 'tableDropdown') {
                    filterDropdown('table', '');
                } else {
                    filterUploadDropdown('table', '');
                }
            }
        });
    });
}

// Update the DOMContentLoaded to include dropdown search initialization
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
});