
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


# viewable flag
first_viewable_flag = '__ALL__'  # 'all' or '__OWN__'
viewable_flag = '__ALL__'  # 'all' or '__OWN__'
# Setup dictionaries based on flags
viewable_dict = {} if viewable_flag == '__ALL__' else {'author': user}
first_viewable_dict = {} if first_viewable_flag == '__ALL__' else {'author': user}
def get_viewable_dicts(user, viewable_flag, first_viewable_flag):
    viewable_dict = {} if viewable_flag == '__ALL__' else {'author': user}
    first_viewable_dict = {} if first_viewable_flag == '__ALL__' else {'author': user}
    return viewable_dict, first_viewable_dict
# ============================================================= #
@login_required
def list_projects(request, org_id):
    user = request.user
    objects_count = 0
    show_all = request.GET.get('all', '25')
    objects_per_page = int(show_all) if show_all != 'all' else 25
    pagination_options = [5, 10, 15, 25, 50, 100, 'all']
    selected_bulk_operations = None
    deleted_count = 0
    has_projects_admin = False
    is_project_admin = False
    user_memberships = None
    relevant_admin = False
    # Fetch the organization
    organization = get_object_or_404(Organization, id=org_id, active=True)
    memberships = Member.objects.filter(user=user, active=True)
    logger.debug(f">>> === PROJECT ENTRY LIST PROJECTS: {user.username} ==> User roles: {organization} === <<<")
    org_admin_roles = MemberOrganizationRole.objects.filter(
        member__in=memberships,
        role__name=org_admin_str
    )
    project_admin_roles = MemberOrganizationRole.objects.filter(
        member__in=memberships,
        role__name=project_admin_str
    )
    
    logger.debug(f">>> === OrgAdmin: org_admin_roles:{org_admin_roles}:{project_admin_roles} === <<<")
    is_org_admin = org_admin_roles.exists()
    is_project_admin = project_admin_roles.exists()

    
    # Filter projects based on user access
    if is_org_admin:
        # Org admins can see all active projects in the organizations they manage
        org_ids = org_admin_roles.values_list('org_id', flat=True).distinct()
        # Query to fetch all active projects in these organizations
        tobjects = Project.objects.filter(
            org_id=org_id,
            active=True
        ).order_by('position')
        
    else:
        role_ids = ProjectRole.objects.filter(active=True).values_list('id', flat=True)
        # Filter projects based on specific project memberships (Admin, Viewer, Editor)
        # Adjusted query to use the correct related_name 'project_members'
        tobjects = Project.objects.filter(
            project_members__member__in=memberships,
            project_members__project_role_id__in=role_ids,
            project_members__active=True,
            org_id=org_id,
            active=True
        ).distinct().order_by('position')
        
        admin_role_id = ProjectRole.objects.get(role_type=PROJECT_ADMIN_ROLE_STR, active=True).id
        has_projects_admin = Projectmembership.objects.filter(
                        member__in=memberships,
                        project_role_id=admin_role_id,
                        project__org_id=org_id,
                        active=True
                    ).exists()
        

    logger.debug(f">>> === LIMITED PROJECTS FOR NON-OA:{tobjects} === <<<")
    
    # Relevant admin
    relevant_admin = is_org_admin or is_project_admin
    
    # Process search query
    search_query = request.GET.get('search', '')
    if search_query:
        tobjects = tobjects.filter(name__icontains=search_query).order_by('position')
    else:
        #tobjects = tobjects.order_by('position')
        deleted = Project.objects.filter(active=False, org_id=org_id)
        deleted_count = deleted.count()

    # Handle pagination
    if show_all == 'all':
        page_obj = tobjects
        objects_per_page = tobjects.count()
    else:
        paginator = Paginator(tobjects, objects_per_page)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    objects_count = tobjects.count()

    ## Handle POST requests for bulk operations
    if request.method == 'POST':
        selected_bulk_operations = request.POST.getlist('bulk_operations')
        bulk_operation = str(selected_bulk_operations[0].strip()) if selected_bulk_operations else None

        if 'selected_item' in request.POST:
            selected_items = request.POST.getlist('selected_item')
            for item_id in selected_items:
                item = int(item_id)
                project = get_object_or_404(Project, pk=item, active=True)

                if bulk_operation == 'bulk_delete':
                    project.active = False
                    project.save()
                elif bulk_operation == 'bulk_done':
                    project.done = True
                    project.save()
                elif bulk_operation == 'bulk_not_done':
                    project.done = False
                    project.save()
                elif bulk_operation == 'bulk_blocked':
                    project.blocked = True
                    project.save()
                else:
                    return redirect('list_projects', org_id=org_id)

            return redirect('list_projects', org_id=org_id)

    # Prepare the context for the template
    context = {
        'parent_page': 'Projects',
        'page': 'list_projects',
        'organization': organization,
        'org_id': org_id,
        'user': user,
        'tobjects': tobjects,
        'page_obj': page_obj,
        'objects_count': objects_count,
        'objects_per_page': objects_per_page,
        'deleted_count': deleted_count,
        'show_all': show_all,
        'pagination_options': pagination_options,
        'selected_bulk_operations': selected_bulk_operations,
        'page_title': 'Project List',
        'is_org_admin': is_org_admin,
        'is_project_admin': is_project_admin,
        'relevant_admin': relevant_admin,
        'user_memberships': user_memberships,
    }

    template_file = f"{app_name}/{module_path}/list_projects.html"
    return render(request, template_file, context)


