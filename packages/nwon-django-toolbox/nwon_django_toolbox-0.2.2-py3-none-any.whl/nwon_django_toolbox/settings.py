from django.conf import settings

from nwon_django_toolbox.nwon_django_settings import NWONDjangoSettings

# Parse Settins from Django setttings
NWON_DJANGO_SETTINGS = (
    NWONDjangoSettings.parse_obj(settings.NWON_DJANGO)
    if "NWON_DJANGO" in settings and isinstance(settings.NWON_DJANGO, dict)
    else NWONDjangoSettings()
)
"""
Settings used withing the NWON-django-toolbox package
"""

__all__ = ["NWON_DJANGO_SETTINGS"]
