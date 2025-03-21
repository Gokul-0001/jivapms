
from app_organization.mod_app.all_view_imports import *
from app_organization.mod_team.models_team import *
from app_organization.mod_team.forms_team import *

from app_organization.mod_organization.models_organization import *
from app_organization.mod_projectmembership.models_projectmembership import *
from app_common.mod_common.models_common import *
from app_jivapms.mod_app.all_view_imports import *
from app_organization.org_decorators import *

app_name = 'app_organization'
app_version = 'v1'

module_name = 'teams'
module_path = f'mod_team'

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
@org_and_pa_only()
def list_teams(request, org_id):
    # take inputs
    # process inputs
    user = request.user       
    objects_count = 0    
    show_all = request.GET.get('all', '25')
    objects_per_page = int(show_all) if show_all != 'all' else 25
    pagination_options = [5, 10, 15, 25, 50, 100, 'all']
    selected_bulk_operations = None
    deleted_count = 0
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    project = None
    project_id = None
    if 'project_id' in request.GET:
        project_id = request.GET.get('project_id')
        project = get_object_or_404(Project, pk=project_id, active=True, **viewable_dict)
    member = Member.objects.get(user=user, active=True)
    user_roles = MemberOrganizationRole.objects.filter(member=member)    
    relevant_admin = user_roles.filter(role__name__in=[org_admin_str, project_admin_str]).exists()
    logger.debug(f">>> === RELEVANT ADMIN: {relevant_admin} === <<<")    
    is_org_admin = user_roles.filter(role__name__in=[org_admin_str]).exists()
    user_memberships = Projectmembership.objects.filter(project__org=organization, member=member, active=True)
    is_project_admin = user_memberships.filter(project_role__role_type=PROJECT_ADMIN_ROLE_STR).exists()
    logger.debug(f">>> === User memberships queryset: {user_memberships.values()} === <<<")
    logger.debug(f">>> === CHECKING1: {user.username} ==> User roles: {user_roles}, Memberships: {user_memberships}, Org Admin: {is_org_admin}, Project Admin: {is_project_admin} === <<<")
    
    search_query = request.GET.get('search', '')
    if search_query:
        tobjects = Team.objects.filter(name__icontains=search_query, 
                                            org_id=org_id, **viewable_dict).order_by('position')
    else:
        tobjects = Team.objects.filter(active=True, org_id=org_id, author=user).order_by('position')
        deleted = Team.objects.filter(active=False, deleted=False,
                                org_id=org_id,
                               **viewable_dict).order_by('position')
        deleted_count = deleted.count()
    
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
                if bulk_operation == 'bulk_delete':
                    object = get_object_or_404(Team, pk=item, active=True, **viewable_dict)
                    object.active = False
                    object.save()
                    
                elif bulk_operation == 'bulk_done':
                    object = get_object_or_404(Team, pk=item, active=True, **viewable_dict)
                    object.done = True
                    object.save()
                    
                elif bulk_operation == 'bulk_not_done':
                    object = get_object_or_404(Team, pk=item, active=True, **viewable_dict)
                    object.done = False
                    object.save()
                    
                elif bulk_operation == 'bulk_blocked':  # Correct the operation check here
                    object = get_object_or_404(Team, pk=item, active=True, **viewable_dict)
                    object.blocked = True
                    object.save()
                    
                else:
                    redirect('list_teams', org_id=org_id)
            return redirect('list_teams', org_id=org_id)
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_teams',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,
        'user': user,
        'tobjects': tobjects,
        'page_obj': page_obj,
        'objects_count': objects_count,
        'objects_per_page': objects_per_page,
        'deleted_count': deleted_count,
        'show_all': show_all,
        
        'pagination_options': pagination_options,
        'selected_bulk_operations': selected_bulk_operations,
        'page_title': f'Team List',
        'is_org_admin': is_org_admin,
        'is_project_admin': is_project_admin,
        'relevant_admin': relevant_admin,
        'user_roles': user_roles,
        'user_memberships': user_memberships,
        
        'project': project,
        'project_id': project_id,
        'pro_id': project_id,
    }       
    template_file = f"{app_name}/{module_path}/list_teams.html"
    return render(request, template_file, context)