# ============================================================= #
@login_required
def list_deleted_projects(request, org_id):
    # take inputs
    # process inputs
    user = request.user       
    objects_count = 0    
    show_all = request.GET.get('all', '25')
    objects_per_page = int(show_all) if show_all != 'all' else 25
    pagination_options = [5, 10, 15, 25, 50, 100, 'all']
    selected_bulk_operations = None
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    # Fetch the organization
    member = Member.objects.get(user=user, org=organization, active=True)
    user_roles = MemberOrganizationRole.objects.filter(member=member)    
    relevant_admin = user_roles.filter(role__name__in=[org_admin_str, project_admin_str]).exists()
    logger.debug(f">>> === RELEVANT ADMIN: {relevant_admin} === <<<")    
    is_org_admin = user_roles.filter(role__name__in=[org_admin_str]).exists()
    user_memberships = Projectmembership.objects.filter(project__org=organization, member=member, active=True)
    is_project_admin = user_memberships.filter(project_role__role_type=PROJECT_ADMIN_ROLE_STR).exists()
    logger.debug(f">>> === User memberships queryset: {user_memberships.values()} === <<<")
    logger.debug(f">>> === CHECKING1: {user.username} ==> User roles: {user_roles}, Memberships: {user_memberships}, Org Admin: {is_org_admin}, Project Admin: {is_project_admin} === <<<")
    # Filter projects based on user access
    if is_org_admin:
        # Org admins can see all active projects in the organization
        tobjects = Project.objects.filter(active=True, org_id=org_id)
        logger.debug(f">>> === Projects:{tobjects} === <<<")
    else:
        # Filter projects where the user has specific project membership (Viewer, Editor, Admin)
        tobjects = Project.objects.filter(
            id__in=user_memberships.values_list('project_id', flat=True),
            active=True,
            org_id=org_id
        )
    logger.debug(f">>> === Projects:{tobjects} === <<<")
    
    search_query = request.GET.get('search', '')
    if search_query:
        tobjects = Project.objects.filter(name__icontains=search_query, 
                                            active=False,
                                            org_id=org_id, **viewable_dict).order_by('position')
    else:
        tobjects = Project.objects.filter(active=False, org_id=org_id,
                                            **viewable_dict).order_by('position')        
    
    if show_all == 'all':
        # No pagination, show all records
        page_obj = tobjects
        objects_per_page = tobjects.count()
    else:
        objects_per_page = int(show_all)     
        paginator = Paginator(tobjects, objects_per_page)  
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    objects_count = tobjects.count()
    
    ## processing the POST
    if request.method == 'POST':
        selected_bulk_operations = request.POST.getlist('bulk_operations')
        bulk_operation = str(selected_bulk_operations[0].strip()) if selected_bulk_operations else None
     
        if 'selected_item' in request.POST:  # Correct the typo here
                selected_items = request.POST.getlist('selected_item')  # Use getlist to ensure all are captured
                for item_id in selected_items:
                    item = int(item_id)  # Ensure item_id is converted to int if necessary
                    if bulk_operation == 'bulk_restore':
                        object = get_object_or_404(Project, pk=item, active=False, **viewable_dict)
                        object.active = True
                        object.save()         
                    elif bulk_operation == 'bulk_erase':
                        object = get_object_or_404(Project, pk=item, active=False, **viewable_dict)
                        object.active = False  
                        object.deleted = True             
                        object.save()    
                    else:
                        redirect('list_projects', org_id=org_id)
                redirect('list_projects', org_id=org_id)
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_deleted_projects',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,
        'user': user,
        'tobjects': tobjects,
        'page_obj': page_obj,
        'objects_count': objects_count,
        'objects_per_page': objects_per_page,
        'show_all': show_all,
        'pagination_options': pagination_options,
        'selected_bulk_operations': selected_bulk_operations,
        'page_title': f'Project List',
        'is_org_admin': is_org_admin,
        'is_project_admin': is_project_admin,
        'relevant_admin': relevant_admin,
        'user_roles': user_roles,
        'user_memberships': user_memberships,
    }       
    template_file = f"{app_name}/{module_path}/list_deleted_projects.html"
    return render(request, template_file, context)


