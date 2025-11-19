@app.route('/api/tables/<database_name>')
def get_tables(database_name):
    """API endpoint to fetch tables for a specific database"""
    try:
        print(f"Fetching tables for database: {database_name}")
        glue_client = get_glue_client()
        
        tables = []
        
        # Use the built-in paginator
        paginator = glue_client.get_paginator('get_tables')
        page_iterator = paginator.paginate(
            DatabaseName=database_name,
            PaginationConfig={'PageSize': 100}
        )
        
        for page_num, page in enumerate(page_iterator, 1):
            for table in page['TableList']:
                table_info = {
                    'name': table['Name'],
                    'location': table.get('StorageDescriptor', {}).get('Location', 'No location found')
                }
                tables.append(table_info)
            
            print(f"Page {page_num}: Fetched {len(page['TableList'])} tables")
            
            # Safety break - limit to 10 pages maximum
            if page_num >= 10:
                print("Reached maximum page limit of 10")
                break
        
        print(f"Fetched {len(tables)} total tables for database {database_name}")
        return jsonify({'tables': tables})
    
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'EntityNotFoundException':
            return jsonify({'error': f"Database '{database_name}' not found"}), 404
        else:
            error_msg = f"AWS Glue error: {str(e)}"
            print(f"Tables fetch error: {error_msg}")
            return jsonify({'error': error_msg}), 500
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        print(f"Unexpected error in tables: {error_msg}")
        return jsonify({'error': error_msg}), 500