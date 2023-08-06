import unittest

from simple_storage_service.exceptions import ProviderBadConfigurationException, ProviderNotFoundException
from parameterized import parameterized


class ProviderNotFoundExceptionTestCase(unittest.TestCase):

    def test_message(self):
        message = 'Provider not found. Choices are: AWS, AZURE or GCP.'
        with self.assertRaisesRegex(ProviderNotFoundException, message):
            raise ProviderNotFoundException()


class ProviderBadConfigurationExceptionTestCase(unittest.TestCase):

    @parameterized.expand([
        ('random_param1', ),
        ('random_param2', ),
        ('random_param3', ),
    ])
    def test_message(self, random_param):
        message = f'{random_param} is required for this provider.'
        with self.assertRaisesRegex(ProviderBadConfigurationException, message):
            raise ProviderBadConfigurationException(missing_param=random_param)