@login_required
@org_access_required()
def create_project(request, member, org_membership, org_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, **first_viewable_dict)
    logger.debug(f">>> === ORG_DECORATOR: {user.username} ==> User roles: {org_membership} === <<<")
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.author = user
            project.org_id = org_id
            project.save()
            
            # STEP1: Create the Project Administration record
            # default is initiation
            ProjectAdministration.objects.create(
                project=project,
                author=user
            )
            
            # Check if the member has 'Project Admin' role in the organization
            if org_membership.role.name == 'Project Admin':
                logger.debug(f">>> === {PROJECT_ADMIN_ROLE_STR}:CHECK === <<<")
                admin_role = ProjectRole.objects.get(role_type=PROJECT_ADMIN_ROLE_STR)
                

                # Assign the member as 'Admin' in the ProjectMembership
                Projectmembership.objects.create(
                    member=member,
                    project=project,
                    project_role=admin_role
                )
            
            return redirect('list_projects', org_id=org_id)
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
    else:
        form = ProjectForm()

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'create_project',
        'organization': organization,
        'org_id': org_id,
        'module_path': module_path,
        'form': form,
        'page_title': f'Create Project',
    }

    template_file = f"{app_name}/{module_path}/create_project.html"
    return render(request, template_file, context)



# Edit
@login_required
@org_or_project_access_required(project_allowed_roles=[PROJECT_ADMIN_ROLE_STR, PROJECT_EDITOR_ROLE_STR])
def edit_project(request, org_id, project_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(Project, pk=project_id, active=True,**viewable_dict)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=object)
        if form.is_valid():
            form.instance.author = user
            form.instance.org_id = org_id
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list_projects', org_id=org_id)
    else:
        form = ProjectForm(instance=object)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'edit_project',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,
        'form': form,
        'object': object,
        'page_title': f'Edit Project',
    }
    template_file = f"{app_name}/{module_path}/edit_project.html"
    return render(request, template_file, context)



