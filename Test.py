<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AWS Glue Catalog File Downloader</title>
    <link href="<https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css>" rel="stylesheet">
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
                    <label for="databaseSelect" class="form-label">Select Database:</label>
                    <select class="form-select" id="databaseSelect">
                        <option value="">-- Select a Database --</option>
                    </select>
                    <div id="databaseLoading" class="loading mt-1">Loading databases...</div>
                    <div id="databaseError" class="error-message mt-1"></div>
                </div>

                <!-- Table Selection -->
                <div class="mb-3">
                    <label for="tableSelect" class="form-label">Select Table:</label>
                    <select class="form-select" id="tableSelect" disabled>
                        <option value="">-- First select a database --</option>
                    </select>
                    <div id="tableLoading" class="loading mt-1">Loading tables...</div>
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
                    <div id="downloadLoading" class="loading mt-1">Preparing download...</div>
                    <div id="downloadError" class="error-message mt-1"></div>
                    <div id="downloadSuccess" class="text-success mt-1" style="display: none;">
                        Download started successfully!
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="<https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js>"></script>
    <script src="{{ url_for('static', filename='script.js') }}"></script>
</body>
</html>
