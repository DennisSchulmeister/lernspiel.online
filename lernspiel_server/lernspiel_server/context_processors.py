from django.conf import settings
from django.contrib.sites.models import Site
from django.http import HttpRequest

def site(request: HttpRequest = None) -> dict:
    """
    Add the current site as customized in Django's Sites app to all templates.
    """
    site_id = settings.SITE_ID or 1
    site_obj = Site.objects.get(pk=site_id)

    return {
        "site": site_obj
    }