from django.conf import settings

MIN_EXPIRY_LINK_TIME = getattr(settings, 'MIN_EXPIRY_LINK_TIME', 300)
MAX_EXPIRY_LINK_TIME = getattr(settings, 'MAX_EXPIRY_LINK_TIME', 30000)
DEFALT_EXPIRY_LINK_TIME = getattr(settings, 'DEFALT_EXPIRY_LINK_TIME', 30000)
MAX_UPLOAD_SIZE = getattr(settings, 'MAX_UPLOAD_SIZE', 10 * 1024 * 1024)
DEFAULT_TIERS_CONFIG = {
    'BASIC': dict(
        thumbnail_size=dict(width=200, height=200),
        get_original_file=False,
        can_generate_expiring_links=False,
    ),
    'PREMIUM': dict(
        thumbnail_size=dict(width=200, height=400),
        get_original_file=True,
        can_generate_expiring_links=False,
    ),
    'ENTERPRISE': dict(
        get_original_file=True,
        can_generate_expiring_links=True,
    ),
}
