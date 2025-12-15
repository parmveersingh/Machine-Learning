@app.route('/api/run_msck_repair', methods=['POST'])
def api_run_msck_repair():
    """API endpoint to run MSCK REPAIR equivalent on a table"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'Request must be JSON'}), 400
        
        database_name = data.get('database_name')
        table_name = data.get('table_name')
        
        if not database_name or not table_name:
            return jsonify({'success': False, 'error': 'Database name and table name are required'}), 400
        
        logger.info(f"MSCK REPAIR request for {database_name}.{table_name}")
        glue_client = get_glue_client()
        
        # 1. First, get the table to understand its partition structure
        try:
            table_response = glue_client.get_table(
                DatabaseName=database_name,
                Name=table_name
            )
        except Exception as e:
            return jsonify({
                'success': False, 
                'error': f'Table {database_name}.{table_name} not found or inaccessible: {str(e)}'
            }), 404
        
        table = table_response['Table']
        s3_location = table.get('StorageDescriptor', {}).get('Location', '')
        
        if not s3_location:
            return jsonify({
                'success': False, 
                'error': f'Table {database_name}.{table_name} has no S3 location'
            }), 400
        
        logger.info(f"Table S3 location: {s3_location}")
        
        # 2. Use batch_create_partitions to add new partitions
        # This is the equivalent of MSCK REPAIR
        partitions_added = add_new_partitions(glue_client, database_name, table_name, s3_location)
        
        logger.info(f"MSCK REPAIR completed. {partitions_added} partitions added/updated")
        return jsonify({
            'success': True,
            'message': f'Added/updated {partitions_added} partitions for {database_name}.{table_name}',
            'partitions_added': partitions_added
        })
        
    except Exception as e:
        error_msg = f"Error running partition update: {str(e)}"
        logger.error(error_msg)
        return jsonify({'success': False, 'error': error_msg}), 500

def add_new_partitions(glue_client, database_name, table_name, s3_location):
    """Discover and add new partitions to a Glue table"""
    try:
        # Parse S3 location
        from urllib.parse import urlparse
        parsed = urlparse(s3_location)
        bucket = parsed.netloc
        prefix = parsed.path.lstrip('/')
        
        s3_client = get_s3_client()
        partitions_added = 0
        
        # 3. List S3 objects to find new partitions
        # This is a simplified version - you might need to adjust based on your partition structure
        paginator = s3_client.get_paginator('list_objects_v2')
        page_iterator = paginator.paginate(Bucket=bucket, Prefix=prefix, Delimiter='/')
        
        partition_paths = []
        for page in page_iterator:
            # Look for common prefixes (these are likely partitions)
            if 'CommonPrefixes' in page:
                for cp in page['CommonPrefixes']:
                    partition_path = cp['Prefix']
                    partition_paths.append(partition_path)
        
        # 4. Create partition entries for each discovered path
        if partition_paths:
            # Get existing partitions to avoid duplicates
            existing_partitions = []
            try:
                partitions_paginator = glue_client.get_paginator('get_partitions')
                partitions_iterator = partitions_paginator.paginate(
                    DatabaseName=database_name,
                    TableName=table_name
                )
                for page in partitions_iterator:
                    existing_partitions.extend(page['Partitions'])
            except Exception as e:
                logger.warning(f"Could not get existing partitions: {str(e)}")
            
            existing_locations = [p.get('StorageDescriptor', {}).get('Location', '') for p in existing_partitions]
            
            # Prepare new partitions
            new_partitions = []
            for partition_path in partition_paths:
                partition_location = f"s3://{bucket}/{partition_path}"
                
                # Skip if partition already exists
                if partition_location in existing_locations:
                    continue
                
                # Extract partition values from path (adjust based on your partition structure)
                # Example: s3://bucket/prefix/year=2025/month=12/day=01/
                # Should extract: {'year': '2025', 'month': '12', 'day': '01'}
                partition_values = extract_partition_values(partition_path, prefix)
                
                if partition_values:
                    new_partitions.append({
                        'Values': list(partition_values.values()),
                        'StorageDescriptor': {
                            'Location': partition_location,
                            'InputFormat': 'org.apache.hadoop.mapred.TextInputFormat',
                            'OutputFormat': 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat',
                            'SerdeInfo': {
                                'SerializationLibrary': 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
                            }
                        }
                    })
            
            # 5. Batch create new partitions (max 100 per call)
            if new_partitions:
                for i in range(0, len(new_partitions), 100):
                    batch = new_partitions[i:i+100]
                    try:
                        response = glue_client.batch_create_partition(
                            DatabaseName=database_name,
                            TableName=table_name,
                            PartitionInputList=batch
                        )
                        partitions_added += len(batch)
                        logger.info(f"Batch created {len(batch)} partitions")
                    except Exception as e:
                        logger.error(f"Failed to create partition batch: {str(e)}")
                        # Try creating partitions one by one
                        for partition in batch:
                            try:
                                glue_client.create_partition(
                                    DatabaseName=database_name,
                                    TableName=table_name,
                                    PartitionInput=partition
                                )
                                partitions_added += 1
                            except Exception as single_error:
                                logger.error(f"Failed to create single partition: {str(single_error)}")
        
        return partitions_added
        
    except Exception as e:
        logger.error(f"Error in add_new_partitions: {str(e)}")
        raise

def extract_partition_values(partition_path, base_prefix):
    """Extract partition key-value pairs from S3 path"""
    try:
        # Remove base prefix and trailing slash
        relative_path = partition_path[len(base_prefix):].rstrip('/')
        
        # Split by '/' to get partition segments
        segments = relative_path.split('/')
        
        partition_values = {}
        for segment in segments:
            if '=' in segment:
                key, value = segment.split('=', 1)
                partition_values[key] = value
        
        return partition_values
        
    except Exception as e:
        logger.error(f"Error extracting partition values from {partition_path}: {str(e)}")
        return {}