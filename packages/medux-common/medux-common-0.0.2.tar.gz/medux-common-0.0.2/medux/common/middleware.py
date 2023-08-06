from django.core.exceptions import ImproperlyConfigured


class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # Any site, even the Django admin, must have a corresponding `Site` model.
        # This is created automatically (by fixture) at the `manage.py initialize` run.
        if not hasattr(request.site, "tenantedsite"):
            raise ImproperlyConfigured(
                "No tenants found. Please run 'manage.py initialize' first"
            )

        request.tenant = request.site.tenantedsite.tenant
        response = self.get_response(request)

        return response
