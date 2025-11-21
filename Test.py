@app.route('/api/download_files', methods=['POST'])
def download_files():
    """API endpoint to download all files from exact S3 path with table name as ZIP"""
    try:
        data = request.get_json()
        s3_path = data.get('s3_path')
        table_name = data.get('table_name', 's3_files')  # Get table name for ZIP
        
        if not s3_path:
            return jsonify({'error': 'S3 path is required'}), 400
        
        logger.info(f"Downloading files from exact path: {s3_path} for table: {table_name}")
        
        # Parse S3 path
        if s3_path.startswith('s3://'):
            parsed = urlparse(s3_path)
            bucket_name = parsed.netloc
            prefix = parsed.path.lstrip('/')
        else:
            return jsonify({'error': f"Invalid S3 path format: {s3_path}"}), 400
        
        # Normalize the prefix - ensure no trailing slash for consistent comparison
        if prefix.endswith('/'):
            prefix = prefix[:-1]
        
        # Create a temporary zip file with table name
        temp_dir = tempfile.mkdtemp()
        safe_table_name = "".join(c for c in table_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        zip_filename = os.path.join(temp_dir, f'{safe_table_name}.zip')
        
        s3_client = get_s3_client()
        
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            file_count = 0
            
            # Check if the path is a folder (has objects with the prefix + '/')
            folder_prefix = prefix + '/'
            
            # List objects that are direct children of our exact path
            paginator = s3_client.get_paginator('list_objects_v2')
            page_iterator = paginator.paginate(
                Bucket=bucket_name, 
                Prefix=folder_prefix,
                Delimiter=''  # No delimiter to get all nested objects
            )
            
            found_files = set()  # Track files to avoid duplicates
            
            for page in page_iterator:
                if 'Contents' in page:
                    for obj in page['Contents']:
                        key = obj['Key']
                        
                        # Skip the folder marker itself
                        if key == folder_prefix:
                            continue
                            
                        # Only process if this key starts with our exact folder prefix
                        if key.startswith(folder_prefix):
                            # Calculate relative path within our folder
                            relative_path = key[len(folder_prefix):]
                            
                            # Avoid processing the same file multiple times
                            if key not in found_files:
                                response = s3_client.get_object(Bucket=bucket_name, Key=key)
                                file_content = response['Body'].read()
                                
                                # Add to zip with relative path
                                zipf.writestr(relative_path, file_content)
                                file_count += 1
                                found_files.add(key)
                                logger.info(f"Added file: {relative_path}")
            
            # Check if the exact path itself is a file (not a folder)
            # This should be mutually exclusive with the folder case above
            if file_count == 0:
                try:
                    # Try to get the object at the exact prefix (without trailing slash)
                    response = s3_client.get_object(Bucket=bucket_name, Key=prefix)
                    file_content = response['Body'].read()
                    
                    # Extract filename from path
                    filename = prefix.split('/')[-1]
                    zipf.writestr(filename, file_content)
                    file_count += 1
                    logger.info(f"Added single file: {filename}")
                except ClientError as e:
                    # It's not a file, and we found no folder contents
                    if e.response['Error']['Code'] not in ['404', 'NoSuchKey']:
                        raise
        
        if file_count == 0:
            return jsonify({'error': f'No files found at the exact S3 path: {s3_path}'}), 404
        
        logger.info(f"Successfully downloaded {file_count} files from exact path")
        return send_file(zip_filename, 
                        as_attachment=True, 
                        download_name=f'{safe_table_name}.zip', 
                        mimetype='application/zip')
    
    except ClientError as e:
        error_msg = f"AWS S3 error: {str(e)}"
        logger.error(error_msg)
        return jsonify({'error': error_msg}), 500
    except Exception as e:
        error_msg = f"Download error: {str(e)}"
        logger.error(error_msg)
        return jsonify({'error': error_msg}), 500