
from app_organization.mod_app.all_view_imports import *
from app_organization.mod_org_iteration.models_org_iteration import *
from app_organization.mod_org_iteration.forms_org_iteration import *

from app_organization.mod_org_release.models_org_release import *

from app_common.mod_common.models_common import *

from app_organization.mod_backlog_type.models_backlog_type import *
from app_organization.mod_backlog.models_backlog import *

from app_organization.mod_project.models_project import *
from app_jivapms.mod_app.all_view_imports import *

app_name = 'app_organization'
app_version = 'v1'

module_name = 'org_iterations'
module_path = f'mod_org_iteration'

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
def list_org_iterations(request, org_release_id):
    # take inputs
    # process inputs
    user = request.user       
    objects_count = 0    
    show_all = request.GET.get('all', '25')
    objects_per_page = int(show_all) if show_all != 'all' else 25
    pagination_options = [5, 10, 15, 25, 50, 100, 'all']
    selected_bulk_operations = None
    deleted_count = 0
    org_release = OrgRelease.objects.get(id=org_release_id, active=True, 
                                                **first_viewable_dict)
    
    search_query = request.GET.get('search', '')
    if search_query:
        tobjects = OrgIteration.objects.filter(name__icontains=search_query, 
                                            org_release_id=org_release_id, **viewable_dict).order_by('position')
    else:
        tobjects = OrgIteration.objects.filter(active=True, org_release_id=org_release_id).order_by('position')
        deleted = OrgIteration.objects.filter(active=False, deleted=False,
                                org_release_id=org_release_id,
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
                    object = get_object_or_404(OrgIteration, pk=item, active=True, **viewable_dict)
                    object.active = False
                    object.save()
                    
                elif bulk_operation == 'bulk_done':
                    object = get_object_or_404(OrgIteration, pk=item, active=True, **viewable_dict)
                    object.done = True
                    object.save()
                    
                elif bulk_operation == 'bulk_not_done':
                    object = get_object_or_404(OrgIteration, pk=item, active=True, **viewable_dict)
                    object.done = False
                    object.save()
                    
                elif bulk_operation == 'bulk_blocked':  # Correct the operation check here
                    object = get_object_or_404(OrgIteration, pk=item, active=True, **viewable_dict)
                    object.blocked = True
                    object.save()
                    
                else:
                    redirect('list_org_iterations', org_release_id=org_release_id)
            return redirect('list_org_iterations', org_release_id=org_release_id)
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_org_iterations',
        'org_release': org_release,
        'org_release_id': org_release_id,
        'org_id': org_release.org_id,
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
        'page_title': f'Org_iteration List',
    }       
    template_file = f"{app_name}/{module_path}/list_org_iterations.html"
    return render(request, template_file, context)





# ============================================================= #
@login_required
def list_deleted_org_iterations(request, org_release_id):
    # take inputs
    # process inputs
    user = request.user       
    objects_count = 0    
    show_all = request.GET.get('all', '25')
    objects_per_page = int(show_all) if show_all != 'all' else 25
    pagination_options = [5, 10, 15, 25, 50, 100, 'all']
    selected_bulk_operations = None
    org_release = OrgRelease.objects.get(id=org_release_id, active=True, 
                                                **first_viewable_dict)
    
    search_query = request.GET.get('search', '')
    if search_query:
        tobjects = OrgIteration.objects.filter(name__icontains=search_query, 
                                            active=False, deleted=False,
                                            org_release_id=org_release_id, **viewable_dict).order_by('position')
    else:
        tobjects = OrgIteration.objects.filter(active=False, deleted=False, org_release_id=org_release_id,
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
                        object = get_object_or_404(OrgIteration, pk=item, active=False, **viewable_dict)
                        object.active = True
                        object.save()         
                    elif bulk_operation == 'bulk_erase':
                        object = get_object_or_404(OrgIteration, pk=item, active=False, **viewable_dict)
                        object.active = False  
                        object.deleted = True             
                        object.save()    
                    else:
                        redirect('list_org_iterations', org_release_id=org_release_id)
                redirect('list_org_iterations', org_release_id=org_release_id)
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_deleted_org_iterations',
        'org_release': org_release,
        'org_release_id': org_release_id,
        'org_id': org_release.org_id,
        'module_path': module_path,
        'user': user,
        'tobjects': tobjects,
        'page_obj': page_obj,
        'objects_count': objects_count,
        'objects_per_page': objects_per_page,
        'show_all': show_all,
        'pagination_options': pagination_options,
        'selected_bulk_operations': selected_bulk_operations,
        'page_title': f'Org_iteration List',
    }       
    template_file = f"{app_name}/{module_path}/list_deleted_org_iterations.html"
    return render(request, template_file, context)



