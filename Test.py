// Fix the populateDropdown function for tables
function populateDropdown(type, items) {
    console.log(`Populating ${type} dropdown with:`, items);
    
    let listElement, displayItems;
    
    if (type === 'database') {
        listElement = databaseList;
        displayItems = items; // items are database names (strings)
        allDatabases = items || [];
    } else if (type === 'table') {
        listElement = tableList;
        // items are table objects, we need to extract names for display
        allTables = items || [];
        displayItems = allTables.map(table => table.name);
        console.log('Table names for display:', displayItems);
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
            console.log(`${type} selected:`, item);
            
            if (type === 'database') {
                handleDropdownSelection(type, item);
            } else if (type === 'table') {
                // For tables, we need to get the full table object
                const tableIndex = this.dataset.tableIndex;
                const tableObject = allTables[tableIndex];
                handleDropdownSelection(type, tableObject);
            }
            
            // Hide the dropdown
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
    
    // Reset search
    if (type === 'database') {
        databaseSearch.value = '';
    } else {
        tableSearch.value = '';
    }
}

// Fix the filterDropdown function for tables
function filterDropdown(type, searchTerm) {
    console.log(`Filtering ${type} with: "${searchTerm}"`);
    
    let listElement, items, displayItems;
    
    if (type === 'database') {
        listElement = databaseList;
        items = allDatabases;
        displayItems = items;
    } else if (type === 'table') {
        listElement = tableList;
        items = allTables;
        // For tables, we filter based on table names but keep the objects
        displayItems = items ? items.map(table => table.name) : [];
    }
    
    console.log(`Total ${type}s:`, displayItems.length);
    
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
    
    console.log(`Filtered ${type}s:`, filteredDisplayNames.length);
    
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
            itemElement.dataset.tableIndex = allTables.indexOf(item);
        }
        
        itemElement.addEventListener('click', function() {
            console.log(`${type} selected:`, displayName);
            
            if (type === 'database') {
                handleDropdownSelection(type, item);
            } else if (type === 'table') {
                handleDropdownSelection(type, item);
            }
            
            // Hide the dropdown
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

// Fix the handleDropdownSelection function for tables
function handleDropdownSelection(type, selectedItem) {
    if (type === 'database') {
        databaseText.textContent = selectedItem;
        loadTables(selectedItem);
    } else if (type === 'table') {
        // selectedItem is now the table object
        tableText.textContent = selectedItem.name;
        selectedTableName = selectedItem.name;
        
        currentS3Path = selectedItem.location;
        s3LocationDiv.textContent = currentS3Path;
        s3LocationDiv.style.color = '#000';
        downloadBtn.disabled = false;
        console.log('Table selected:', selectedTableName, 'S3 path:', currentS3Path);
    }
}

// Fix the upload section functions similarly
function populateUploadDropdown(type, items) {
    console.log(`Populating upload ${type} dropdown with:`, items);
    
    let listElement, displayItems;
    
    if (type === 'database') {
        listElement = uploadDatabaseList;
        displayItems = items;
        uploadAllDatabases = items || [];
    } else if (type === 'table') {
        listElement = uploadTableList;
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
        
        if (type === 'table') {
            itemElement.dataset.tableIndex = index;
        }
        
        itemElement.addEventListener('click', function() {
            console.log(`Upload ${type} selected:`, item);
            
            if (type === 'database') {
                handleUploadDropdownSelection(type, item);
            } else if (type === 'table') {
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
            return true;
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

function handleUploadDropdownSelection(type, selectedItem) {
    if (type === 'database') {
        uploadDatabaseText.textContent = selectedItem;
        loadUploadTables(selectedItem);
    } else if (type === 'table') {
        uploadTableText.textContent = selectedItem.name;
        uploadSelectedTableName = selectedItem.name;
        
        const selectedTable = uploadAllTables.find(table => table.name === selectedItem.name);
        if (selectedTable) {
            uploadSelectedTableLocation = selectedTable.location;
            uploadS3LocationDiv.textContent = uploadSelectedTableLocation;
            uploadS3LocationDiv.style.color = '#000';
        }
    }
    updateUploadButtonState();
}

// Add debug function to check table data
function debugTableData() {
    console.log('=== DEBUG TABLE DATA ===');
    console.log('allTables:', allTables);
    console.log('uploadAllTables:', uploadAllTables);
    
    if (allTables && allTables.length > 0) {
        console.log('First table object:', allTables[0]);
        console.log('Table name:', allTables[0].name);
        console.log('Table location:', allTables[0].location);
    }
    
    if (uploadAllTables && uploadAllTables.length > 0) {
        console.log('First upload table object:', uploadAllTables[0]);
        console.log('Upload table name:', uploadAllTables[0].name);
        console.log('Upload table location:', uploadAllTables[0].location);
    }
}

// Call debug in loadTables to see what's happening
function loadTables(databaseName) {
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
            console.log('Raw tables data from API:', data.tables);
            populateDropdown('table', data.tables);
            console.log(`Loaded ${data.tables ? data.tables.length : 0} tables`);
            
            // Debug the table data
            debugTableData();
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