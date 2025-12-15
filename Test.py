from botocore.exceptions import ClientError

@app.route('/api/run_msck_repair', methods=['POST'])
def api_run_msck_repair():
    """API endpoint to manually run MSCK REPAIR on a table"""
    try:
        # Use request.get_json() for JSON data
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'Request must be JSON'}), 400

        database_name = data.get('database_name')
        table_name = data.get('table_name')

        if not database_name or not table_name:
            return jsonify({'success': False, 'error': 'Database name and table name are required'}), 400

        logger.info(f"Manual MSCK REPAIR request for {database_name}.{table_name}")
        glue_client = get_glue_client()

        # CORRECT METHOD NAME: The Boto3 method uses underscores
        response = glue_client.run_m_s_c_k_repair_table(
            DatabaseName=database_name,
            TableName=table_name
        )
        # The response doesn't have detailed info, but no error means success
        logger.info(f"MSCK REPAIR successful for {database_name}.{table_name}. Response: {response}")
        return jsonify({
            'success': True,
            'message': f'MSCK REPAIR TABLE completed for {database_name}.{table_name}.'
        })

    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        logger.error(f"AWS ClientError during MSCK REPAIR: {error_code} - {error_message}")

        # Provide user-friendly error messages
        if error_code == 'EntityNotFoundException':
            error_msg = f"Table {database_name}.{table_name} not found."
        elif error_code == 'AccessDeniedException':
            error_msg = f"Permission denied. Check IAM policies for 'glue:BatchCreatePartition'."
        else:
            error_msg = f"AWS Glue error: {error_message}"
        return jsonify({'success': False, 'error': error_msg}), 500

    except Exception as e:
        logger.error(f"Unexpected error running MSCK REPAIR: {str(e)}")
        return jsonify({'success': False, 'error': f'Unexpected error: {str(e)}'}), 500