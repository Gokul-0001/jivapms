from app_web.mod_app.all_view_imports import *
from app_memberprofilerole.mod_app.all_model_imports import *
from app_memberprofilerole.mod_member.models_member import *

from app_common.mod_app.all_view_imports import *
from app_jivapms.mod_app.all_view_imports import *
from app_organization.mod_projectmembership.models_projectmembership import *

from app_organization.mod_framework.models_framework import *
from app_organization.mod_org_image_map.models_org_image_map import *
from app_organization.org_decorators import *

app_name = "app_jivapms"
version = "v1"
module_dirname = "mod_web"

from app_jivapms.mod_web.helper_web import *
from app_jivapms.mod_web.views_ajax_web import *


def stats(request):
    user = request.user
    organization = Organization.objects.filter(active=True)
    framework = Framework.objects.filter(active=True)
    public_frameworks = Framework.objects.filter(public_framework=True, active=True)
    # Get the related Organization objects for those Frameworks
    org_ids = public_frameworks.values_list('organization__id', flat=True).distinct()
    organizations = Organization.objects.filter(id__in=org_ids)
    all_orgs = Organization.objects.filter(active=True)
    # Check the stats
    org_count = organization.count()
    framework_count = framework.count()
    public_framework_count = public_frameworks.count()
   
    org_project_member_counts = []

    for org in all_orgs:
        project_count = org.org_projects.filter(active=True).count()
        member_count = Member.objects.filter(member_roles__org=org).count()
        org_project_member_counts.append({
            'org_id': org.id,
            'org_name': org.name,
            'project_count': project_count,
            'member_count': member_count,
        })
    logger.info(f"Total organizations: {org_count}")
    logger.info(f"Total frameworks: {framework_count}")
    logger.info(f"Total public frameworks: {public_framework_count}")
    for org_stat in org_project_member_counts:
        logger.info(f"Organization ID: {org_stat['org_id']}, Name: {org_stat['org_name']}, Projects: {org_stat['project_count']}, Members: {org_stat['member_count']}")
    
    stats_context = {}
    
    org_project_member_roles = []
    
    # Get the roles for each member in each organization
    mors_site_admin = MemberOrganizationRole.objects.filter(active=True, role__name='Site Admin')
    mors_org_admin = MemberOrganizationRole.objects.filter(active=True, role__name='Org Admin')
    mors_project_admin = MemberOrganizationRole.objects.filter(active=True, role__name='Project Admin')
    mors_other_members = MemberOrganizationRole.objects.filter(active=True).exclude(role__name='Site Admin').exclude(role__name='Org Admin').exclude(role__name='Project Admin')

    print(f">>> === Site Admins {mors_site_admin} === <<<")
    print(f">>> === Org Admins {mors_org_admin} === <<<")
    print(f">>> === Project Admins {mors_project_admin} === <<<")
    
    # find all the projectmembership
    project_memberships = Projectmembership.objects.filter(active=True).order_by('project_role__role_type')
    print(f">>> === Project Memberships {project_memberships} === <<<")
        

    stats_context['org_project_member_roles'] = org_project_member_roles
    
    stats_context = { 'org_count': org_count, 'framework_count': framework_count, 
            'public_framework_count': public_framework_count, 
            'project_memberships': project_memberships,
            'org_project_member_counts': org_project_member_counts }
    
    template_super_user_home_page = f"{app_name}/{module_dirname}/super_user/super_user_homepage.html"
    context = {
        'parent_page': 'home',
        'page': 'stats',
        'page_title': 'Stats Page',
    }
    context.update(stats_context)
    template_url = f"{app_name}/{module_dirname}/super_user/stats.html"
    return render(request, template_url, context)   



def super_user_admin(request):
    user = request.user
    organization = Organization.objects.filter(active=True)
    
    template_super_user_home_page = f"{app_name}/{module_dirname}/super_user/super_user_homepage.html"
    context = {
        'parent_page': 'home',
        'page': 'super_user_admin',
        'page_title': 'Super User Admin Page',
    }

    template_url = f"{app_name}/{module_dirname}/super_user/super_user_admin.html"
    return render(request, template_url, context)   