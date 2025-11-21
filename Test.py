<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AWS Glue Catalog File Downloader</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .loading {
            display: none;
            color: #6c757d;
        }
        .error-message {
            color: #dc3545;
            display: none;
        }
        .success-message {
            color: #198754;
            display: none;
        }
        #s3Location, #uploadS3Location {
            background-color: #f8f9fa;
            font-family: monospace;
            min-height: 48px;
            padding: 12px;
        }
        .custom-dropdown {
            position: relative;
            width: 100%;
        }
        .dropdown-toggle {
            width: 100%;
            text-align: left;
            padding-right: 40px;
            background: white;
            border: 1px solid #ced4da;
            border-radius: 0.375rem;
            height: 38px;
            display: flex;
            align-items: center;
            padding: 0.375rem 0.75rem;
            cursor: pointer;
        }
        .dropdown-toggle:disabled {
            background-color: #e9ecef;
            cursor: not-allowed;
        }
        .dropdown-toggle::after {
            position: absolute;
            right: 12px;
            top: 50%;
            transform: translateY(-50%);
        }
        .dropdown-menu {
            width: 100%;
            max-height: 300px;
            overflow-y: auto;
        }
        .search-input {
            margin: 8px;
            width: calc(100% - 16px);
        }
        .dropdown-item {
            cursor: pointer;
            padding: 8px 12px;
        }
        .dropdown-item:hover {
            background-color: #f8f9fa;
        }
        .no-results {
            padding: 8px 12px;
            color: #6c757d;
            font-style: italic;
        }
        .section-divider {
            border-top: 2px solid #dee2e6;
            margin: 2rem 0;
            padding-top: 2rem;
        }
        .file-input-wrapper {
            position: relative;
            overflow: hidden;
            display: inline-block;
            width: 100%;
        }
        .file-input-wrapper input[type=file] {
            position: absolute;
            left: 0;
            top: 0;
            opacity: 0;
            width: 100%;
            height: 100%;
            cursor: pointer;
        }
        .file-input-display {
            border: 1px dashed #ced4da;
            border-radius: 0.375rem;
            padding: 12px;
            text-align: center;
            background-color: #f8f9fa;
        }
    </style>
