import zipfile
import tempfile
import os
from urllib.parse import urlparse

@app.route('/api/upload_files', methods=['POST'])
def upload_files():
    """API endpoint to upload and extract ZIP files to S3 path"""
    try:
        # Check if the post request has the file part
        if 'zip_file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        zip_file = request.files['zip_file']
        s3_path = request.form.get('s3_path')
        
        if not zip_file or zip_file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not s3_path:
            return jsonify({'error': 'S3 path is required'}), 400
        
        # Validate file is a ZIP
        if not zip_file.filename.lower().endswith('.zip'):
            return jsonify({'error': 'File must be a ZIP archive'}), 400
        
        logger.info(f"Uploading and extracting ZIP file to: {s3_path}")
        
        # Parse S3 path
        if s3_path.startswith('s3://'):
            parsed = urlparse(s3_path)
            bucket_name = parsed.netloc
            base_prefix = parsed.path.lstrip('/')
        else:
            return jsonify({'error': f"Invalid S3 path format: {s3_path}"}), 400
        
        # Ensure base prefix ends with /
        if not base_prefix.endswith('/'):
            base_prefix = base_prefix + '/'
        
        s3_client = get_s3_client()
        
        # Create temporary directory for extraction
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_path = os.path.join(temp_dir, zip_file.filename)
            zip_file.save(zip_path)
            
            # Extract ZIP file
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
                
                uploaded_files = 0
                
                # Walk through extracted files and upload to S3
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        
                        # Calculate relative path from extraction root
                        relative_path = os.path.relpath(file_path, temp_dir)
                        
                        # Create S3 key by combining base prefix and relative path
                        s3_key = base_prefix + relative_path.replace('\\', '/')  # Windows path fix
                        
                        # Upload file to S3
                        with open(file_path, 'rb') as f:
                            s3_client.put_object(
                                Bucket=bucket_name,
                                Key=s3_key,
                                Body=f
                            )
                        
                        uploaded_files += 1
                        logger.info(f"Uploaded file to: s3://{bucket_name}/{s3_key}")
        
        logger.info(f"Upload completed. {uploaded_files} files uploaded to S3.")
        return jsonify({
            'success': True,
            'message': f'Successfully uploaded {uploaded_files} files to {s3_path}',
            'file_count': uploaded_files
        })
    
    except zipfile.BadZipFile:
        error_msg = 'Invalid ZIP file format'
        logger.error(error_msg)
        return jsonify({'error': error_msg}), 400
    except ClientError as e:
        error_msg = f"AWS S3 error: {str(e)}"
        logger.error(error_msg)
        return jsonify({'error': error_msg}), 500
    except Exception as e:
        error_msg = f"Upload error: {str(e)}"
        logger.error(error_msg)
        return jsonify({'error': error_msg}), 500