
import argparse
from google.cloud import storage

def upload_blob(bucket_name, source_file_name, destination_blob_name):
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

    # Optional: set a generation-match precondition to avoid potential race conditions
    # and data corruptions. The request to upload is aborted if the object's
    # generation number does not match your precondition. For a destination
    # object that does not yet exist, set the if_generation_match precondition to 0.
    # If the destination object already exists in your bucket, set instead a
    # generation-match precondition using its generation number.
    generation_match_precondition = 0

    blob.upload_from_filename(source_file_name, if_generation_match=generation_match_precondition)

    print(
        f"File {source_file_name} uploaded to {destination_blob_name}."
    )

# upload_blob("aia-transcript-data", "./data/gl-001500-002000.mp3", 'gl-001500-002000.mp3')

def main():
    
    bucket_name = None
    file_name = None
    blob_name = None

    print("blob_upload v0.1.0")

    parser = argparse.ArgumentParser(description="Upload a file to Google Cloud Storage")
    parser.add_argument("--bucket", help="Bucket name")
    parser.add_argument("--fname", help="File to upload")
    parser.add_argument("--bname", help="blob name")

    args = parser.parse_args()
    
    if args.bucket:
        bucket_name = args.bucket

    if args.bname:
        blob_name = args.bname

    if args.fname:
        file_name = args.fname    

    if (not blob_name) and (file_name):
        blob_name = file_name.split("/")[-1]

    if (bucket_name and file_name and blob_name):
        print(f"Uploading {file_name} to GCS: {bucket_name}/{blob_name}")
        upload_blob(bucket_name, file_name, blob_name)

if __name__ == "__main__":

    main()

