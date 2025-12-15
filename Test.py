// Replace the addManualMsckRepairButton function with this fixed version
function addManualMsckRepairButton() {
    // Wait for the DOM to be fully ready
    setTimeout(() => {
        // Find the download section container more safely
        const downloadBtn = document.getElementById('downloadBtn');
        
        if (!downloadBtn) {
            console.error('Download button not found');
            return;
        }
        
        // Get the parent container (form-section)
        const downloadSection = downloadBtn.closest('.form-section');
        
        if (!downloadSection) {
            console.error('Download section container not found');
            return;
        }
        
        // Create MSCK REPAIR button and related elements
        const msckButton = document.createElement('button');
        msckButton.id = 'msckRepairBtn';
        msckButton.className = 'btn btn-warning mt-2';
        msckButton.innerHTML = '<i class="fas fa-sync-alt me-2"></i>Run MSCK REPAIR';
        msckButton.disabled = true;
        
        const msckLoading = document.createElement('div');
        msckLoading.id = 'msckLoading';
        msckLoading.className = 'loading mt-1';
        msckLoading.innerHTML = '<div class="spinner-border spinner-border-sm" role="status"></div> Running MSCK REPAIR...';
        
        const msckError = document.createElement('div');
        msckError.id = 'msckError';
        msckError.className = 'alert-message alert-error mt-1';
        
        const msckSuccess = document.createElement('div');
        msckSuccess.id = 'msckSuccess';
        msckSuccess.className = 'alert-message alert-success mt-1';
        msckSuccess.style.display = 'none';
        
        // Insert the MSCK REPAIR elements after the download button
        downloadSection.appendChild(msckButton);
        downloadSection.appendChild(msckLoading);
        downloadSection.appendChild(msckError);
        downloadSection.appendChild(msckSuccess);
        
        // Update MSCK button state based on table selection
        function updateMsckButtonState() {
            const msckBtn = document.getElementById('msckRepairBtn');
            if (!msckBtn) return;
            
            if (selectedTableName && selectedTableName !== 'Select table...') {
                msckBtn.disabled = false;
                msckBtn.title = `Run MSCK REPAIR on ${selectedTableName}`;
            } else {
                msckBtn.disabled = true;
                msckBtn.title = 'Select a table first';
            }
        }
        
        // Add event listener for MSCK REPAIR button
        msckButton.addEventListener('click', function() {
            if (!selectedTableName || selectedTableName === 'Select table...') {
                showError(msckError, 'Please select a table first');
                return;
            }
            
            const databaseName = databaseText.textContent;
            if (databaseName === 'Select database...' || !databaseName) {
                showError(msckError, 'Please select a database first');
                return;
            }
            
            if (!confirm(`Run MSCK REPAIR TABLE on ${databaseName}.${selectedTableName}?\n\nThis will update the Glue catalog with new partitions.`)) {
                return;
            }
            
            // Show loading state
            msckButton.disabled = true;
            msckButton.innerHTML = '<div class="spinner-border spinner-border-sm me-2" role="status"></div>Processing...';
            showElement(msckLoading);
            hideElement(msckError);
            hideElement(msckSuccess);
            
            fetch('/api/run_msck_repair', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    database_name: databaseName,
                    table_name: selectedTableName
                })
            })
            .then(response => response.json())
            .then(data => {
                // Reset button
                msckButton.disabled = false;
                msckButton.innerHTML = '<i class="fas fa-sync-alt me-2"></i>Run MSCK REPAIR';
                hideElement(msckLoading);
                
                if (data.error || !data.success) {
                    showError(msckError, data.error || 'MSCK REPAIR failed');
                } else {
                    showSuccess(msckSuccess, data.message || 'MSCK REPAIR completed successfully');
                    setTimeout(() => hideElement(msckSuccess), 5000);
                }
            })
            .catch(error => {
                msckButton.disabled = false;
                msckButton.innerHTML = '<i class="fas fa-sync-alt me-2"></i>Run MSCK REPAIR';
                hideElement(msckLoading);
                showError(msckError, `MSCK REPAIR failed: ${error.message}`);
            });
        });
        
        // Update MSCK button when table is selected
        document.addEventListener('tableSelected', function() {
            updateMsckButtonState();
        });
        
        // Also update when database selection changes
        databaseText.addEventListener('DOMSubtreeModified', function() {
            updateMsckButtonState();
        });
        
        // Initial update
        updateMsckButtonState();
        
    }, 500); // Wait 500ms for DOM to be ready
}

// Alternative: Simpler version without complex DOM traversal
function addManualMsckRepairButtonSimple() {
    // Create a container div for MSCK REPAIR button
    const msckContainer = document.createElement('div');
    msckContainer.id = 'msckContainer';
    msckContainer.className = 'mt-2';
    
    // Create the button and elements
    const msckButton = document.createElement('button');
    msckButton.id = 'msckRepairBtn';
    msckButton.className = 'btn btn-warning';
    msckButton.innerHTML = '<i class="fas fa-sync-alt me-2"></i>Run MSCK REPAIR';
    msckButton.disabled = true;
    
    const msckLoading = document.createElement('div');
    msckLoading.id = 'msckLoading';
    msckLoading.className = 'loading mt-1';
    msckLoading.innerHTML = '<div class="spinner-border spinner-border-sm" role="status"></div> Running MSCK REPAIR...';
    
    const msckError = document.createElement('div');
    msckError.id = 'msckError';
    msckError.className = 'alert-message alert-error mt-1';
    
    const msckSuccess = document.createElement('div');
    msckSuccess.id = 'msckSuccess';
    msckSuccess.className = 'alert-message alert-success mt-1';
    
    // Add elements to container
    msckContainer.appendChild(msckButton);
    msckContainer.appendChild(msckLoading);
    msckContainer.appendChild(msckError);
    msckContainer.appendChild(msckSuccess);
    
    // Find where to insert - after the download section's last element
    const downloadSection = document.querySelector('#downloadBtn')?.closest('.form-section');
    if (downloadSection) {
        downloadSection.appendChild(msckContainer);
    } else {
        // Fallback: Add to body or specific location
        console.warn('Download section not found, adding MSCK button to body');
        document.body.appendChild(msckContainer);
    }
    
    // Rest of the button functionality remains the same as above
    // ... [same event listeners and updateMsckButtonState function]
}