# ============================================================= #
@login_required
@org_and_pa_only()
def list_deleted_teams(request, org_id):
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
    project = None
    project_id = None
    if 'project_id' in request.GET:
        project_id = request.GET.get('project_id')
        project = get_object_or_404(Project, pk=project_id, active=True, **viewable_dict)
    search_query = request.GET.get('search', '')
    if search_query:
        tobjects = Team.objects.filter(name__icontains=search_query, 
                                            active=False,
                                            org_id=org_id, **viewable_dict).order_by('position')
    else:
        tobjects = Team.objects.filter(active=False, org_id=org_id,
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
                        object = get_object_or_404(Team, pk=item, active=False, **viewable_dict)
                        object.active = True
                        object.save()         
                    elif bulk_operation == 'bulk_erase':
                        object = get_object_or_404(Team, pk=item, active=False, **viewable_dict)
                        object.active = False  
                        object.deleted = True             
                        object.save()    
                    else:
                        redirect('list_teams', org_id=org_id)
                redirect('list_teams', org_id=org_id)
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_deleted_teams',
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
        'page_title': f'Team List',
        
        'project': project,
        'project_id': project_id,
        'pro_id': project_id,
    }       
    template_file = f"{app_name}/{module_path}/list_deleted_teams.html"
    return render(request, template_file, context)



# Create View
@login_required
@org_and_pa_only()
def create_team(request, org_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    project = None
    project_id = None
    if 'project_id' in request.GET:
        project_id = request.GET.get('project_id')
        project = get_object_or_404(Project, pk=project_id, active=True, **viewable_dict)
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            form.instance.author = user
            form.instance.org_id = org_id
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list_teams', org_id=org_id)
    else:
        form = TeamForm()

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'create_team',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,
        'form': form,
        'page_title': f'Create Team',
        
        'project': project,
        'project_id': project_id,
        'pro_id': project_id,
    }
    template_file = f"{app_name}/{module_path}/create_team.html"
    return render(request, template_file, context)




# Edit
@login_required
@org_and_pa_only()
def edit_team(request, org_id, team_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    project = None
    project_id = None
    if 'project_id' in request.GET:
        project_id = request.GET.get('project_id')
        project = get_object_or_404(Project, pk=project_id, active=True, **viewable_dict)
    object = get_object_or_404(Team, pk=team_id, active=True,**viewable_dict)
    if request.method == 'POST':
        form = TeamForm(request.POST, instance=object)
        if form.is_valid():
            form.instance.author = user
            form.instance.org_id = org_id
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list_teams', org_id=org_id)
    else:
        form = TeamForm(instance=object)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'edit_team',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,
        'form': form,
        'object': object,
        'page_title': f'Edit Team',
        
        'project': project,
        'project_id': project_id,
        'pro_id': project_id,
    }
    template_file = f"{app_name}/{module_path}/edit_team.html"
    return render(request, template_file, context)



@login_required
@org_and_pa_only()
def delete_team(request, org_id, team_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    project = None
    project_id = None
    if 'project_id' in request.GET:
        project_id = request.GET.get('project_id')
        project = get_object_or_404(Project, pk=project_id, active=True, **viewable_dict)
    object = get_object_or_404(Team, pk=team_id, active=True,**viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.save()
        return redirect('list_teams', org_id=org_id)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'delete_team',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,        
        'object': object,
        'page_title': f'Delete Team',
        
        'project': project,
        'project_id': project_id,
        'pro_id': project_id,
    }
    template_file = f"{app_name}/{module_path}/delete_team.html"
    return render(request, template_file, context)


@login_required
@org_and_pa_only()
def permanent_deletion_team(request, org_id, team_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    project = None
    project_id = None
    if 'project_id' in request.GET:
        project_id = request.GET.get('project_id')
        project = get_object_or_404(Project, pk=project_id, active=True, **viewable_dict)
    object = get_object_or_404(Team, pk=team_id, active=False, deleted=False, **viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.deleted = True
        object.save()
        return redirect('list_teams', org_id=org_id)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'permanent_deletion_team',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,        
        'object': object,
        'page_title': f'Permanent Deletion Team',
        
        'project': project,
        'project_id': project_id,
        'pro_id': project_id,
    }
    template_file = f"{app_name}/{module_path}/permanent_deletion_team.html"
    return render(request, template_file, context)


@login_required
@org_and_pa_only()
def restore_team(request,  org_id, team_id):
    user = request.user
    object = get_object_or_404(Team, pk=team_id, active=False,**viewable_dict)
    object.active = True
    object.save()
    return redirect('list_teams', org_id=org_id)
   


@login_required
@org_and_pa_only()
def view_team(request, org_id, team_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    project = None
    project_id = None
    if 'project_id' in request.GET:
        project_id = request.GET.get('project_id')
        project = get_object_or_404(Project, pk=project_id, active=True, **viewable_dict)
    object = get_object_or_404(Team, pk=team_id, active=True,**viewable_dict)    

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'view_team',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,
        'object': object,
        'page_title': f'View Team',
        
        'project': project,
        'project_id': project_id,
        'pro_id': project_id,
    }
    template_file = f"{app_name}/{module_path}/view_team.html"
    return render(request, template_file, context)


