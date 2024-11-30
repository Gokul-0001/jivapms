from app_web.mod_app.all_view_imports import *
from app_memberprofilerole.mod_app.all_model_imports import *
from app_memberprofilerole.mod_member.models_member import *

from app_common.mod_app.all_view_imports import *
from app_jivapms.mod_app.all_view_imports import *
from app_organization.mod_projectmembership.models_projectmembership import *

from app_organization.mod_framework.models_framework import *
from app_organization.mod_org_image_map.models_org_image_map import *
from app_organization.org_decorators import *

from app_analytics.mod_base.models_base import *

from app_jivapms.mod_web.helper_web import *
from app_jivapms.mod_web.views_ajax_web import *
from urllib.parse import urlparse, parse_qs
app_name = "app_analytics"
version = "v1"
module_dirname = "mod_base"
module_name="base"
module_path = f'mod_base'

def analytics_home(request):
    user = request.user
    context = {
        'parent_page': 'home',
        'page': 'analytics_home',
        'page_title': 'Analytics Home Page',
    }
    template_file = f"{app_name}/{module_path}/analytics_home.html"
    return render(request, template_file, context)

def dashboard(request):
    user = request.user
    context = {
        'parent_page': 'home',
        'page': 'analytics_home',
        'page_title': 'Analytics Home Page',
    }
    template_file = f"{app_name}/{module_path}/dashboard.html"
    return render(request, template_file, context)

def analytics_view(request):
    daily_visits = (
        PageVisit.objects.extra({'day': 'DATE(visit_date)'})
        .values('day', 'url')
        .annotate(visits=Count('id'))
        .order_by('day')
    )

    # Add URI breakdown for each URL
    for visit in daily_visits:
        parsed_url = urlparse(visit['url'])
        visit['path'] = parsed_url.path  # Path (e.g., /page/)
        visit['query'] = parse_qs(parsed_url.query)  # Query parameters as dict (e.g., {'q': ['test']})

    

    # Render the analytics page
    context = {
        'daily_visits': list(daily_visits),
       
        
        'parent_page': 'home',
        'page': 'analytics_view',
        'page_title': 'Analytics View',
        
    }
    
    template_file = f"{app_name}/{module_path}/analytics_view.html"
    return render(request, template_file, context)


def detailed_analytics_view(request):
    daily_visits = (
        PageVisit.objects.extra({'day': 'DATE(visit_date)'})
        .values('day', 'url')
        .annotate(visits=Count('id'))
        .order_by('day')
    )

    # Add URI breakdown for each URL
    for visit in daily_visits:
        parsed_url = urlparse(visit['url'])
        visit['path'] = parsed_url.path  # Path (e.g., /page/)
        visit['query'] = parse_qs(parsed_url.query)  # Query parameters as dict (e.g., {'q': ['test']})

    weekly_visits = (
        PageVisit.objects.extra({'week': 'strftime("%Y-%W", visit_date)'})
        .values('week', 'url')
        .annotate(visits=Count('id'))
        .order_by('week')
    )

    for visit in weekly_visits:
        parsed_url = urlparse(visit['url'])
        visit['path'] = parsed_url.path
        visit['query'] = parse_qs(parsed_url.query)

    monthly_visits = (
        PageVisit.objects.extra({'month': 'strftime("%Y-%m", visit_date)'})
        .values('month', 'url')
        .annotate(visits=Count('id'))
        .order_by('month')
    )

    for visit in monthly_visits:
        parsed_url = urlparse(visit['url'])
        visit['path'] = parsed_url.path
        visit['query'] = parse_qs(parsed_url.query)

    # Render the analytics page
    context = {
        'daily_visits': list(daily_visits),
        'weekly_visits': list(weekly_visits),
        'monthly_visits': list(monthly_visits),
        
        
        'parent_page': 'home',
        'page': 'detailed_analytics_view',
        'page_title': 'Detailed Analytics View',
        
    }
    
    template_file = f"{app_name}/{module_path}/detailed_analytics_view.html"
    return render(request, template_file, context)
