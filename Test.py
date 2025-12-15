# In your /api/upload_files function, after successful upload:
msck_status = None
msck_message = None
partitions_added = 0

# Only run partition update when using table selection (not custom path)
if not is_custom_path and database_name and table_name:
    try:
        logger.info(f"Running automatic partition update for {database_name}.{table_name}")
        
        # Get the table to find its location
        glue_client = get_glue_client()
        table_response = glue_client.get_table(
            DatabaseName=database_name,
            Name=table_name
        )
        
        s3_location = table_response['Table'].get('StorageDescriptor', {}).get('Location', '')
        if s3_location:
            partitions_added = add_new_partitions(glue_client, database_name, table_name, s3_location)
            msck_status = "success"
            msck_message = f"Added {partitions_added} new partitions to table"
        else:
            msck_status = "failed"
            msck_message = "Table has no S3 location"
            
    except Exception as msck_error:
        logger.error(f"Automatic partition update failed: {str(msck_error)}")
        msck_status = "failed"
        msck_message = f"Files uploaded successfully, but partition update failed: {str(msck_error)}"

# Include in response
response_data = {
    'success': True,
    'message': f'Successfully uploaded {uploaded_files} files',
    'file_count': uploaded_files,
    'msck_run': not is_custom_path and database_name and table_name,
    'msck_status': msck_status,
    'msck_message': msck_message,
    'partitions_added': partitions_added
}