</head>
<body>
    <div class="container mt-5">
        <div class="row">
            <div class="col-md-8 offset-md-2">
                <h1 class="mb-4">AWS Glue Catalog File Manager</h1>
                
                <!-- Download Section -->
                <h3>Download Files from S3</h3>
                <!-- Your existing download section code remains the same -->
                <div class="mb-3">
                    <label class="form-label">Select Database:</label>
                    <div class="custom-dropdown">
                        <button class="dropdown-toggle" type="button" id="databaseDropdown" data-bs-toggle="dropdown" aria-expanded="false">
                            <span id="databaseText">Select database...</span>
                        </button>
                        <div class="dropdown-menu" aria-labelledby="databaseDropdown">
                            <input type="text" class="form-control search-input" placeholder="Search databases..." id="databaseSearch">
                            <div id="databaseList"></div>
                        </div>
                    </div>
                    <div id="databaseLoading" class="loading mt-1">
                        <div class="spinner-border spinner-border-sm" role="status"></div>
                        Loading databases...
                    </div>
                    <div id="databaseError" class="error-message mt-1"></div>
                </div>
                
                <div class="mb-3">
                    <label class="form-label">Select Table:</label>
                    <div class="custom-dropdown">
                        <button class="dropdown-toggle" type="button" id="tableDropdown" data-bs-toggle="dropdown" aria-expanded="false" disabled>
                            <span id="tableText">Select table...</span>
                        </button>
                        <div class="dropdown-menu" aria-labelledby="tableDropdown">
                            <input type="text" class="form-control search-input" placeholder="Search tables..." id="tableSearch">
                            <div id="tableList"></div>
                        </div>
                    </div>
                    <div id="tableLoading" class="loading mt-1">
                        <div class="spinner-border spinner-border-sm" role="status"></div>
                        Loading tables...
                    </div>
                    <div id="tableError" class="error-message mt-1"></div>
                </div>
                
                <div class="mb-3">
                    <label class="form-label">S3 Location:</label>
                    <div id="s3Location" class="p-3 border rounded">
                        No table selected
                    </div>
                </div>
                
                <div class="mb-3">
                    <button id="downloadBtn" class="btn btn-primary" disabled>
                        Download Files
                    </button>
                    <div id="downloadLoading" class="loading mt-1">
                        <div class="spinner-border spinner-border-sm" role="status"></div>
                        Preparing download...
                    </div>
                    <div id="downloadError" class="error-message mt-1"></div>
                    <div id="downloadSuccess" class="success-message mt-1">
                        Download started successfully!
                    </div>
                </div>

                <!-- Upload Section -->
                <div class="section-divider"></div>
                <h3>Upload Files to S3</h3>
                
                <!-- File Upload -->
                <div class="mb-3">
                    <label class="form-label">Select ZIP File to Upload:</label>
                    <div class="file-input-wrapper">
                        <div class="file-input-display" id="fileDisplay">
                            Click to select ZIP file or drag and drop here
                        </div>
                        <input type="file" id="zipFile" accept=".zip" class="form-control">
                    </div>
                    <div id="fileError" class="error-message mt-1"></div>
                </div>
                
                <!-- Target Database Selection -->
                <div class="mb-3">
                    <label class="form-label">Select Target Database:</label>
                    <div class="custom-dropdown">
                        <button class="dropdown-toggle" type="button" id="uploadDatabaseDropdown" data-bs-toggle="dropdown" aria-expanded="false">
                            <span id="uploadDatabaseText">Select database...</span>
                        </button>
                        <div class="dropdown-menu" aria-labelledby="uploadDatabaseDropdown">
                            <input type="text" class="form-control search-input" placeholder="Search databases..." id="uploadDatabaseSearch">
                            <div id="uploadDatabaseList"></div>
                        </div>
                    </div>
                    <div id="uploadDatabaseLoading" class="loading mt-1">
                        <div class="spinner-border spinner-border-sm" role="status"></div>
                        Loading databases...
                    </div>
                    <div id="uploadDatabaseError" class="error-message mt-1"></div>
                </div>
                
                <!-- Target Table Selection -->
                <div class="mb-3">
                    <label class="form-label">Select Target Table:</label>
                    <div class="custom-dropdown">
                        <button class="dropdown-toggle" type="button" id="uploadTableDropdown" data-bs-toggle="dropdown" aria-expanded="false" disabled>
                            <span id="uploadTableText">Select table...</span>
                        </button>
                        <div class="dropdown-menu" aria-labelledby="uploadTableDropdown">
                            <input type="text" class="form-control search-input" placeholder="Search tables..." id="uploadTableSearch">
                            <div id="uploadTableList"></div>
                        </div>
                    </div>
                    <div id="uploadTableLoading" class="loading mt-1">
                        <div class="spinner-border spinner-border-sm" role="status"></div>
                        Loading tables...
                    </div>
                    <div id="uploadTableError" class="error-message mt-1"></div>
                </div>
                
                <!-- Target S3 Path Display -->
                <div class="mb-3">
                    <label class="form-label">Target S3 Location:</label>
                    <div id="uploadS3Location" class="p-3 border rounded">
                        No table selected
                    </div>
                </div>
                
                <!-- Custom S3 Path Input (Optional) -->
                <div class="mb-3">
                    <label for="customS3Path" class="form-label">Or Enter Custom S3 Path:</label>
                    <input type="text" class="form-control" id="customS3Path" placeholder="s3://bucket-name/path/">
                    <div class="form-text">Leave empty to use the table location above</div>
                </div>
                
                <!-- Upload Button -->
                <div class="mb-3">
                    <button id="uploadBtn" class="btn btn-success" disabled>
                        Upload and Extract to S3
                    </button>
                    <div id="uploadLoading" class="loading mt-1">
                        <div class="spinner-border spinner-border-sm" role="status"></div>
                        Uploading files to S3...
                    </div>
                    <div id="uploadError" class="error-message mt-1"></div>
                    <div id="uploadSuccess" class="success-message mt-1">
                        Files uploaded successfully!
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script src="{{ url_for('static', filename='script.js') }}"></script>
</body>
</html>