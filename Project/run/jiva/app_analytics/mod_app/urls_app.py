from django.urls import include, path

urlpatterns = [
    path('base/', include('app_analytics.mod_base.urls_base')),
]
