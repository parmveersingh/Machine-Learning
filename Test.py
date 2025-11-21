@app.route('/api/download_files', methods=['POST'])
def download_files():
    """API endpoint to download all files from an S3 path"""
    try:
        data = request.get_json()
        s3_path = data.get('s3_path')
        table_name = data.get('table_name', 's3_files')  # Get table name or default
        
        if not s3_path:
            return jsonify({'error': 'S3 path is required'}), 400
        
        logger.info(f"Downloading files from: {s3_path} for table: {table_name}")
        
        # Parse S3 path
        if s3_path.startswith('s3://'):
            parsed = urlparse(s3_path)
            bucket_name = parsed.netloc
            prefix = parsed.path.lstrip('/')
        else:
            return jsonify({'error': f"Invalid S3 path format: {s3_path}"}), 400
        
        # Create a temporary zip file with table name
        temp_dir = tempfile.mkdtemp()
        safe_table_name = "".join(c for c in table_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        zip_filename = os.path.join(temp_dir, f'{safe_table_name}.zip')
        
        s3_client = get_s3_client()
        
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            paginator = s3_client.get_paginator('list_objects_v2')
            page_iterator = paginator.paginate(Bucket=bucket_name, Prefix=prefix)
            
            file_count = 0
            folder_count = 0
            
            for page in page_iterator:
                if 'Contents' in page:
                    for obj in page['Contents']:
                        key = obj['Key']
                        
                        # Skip the prefix itself if it's a "folder"
                        if key == prefix:
                            continue
                            
                        # Check if this is a folder (ends with /) or a file
                        if key.endswith('/'):
                            # It's a folder - create empty directory in zip
                            folder_count += 1
                            # ZipFile doesn't create empty directories by default, 
                            # so we create them by adding a placeholder
                            dir_path = key[len(prefix):] if key.startswith(prefix) else key
                            if dir_path:  # Only if there's a subpath
                                zipf.writestr(dir_path, '')  # Create empty directory
                        else:
                            # It's a file - download and add to zip
                            response = s3_client.get_object(Bucket=bucket_name, Key=key)
                            file_content = response['Body'].read()
                            
                            # Preserve folder structure in zip
                            local_path = key[len(prefix):] if key.startswith(prefix) else key
                            zipf.writestr(local_path, file_content)
                            file_count += 1
        
        logger.info(f"Download completed. {file_count} files and {folder_count} folders zipped.")
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