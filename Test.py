// Update the populateDropdown function for both sections
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
        itemElement.title = item; // Show full text on hover
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
        itemElement.title = item; // Show full text on hover
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

// Update the populateUploadDropdown function
function populateUploadDropdown(type, items) {
    const listElement = type === 'database' ? uploadDatabaseList : uploadTableList;
    const searchElement = type === 'database' ? uploadDatabaseSearch : uploadTableSearch;
    
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
        itemElement.title = item; // Show full text on hover
        itemElement.addEventListener('click', function() {
            handleUploadDropdownSelection(type, item);
            const dropdown = type === 'database' ? uploadDatabaseDropdown : uploadTableDropdown;
            const bsDropdown = bootstrap.Dropdown.getInstance(dropdown);
            if (bsDropdown) bsDropdown.hide();
        });
        listElement.appendChild(itemElement);
    });
    
    // Reset search
    searchElement.value = '';
}

function filterUploadDropdown(type, searchTerm) {
    const listElement = type === 'database' ? uploadDatabaseList : uploadTableList;
    const items = type === 'database' ? uploadAllDatabases : uploadAllTables.map(table => table.name);
    
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
        itemElement.title = item; // Show full text on hover
        itemElement.addEventListener('click', function() {
            handleUploadDropdownSelection(type, item);
            const dropdown = type === 'database' ? uploadDatabaseDropdown : uploadTableDropdown;
            const bsDropdown = bootstrap.Dropdown.getInstance(dropdown);
            if (bsDropdown) bsDropdown.hide();
        });
        listElement.appendChild(itemElement);
    });
}

// Update the handleDropdownSelection functions to use dropdown-toggle-text
function handleDropdownSelection(type, selectedValue) {
    if (type === 'database') {
        databaseText.textContent = selectedValue;
        loadTables(selectedValue);
    } else if (type === 'table') {
        tableText.textContent = selectedValue;
        selectedTableName = selectedValue;
        
        const selectedTable = allTables.find(table => table.name === selectedValue);
        if (selectedTable) {
            currentS3Path = selectedTable.location;
            s3LocationDiv.textContent = currentS3Path;
            s3LocationDiv.style.color = '#000';
            downloadBtn.disabled = false;
            console.log('Table selected:', selectedTableName, 'S3 path:', currentS3Path);
        }
    }
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