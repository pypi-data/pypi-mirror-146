import unittest
from unittest import mock
from simple_storage_service import SimpleStorage
from simple_storage_service.exceptions import ProviderNotFoundException
from simple_storage_service.providers import AWSProvider, AzureProvider, GCPProvider
from parameterized import parameterized


class StorageFactoryTestCase(unittest.TestCase):

    def setUp(self):
        self.base_config = {}

    def test_raise_exception_when_provider_not_found(self):
        with self.assertRaises(ProviderNotFoundException):
            SimpleStorage.initialize('RANDOM_PROVIDER', self.base_config)

    @parameterized.expand([
        ('AWS', AWSProvider),
        ('AZURE', AzureProvider),
        ('GCP', GCPProvider),
    ])
    def test_get_correct_class_based_on_provider_name(self, provider_name, provider_class):
        with mock.patch.object(provider_class, '__init__', return_value=None):
            self.assertIsInstance(SimpleStorage.initialize(provider_name, self.base_config), provider_class)
