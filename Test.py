@app.route('/api/upload_files', methods=['POST'])
def upload_files():
    """API endpoint to extract ZIP and upload individual files/folders to S3"""
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
        
        logger.info(f"Extracting and uploading ZIP contents to: {s3_path}")
        
        # Parse S3 path
        if s3_path.startswith('s3://'):
            parsed = urlparse(s3_path)
            bucket_name = parsed.netloc
            base_prefix = parsed.path.lstrip('/')
        else:
            return jsonify({'error': f"Invalid S3 path format: {s3_path}"}), 400
        
        # Ensure base prefix ends with / (so we're uploading INTO this folder)
        if not base_prefix.endswith('/'):
            base_prefix = base_prefix + '/'
        
        s3_client = get_s3_client()
        
        # Create temporary directory for extraction
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_path = os.path.join(temp_dir, zip_file.filename)
            zip_file.save(zip_path)
            
            uploaded_files = 0
            uploaded_folders = set()
            
            # Extract ZIP file and upload individual files
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                # Get list of all files in the ZIP
                file_list = zip_ref.namelist()
                
                for file_info in file_list:
                    # Extract each file to temp directory
                    extracted_path = zip_ref.extract(file_info, temp_dir)
                    
                    # Check if it's a directory (ends with / in ZIP)
                    if file_info.endswith('/'):
                        # It's a directory - we'll create it in S3 by putting objects with the path
                        folder_key = base_prefix + file_info
                        uploaded_folders.add(folder_key)
                        logger.info(f"Created folder: s3://{bucket_name}/{folder_key}")
                    else:
                        # It's a file - upload it to S3
                        s3_key = base_prefix + file_info
                        
                        # Upload the actual file content
                        with open(extracted_path, 'rb') as f:
                            s3_client.put_object(
                                Bucket=bucket_name,
                                Key=s3_key,
                                Body=f
                            )
                        
                        uploaded_files += 1
                        logger.info(f"Uploaded file: s3://{bucket_name}/{s3_key}")
            
            # Note: In S3, folders are implicit (created when objects are placed with paths)
            # So we don't need to explicitly create empty folders
            
            # If no files were uploaded but we have folders, it might be an empty ZIP or only folders
            if uploaded_files == 0 and len(uploaded_folders) == 0:
                return jsonify({'error': 'ZIP file is empty or contains no files'}), 400
        
        logger.info(f"Upload completed. {uploaded_files} files uploaded to S3.")
        return jsonify({
            'success': True,
            'message': f'Successfully extracted and uploaded {uploaded_files} files to {s3_path}',
            'file_count': uploaded_files,
            'folder_count': len(uploaded_folders)
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