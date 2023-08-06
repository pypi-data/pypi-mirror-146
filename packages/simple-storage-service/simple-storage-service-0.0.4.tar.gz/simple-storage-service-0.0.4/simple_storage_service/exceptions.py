class StorageServiceException(Exception):
    pass


class ProviderNotFoundException(StorageServiceException):
    def __str__(self):
        return 'Provider not found. Choices are: AWS, AZURE or GCP.'


class ProviderBadConfigurationException(StorageServiceException):

    def __init__(self, *args: object, missing_param=None) -> None:
        super().__init__(*args)
        self.missing_param = missing_param

    def __str__(self) -> str:
        return f'{self.missing_param} is required for this provider.'
