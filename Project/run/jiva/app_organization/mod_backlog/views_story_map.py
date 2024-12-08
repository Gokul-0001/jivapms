from app_organization.mod_project.models_project import *

from app_organization.mod_app.all_view_imports import *
from app_organization.mod_backlog.models_backlog import *
from app_organization.mod_backlog.forms_backlog import *
from app_organization.mod_org_release.models_org_release import *
from app_organization.mod_persona.models_persona import *
from app_organization.mod_activity.models_activity import *
from app_organization.mod_step.models_step import *
from app_jivapms.mod_app.all_view_imports import *

app_name = 'app_organization'
app_version = 'v1'

module_name = 'backlog'
module_path = f'mod_backlog'


@login_required
def create_story_map(request, org_id):    
    projects = Organization.objects.get(pk=org_id).org_projects.filter(active=True)
    if request.method == 'POST':
        selected_project_id = request.POST.get('project')
        selected_story_map_option = request.POST.get('story_mapping_name')
        print(f"====> {selected_project_id} ===> {selected_story_map_option}")
        if selected_story_map_option == '2':
            return redirect('create_story_map_from_backlog', pro_id=selected_project_id)
        return redirect('create_backlog_from_story_map', pro_id=selected_project_id)
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_backlogs',
        'org_id': org_id,
        'projects': projects,
        'page_title': f'Backlog List',
    }       
    template_file = f"{app_name}/{module_path}/story_map/create_story_map.html"
    return render(request, template_file, context)

@login_required
def create_backlog_from_story_map(request, pro_id):
    pro = Project.objects.get(pk=pro_id)
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'create_backlog_from_story_map',
        'pro_id': pro_id,
        'pro': pro,
        'project': pro,
        'org': pro.org,
        'organization': pro.org,
        'org_id': pro.org_id,
        'page_title': f'Backlog from Story Map',
    }       
    template_file = f"{app_name}/{module_path}/story_map/create_backlog_from_story_map.html"
    return render(request, template_file, context)

@login_required
def create_story_map_from_backlog(request, pro_id):    
    pro = Project.objects.get(pk=pro_id)
    organization = pro.org
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'create_story_map_from_backlog',
        'pro_id': pro_id,
        'pro': pro,
        'project': pro,
        'org': pro.org,
        'organization': pro.org,
        'org_id': pro.org_id,
        'page_title': f'Story Map from Backlog',
    }       
    template_file = f"{app_name}/{module_path}/story_map/create_story_map_from_backlog.html"
    return render(request, template_file, context)