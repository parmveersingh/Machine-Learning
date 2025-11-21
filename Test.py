function downloadFiles(s3Path, tableName) {
    showElement(downloadLoading);
    hideElement(downloadError);
    hideElement(downloadSuccess);
    
    fetch('/api/download_files', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
            s3_path: s3Path,
            table_name: tableName  // Pass table name for ZIP filename
        })
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
        
        // Create download link - filename will be set by backend from table_name
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
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

// Update the download button click handler to get table name
downloadBtn.addEventListener('click', function() {
    if (currentS3Path) {
        const tableName = tableText.textContent;
        // Make sure we have a valid table name (not the placeholder)
        if (tableName && tableName !== 'Select table...') {
            console.log('Download initiated for:', currentS3Path, 'Table:', tableName);
            downloadFiles(currentS3Path, tableName);
        } else {
            showError(downloadError, 'Please select a valid table first');
        }
    }
});