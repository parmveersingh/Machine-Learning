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
            table_name: tableName 
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
        
        // Create download link - filename will be set by backend
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        // Note: We're not setting download attribute here because backend sets the filename
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