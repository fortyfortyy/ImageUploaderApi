from django.core.files.storage import FileSystemStorage
from django.utils.deconstruct import deconstructible


@deconstructible
class CustomImageStorage(FileSystemStorage):
    def get_available_name(self, name, **kwargs):
        """
        Overrides the default get_available_name method to use the original filename provided by the user image.
        """
        return name
