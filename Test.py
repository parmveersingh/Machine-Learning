// Update the handleUpload function to include database and table names
function handleUpload() {
    if (!selectedZipFile) {
        showError(uploadError, 'Please select a ZIP file');
        return;
    }
    
    const customPath = customS3PathInput.value.trim();
    const s3Path = customPath || uploadSelectedTableLocation;
    const isCustomPath = customPath !== '';
    const deleteCheckbox = document.getElementById('deleteExisting');
    const shouldDelete = !isCustomPath && deleteCheckbox.checked;
    
    if (!s3Path) {
        showError(uploadError, 'Please select a target S3 path');
        return;
    }
    
    // Confirm deletion if enabled
    if (shouldDelete) {
        if (!confirm(`Are you sure you want to delete all existing files at:\n${s3Path}\n\nThis action cannot be undone.`)) {
            return;
        }
    }
    
    setButtonLoading(uploadBtn, true);
    showElement(uploadLoading);
    hideElement(uploadError);
    hideElement(uploadSuccess);
    
    const formData = new FormData();
    formData.append('zip_file', selectedZipFile);
    formData.append('s3_path', s3Path);
    formData.append('delete_existing', shouldDelete.toString());
    formData.append('is_custom_path', isCustomPath.toString());
    
    // Add database and table names if using table selection
    if (!isCustomPath && uploadSelectedDatabase && uploadSelectedTableName) {
        formData.append('database_name', uploadSelectedDatabase);
        formData.append('table_name', uploadSelectedTableName);
    }
    
    console.log(`Uploading to: ${s3Path}, Delete: ${shouldDelete}, Custom: ${isCustomPath}`);
    console.log(`Database: ${uploadSelectedDatabase}, Table: ${uploadSelectedTableName}`);
    
    fetch('/api/upload_files', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        setButtonLoading(uploadBtn, false);
        hideElement(uploadLoading);
        
        if (data.error) {
            showError(uploadError, data.error);
        } else {
            let successMessage = `✅ Successfully uploaded ${data.file_count} files to ${s3Path}`;
            
            // Add deletion info if applicable
            if (data.deletion_performed && data.files_deleted > 0) {
                successMessage += `\n🗑️ ${data.files_deleted} existing files were deleted`;
            } else if (data.deletion_performed) {
                successMessage += `\nℹ️ No existing files to delete`;
            }
            
            // Add MSCK REPAIR info if applicable
            if (data.msck_repair_run) {
                if (data.msck_success) {
                    successMessage += `\n🔧 MSCK REPAIR completed successfully`;
                    if (data.msck_message) {
                        successMessage += `: ${data.msck_message}`;
                    }
                } else {
                    successMessage += `\n⚠️ Files uploaded successfully but MSCK REPAIR failed`;
                    if (data.msck_message) {
                        successMessage += `:\n${data.msck_message}`;
                    }
                    successMessage += `\n📝 Please run MSCK REPAIR manually on the table.`;
                }
            }
            
            showSuccess(uploadSuccess, successMessage);
            setTimeout(() => hideElement(uploadSuccess), 10000); // Longer timeout for more info
            console.log(`Upload successful: ${data.file_count} files uploaded`);
        }
    })
    .catch(error => {
        setButtonLoading(uploadBtn, false);
        hideElement(uploadLoading);
        showError(uploadError, `Upload failed: ${error.message}`);
    });
}

// Add manual MSCK REPAIR button functionality
function addManualMsckRepairButton() {
    // Create a manual MSCK REPAIR button for the download section
    const downloadSection = document.querySelector('.section-body:first-child');
    const afterDownloadButton = downloadSection.querySelector('#downloadSuccess').parentElement;
    
    const msckButton = document.createElement('button');
    msckButton.id = 'msckRepairBtn';
    msckButton.className = 'btn btn-warning mt-2';
    msckButton.innerHTML = '<i class="fas fa-sync-alt"></i> Run MSCK REPAIR';
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
    
    afterDownloadButton.parentNode.insertBefore(msckButton, afterDownloadButton.nextSibling);
    afterDownloadButton.parentNode.insertBefore(msckLoading, msckButton.nextSibling);
    afterDownloadButton.parentNode.insertBefore(msckError, msckLoading.nextSibling);
    afterDownloadButton.parentNode.insertBefore(msckSuccess, msckError.nextSibling);
    
    // Update MSCK button state based on table selection
    function updateMsckButtonState() {
        const msckBtn = document.getElementById('msckRepairBtn');
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
            msckButton.innerHTML = '<i class="fas fa-sync-alt"></i> Run MSCK REPAIR';
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
            msckButton.innerHTML = '<i class="fas fa-sync-alt"></i> Run MSCK REPAIR';
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
}

// Update the handleDropdownSelection to trigger event for MSCK button
function handleDropdownSelection(type, selectedItem) {
    if (type === 'database') {
        databaseText.textContent = selectedItem;
        loadTables(selectedItem);
    } else if (type === 'table') {
        // selectedItem is the table object
        tableText.textContent = selectedItem.name;
        selectedTableName = selectedItem.name;
        
        currentS3Path = selectedItem.location;
        s3LocationDiv.textContent = currentS3Path;
        s3LocationDiv.style.color = '#000';
        downloadBtn.disabled = false;
        console.log('Table selected:', selectedTableName, 'S3 path:', currentS3Path);
        
        // Trigger custom event for MSCK button
        const event = new CustomEvent('tableSelected', { detail: { tableName: selectedTableName } });
        document.dispatchEvent(event);
    }
}

// Initialize MSCK REPAIR button when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // ... existing initialization code ...
    
    // Add MSCK REPAIR button after initialization
    setTimeout(() => {
        addManualMsckRepairButton();
    }, 1000);
});

/* MSCK REPAIR Button Styling */
.btn-warning {
    background: linear-gradient(135deg, #f39c12, #e67e22);
    color: white;
    border: none;
}

.btn-warning:hover {
    background: linear-gradient(135deg, #e67e22, #d35400);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(243, 156, 18, 0.4);
}

.btn-warning:disabled {
    background: #e9ecef;
    color: #6c757d;
    transform: none;
    box-shadow: none;
    cursor: not-allowed;
}

/* Success message with line breaks */
.alert-success {
    white-space: pre-line;
    line-height: 1.6;
}
