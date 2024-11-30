from django.contrib import admin
from django.urls import path, include

from app_analytics.mod_base import views_base as base   
from app_common.mod_common import views_common as common
from app_analytics.mod_base.models_base import *

urlpatterns = [
    path('', base.analytics_home, name='analytics_home'), 
    path('dashboard/', base.dashboard, name='dashboard'),
    path('analytics_view/', base.analytics_view, name='analytics_view'),
    
]
