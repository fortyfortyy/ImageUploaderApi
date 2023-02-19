from __future__ import annotations

import time
import uuid

from django.core import signing
from django.urls import reverse
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError

from default_configs import (
    DEFALT_EXPIRY_LINK_TIME,
    MAX_EXPIRY_LINK_TIME,
    MIN_EXPIRY_LINK_TIME,
)
from images.models import ExpiringLink, Image


class ExpiringLinkMixin:
    def generate_expiring_link(self, image: Image, expires_in: str = DEFALT_EXPIRY_LINK_TIME) -> dict:
        # Check that user has permission to generate expiring link
        user_account_tier = image.user.account_tier
        if not user_account_tier.can_generate_expiring_links:
            raise PermissionDenied("User not authorized to generate expiring link")

        if not expires_in.isdigit() or not MIN_EXPIRY_LINK_TIME <= (expires := int(expires_in)) <= MAX_EXPIRY_LINK_TIME:
            raise ValidationError("Invalid value for expires_in")

        pk = uuid.uuid4()
        signed_link = signing.dumps(str(pk))

        # Build the full URL for the expiring link
        full_url = self.request.build_absolute_uri(reverse('expiring-link-detail', kwargs={'signed_link': signed_link}))

        current_timestamp = int(time.time())
        expiry_time = current_timestamp + expires

        # create expiring link
        ExpiringLink.objects.create(id=pk, link=full_url, image=image, expires_in=expiry_time)

        return {'link': full_url}

    @staticmethod
    def decode_signed_value(value: str) -> ExpiringLink.id:
        try:
            return signing.loads(value)
        except signing.BadSignature:
            raise NotFound("Invalid signed link")
