from django.conf import settings
from django.contrib import admin

from shatail.images.models import Image

if (
    hasattr(settings, "SHATAILIMAGES_IMAGE_MODEL")
    and settings.SHATAILIMAGES_IMAGE_MODEL != "shatailimages.Image"
):
    # This installation provides its own custom image class;
    # to avoid confusion, we won't expose the unused shatailimages.Image class
    # in the admin.
    pass
else:
    admin.site.register(Image)
