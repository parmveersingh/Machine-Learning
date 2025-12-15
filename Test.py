@app.route('/api/upload_files', methods=['POST'])
def upload_files():
    """API endpoint to extract ZIP and upload individual files/folders to S3 with optional MSCK REPAIR"""
    try:
        if 'zip_file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        zip_file = request.files['zip_file']
        s3_path = request.form.get('s3_path')
        delete_existing = request.form.get('delete_existing', 'false').lower() == 'true'
        is_custom_path = request.form.get('is_custom_path', 'false').lower() == 'true'
        run_msck_repair = request.form.get('run_msck_repair', 'false').lower() == 'true'
        database_name = request.form.get('database_name', '')
        table_name = request.form.get('table_name', '')
        
        if not zip_file or zip_file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not s3_path:
            return jsonify({'error': 'S3 path is required'}), 400
        
        if not zip_file.filename.lower().endswith('.zip'):
            return jsonify({'error': 'File must be a ZIP archive'}), 400
        
        logger.info(f"Extracting and uploading ZIP to: {s3_path}")
        logger.info(f"Delete existing: {delete_existing}, Is custom path: {is_custom_path}")
        logger.info(f"Run MSCK REPAIR: {run_msck_repair}, Database: {database_name}, Table: {table_name}")
        
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
        glue_client = get_glue_client()
        
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
        
        # Run MSCK REPAIR if requested and not using custom path
        msck_repair_success = False
        msck_repair_error = None
        if run_msck_repair and not is_custom_path and database_name and table_name:
            try:
                logger.info(f"Running MSCK REPAIR on table: {database_name}.{table_name}")
                msck_repair_response = run_msck_repair_table(glue_client, database_name, table_name)
                msck_repair_success = True
                logger.info(f"MSCK REPAIR successful for {database_name}.{table_name}")
            except Exception as e:
                msck_repair_error = str(e)
                logger.error(f"MSCK REPAIR failed for {database_name}.{table_name}: {msck_repair_error}")
        
        logger.info(f"Upload completed. {uploaded_files} files uploaded to S3.")
        
        response_data = {
            'success': True,
            'message': f'Successfully extracted and uploaded {uploaded_files} files to {s3_path}',
            'file_count': uploaded_files,
            'folder_count': len(uploaded_folders),
            'files_deleted': files_deleted,
            'deletion_performed': delete_existing and not is_custom_path,
            'msck_repair_performed': run_msck_repair and not is_custom_path and database_name and table_name,
            'msck_repair_success': msck_repair_success,
            'msck_repair_error': msck_repair_error
        }
        
        return jsonify(response_data)
    
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

def run_msck_repair_table(glue_client, database_name, table_name):
    """Run MSCK REPAIR TABLE command on Glue table"""
    try:
        # MSCK REPAIR TABLE is an async operation in Glue
        # We'll use the start_import_labels_task_run API for MSCK REPAIR
        # Note: This is a simplification - actual MSCK REPAIR might require different approach
        
        # For AWS Glue, we can use batch_update_partition or other methods
        # However, MSCK REPAIR is typically run via Athena or Hive
        # Since we're using Glue catalog directly, we'll use the repair_table API
        
        logger.info(f"Running MSCK REPAIR equivalent for {database_name}.{table_name}")
        
        # In AWS Glue, you can use the update_table operation to refresh table metadata
        # But for partition discovery, we might need to use batch_create_partition or similar
        
        # For now, we'll use a simple approach - just log that MSCK REPAIR was requested
        # In production, you might want to trigger an Athena MSCK REPAIR query or use Glue workflows
        
        # This is a placeholder - you might need to implement actual MSCK REPAIR based on your setup
        # For example, you could use:
        # 1. Athena: start_query_execution with "MSCK REPAIR TABLE table_name"
        # 2. Glue: batch_create_partition to add new partitions
        
        raise Exception("MSCK REPAIR functionality requires Athena integration or Glue partition management")
        
    except Exception as e:
        logger.error(f"MSCK REPAIR error: {str(e)}")
        raise

# Alternative: Implement actual MSCK REPAIR using Athena
def run_msck_repair_with_athena(database_name, table_name):
    """Run MSCK REPAIR TABLE using Athena (requires Athena setup)"""
    try:
        import boto3
        
        # Initialize Athena client
        athena_client = boto3.client('athena', region_name='us-east-1')
        
        # Create query string
        query = f"MSCK REPAIR TABLE {database_name}.{table_name}"
        
        # Start query execution
        response = athena_client.start_query_execution(
            QueryString=query,
            QueryExecutionContext={
                'Database': database_name
            },
            ResultConfiguration={
                'OutputLocation': 's3://your-athena-results-bucket/'  # Replace with your Athena results location
            }
        )
        
        query_execution_id = response['QueryExecutionId']
        logger.info(f"Athena query started: {query_execution_id}")
        
        # Wait for query to complete
        while True:
            query_status = athena_client.get_query_execution(QueryExecutionId=query_execution_id)
            status = query_status['QueryExecution']['Status']['State']
            
            if status in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
                break
            
            time.sleep(2)  # Wait 2 seconds before checking again
        
        if status == 'SUCCEEDED':
            return True, "MSCK REPAIR completed successfully"
        else:
            error_message = query_status['QueryExecution']['Status'].get('StateChangeReason', 'Unknown error')
            return False, error_message
            
    except Exception as e:
        return False, str(e)