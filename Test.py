@app.route('/api/upload_files', methods=['POST'])
def upload_files():
    """API endpoint to extract ZIP and upload individual files/folders to S3 with conditional delete"""
    try:
        if 'zip_file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        zip_file = request.files['zip_file']
        s3_path = request.form.get('s3_path')
        delete_existing = request.form.get('delete_existing', 'false').lower() == 'true'
        is_custom_path = request.form.get('is_custom_path', 'false').lower() == 'true'
        
        if not zip_file or zip_file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not s3_path:
            return jsonify({'error': 'S3 path is required'}), 400
        
        if not zip_file.filename.lower().endswith('.zip'):
            return jsonify({'error': 'File must be a ZIP archive'}), 400
        
        logger.info(f"Extracting and uploading ZIP to: {s3_path}")
        logger.info(f"Delete existing: {delete_existing}, Is custom path: {is_custom_path}")
        
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
        
        # Conditionally delete existing files
        files_deleted = 0
        if delete_existing and not is_custom_path:
            logger.info(f"Deleting existing files from: s3://{bucket_name}/{base_prefix}")
            files_deleted = delete_existing_files(s3_client, bucket_name, base_prefix)
            logger.info(f"Deleted {files_deleted} existing files")
        
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
                        logger.debug(f"Created folder: s3://{bucket_name}/{folder_key}")
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
                        logger.debug(f"Uploaded file: s3://{bucket_name}/{s3_key}")
            
            # If no files were uploaded but we have folders, it might be an empty ZIP or only folders
            if uploaded_files == 0 and len(uploaded_folders) == 0:
                return jsonify({'error': 'ZIP file is empty or contains no files'}), 400
        
        logger.info(f"Upload completed. {uploaded_files} files uploaded to S3.")
        return jsonify({
            'success': True,
            'message': f'Successfully extracted and uploaded {uploaded_files} files to {s3_path}',
            'file_count': uploaded_files,
            'folder_count': len(uploaded_folders),
            'files_deleted': files_deleted,
            'deletion_performed': delete_existing and not is_custom_path
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

def delete_existing_files(s3_client, bucket_name, prefix):
    """Delete all existing files at the given S3 prefix"""
    try:
        deleted_count = 0
        
        # List all objects with the given prefix
        paginator = s3_client.get_paginator('list_objects_v2')
        page_iterator = paginator.paginate(
            Bucket=bucket_name,
            Prefix=prefix
        )
        
        # Collect all objects to delete
        objects_to_delete = []
        for page in page_iterator:
            if 'Contents' in page:
                for obj in page['Contents']:
                    objects_to_delete.append({'Key': obj['Key']})
        
        # Delete in batches of 1000 (S3 limit)
        for i in range(0, len(objects_to_delete), 1000):
            batch = objects_to_delete[i:i+1000]
            response = s3_client.delete_objects(
                Bucket=bucket_name,
                Delete={'Objects': batch}
            )
            
            # Count successfully deleted objects
            if 'Deleted' in response:
                deleted_count += len(response['Deleted'])
            
            # Log any errors
            if 'Errors' in response:
                for error in response['Errors']:
                    logger.error(f"Failed to delete {error['Key']}: {error['Message']}")
        
        return deleted_count
        
    except Exception as e:
        logger.error(f"Error deleting existing files: {str(e)}")
        raise