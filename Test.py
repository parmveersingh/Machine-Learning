@app.route('/api/databases')
def get_databases():
    """API endpoint to fetch all Glue databases using paginator"""
    try:
        print("Starting to fetch databases using paginator...")
        glue_client = get_glue_client()
        
        databases = []
        
        # Use the built-in paginator which handles NextToken automatically
        paginator = glue_client.get_paginator('get_databases')
        page_iterator = paginator.paginate(PaginationConfig={'PageSize': 100})
        
        for page_num, page in enumerate(page_iterator, 1):
            db_names = [db['Name'] for db in page['DatabaseList']]
            databases.extend(db_names)
            print(f"Page {page_num}: Fetched {len(db_names)} databases")
            
            # Safety break - limit to 10 pages maximum
            if page_num >= 10:
                print("Reached maximum page limit of 10")
                break
        
        print(f"Successfully fetched {len(databases)} total databases")
        return jsonify({'databases': databases})
    
    except (ClientError, NoCredentialsError) as e:
        error_msg = f"AWS API error: {str(e)}"
        print(f"Database fetch error: {error_msg}")
        return jsonify({'error': error_msg}), 500
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        print(f"Unexpected error in get_databases: {error_msg}")
        return jsonify({'error': error_msg}), 500