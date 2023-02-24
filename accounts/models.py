import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver

from default_configs import DEFAULT_TIERS_CONFIG
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
