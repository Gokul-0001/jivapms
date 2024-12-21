
from app_organization.mod_app.all_view_imports import *
from app_organization.mod_project.models_project import *
from app_organization.mod_project.forms_project import *
from app_common.mod_app.all_view_imports import *
from app_organization.mod_organization.models_organization import *
from app_common.mod_common.models_common import *
from app_memberprofilerole.mod_role.models_role import *
from app_jivapms.mod_app.all_view_imports import *
from app_organization.org_decorators import *
from app_organization.mod_projectmembership.models_projectmembership import *
from app_organization.mod_project_template.models_project_template import *
from app_organization.mod_project_roadmap.models_project_roadmap import *
from app_organization.mod_project_detail.forms_project_detail import *
from app_organization.mod_project_template.forms_project_template import *
from app_organization.mod_dev_value_stream.models_dev_value_stream import *

from app_organization.mod_backlog.models_backlog import *

app_name = 'app_organization'
app_version = 'v1'

module_name = 'projects'
module_path = f'mod_project'

@login_required
def project_roadmap(request, org_id, project_id):
    user = request.user
    org_id = int(org_id)
    project_id = int(project_id)
    org = Organization.objects.get(pk=org_id)
    project = Project.objects.get(pk=project_id)
    project_roadmap = ProjectRoadmap.objects.get_or_create(pro=project)
    
    # Prepare the context for the template
    context = {
        'parent_page': 'Projects',
        'page': 'list_projects',
        'organization': project.org,
        'org': org,
        'org_id': org_id,
        'user': user,
        'project': project,
        'project_roadmap': project_roadmap,
        
        'page_title': f"{project.name} Roadmap",
    }

    template_file = f"{app_name}/{module_path}/project_roadmap/project_roadmap.html"
    return render(request, template_file, context)
    