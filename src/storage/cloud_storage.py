from dotenv import load_dotenv
from os import environ
# Imports the Google Cloud client library
from google.cloud import storage
# from src.middleware.cloud_credentials import get_cloud_credentials
from google.oauth2 import service_account

# load environment variables
# this will include in the Google Credentials file path
# load_dotenv()


# use service_account to generate credentials object
json_data = json.loads(environ.get('GOOGLE_APPLICATION_CREDENTIALS'))
credentials = service_account.Credentials.from_service_account_info(json_data)

# Instantiates a client
storage_client = storage.Client(credentials=credentials)

# The name for the new bucket
bucket_name = environ.get('GOOGLE_CLOUD_STORAGE_BUCKET_NAME')

# Creates the new bucket
bucket = storage_client.get_bucket(bucket_name)


def download_blob(source_blob_name, destination_file_name, bucket_name=bucket_name):
    """Downloads a blob from the bucket."""
    # bucket_name = "your-bucket-name"
    # source_blob_name = "storage-object-name"
    # destination_file_name = "local/path/to/file"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)

    # Construct a client side representation of a blob.
    # Note `Bucket.blob` differs from `Bucket.get_blob` as it doesn't retrieve
    # any content from Google Cloud Storage. As we don't need additional data,
    # using `Bucket.blob` is preferred here.
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

    print(
        "Blob {} downloaded to {}.".format(
            source_blob_name, destination_file_name
        )
    )


def upload_blob(source_file, destination_blob_name, bucket_name=bucket_name):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # blob.upload_from_filename(source_file_name)
    # blob.upload_from_string(source_file.stream.read(), content_type='application/octet-stream')
    blob.upload_from_file(source_file, rewind=True,
                          content_type='application/octet-stream')
    # blob.upload
    return blob.public_url if blob.public_url else None

  
def delete_blob(blob_name, bucket_name=bucket_name):
    """Deletes a blob from the bucket."""
    # bucket_name = "your-bucket-name"
    # blob_name = "your-object-name"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    try:
        blob.delete()
        return True
    except:
        return False
