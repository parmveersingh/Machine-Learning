@app.route('/api/upload_files', methods=['POST'])
def upload_files():
    """API endpoint to extract ZIP and upload individual files/folders to S3 - robust version"""
    try:
        if 'zip_file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        zip_file = request.files['zip_file']
        s3_path = request.form.get('s3_path')
        
        if not zip_file or zip_file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not s3_path:
            return jsonify({'error': 'S3 path is required'}), 400
        
        if not zip_file.filename.lower().endswith('.zip'):
            return jsonify({'error': 'File must be a ZIP archive'}), 400
        
        logger.info(f"Extracting and uploading ZIP contents to: {s3_path}")
        
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
        
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_path = os.path.join(temp_dir, zip_file.filename)
            zip_file.save(zip_path)
            
            uploaded_files = 0
            
            # Extract entire ZIP first
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # Walk through the extracted directory structure
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    
                    # Calculate relative path from extraction root
                    relative_path = os.path.relpath(file_path, temp_dir)
                    
                    # Convert to S3 key format (use forward slashes)
                    s3_key = base_prefix + relative_path.replace('\\', '/')
                    
                    # Upload file to S3
                    with open(file_path, 'rb') as f:
                        s3_client.put_object(
                            Bucket=bucket_name,
                            Key=s3_key,
                            Body=f
                        )
                    
                    uploaded_files += 1
                    logger.info(f"Uploaded: s3://{bucket_name}/{s3_key}")
            
            if uploaded_files == 0:
                return jsonify({'error': 'No files found in ZIP archive'}), 400
        
        logger.info(f"Upload completed. {uploaded_files} files uploaded.")
        return jsonify({
            'success': True,
            'message': f'Successfully extracted and uploaded {uploaded_files} files to {s3_path}',
            'file_count': uploaded_files
        })
    
    except zipfile.BadZipFile:
        error_msg = 'Invalid or corrupted ZIP file'
        logger.error(error_msg)
        return jsonify({'error': error_msg}), 400
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'NoSuchBucket':
            error_msg = f"Bucket does not exist: {bucket_name}"
        else:
            error_msg = f"AWS S3 error: {str(e)}"
        logger.error(error_msg)
        return jsonify({'error': error_msg}), 500
    except Exception as e:
        error_msg = f"Upload error: {str(e)}"
        logger.error(error_msg)
        return jsonify({'error': error_msg}), 500