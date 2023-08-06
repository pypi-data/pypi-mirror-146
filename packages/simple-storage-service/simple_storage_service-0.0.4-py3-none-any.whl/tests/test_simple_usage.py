import unittest

from simple_storage_service.factory import SimpleStorage
from simple_storage_service.providers import AWSProvider, AzureProvider, GCPProvider
from unittest import mock

from parameterized import parameterized

class SimpleUsageTestCase(unittest.TestCase):

    @parameterized.expand([
        ('AWS', AWSProvider, {'bucket_name': 'some-bucket'}),
        ('AZURE', AzureProvider, {
            'container_name': 'some-container-name',
            'account_name': 'some-account-name',
            'account_key': 'some-account-key'
        }),
        ('GCP', GCPProvider, {'bucket_name': 'some-bucket'}),
    ])
    def test_simple_usage(self, provider_name, provider_class, params):
        simple_storage = SimpleStorage.initialize(provider_name, params)

        with mock.patch.object(provider_class, 'get_object', return_value=None):
            simple_storage.get_object('some-key')

        with mock.patch.object(provider_class, 'upload_object', return_value=None):
            simple_storage.upload_object('some-key', 'path/to/file.txt')
