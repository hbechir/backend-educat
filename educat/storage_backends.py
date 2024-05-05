# storage_backends.py

from storages.backends.s3boto3 import S3Boto3Storage

class CleanURLS3Boto3Storage(S3Boto3Storage):
    def url(self, name, parameters=None, expire=None):
        """
        Returns the URL to the file with the given name.
        """
        url = super().url(name, parameters, expire)
        # Remove query parameters
        clean_url = url.split('?')[0]
        return clean_url
