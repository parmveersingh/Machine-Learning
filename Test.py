function downloadFiles(s3Path) {
    showElement(downloadLoading);
    hideElement(downloadError);
    hideElement(downloadSuccess);
    
    fetch('/api/download_files', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
            s3_path: s3Path
            // Removed table_name parameter
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
        
        // Create download link
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = 's3_files.zip'; // This will be overridden by backend, but kept for fallback
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

// Update the download button click handler
downloadBtn.addEventListener('click', function() {
    if (currentS3Path) {
        console.log('Download initiated for exact path:', currentS3Path);
        downloadFiles(currentS3Path); // Only pass s3Path, not table name
    }
});