@login_required
@org_or_project_access_required(project_allowed_roles=[PROJECT_ADMIN_ROLE_STR])
def delete_project(request, org_id, project_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(Project, pk=project_id, active=True,**viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.save()
        return redirect('list_projects', org_id=org_id)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'delete_project',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,        
        'object': object,
        'page_title': f'Delete Project',
    }
    template_file = f"{app_name}/{module_path}/delete_project.html"
    return render(request, template_file, context)


@login_required
@org_access_required()
def permanent_deletion_project(request, member, org_membership,  org_id, project_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(Project, pk=project_id, active=False, deleted=False, **viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.deleted = True
        object.save()
        return redirect('list_projects', org_id=org_id)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'permanent_deletion_project',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,        
        'object': object,
        'page_title': f'Permanent Deletion Project',
    }
    template_file = f"{app_name}/{module_path}/permanent_deletion_project.html"
    return render(request, template_file, context)


@login_required
@org_or_project_access_required(project_allowed_roles=[PROJECT_ADMIN_ROLE_STR])
def restore_project(request,  org_id, project_id):
    user = request.user
    object = get_object_or_404(Project, pk=project_id, active=False,**viewable_dict)
    object.active = True
    object.save()
    return redirect('list_projects', org_id=org_id)
   


@login_required
@org_or_project_access_required()
def view_project(request, org_id, project_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(Project, pk=project_id, active=True,**viewable_dict)    

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'view_project',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,
        'object': object,
        'page_title': f'View Project',
    }
    template_file = f"{app_name}/{module_path}/view_project.html"
    return render(request, template_file, context)


@login_required
@org_admin_this_project_admin_or_member_of_project
def project_homepage(request, org_id, project_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    
    # Backlog
    backlog = Backlog.objects.filter(pro_id=project_id, active=True)
    
    check_model_rec_count('****PROJECT_HOME_PAGE', BacklogType, f"{project_id}_PROJECT_TREE")
    
    # get project administration details
    project_administration = ProjectAdministration.objects.filter(project_id=project_id, 
                                                                  active=True).first()
    
    project = get_object_or_404(Project, pk=project_id, active=True,**viewable_dict)   
    project_detail = project.project_details if hasattr(project, 'project_details') else None
    
        
    roadmap_items = ProjectRoadmap.objects.filter(active=True)
    logger.debug(f"Roadmap items for project {project.id}: {roadmap_items}")

    roadmap_items = project.project_roadmap_items.order_by('start_date').filter(active=True)
    logger.debug(f">>> === ROADMAP ITEMS: {roadmap_items} === <<<")
    # Create a dynamic Gantt chart string for Mermaid.js
    
    # Initialize the Gantt chart string
    roadmap_str = "gantt\n    title Project Roadmap\n    dateFormat  YYYY-MM-DD\n    axisFormat  %Y-%m-%d\n"

    # Track the current section to avoid repeating the same section header
    current_section = ""

    # Loop through each item in roadmap_items and build the Gantt chart string dynamically
    for item in roadmap_items:
        # Check if the section has changed; if so, add a new section to the Gantt chart
        if item.section != current_section:
            roadmap_str += f"    section {item.section}\n"
            current_section = item.section
        
        # Append each task (task name, status, start date, end date) to the Gantt chart
        if item.start_date and item.end_date:
            roadmap_str += f"    {item.task_name} :{item.status}, {item.start_date}, {item.end_date}\n"

    # Ensure there is no hardcoded string overwriting the dynamic one
    # Log the final Gantt chart string to check its structure
    logger.debug(f"Generated roadmap_str: {roadmap_str}")

    object = project
    
    # Project Administration 
    project_administration = ProjectAdministration.objects.filter(project_id=project_id, 
                                                                  active=True).first()
    
    # HANDLING POST DATA
    if request.method == 'POST':
        form = ProjectDetailForm(request.POST, instance=project_detail)
        if form.is_valid():
            form.instance.author = user
            form.instance.org_id = org_id
            form.instance.pro = project
            project_administration.project_state = 'Started'
            project_administration.save()
            form.save()
            # pr_start_date = form.instance.start_date
            # pr_end_date = form.instance.end_date
            # project_roadmap, created = ProjectRoadmap.objects.get_or_create(
            #     pro=project, 
            #     active=True
            # )
            # Initiation 
            CHECK_BACKLOG_TYPE = BacklogType.objects.filter(name=f"{project_id}_PROJECT_TREE")
            logger.debug(f">>> === **PROJECT_HOME_PAGE** form creation CHECK_BACKLOG_TYPE: {CHECK_BACKLOG_TYPE} === <<<")
            if not CHECK_BACKLOG_TYPE.exists():                
                backlog_project_type_root, create = BacklogType.objects.get_or_create(pro=project, name=f"{project_id}_PROJECT_TREE")
            else:
                backlog_project_type_root = CHECK_BACKLOG_TYPE.first()
            
            # # Roadmap, self entry
            # project_roadmap.section = f"{project.name} Project Roadmap"
            # project_roadmap.task_name = f"{project.name} Project"
            # project_roadmap.status = 'init'
            # project_roadmap.start_date = pr_start_date
            # project_roadmap.end_date = pr_end_date,
            # project_roadmap.author = user
            # project_roadmap.active = True
            # project_roadmap.save()

        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('project_homepage', org_id=org_id, project_id=project_id)
    print(f">>> === backlog: {backlog} === <<<")
    
    
    ##
    ##
    ##
    check_backlog_types = BacklogType.objects.filter(name=f"{project_id}_PROJECT_TREE")
    logger.debug(f">>> === **PROJECT_HOME_PAGE** AFTER CHECK_BACKLOG_TYPES: {check_backlog_types} === <<<")
    ##
    ##
    ##
    
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'project_homepage',
        'organization': organization,
        'org_id': org_id,
        
        'project_administration': project_administration,
        'backlog': backlog,
        'module_path': module_path,
        'object': object,
        'project': object,
        'project_detail': project_detail,
        'form': ProjectDetailForm(instance=project_detail),
        'roadmap': roadmap_str,
        'page_title': f'Project Homepage',
    }
    editable = request.editable

    if editable:
        template_file = f"{app_name}/{module_path}/project_homepage.html"
    else:
        template_file = f"{app_name}/{module_path}/viewer_project_homepage.html"
    
    return render(request, template_file, context)



@login_required
@org_admin_this_project_admin_or_member_of_project
def project_dvs(request, org_id, project_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    project = get_object_or_404(Project, pk=project_id, active=True,**viewable_dict)   
    project_detail = project.project_details if hasattr(project, 'project_details') else None
    object = project
    
    # Get the DevValueStream Relation
    dvs = DevValueStream.objects.filter(project=project, active=True).first()
    if dvs != None:
        ops = dvs.ops
    else:
        ops = None
    
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'project_dvs',
        'organization': organization,
        'org_id': org_id,
        'ops': ops,
        'module_path': module_path,
        'object': object,
        'project': object,
        'project_detail': project_detail,
        'dvs': dvs,
        'page_title': f'Project DVS',
    }

    template_file = f"{app_name}/{module_path}/project_dvs.html"
    
    return render(request, template_file, context)

@login_required
@org_and_pa_only()
def project_settings_page(request, org_id, project_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(Project, pk=project_id, active=True,**viewable_dict)    

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'project_settings',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,
        'object': object,
        'project': object,
        'page_title': f'Project Settings',
    }
    template_file = f"{app_name}/{module_path}/project_settings.html"
    return render(request, template_file, context)
