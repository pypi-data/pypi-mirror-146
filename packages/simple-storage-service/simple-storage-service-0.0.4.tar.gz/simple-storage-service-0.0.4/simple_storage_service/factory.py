from .exceptions import ProviderNotFoundException
from .providers.azure import AzureProvider
from .providers.gcp import GCPProvider
from .providers.aws import AWSProvider


class SimpleStorage:

    @staticmethod
    def get_provider_class(provider):
        if provider == 'GCP':
            return GCPProvider

        if provider == 'AWS':
            return AWSProvider

        if provider == 'AZURE':
            return AzureProvider

        raise ProviderNotFoundException

    @classmethod
    def initialize(cls, provider, config):
        ProviderClass = cls.get_provider_class(provider)
        return ProviderClass(**config)
