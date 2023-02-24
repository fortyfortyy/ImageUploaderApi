from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver

from accounts.models import AccountTier, UserAccount
from default_configs import DEFAULT_TIERS_CONFIG
from images.models import ThumbnailSize


@receiver(post_migrate)
def create_default_account_tiers(sender, **kwargs):
    if sender.name == UserAccount._meta.app_label:
        # Create a default AccountTiers if it doesn't exist
        if AccountTier.objects.filter(name="Basic").exists():
            return

        # CREATE BASIC TIER ACCOUNT
        basic_tier = AccountTier.objects.create(
            name="Basic",
            get_original_file=DEFAULT_TIERS_CONFIG['BASIC']['get_original_file'],
            can_generate_expiring_links=DEFAULT_TIERS_CONFIG['BASIC']['can_generate_expiring_links'],
        )
        basic_thumbnail = ThumbnailSize.objects.create(**DEFAULT_TIERS_CONFIG['BASIC']['thumbnail_size'])
        basic_tier.thumbnail_sizes.add(basic_thumbnail)

        # CREATE PREMIUM TIER ACCOUNT
        premium_tier = AccountTier.objects.create(
            name="Premium",
            get_original_file=DEFAULT_TIERS_CONFIG['PREMIUM']['get_original_file'],
            can_generate_expiring_links=DEFAULT_TIERS_CONFIG['PREMIUM']['can_generate_expiring_links'],
        )
        premium_thumbnail = ThumbnailSize.objects.create(**DEFAULT_TIERS_CONFIG['PREMIUM']['thumbnail_size'])
        premium_tier.thumbnail_sizes.set([basic_thumbnail, premium_thumbnail])

        # CREATE ENTERPRISE TIER ACCOUNT
        enterprise_tier = AccountTier.objects.create(
            name="Enterprise",
            get_original_file=DEFAULT_TIERS_CONFIG['ENTERPRISE']['get_original_file'],
            can_generate_expiring_links=DEFAULT_TIERS_CONFIG['ENTERPRISE']['can_generate_expiring_links'],
        )
        enterprise_tier.thumbnail_sizes.set([basic_thumbnail, premium_thumbnail])


@receiver(post_save, sender=UserAccount)
def create_user_account(sender, instance, created, **kwargs):
    if created and not instance.account_tier:
        instance.account_tier = AccountTier.objects.get(name="Basic")
        instance.save()
