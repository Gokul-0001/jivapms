from datetime import datetime
from app_analytics.mod_base.models_base import *

class PageAnalyticsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.method == "GET":
            # Log the page visit
            PageVisit.objects.create(
                url=request.build_absolute_uri(),
            )
        
        return response
