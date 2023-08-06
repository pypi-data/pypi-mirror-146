import unittest
from parameterized import parameterized
from simple_storage_service.providers import AzureProvider, AWSProvider, GCPProvider
from simple_storage_service.exceptions import ProviderBadConfigurationException


class ProviderValidationConfigTestCase(unittest.TestCase):

    @parameterized.expand([
        (AWSProvider, {'lorem': 'wrong bucket'}),
        (AzureProvider, {'lorem': 'wrong bucket'}),
        (GCPProvider, {'lorem': 'wrong bucket'}),
    ])
    def test_raise_exeception_when_missing_params(self, provider_class, params):
        with self.assertRaises(ProviderBadConfigurationException):
            provider_class.validate_params(params)


    @parameterized.expand([
        (AWSProvider, {
            'bucket_name': 'corret bucket',
            'region_name': 'sa-east-1',
            'aws_access_key_id': 'some-aws-access-key-id',
            'aws_secret_access_key': 'some-aws-secret-access-key',
        }),
        (AzureProvider, {
            'container_name': 'correct container name',
            'account_name': 'correct account name',
            'account_key': 'correct account key',
        }),
        (GCPProvider, {'bucket_name': 'correct bucket'}),
    ])
    def test_not_raise_exeception_when_no_missing_params(self, provider_class, params):
        self.assertIsNone(provider_class.validate_params(params))
