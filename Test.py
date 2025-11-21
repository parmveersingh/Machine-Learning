<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AWS Glue Catalog File Manager</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        :root {
            --primary-color: #2c3e50;
            --secondary-color: #3498db;
            --success-color: #27ae60;
            --warning-color: #f39c12;
            --danger-color: #e74c3c;
            --light-bg: #f8f9fa;
            --card-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            --hover-shadow: 0 8px 15px rgba(0, 0, 0, 0.15);
        }

        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        .app-container {
            background: white;
            border-radius: 15px;
            box-shadow: var(--card-shadow);
            margin: 2rem auto;
            padding: 2rem;
            position: relative;
            overflow: hidden;
        }

        .app-container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--secondary-color), var(--success-color));
        }

        .app-header {
            text-align: center;
            margin-bottom: 2rem;
            padding-bottom: 1rem;
            border-bottom: 2px solid var(--light-bg);
        }

        .app-header h1 {
            color: var(--primary-color);
            font-weight: 700;
            margin-bottom: 0.5rem;
        }

        .app-header .subtitle {
            color: #6c757d;
            font-size: 1.1rem;
        }

        .section-card {
            border: none;
            border-radius: 10px;
            box-shadow: var(--card-shadow);
            margin-bottom: 2rem;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            overflow: hidden;
        }

        .section-card:hover {
            transform: translateY(-2px);
            box-shadow: var(--hover-shadow);
        }

        .section-header {
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            padding: 1rem 1.5rem;
            border-bottom: none;
        }

        .section-header h3 {
            margin: 0;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .section-body {
            padding: 1.5rem;
        }

        .form-label {
            font-weight: 600;
            color: var(--primary-color);
            margin-bottom: 0.5rem;
        }

        .custom-dropdown {
            position: relative;
            width: 100%;
        }

        .dropdown-toggle {
            width: 100%;
            text-align: left;
            padding: 0.75rem 1rem;
            background: white;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            font-size: 0.95rem;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .dropdown-toggle:hover {
            border-color: var(--secondary-color);
        }

        .dropdown-toggle:focus {
            border-color: var(--secondary-color);
            box-shadow: 0 0 0 0.2rem rgba(52, 152, 219, 0.25);
        }

        .dropdown-toggle::after {
            border-top: 0.3em solid;
            border-right: 0.3em solid transparent;
            border-left: 0.3em solid transparent;
        }

        .dropdown-menu {
            border: none;
            border-radius: 8px;
            box-shadow: var(--card-shadow);
            padding: 0.5rem;
            margin-top: 0.5rem;
        }

        .search-input {
            border: 2px solid #e9ecef;
            border-radius: 6px;
            padding: 0.5rem 0.75rem;
            margin-bottom: 0.5rem;
            font-size: 0.9rem;
        }

        .search-input:focus {
            border-color: var(--secondary-color);
            box-shadow: none;
        }

        .dropdown-item {
            padding: 0.75rem 1rem;
            border-radius: 6px;
            margin-bottom: 0.25rem;
            transition: all 0.2s ease;
            font-size: 0.9rem;
        }

        .dropdown-item:hover {
            background-color: var(--secondary-color);
            color: white;
        }

        .s3-location-display {
            background: var(--light-bg);
            border: 2px dashed #dee2e6;
            border-radius: 8px;
            padding: 1rem;
            font-family: 'Courier New', monospace;
            font-size: 0.9rem;
            min-height: 60px;
            display: flex;
            align-items: center;
            word-break: break-all;
        }

        .file-upload-area {
            border: 2px dashed #dee2e6;
            border-radius: 10px;
            padding: 2rem;
            text-align: center;
            background: var(--light-bg);
            transition: all 0.3s ease;
            cursor: pointer;
        }

        .file-upload-area:hover {
            border-color: var(--secondary-color);
            background: #f0f8ff;
        }

        .file-upload-area.dragover {
            border-color: var(--success-color);
            background: #f0fff4;
        }

        .file-upload-icon {
            font-size: 3rem;
            color: var(--secondary-color);
            margin-bottom: 1rem;
        }

        .btn-custom {
            padding: 0.75rem 2rem;
            border-radius: 8px;
            font-weight: 600;
            font-size: 1rem;
            transition: all 0.3s ease;
            border: none;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
        }

        .btn-download {
            background: linear-gradient(135deg, var(--secondary-color), #2980b9);
            color: white;
        }

        .btn-download:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(52, 152, 219, 0.4);
        }

        .btn-upload {
            background: linear-gradient(135deg, var(--success-color), #219653);
            color: white;
        }

        .btn-upload:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(39, 174, 96, 0.4);
        }

        .loading {
            display: none;
            color: var(--secondary-color);
            font-size: 0.9rem;
        }

        .loading .spinner-border {
            width: 1rem;
            height: 1rem;
            margin-right: 0.5rem;
        }

        .alert-message {
            border-radius: 8px;
            padding: 0.75rem 1rem;
            margin-top: 0.5rem;
            font-size: 0.9rem;
            border: none;
        }

        .alert-error {
            background: #fee;
            color: var(--danger-color);
            border-left: 4px solid var(--danger-color);
        }

        .alert-success {
            background: #f0fff4;
            color: var(--success-color);
            border-left: 4px solid var(--success-color);
        }

        .status-badge {
            background: var(--light-bg);
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.8rem;
            color: #6c757d;
            display: inline-flex;
            align-items: center;
            gap: 0.25rem;
        }

        .form-section {
            margin-bottom: 1.5rem;
        }

        .form-section:last-child {
            margin-bottom: 0;
        }

        .custom-path-input {
            border: 2px solid #e9ecef;
            border-radius: 8px;
            padding: 0.75rem 1rem;
            font-size: 0.95rem;
            transition: all 0.3s ease;
        }

        .custom-path-input:focus {
            border-color: var(--secondary-color);
            box-shadow: 0 0 0 0.2rem rgba(52, 152, 219, 0.25);
        }

        @media (max-width: 768px) {
            .app-container {
                margin: 1rem;
                padding: 1.5rem;
            }

            .section-body {
                padding: 1rem;
            }

            .btn-custom {
                width: 100%;
                justify-content: center;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-12 col-lg-10 col-xl-8">
                <div class="app-container">
                    <!-- Header -->
                    <div class="app-header">
                        <h1><i class="fas fa-database me-2"></i>AWS Glue Catalog Manager</h1>
                        <p class="subtitle">Manage S3 files through AWS Glue database and table metadata</p>
                    </div>

                    <!-- Download Section -->
                    <div class="section-card">
                        <div class="section-header">
                            <h3><i class="fas fa-download"></i> Download Files from S3</h3>
                        </div>
                        <div class="section-body">
                            <div class="form-section">
                                <label class="form-label">Select Database</label>
                                <div class="custom-dropdown">
                                    <button class="dropdown-toggle" type="button" id="databaseDropdown" data-bs-toggle="dropdown" aria-expanded="false">
                                        <span id="databaseText">Choose a database...</span>
                                        <i class="fas fa-chevron-down"></i>
                                    </button>
                                    <div class="dropdown-menu" aria-labelledby="databaseDropdown">
                                        <input type="text" class="form-control search-input" placeholder="Search databases..." id="databaseSearch">
                                        <div id="databaseList"></div>
                                    </div>
                                </div>
                                <div id="databaseLoading" class="loading mt-2">
                                    <div class="spinner-border" role="status"></div>
                                    Loading databases...
                                </div>
                                <div id="databaseError" class="alert-message alert-error mt-2"></div>
                            </div>

                            <div class="form-section">
                                <label class="form-label">Select Table</label>
                                <div class="custom-dropdown">
                                    <button class="dropdown-toggle" type="button" id="tableDropdown" data-bs-toggle="dropdown" aria-expanded="false" disabled>
                                        <span id="tableText">Select database first...</span>
                                        <i class="fas fa-chevron-down"></i>
                                    </button>
                                    <div class="dropdown-menu" aria-labelledby="tableDropdown">
                                        <input type="text" class="form-control search-input" placeholder="Search tables..." id="tableSearch">
                                        <div id="tableList"></div>
                                    </div>
                                </div>
                                <div id="tableLoading" class="loading mt-2">
                                    <div class="spinner-border" role="status"></div>
                                    Loading tables...
                                </div>
                                <div id="tableError" class="alert-message alert-error mt-2"></div>
                            </div>

                            <div class="form-section">
                                <label class="form-label">S3 Location</label>
                                <div id="s3Location" class="s3-location-display">
                                    <i class="fas fa-folder me-2 text-muted"></i>
                                    <span class="text-muted">No table selected</span>
                                </div>
                            </div>

                            <div class="form-section">
                                <button id="downloadBtn" class="btn btn-custom btn-download" disabled>
                                    <i class="fas fa-file-download"></i>
                                    Download Files
                                </button>
                                <div id="downloadLoading" class="loading mt-2">
                                    <div class="spinner-border" role="status"></div>
                                    Preparing download...
                                </div>
                                <div id="downloadError" class="alert-message alert-error mt-2"></div>
                                <div id="downloadSuccess" class="alert-message alert-success mt-2" style="display: none;">
                                    <i class="fas fa-check-circle me-2"></i>
                                    Download started successfully!
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Upload Section -->
                    <div class="section-card">
                        <div class="section-header">
                            <h3><i class="fas fa-upload"></i> Upload Files to S3</h3>
                        </div>
                        <div class="section-body">
                            <div class="form-section">
                                <label class="form-label">Select ZIP File</label>
                                <div class="file-upload-area" id="fileUploadArea">
                                    <div class="file-upload-icon">
                                        <i class="fas fa-file-archive"></i>
                                    </div>
                                    <h5>Drop your ZIP file here or click to browse</h5>
                                    <p class="text-muted mb-3">Supported format: .zip</p>
                                    <div id="fileDisplay" class="status-badge">
                                        <i class="fas fa-cloud-upload-alt"></i>
                                        No file selected
                                    </div>
                                    <input type="file" id="zipFile" accept=".zip" class="d-none">
                                </div>
                                <div id="fileError" class="alert-message alert-error mt-2"></div>
                            </div>

                            <div class="form-section">
                                <label class="form-label">Target Database</label>
                                <div class="custom-dropdown">
                                    <button class="dropdown-toggle" type="button" id="uploadDatabaseDropdown" data-bs-toggle="dropdown" aria-expanded="false">
                                        <span id="uploadDatabaseText">Choose a database...</span>
                                        <i class="fas fa-chevron-down"></i>
                                    </button>
                                    <div class="dropdown-menu" aria-labelledby="uploadDatabaseDropdown">
                                        <input type="text" class="form-control search-input" placeholder="Search databases..." id="uploadDatabaseSearch">
                                        <div id="uploadDatabaseList"></div>
                                    </div>
                                </div>
                                <div id="uploadDatabaseLoading" class="loading mt-2">
                                    <div class="spinner-border" role="status"></div>
                                    Loading databases...
                                </div>
                                <div id="uploadDatabaseError" class="alert-message alert-error mt-2"></div>
                            </div>

                            <div class="form-section">
                                <label class="form-label">Target Table</label>
                                <div class="custom-dropdown">
                                    <button class="dropdown-toggle" type="button" id="uploadTableDropdown" data-bs-toggle="dropdown" aria-expanded="false" disabled>
                                        <span id="uploadTableText">Select database first...</span>
                                        <i class="fas fa-chevron-down"></i>
                                    </button>
                                    <div class="dropdown-menu" aria-labelledby="uploadTableDropdown">
                                        <input type="text" class="form-control search-input" placeholder="Search tables..." id="uploadTableSearch">
                                        <div id="uploadTableList"></div>
                                    </div>
                                </div>
                                <div id="uploadTableLoading" class="loading mt-2">
                                    <div class="spinner-border" role="status"></div>
                                    Loading tables...
                                </div>
                                <div id="uploadTableError" class="alert-message alert-error mt-2"></div>
                            </div>

                            <div class="form-section">
                                <label class="form-label">Target S3 Location</label>
                                <div id="uploadS3Location" class="s3-location-display">
                                    <i class="fas fa-folder me-2 text-muted"></i>
                                    <span class="text-muted">No table selected</span>
                                </div>
                            </div>

                            <div class="form-section">
                                <label class="form-label">Custom S3 Path (Optional)</label>
                                <input type="text" class="form-control custom-path-input" id="customS3Path" placeholder="s3://your-bucket/path/">
                                <div class="form-text mt-1">
                                    <i class="fas fa-info-circle me-1"></i>
                                    Leave empty to use the table location above
                                </div>
                            </div>

                            <div class="form-section">
                                <button id="uploadBtn" class="btn btn-custom btn-upload" disabled>
                                    <i class="fas fa-file-export"></i>
                                    Extract & Upload to S3
                                </button>
                                <div id="uploadLoading" class="loading mt-2">
                                    <div class="spinner-border" role="status"></div>
                                    Extracting and uploading files...
                                </div>
                                <div id="uploadError" class="alert-message alert-error mt-2"></div>
                                <div id="uploadSuccess" class="alert-message alert-success mt-2" style="display: none;">
                                    <i class="fas fa-check-circle me-2"></i>
                                    Files uploaded successfully!
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Footer -->
                    <div class="text-center mt-4 pt-3 border-top">
                        <p class="text-muted small">
                            <i class="fas fa-shield-alt me-1"></i>
                            Secure AWS Glue Integration • Built with Flask & Bootstrap 5
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/js/all.min.js"></script>
    <script src="{{ url_for('static', filename='script.js') }}"></script>
</body>
</html>