# Create View
@login_required
def create_org_basic_iteration(request, org_release_id):
    user = request.user
    org_release = OrgRelease.objects.get(id=org_release_id, active=True, 
                                                **first_viewable_dict)
    
    if request.method == 'POST':
        form = OrgIterationForm(request.POST)
        if form.is_valid():
            form.instance.author = user
            form.instance.org_release_id = org_release_id
            form.instance.iteration_start_date = form.cleaned_data['start_date']
            form.instance.iteration_end_date = form.cleaned_data['end_date']
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list_org_iterations', org_release_id=org_release_id)
    else:
        form = OrgIterationForm()

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'create_org_iteration',
        'org_release': org_release,
        'org_release_id': org_release_id,
        'org_id': org_release.org_id,
        'module_path': module_path,
        'form': form,
        'page_title': f'Create Org Iteration',
    }
    template_file = f"{app_name}/{module_path}/create_org_iteration.html"
    return render(request, template_file, context)


# Create View
@login_required
def create_org_iteration(request, org_release_id):
    user = request.user
    org_release = OrgRelease.objects.get(id=org_release_id, active=True, 
                                                **first_viewable_dict)
    
    if request.method == 'POST':
        form = OrgIterationForm(request.POST)
        if form.is_valid():
            form.instance.author = user
            form.instance.org_release_id = org_release_id
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list_org_iterations', org_release_id=org_release_id)
    else:
        form = OrgIterationForm()

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'create_org_iteration',
        'org_release': org_release,
        'org_release_id': org_release_id,
        'org_id': org_release.org_id,
        'module_path': module_path,
        'form': form,
        'page_title': f'Create Org Iteration',
    }
    template_file = f"{app_name}/{module_path}/create_org_iteration.html"
    return render(request, template_file, context)



# Edit
@login_required
def edit_org_iteration(request, org_release_id, org_iteration_id):
    user = request.user
    org_release = OrgRelease.objects.get(id=org_release_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(OrgIteration, pk=org_iteration_id, active=True,**viewable_dict)
    if request.method == 'POST':
        form = OrgIterationForm(request.POST, instance=object)
        if form.is_valid():
            form.instance.author = user
            form.instance.org_release_id = org_release_id
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list_org_iterations', org_release_id=org_release_id)
    else:
        form = OrgIterationForm(instance=object)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'edit_org_iteration',
        'org_release': org_release,
        'org_release_id': org_release_id,
        'org_id': org_release.org_id,
        'module_path': module_path,
        'form': form,
        'object': object,
        'page_title': f'Edit Org Iteration',
    }
    template_file = f"{app_name}/{module_path}/edit_org_iteration.html"
    return render(request, template_file, context)



