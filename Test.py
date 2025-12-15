# ... after your file upload loop completes successfully in /api/upload_files ...
msck_status = None
msck_message = None

# Conditionally run MSCK REPAIR
if not is_custom_path and database_name and table_name:
    try:
        logger.info(f"Running MSCK REPAIR after upload for {database_name}.{table_name}")
        glue_client.run_m_s_c_k_repair_table(
            DatabaseName=database_name,
            TableName=table_name
        )
        msck_status = "success"
        msck_message = "MSCK REPAIR completed successfully."
    except Exception as msck_error:
        # Log the error but don't fail the whole upload
        logger.error(f"MSCK REPAIR failed after upload: {str(msck_error)}")
        msck_status = "failed"
        msck_message = f"Upload succeeded, but MSCK REPAIR failed. Please run it manually. Error: {str(msck_error)}"

# Then include msck_status and msck_message in your final jsonify response back to the frontend