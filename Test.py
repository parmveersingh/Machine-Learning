function loadTables(databaseName) {
    // Reset table selection
    resetTableSelection();
    tableSelect.disabled = true;

    console.log(`Loading tables for database: ${databaseName}`);
    showElement(tableLoading);
    hideElement(tableError);

    fetch(`/api/tables/${encodeURIComponent(databaseName)}`)
        .then(response => {
            console.log('Tables API response status:', response.status);
            if (!response.ok) {
                // If response is not OK, try to get error message from response body
                return response.json().then(errorData => {
                    throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
                }).catch(() => {
                    // If we can't parse JSON, throw with status only
                    throw new Error(`HTTP error! status: ${response.status}`);
                });
            }
            return response.json();
        })
        .then(data => {
            console.log('Tables API response data:', data);
            hideElement(tableLoading);
            tableSelect.disabled = false;

            // Check if data exists and has error property
            if (data && data.error) {
                showError(tableError, data.error);
                console.error('Tables API error:', data.error);
                return;
            }

            // Check if tables array exists
            if (!data || !data.tables) {
                showError(tableError, 'Invalid response from server');
                return;
            }

            // Populate table dropdown
            tableSelect.innerHTML = '<option value="">-- Select a Table --</option>';
            if (data.tables.length > 0) {
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
            const errorMsg = `Failed to load tables: ${error.message}`;
            showError(tableError, errorMsg);
            console.error('Tables fetch error:', error);
        });
}