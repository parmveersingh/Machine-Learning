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
        #s3Location {
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
    </style>
</head>
<body>
    <div class="container mt-5">
        <div class="row">
            <div class="col-md-8 offset-md-2">
                <h1 class="mb-4">AWS Glue Catalog File Downloader</h1>
                
                <!-- Database Selection -->
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
                
                <!-- Table Selection -->
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
                
                <!-- S3 Location Display -->
                <div class="mb-3">
                    <label class="form-label">S3 Location:</label>
                    <div id="s3Location" class="p-3 border rounded">
                        No table selected
                    </div>
                </div>
                
                <!-- Download Button -->
                <div class="mb-3">
                    <button id="downloadBtn" class="btn btn-primary" disabled>
                        Download Files
                    </button>
                    <div id="downloadLoading" class="loading mt-1">
                        <div class="spinner-border spinner-border-sm" role="status"></div>
                        Preparing download...
                    </div>
                    <div id="downloadError" class="error-message mt-1"></div>
                    <div id="downloadSuccess" class="text-success mt-1" style="display: none;">
                        Download started successfully!
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script src="{{ url_for('static', filename='script.js') }}"></script>
</body>
</html>