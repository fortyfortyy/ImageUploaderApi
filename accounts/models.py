import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from images.models import ThumbnailSize


class UserAccount(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account_tier = models.ForeignKey("AccountTier", on_delete=models.SET_NULL, null=True, related_name="users")

    def __str__(self):
        return f"{self.username} ({self.account_tier.name if self.account_tier else 'Basic'})"


class AccountTier(models.Model):
    name = models.CharField(max_length=100)
    thumbnail_sizes = models.ManyToManyField(ThumbnailSize, blank=True)
    can_generate_expiring_links = models.BooleanField(default=False)
    get_original_file = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @property
    def get_thumbnail_sizes(self):
        return self.thumbnail_sizes.all()

    @property
    def get_available_heights(self):
        thumnails = self.get_thumbnail_sizes
        return [t.height for t in thumnails]


@receiver(post_migrate)
def create_default_account_tiers(sender, **kwargs):
    if sender.name == UserAccount._meta.app_label:
        # Create a default AccountTiers if it doesn't exist
        if AccountTier.objects.filter(name="Basic").exists():
            return

        basic_thumbnail = ThumbnailSize.objects.create(width=200, height=200)
        basic_tier = AccountTier.objects.create(name="Basic")
        basic_tier.thumbnail_sizes.add(basic_thumbnail)

        premium_thumbnail = ThumbnailSize.objects.create(width=200, height=400)
        premium_account = AccountTier.objects.create(name="Premium")
        premium_account.thumbnail_sizes.add(premium_thumbnail)
        premium_account.get_original_file = True

        enterprise_account = AccountTier.objects.create(name="Enterprise", can_generate_expiring_links=True)
        enterprise_account.thumbnail_sizes.set([basic_thumbnail, premium_thumbnail])
        enterprise_account.get_original_file = True


def create_user_account(sender, instance, created, **kwargs):
    if created and not instance.account_tier:
        instance.account_tier = AccountTier.objects.get(name="Basic")
        instance.save()


models.signals.post_save.connect(create_user_account, sender=UserAccount)
