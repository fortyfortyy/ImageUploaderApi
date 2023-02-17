import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser


class UserAccount(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account_tier = models.ForeignKey("AccountTier", on_delete=models.SET_DEFAULT, default=1)

    def __str__(self):
        return "%s - %s", self.username, self.account_tier.name


class AccountTier(models.Model):
    name = models.CharField(max_length=100)
    # thumbnail_sizes = models.ManyToManyField(ThumbnailSize)
    can_generate_expiring_links = models.BooleanField(default=False)

    def __str__(self):
        return self.name
