from azure.storage.blob import BlockBlobService
from azure.common import AzureMissingResourceHttpError
from .base_provider import BaseProvider


class AzureProvider(BaseProvider):
    REQUIRED_PARAMS = ['container_name', 'account_name', 'account_key']

    def __init__(self, container_name, account_name, account_key) -> None:
        self.container_name = container_name
        self.account_name = account_name
        self.account_key = account_key


    def get_blob_service(self):
        return BlockBlobService(
            account_name=self.account_name,
            account_key=self.account_key
        )

    def get_object_to_stream(self, key):
        block_blob_service = self.get_blob_service()
        try:
            return block_blob_service.get_blob_to_bytes(
                self.container_name,
                key,
            ).content
        except AzureMissingResourceHttpError:
            return None

    def get_object_to_path(self, key, path):
        block_blob_service = self.get_blob_service()
        block_blob_service.get_blob_to_path(
            self.container_name,
            key,
            path
        )

    def upload_object_from_stream(self, key, stream):
        block_blob_service = self.get_blob_service()
        block_blob_service.create_blob_from_stream(
            self.container_name,
            key,
            stream
        )

    def upload_object_from_path(self, key, path):
        block_blob_service = self.get_blob_service()
        block_blob_service.create_blob_from_path(
            self.container_name,
            key,
            path
        )

    def list_objects(self, prefix=None, delimiter=False):
        block_blob_service = self.get_blob_service()
        return block_blob_service.list_blob_names(
            self.container_name,
            prefix=prefix,
            delimiter=delimiter
        )
