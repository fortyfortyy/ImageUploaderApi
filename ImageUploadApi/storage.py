from urllib.parse import urljoin

from django.conf import settings
from django.utils.deconstruct import deconstructible
from storages.backends.gcloud import GoogleCloudStorage
from storages.utils import setting
from storages.utils import clean_name
from storages.utils import get_available_overwrite_name
from storages.utils import safe_join
from storages.utils import setting
from storages.utils import to_bytes


@deconstructible
class GoogleCloudMediaFileStorage(GoogleCloudStorage):
    """
      Google file storage class which gives a media file path from MEDIA_URL not google generated one.
    """
    bucket_name = setting('GS_BUCKET_NAME')

    def url(self, name):
        """
        Gives correct MEDIA_URL and not google generated url.
        """
        return urljoin(settings.MEDIA_URL, name)

    def get_available_name(self, name, max_length=None):
        return clean_name(name)
