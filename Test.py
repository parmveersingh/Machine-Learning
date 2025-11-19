import os
import boto3
from flask import Flask, render_template, request, jsonify, send_file
from botocore.exceptions import ClientError, NoCredentialsError
import zipfile
import tempfile
from urllib.parse import urlparse

app = Flask(__name__)

# Initialize AWS clients
def get_glue_client():
    """Initialize and return Glue client using AWS credentials"""
    # AWS best practice: uses IAM roles, environment variables, or ~/.aws/credentials
    return boto3.client('glue')

def get_s3_client():
    """Initialize and return S3 client using AWS credentials"""
    return boto3.client('s3')

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/api/databases')
def get_databases():
    """API endpoint to fetch all Glue databases"""
    try:
        glue_client = get_glue_client()
        response = glue_client.get_databases()

        databases = [db['Name'] for db in response['DatabaseList']]
        return jsonify({'databases': databases})

    except (ClientError, NoCredentialsError) as e:
        error_msg = f"AWS API error: {str(e)}"
        return jsonify({'error': error_msg}), 500
    except Exception as e:
        return jsonify({'error': f"Unexpected error: {str(e)}'}), 500

@app.route('/api/tables/<database_name>')
def get_tables(database_name):
    """API endpoint to fetch tables for a specific database"""
    try:
        glue_client = get_glue_client()
        response = glue_client.get_tables(DatabaseName=database_name)

        tables = []
        for table in response['TableList']:
            table_info = {
                'name': table['Name'],
                'location': table.get('StorageDescriptor', {}).get('Location', 'No location found')
            }
            tables.append(table_info)

        return jsonify({'tables': tables})

    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'EntityNotFoundException':
            return jsonify({'error': f"Database '{database_name}' not found"}), 404
        else:
            return jsonify({'error': f"AWS Glue error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({'error': f"Unexpected error: {str(e)}"}), 500

@app.route('/api/download_files', methods=['POST'])
def download_files():
    """API endpoint to download all files from an S3 path"""
    try:
        data = request.get_json()
        s3_path = data.get('s3_path')

        if not s3_path:
            return jsonify({'error': 'S3 path is required'}), 400

        # Parse S3 path (supports both s3://bucket/path and virtual-hosted style)
        if s3_path.startswith('s3://'):
            parsed = urlparse(s3_path)
            bucket_name = parsed.netloc
            prefix = parsed.path.lstrip('/')
        else:
            # Try to parse as virtual-hosted style
            parts = s3_path.replace('https://', '').split('.s3.')
            if len(parts) > 1:
                bucket_name = parts[0]
                path_parts = parts[1].split('/')
                prefix = '/'.join(path_parts[1:]) if len(path_parts) > 1 else ''
            else:
                return jsonify({'error': f"Invalid S3 path format: {s3_path}"}), 400

        # Create a temporary zip file
        temp_dir = tempfile.mkdtemp()
        zip_filename = os.path.join(temp_dir, 'download.zip')

        s3_client = get_s3_client()

        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            paginator = s3_client.get_paginator('list_objects_v2')
            page_iterator = paginator.paginate(Bucket=bucket_name, Prefix=prefix)

            for page in page_iterator:
                if 'Contents' in page:
                    for obj in page['Contents']:
                        key = obj['Key']
                        if not key.endswith('/'):  # Skip directories
                            # Download file content
                            response = s3_client.get_object(Bucket=bucket_name, Key=key)
                            file_content = response['Body'].read()

                            # Preserve folder structure in zip
                            local_path = key
                            zipf.writestr(local_path, file_content)

        return send_file(zip_filename,
                        as_attachment=True,
                        download_name='s3_files.zip',
                        mimetype='application/zip')

    except ClientError as e:
        return jsonify({'error': f"AWS S3 error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({'error': f"Download error: {str(e)}"}), 500

if __name__ == '__main__':
    # Create downloads directory if it doesn't exist
    os.makedirs('downloads', exist_ok=True)
    app.run(debug=True, host='127.0.0.1', port=5000)
