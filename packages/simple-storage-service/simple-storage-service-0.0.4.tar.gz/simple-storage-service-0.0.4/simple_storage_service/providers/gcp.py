from google.cloud import storage
from google.api_core.exceptions import NotFound as GCPNotFound

import io

from .base_provider import BaseProvider


class GCPProvider(BaseProvider):
    REQUIRED_PARAMS = ['bucket_name']

    def __init__(self, bucket_name) -> None:
        self.bucket_name = bucket_name

    def get_object(self, key, data):
        client = storage.Client()
        bucket = client.get_bucket(self.bucket_name)
        blob = storage.Blob(key, bucket)
        client.download_blob_to_file(blob, data)

    def get_object_to_stream(self, key):
        data = io.BytesIO()
        try:
            self.get_object(key, data)
        except GCPNotFound:
            return None
        data.seek(0)
        return data.read()

    def get_object_to_path(self, key, path):
        with open(path, 'wb') as data:
            self.get_object(key, data)

    def upload_object_from_path(self, key, path):
        client = storage.Client()
        bucket = client.get_bucket(self.bucket_name)
        blob = storage.Blob(key, bucket)
        blob.upload_from_filename(path)

    def upload_object_from_stream(self, key, stream):
        client = storage.Client()
        bucket = client.get_bucket(self.bucket_name)
        blob = storage.Blob(key, bucket)
        blob.upload_from_file(stream)

    def list_objects(self, prefix=None, delimiter=False):
        storage_client = storage.Client()

        blobs = storage_client.list_blobs(self.bucket_name, prefix=prefix, delimiter=delimiter)

        blob_names = [blob.name for blob in blobs]

        if delimiter:
            return blobs.prefixes

        return blob_names
