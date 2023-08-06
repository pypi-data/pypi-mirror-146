from ..exceptions import ProviderBadConfigurationException


class BaseProvider:
    REQUIRED_PARAMS = []

    @classmethod
    def validate_params(cls, params):
        param_keys = list(params.keys())
        for required_param in cls.REQUIRED_PARAMS:
            if required_param not in param_keys:
                raise ProviderBadConfigurationException(missing_param=required_param)

    def get_object_to_path(self, key, path):
        raise NotImplementedError

    def get_object_to_stream(self, key):
        raise NotImplementedError

    def upload_object_from_path(self, key, path):
        raise NotImplementedError

    def get_presigned_url(self, key, expiration=3600, method='get_object'):
        raise NotImplementedError

    def upload_object_from_stream(self, key, stream):
        raise NotImplementedError
