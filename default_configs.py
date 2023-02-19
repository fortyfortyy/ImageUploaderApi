from django.conf import settings

MIN_EXPIRY_LINK_TIME = getattr(settings, 'MIN_EXPIRY_LINK_TIME', 300)
MAX_EXPIRY_LINK_TIME = getattr(settings, 'MAX_EXPIRY_LINK_TIME', 30000)
DEFALT_EXPIRY_LINK_TIME = getattr(settings, 'DEFALT_EXPIRY_LINK_TIME', 30000)
MAX_UPLOAD_SIZE = getattr(settings, 'MAX_UPLOAD_SIZE', 10 * 1024 * 1024)
