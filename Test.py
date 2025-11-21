@app.route('/api/download_files', methods=['POST'])
def download_files():
    """API endpoint to download all files from exact S3 path"""
    try:
        data = request.get_json()
        s3_path = data.get('s3_path')
        
        if not s3_path:
            return jsonify({'error': 'S3 path is required'}), 400
        
        logger.info(f"Downloading files from exact path: {s3_path}")
        
        # Parse S3 path
        if s3_path.startswith('s3://'):
            parsed = urlparse(s3_path)
            bucket_name = parsed.netloc
            prefix = parsed.path.lstrip('/')
        else:
            return jsonify({'error': f"Invalid S3 path format: {s3_path}"}), 400
        
        # Ensure we're working with the exact path (not just prefix)
        # Remove trailing slash if present to be consistent
        if prefix.endswith('/'):
            prefix = prefix[:-1]
        
        # Create a temporary zip file with generic name
        temp_dir = tempfile.mkdtemp()
        zip_filename = os.path.join(temp_dir, 's3_files.zip')
        
        s3_client = get_s3_client()
        
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # First, check if the exact path exists as a folder
            # In S3, folders don't actually exist - they're just prefixes
            # So we list objects that start with the exact prefix + '/'
            folder_prefix = prefix + '/'
            
            paginator = s3_client.get_paginator('list_objects_v2')
            page_iterator = paginator.paginate(
                Bucket=bucket_name, 
                Prefix=folder_prefix,
                Delimiter=''  # No delimiter to get all objects recursively
            )
            
            file_count = 0
            
            for page in page_iterator:
                if 'Contents' in page:
                    for obj in page['Contents']:
                        key = obj['Key']
                        
                        # Skip the folder marker itself (if it exists)
                        if key == folder_prefix:
                            continue
                            
                        # Only include files that are DIRECTLY under our exact path
                        # This ensures we don't get files from similar prefixes
                        if key.startswith(folder_prefix):
                            # Calculate the relative path within our folder
                            relative_path = key[len(folder_prefix):]
                            
                            # Only process if this is a direct child (not in subfolders if you want only immediate files)
                            # If you want to include subfolders, remove this check
                            if '/' not in relative_path or True:  # Set to False if you only want immediate files
                                response = s3_client.get_object(Bucket=bucket_name, Key=key)
                                file_content = response['Body'].read()
                                
                                # Add to zip with relative path
                                zipf.writestr(relative_path, file_content)
                                file_count += 1
                                logger.debug(f"Added file: {relative_path}")
            
            # Also check if there are any files at the exact prefix (without trailing slash)
            # This handles the case where the path might be a file instead of a folder
            try:
                head_response = s3_client.head_object(Bucket=bucket_name, Key=prefix)
                # If we get here, the exact path is a file (not a folder)
                response = s3_client.get_object(Bucket=bucket_name, Key=prefix)
                file_content = response['Body'].read()
                
                # Use the filename from the key
                filename = prefix.split('/')[-1] if '/' in prefix else prefix
                zipf.writestr(filename, file_content)
                file_count += 1
                logger.debug(f"Added single file: {filename}")
            except ClientError as e:
                # If head_object fails, it means the exact path is not a file (it's a folder or doesn't exist)
                if e.response['Error']['Code'] != '404':
                    raise
        
        if file_count == 0:
            return jsonify({'error': f'No files found at the exact path: {s3_path}'}), 404
        
        logger.info(f"Download completed. {file_count} files zipped from exact path.")
        return send_file(zip_filename, 
                        as_attachment=True, 
                        download_name='s3_files.zip', 
                        mimetype='application/zip')
    
    except ClientError as e:
        error_msg = f"AWS S3 error: {str(e)}"
        logger.error(error_msg)
        return jsonify({'error': error_msg}), 500
    except Exception as e:
        error_msg = f"Download error: {str(e)}"
        logger.error(error_msg)
        return jsonify({'error': error_msg}), 500