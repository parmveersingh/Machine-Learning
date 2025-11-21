@app.route('/api/download_files', methods=['POST'])
def download_files():
    """Simplified endpoint - only downloads from exact folder path"""
    try:
        data = request.get_json()
        s3_path = data.get('s3_path')
        table_name = data.get('table_name', 's3_files')
        
        if not s3_path:
            return jsonify({'error': 'S3 path is required'}), 400
        
        logger.info(f"Downloading from: {s3_path} for table: {table_name}")
        
        # Parse S3 path
        if s3_path.startswith('s3://'):
            parsed = urlparse(s3_path)
            bucket_name = parsed.netloc
            prefix = parsed.path.lstrip('/')
        else:
            return jsonify({'error': f"Invalid S3 path format: {s3_path}"}), 400
        
        # Ensure prefix ends with / to indicate it's a folder
        if not prefix.endswith('/'):
            prefix = prefix + '/'
        
        # Create ZIP with table name
        temp_dir = tempfile.mkdtemp()
        safe_table_name = "".join(c for c in table_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        zip_filename = os.path.join(temp_dir, f'{safe_table_name}.zip')
        
        s3_client = get_s3_client()
        
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            file_count = 0
            
            # List ONLY objects that are direct children of the folder
            paginator = s3_client.get_paginator('list_objects_v2')
            page_iterator = paginator.paginate(
                Bucket=bucket_name, 
                Prefix=prefix
            )
            
            for page in page_iterator:
                if 'Contents' in page:
                    for obj in page['Contents']:
                        key = obj['Key']
                        
                        # Skip the folder marker itself
                        if key == prefix:
                            continue
                            
                        # Only process files that are in this exact folder
                        # This ensures we don't process the same file multiple times
                        response = s3_client.get_object(Bucket=bucket_name, Key=key)
                        file_content = response['Body'].read()
                        
                        # Calculate relative path (remove the prefix)
                        relative_path = key[len(prefix):]
                        
                        # Add to zip
                        zipf.writestr(relative_path, file_content)
                        file_count += 1
                        logger.info(f"Added file: {relative_path}")
        
        if file_count == 0:
            return jsonify({'error': f'No files found at: {s3_path}'}), 404
        
        logger.info(f"Downloaded {file_count} files")
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