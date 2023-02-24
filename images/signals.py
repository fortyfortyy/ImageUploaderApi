import logging

from django.db.models.signals import post_save
from django.dispatch import receiver
from django_cleanup.signals import cleanup_pre_delete

from images.models import Image
from images.tasks import cleanup_image_folder_task, generate_thumbnail_task

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Image)
def create_thumbnails(sender, instance: Image, **kwargs):
    """Signal creates a task in celery to generate thumbnails based on user account tier"""
    generate_thumbnail_task.delay(instance.id)


@receiver(cleanup_pre_delete, sender=Image)
def custom_cleanup_pre_delete(sender, instance, **kwargs):
    """Create a task in celery to delete image folder"""
    cleanup_image_folder_task.delay(instance.image.name)