@login_required
def delete_org_iteration(request, org_release_id, org_iteration_id):
    user = request.user
    org_release = OrgRelease.objects.get(id=org_release_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(OrgIteration, pk=org_iteration_id, active=True,**viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.save()
        return redirect('list_org_iterations', org_release_id=org_release_id)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'delete_org_iteration',
        'org_release': org_release,
        'org_release_id': org_release_id,
        'org_id': org_release.org_id,
        'module_path': module_path,        
        'object': object,
        'page_title': f'Delete Org Iteration',
    }
    template_file = f"{app_name}/{module_path}/delete_org_iteration.html"
    return render(request, template_file, context)


@login_required
def permanent_deletion_org_iteration(request, org_release_id, org_iteration_id):
    user = request.user
    org_release = OrgRelease.objects.get(id=org_release_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(OrgIteration, pk=org_iteration_id, active=False, deleted=False, **viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.deleted = True
        object.save()
        return redirect('list_org_iterations', org_release_id=org_release_id)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'permanent_deletion_org_iteration',
        'org_release': org_release,
        'org_release_id': org_release_id,
        'org_id': org_release.org_id,
        'module_path': module_path,        
        'object': object,
        'page_title': f'Permanent Deletion Org Iteration',
    }
    template_file = f"{app_name}/{module_path}/permanent_deletion_org_iteration.html"
    return render(request, template_file, context)


@login_required
def restore_org_iteration(request,  org_release_id, org_iteration_id):
    user = request.user
    object = get_object_or_404(OrgIteration, pk=org_iteration_id, active=False,**viewable_dict)
    object.active = True
    object.save()
    return redirect('list_org_iterations', org_release_id=org_release_id)
   


@login_required
def view_org_iteration(request, org_release_id, org_iteration_id):
    user = request.user
    org_release = OrgRelease.objects.get(id=org_release_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(OrgIteration, pk=org_iteration_id, active=True,**viewable_dict)    

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'view_org_iteration',
        'org_release': org_release,
        'org_release_id': org_release_id,
        'org_id': org_release.org_id,
        'module_path': module_path,
        'object': object,
        'page_title': f'View Org Iteration',
    }
    template_file = f"{app_name}/{module_path}/view_org_iteration.html"
    return render(request, template_file, context)



from app_organization.mod_backlog.views_project_tree import get_tree_name_id
@login_required
def view_iteration_kanban(request, org_id, project_id):
    user = request.user
    
    project = get_object_or_404(Project, pk=project_id, active=True, **viewable_dict)
    org = get_object_or_404(Organization, pk=org_id, active=True, **viewable_dict)
    pro_id = project.id
    pro = project
    # Prepare the Backlog types
    project_id_str = f"{pro_id}_PROJECT_TREE"
    root_project_type = BacklogType.objects.filter(name=project_id_str, active=True).first()
    project_backlog_root = Backlog.objects.filter(pro=pro, name=project_id_str).first()
    bt_tree_name_and_id = get_tree_name_id(root_project_type)
    bug_type_id = bt_tree_name_and_id.get("Bug")
    story_type_id = bt_tree_name_and_id.get("User Story")
    tech_task_type_id = bt_tree_name_and_id.get("Technical Task")
    feature_type_id = bt_tree_name_and_id.get("Feature")
    component_type_id = bt_tree_name_and_id.get("Component")
    capability_type_id = bt_tree_name_and_id.get("Capability")
    include_types = [bug_type_id, story_type_id, tech_task_type_id, feature_type_id, component_type_id, capability_type_id]  
    display_backlog_items = Backlog.objects.filter(pro=pro, active=True, type__in=include_types).order_by('position')
    
    # Prepare the include types
    
    # Send the display backlog items
    
    # Send the current iteration details
    
    # Send the next iteration details 
    
    today = date.today()
  
    # Query for the nearest release
    nearest_release = OrgRelease.objects.filter(
        Q(release_start_date__gte=today, active=True)  # Start date is today or in the future
    ).order_by('release_start_date').first()  # Get the nearest release by start date
    
    
    # prepare for Backlog, two iteration kanban
    if nearest_release:
        iterations = OrgIteration.objects.filter(
            org_release=nearest_release  # Filter iterations by release
        ).order_by('iteration_start_date')[:2]  # Get the first two iterations

    # Backlog items NOT linked to any release or iteration
    unassigned_backlog = Backlog.objects.filter(
        Q(release__isnull=True) & Q(iteration__isnull=True) & Q(pro=project)
    )

    # Backlog items linked to the nearest release or first two iterations
    if iterations.exists():
        backlog_in_iterations = Backlog.objects.filter(
            Q(release=nearest_release) &
            Q(iteration__in=iterations)
        )
    else:
        backlog_in_iterations = Backlog.objects.filter(
            Q(release=nearest_release)
        )

    # Backlog items NOT linked to the nearest release or its first two iterations
    display_backlog_items = Backlog.objects.exclude(
        Q(release=nearest_release) & Q(iteration__in=iterations)  # Exclude items in the nearest release and first two iterations
    ).filter(pro=pro, active=True, type__in=include_types).order_by('position')
        
    
    
    
    # Check all releases ordered by start date
    releases = OrgRelease.objects.filter(active=True).order_by('release_start_date')
    for r in releases:
        logger.debug(f">>> === {r.name}, Start: {r.release_start_date}, Active: {r.active} === <<<")
   
    # Fetch all releases and prefetch iterations
    releases = OrgRelease.objects.prefetch_related('org_release_org_iterations').order_by('release_start_date', 'position')
    org_releases = releases
    current_iteration = None
    next_iteration = None
    # Fetch related OrgIterations within active OrgReleases
    org_release_org_iterations = (
        OrgIteration.objects.filter(
            org_release__in=org_releases,  # Filter by releases linked to OrgIterations
            iteration_start_date__lte=today,
            iteration_end_date__gte=today,
            active=True  # Ensure only active iterations
        ).select_related('org_release')  # Optimize queries with joins
    )
    logger.debug(f">>> === ORG RELEASE ORG ITERATIONS: {org_release_org_iterations} === <<<")
    current_iteration = org_release_org_iterations.first()
    next_iteration = OrgIteration.objects.filter(
        org_release__in=org_releases,  # Filter by releases linked to OrgIterations
        iteration_start_date__gt=today,
        active=True  # Ensure only active iterations
    ).order_by('iteration_start_date').first()
    project_backlog = Backlog.objects.filter(pro=pro, active=True).order_by('position')

   # Group releases by year and calculate positions
    year_data = {}
    for release in releases:
        year = release.release_start_date.year

        # Ensure the year is initialized
        if year not in year_data:
            year_data[year] = []

        # Calculate total days in the year
        year_start = date(year, 1, 1)
        year_end = date(year, 12, 31)
        total_year_days = (year_end - year_start).days

        # Normalize release_start_date to a date type
        release_start_date = release.release_start_date.date()

        # Calculate position of release as a percentage within the year
        release_days_from_start = (release_start_date - year_start).days
        release_position = (release_days_from_start / total_year_days) * 100
        release_position = max(0, min(release_position, 100))  # Clamp to 0-100%

        # Handle iterations within the release
        total_release_days = (release.release_end_date - release.release_start_date).days
        iterations = []
        for iteration in release.org_release_org_iterations.filter(active=True):
            iter_days_from_start = (iteration.iteration_start_date - release.release_start_date).days
            iter_position = (iter_days_from_start / total_release_days) * 100 if total_release_days > 0 else 0
            iter_position = max(0, min(iter_position, 100))  # Clamp to 0-100%
            iterations.append({
                'id': iteration.id,
                'name': iteration.name,
                'start_date': iteration.iteration_start_date,
                'end_date': iteration.iteration_end_date,
                'position': iter_position
            })

        # Append release data
        year_data[year].append({
            'id': release.id,
            'name': release.name,
            'start_date': release.release_start_date,
            'end_date': release.release_end_date,
            'release_position': release_position,
            'iterations': iterations
        })

    # Calculate positions for markers
    month_positions = [(i / 12) * 100 for i in range(1, 13)]
    week_positions = [(i / 52) * 100 for i in range(1, 53)]


    if 'edit_map_project_release' in request.GET:
        project.project_release_mapped_flag = False
        project.save()
        return redirect('view_iteration_kanban', org_id=org_id, project_id=project_id)
    if request.method == 'POST':
        iteration_id = request.POST.get('map_project_release')
        if iteration_id:  
            try:
                iteration = OrgIteration.objects.get(id=iteration_id, active=True)
                project.project_release_mapped_flag = True
                project.project_iteration = iteration
                project.project_release = iteration.org_release
                project.save()

            except OrgIteration.DoesNotExist:
                return HttpResponse("Invalid selection!", status=400)
        else:
            project.project_release_mapped_flag = False
            project.project_iteration = None
            project.project_release = None
            project.save()


    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'view_iteration_kanban',
       
        
        'project': project,
        'project_id': project_id,
        'org': org,
        'organization': org,
        'organization': org,
        'org_id': org_id,
        'pro_id': project_id,
        
        'release': nearest_release,   
        'nearest_release': nearest_release,    
        'releases': releases,        
        'years': year_data,
        'month_positions': month_positions,
        'week_positions': week_positions,
        
        'current_iteration': current_iteration,
        'next_iteration': next_iteration,
        
        'display_backlog_items': display_backlog_items,
        'project_backlog': project_backlog,
        
        
        'module_path': module_path,
        'object': object,
        'page_title': f'View Iteration Kanban',
    }
    template_file = f"{app_name}/{module_path}/view_iteration_kanban.html"
    return render(request, template_file, context)


@login_required
def ajax_backlog_iteration_planning_update(request):
    if request.method == "POST":
        data = json.loads(request.body)
        card_id = data.get('card_id')
        from_state_id = data.get('from_state_id')
        to_state_id = data.get('to_state_id')

        # position 
        positions = data.get('positions')
        from_column = data.get('from_column')
        dest_column = data.get('dest_column')
        project_id = data.get('project_id')

        
        logger.debug(f">>> === card_id: {card_id}, from_state_id: {from_state_id}, to_state_id: {to_state_id} === <<<")
        logger.debug(f">>> === positions: {positions}, from_column: {from_column}, dest_column: {dest_column} === <<<")
        logger.debug(f">>> === project_id: {project_id} === <<<")
        
        if from_state_id != 0 and to_state_id == 0:
            # This is from iteration to backlog
            backlog = Backlog.objects.get(id=card_id)
            backlog.iteration = None
            backlog.release = None
            backlog.save()
            store_backlog_positions(request, positions)
        elif from_state_id == 0 and to_state_id != 0:
            # This is from backlog to iteration
            iteration = OrgIteration.objects.get(id=to_state_id)
            backlog = Backlog.objects.get(id=card_id)
            backlog.iteration = iteration
            backlog.release = iteration.org_release
            backlog.save()
            store_backlog_positions(request, positions)
        elif from_state_id != 0 and to_state_id != 0:
            # This is from iteration to iteration
            iteration = OrgIteration.objects.get(id=to_state_id)
            backlog = Backlog.objects.get(id=card_id)
            backlog.iteration = iteration
            backlog.release = iteration.org_release           
            backlog.save()
            store_backlog_positions(request, positions)
        elif from_state_id == 0 and to_state_id == 0:
            # This is from backlog to backlog
            # update the positions
            for i, card_id in enumerate(positions):
                backlog = Backlog.objects.get(id=card_id)
                backlog.position = i
                backlog.save()
        else:
            pass
        
        return JsonResponse({'message': 'success'}, status=200)
    
def store_backlog_positions(request, positions):
    for i, card in enumerate(positions):
        card_id = card.get('card_id')
        backlog = Backlog.objects.get(id=card_id)
        backlog.position = i
        backlog.save()
        
    return True
    