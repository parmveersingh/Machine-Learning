// Update the handleUpload function to include delete logic
function handleUpload() {
    if (!selectedZipFile) {
        showError(uploadError, 'Please select a ZIP file');
        return;
    }
    
    const customPath = customS3PathInput.value.trim();
    const s3Path = customPath || uploadSelectedTableLocation;
    const isCustomPath = customPath !== '';
    
    if (!s3Path) {
        showError(uploadError, 'Please select a target S3 path');
        return;
    }
    
    // Determine if we should delete existing files
    // Only delete when using table selection (not custom path) AND checkbox is checked
    const deleteCheckbox = document.getElementById('deleteExisting');
    const shouldDelete = !isCustomPath && deleteCheckbox.checked;
    
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
    
    console.log(`Uploading to: ${s3Path}, Delete existing: ${shouldDelete}, Is custom path: ${isCustomPath}`);
    
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
            let successMessage = `Successfully uploaded ${data.file_count} files to ${s3Path}`;
            if (data.deletion_performed && data.files_deleted > 0) {
                successMessage += ` (${data.files_deleted} existing files were deleted)`;
            } else if (data.deletion_performed) {
                successMessage += ' (No existing files to delete)';
            }
            
            showSuccess(uploadSuccess, successMessage);
            setTimeout(() => hideElement(uploadSuccess), 7000);
            console.log(`Upload successful: ${data.file_count} files uploaded`);
        }
    })
    .catch(error => {
        setButtonLoading(uploadBtn, false);
        hideElement(uploadLoading);
        showError(uploadError, `Upload failed: ${error.message}`);
    });
}

// Update the updateUploadButtonState function
function updateUploadButtonState() {
    const hasFile = selectedZipFile !== null;
    const hasS3Path = customS3PathInput.value.trim() !== '' || uploadSelectedTableLocation !== '';
    
    uploadBtn.disabled = !(hasFile && hasS3Path);
    
    // Update delete checkbox state based on whether using custom path
    const deleteCheckbox = document.getElementById('deleteExisting');
    const isCustomPath = customS3PathInput.value.trim() !== '';
    
    if (isCustomPath) {
        deleteCheckbox.disabled = true;
        deleteCheckbox.checked = false;
        deleteCheckbox.parentElement.classList.add('text-muted');
    } else {
        deleteCheckbox.disabled = false;
        deleteCheckbox.parentElement.classList.remove('text-muted');
    }
}

// Update event listeners for custom path input
customS3PathInput.addEventListener('input', function() {
    updateUploadButtonState();
    updateDeleteCheckboxState();
});

// Add function to update delete checkbox state
function updateDeleteCheckboxState() {
    const deleteCheckbox = document.getElementById('deleteExisting');
    const isCustomPath = customS3PathInput.value.trim() !== '';
    
    if (isCustomPath) {
        deleteCheckbox.disabled = true;
        deleteCheckbox.checked = false;
        // Add visual indication
        const label = deleteCheckbox.nextElementSibling;
        label.innerHTML = '<strong>Delete existing files before upload</strong> <span class="text-muted">(disabled for custom paths)</span>';
    } else {
        deleteCheckbox.disabled = false;
        // Restore original label
        const label = deleteCheckbox.nextElementSibling;
        label.innerHTML = '<strong>Delete existing files before upload</strong>';
    }
}

// Update the handleUploadDropdownSelection to reset delete checkbox when table is selected
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
    
    // Clear custom path input when selecting from dropdown
    customS3PathInput.value = '';
    updateUploadButtonState();
    updateDeleteCheckboxState();
}