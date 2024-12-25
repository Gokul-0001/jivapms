
from app_organization.mod_app.all_view_imports import *
from app_organization.mod_org_release.models_org_release import *
from app_organization.mod_org_release.forms_org_release import *

from app_organization.mod_organization.models_organization import *
from app_organization.mod_org_iteration.models_org_iteration import *

from app_organization.mod_app.all_view_imports import *
from app_organization.mod_project.models_project import *
from app_common.mod_common.models_common import *

from app_jivapms.mod_app.all_view_imports import *

app_name = 'app_organization'
app_version = 'v1'

module_name = 'org_releases'
module_path = f'mod_org_release'

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
def list_org_releases(request, org_id):
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
    search_query = request.GET.get('search', '')
    if search_query:
        tobjects = OrgRelease.objects.filter(name__icontains=search_query, 
                                            org_id=org_id, **viewable_dict).order_by('position').annotate(
                                iteration_count=Count('org_release_org_iterations', filter=Q(org_release_org_iterations__active=True))
                            )
    else:
        tobjects = OrgRelease.objects.filter(active=True, org_id=org_id).order_by('position').annotate(
                            iteration_count=Count('org_release_org_iterations', filter=Q(org_release_org_iterations__active=True))
                        )
        deleted = OrgRelease.objects.filter(active=False, deleted=False,
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
                    object = get_object_or_404(OrgRelease, pk=item, active=True, **viewable_dict)
                    object.active = False
                    object.save()
                    
                elif bulk_operation == 'bulk_done':
                    object = get_object_or_404(OrgRelease, pk=item, active=True, **viewable_dict)
                    object.done = True
                    object.save()
                    
                elif bulk_operation == 'bulk_not_done':
                    object = get_object_or_404(OrgRelease, pk=item, active=True, **viewable_dict)
                    object.done = False
                    object.save()
                    
                elif bulk_operation == 'bulk_blocked':  # Correct the operation check here
                    object = get_object_or_404(OrgRelease, pk=item, active=True, **viewable_dict)
                    object.blocked = True
                    object.save()
                    
                else:
                    redirect('list_org_releases', org_id=org_id)
            return redirect('list_org_releases', org_id=org_id)
    
    
    # sending the iterations count 
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_org_releases',
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
        'page_title': f'Org_release List',
        
        'project': project,
        'project_id': project_id,
        'pro_id': project_id,
    }       
    template_file = f"{app_name}/{module_path}/list_org_releases.html"
    return render(request, template_file, context)





# ============================================================= #
@login_required
def list_deleted_org_releases(request, org_id):
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
        tobjects = OrgRelease.objects.filter(name__icontains=search_query, 
                                            active=False, deleted=False,
                                            org_id=org_id, **viewable_dict).order_by('position')
    else:
        tobjects = OrgRelease.objects.filter(active=False, deleted=False, org_id=org_id,
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
                        object = get_object_or_404(OrgRelease, pk=item, active=False, **viewable_dict)
                        object.active = True
                        object.save()         
                    elif bulk_operation == 'bulk_erase':
                        object = get_object_or_404(OrgRelease, pk=item, active=False, **viewable_dict)
                        object.active = False  
                        object.deleted = True             
                        object.save()    
                    else:
                        redirect('list_org_releases', org_id=org_id)
                redirect('list_org_releases', org_id=org_id)
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_deleted_org_releases',
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
        'page_title': f'Org_release List',
        
        'project': project,
        'project_id': project_id,
        'pro_id': project_id,
    }       
    template_file = f"{app_name}/{module_path}/list_deleted_org_releases.html"
    return render(request, template_file, context)



# # Create View
# @login_required
# def create_org_release(request, org_id):
#     user = request.user
#     organization = Organization.objects.get(id=org_id, active=True, 
#                                                 **first_viewable_dict)
    
#     if request.method == 'POST':
#         form = OrgReleaseForm(request.POST)
#         if form.is_valid():
#             form.instance.author = user
#             form.instance.org_id = org_id
#             form.save()
#         else:
#             print(f">>> === form.errors: {form.errors} === <<<")
#         return redirect('list_org_releases', org_id=org_id)
#     else:
#         form = OrgReleaseForm()

#     context = {
#         'parent_page': '___PARENTPAGE___',
#         'page': 'create_org_release',
#         'organization': organization,
#         'org_id': org_id,
        
#         'module_path': module_path,
#         'form': form,
#         'page_title': f'Create Org Release',
#     }
#     template_file = f"{app_name}/{module_path}/create_org_release.html"
#     return render(request, template_file, context)

# Create View
from datetime import datetime, time, timedelta
import pytz
@login_required
def create_org_release(request, org_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    project = None
    project_id = None
    if 'project_id' in request.GET:
        project_id = request.GET.get('project_id')
        project = get_object_or_404(Project, pk=project_id, active=True, **viewable_dict)
    if request.method == 'POST':
        form = OrgReleaseForm(request.POST)
        if form.is_valid():
            form.instance.author = user
            form.instance.org_id = org_id
            
            # Set the time to 9:00 AM IST
            ist = pytz.timezone('Asia/Kolkata')

            # Handle start_date
            start_date = form.cleaned_data['start_date']
            if isinstance(start_date, datetime):
                # Already datetime, just add time and set timezone
                start_date = start_date.replace(hour=9, minute=0, second=0, tzinfo=ist)
            else:
                # Convert to datetime with 9 AM time and set timezone
                start_date = datetime.combine(start_date, time(9, 0))
                start_date = ist.localize(start_date)  # Make it timezone-aware

            # Handle end_date
            end_date = form.cleaned_data['end_date']
            if isinstance(end_date, datetime):
                # Already datetime, just add time and set timezone
                end_date = end_date.replace(hour=9, minute=0, second=0, tzinfo=ist)
            else:
                # Convert to datetime with 9 AM time and set timezone
                end_date = datetime.combine(end_date, time(9, 0))
                end_date = ist.localize(end_date)  # Make it timezone-aware

            # Assign updated values to the form
            form.instance.start_date = start_date
            form.instance.end_date = end_date

            release = form.save()   
            
            
            # Predecessors assignment
            # Handle predecessors
            predecessor_ids = request.POST.get('predecessors', '')
            if predecessor_ids:
                predecessor_ids = [int(id) for id in predecessor_ids.split(',')]
                release.predecessors.set(predecessor_ids)

            if 'create_iterations' in request.POST:
                no_of_iterations = int(request.POST.get('no_of_iterations', 5))
                iteration_length = int(form.cleaned_data['apply_release_iteration_length'])
                start_date = form.cleaned_data['start_date']

                # Set the default time to 9:00 AM IST
                ist = pytz.timezone('Asia/Kolkata')
                start_date = datetime.combine(start_date, time(9, 0))  # Add 9 AM time
                start_date = ist.localize(start_date)  # Make it timezone-aware

                # Clear old iterations
                OrgIteration.objects.filter(org_release=release).update(active=False, deleted=True)

                for i in range(no_of_iterations):
                    # Calculate iteration end date
                    iteration_end = start_date + timedelta(weeks=iteration_length)

                    # Create iteration
                    OrgIteration.objects.create(
                        org_release=release,
                        name=f"Iteration {i + 1}",
                        start_date=start_date,  # Already has 9:00 AM IST
                        end_date=iteration_end  # Already has 9:00 AM IST
                    )

                    # Move to next start date
                    start_date = iteration_end

            messages.success(request, 'Release saved successfully!')
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list_org_releases', org_id=org_id)
    else:
        form = OrgReleaseForm()

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'create_org_release',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,
        'form': form,
        'page_title': f'Create Org Release',
        
        'project': project,
        'project_id': project_id,
        'pro_id': project_id,
    }
    template_file = f"{app_name}/{module_path}/create_org_release.html"
    return render(request, template_file, context)


# Edit
@login_required
def edit_org_release(request, org_id, org_release_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    project = None
    project_id = None
    if 'project_id' in request.GET:
        project_id = request.GET.get('project_id')
        project = get_object_or_404(Project, pk=project_id, active=True, **viewable_dict)
    object = get_object_or_404(OrgRelease, pk=org_release_id, active=True,**viewable_dict)
    if request.method == 'POST':
        form = OrgReleaseForm(request.POST, instance=object)
        if form.is_valid():
            form.instance.author = user
            form.instance.org_id = org_id
              # Set the time to 9:00 AM IST
            ist = pytz.timezone('Asia/Kolkata')

            # Handle start_date
            start_date = form.cleaned_data['start_date']
            if isinstance(start_date, datetime):
                # Already datetime, just add time and set timezone
                start_date = start_date.replace(hour=9, minute=0, second=0, tzinfo=ist)
            else:
                # Convert to datetime with 9 AM time and set timezone
                start_date = datetime.combine(start_date, time(9, 0))
                start_date = ist.localize(start_date)  # Make it timezone-aware

            # Handle end_date
            end_date = form.cleaned_data['end_date']
            if isinstance(end_date, datetime):
                # Already datetime, just add time and set timezone
                end_date = end_date.replace(hour=9, minute=0, second=0, tzinfo=ist)
            else:
                # Convert to datetime with 9 AM time and set timezone
                end_date = datetime.combine(end_date, time(9, 0))
                end_date = ist.localize(end_date)  # Make it timezone-aware

            # Assign updated values to the form
            form.instance.start_date = start_date
            form.instance.end_date = end_date

            release = form.save()   
             # Predecessors assignment
            # Handle predecessors
            predecessor_ids = request.POST.get('predecessors', '')
            if predecessor_ids:
                predecessor_ids = [int(id) for id in predecessor_ids.split(',')]
                release.predecessors.set(predecessor_ids)

            if 'create_iterations' in request.POST:
                no_of_iterations = int(request.POST.get('no_of_iterations', 5))
                iteration_length = int(form.cleaned_data['apply_release_iteration_length'])
                start_date = form.cleaned_data['start_date']

                # Set the default time to 9:00 AM IST
                ist = pytz.timezone('Asia/Kolkata')
                start_date = datetime.combine(start_date, time(9, 0))  # Add 9 AM time
                start_date = ist.localize(start_date)  # Make it timezone-aware

                # Clear old iterations
                OrgIteration.objects.filter(org_release=release).update(active=False, deleted=True)

                for i in range(no_of_iterations):
                    # Calculate iteration end date
                    iteration_end = start_date + timedelta(weeks=iteration_length)

                    # Create iteration
                    OrgIteration.objects.create(
                        org_release=release,
                        name=f"Iteration {i + 1}",
                        start_date=start_date,  # Already has 9:00 AM IST
                        end_date=iteration_end  # Already has 9:00 AM IST
                    )

                    # Move to next start date
                    start_date = iteration_end

            messages.success(request, 'Release saved successfully!')
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list_org_releases', org_id=org_id)
    else:
        form = OrgReleaseForm(instance=object)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'edit_org_release',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,
        'form': form,
        'object': object,
        'page_title': f'Edit Org Release',
        
        'project': project,
        'project_id': project_id,
        'pro_id': project_id,
    }
    template_file = f"{app_name}/{module_path}/edit_org_release.html"
    return render(request, template_file, context)



@login_required
def delete_org_release(request, org_id, org_release_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    project = None
    project_id = None
    if 'project_id' in request.GET:
        project_id = request.GET.get('project_id')
        project = get_object_or_404(Project, pk=project_id, active=True, **viewable_dict)
    object = get_object_or_404(OrgRelease, pk=org_release_id, active=True,**viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.save()
        return redirect('list_org_releases', org_id=org_id)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'delete_org_release',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,        
        'object': object,
        'page_title': f'Delete Org Release',
        
        'project': project,
        'project_id': project_id,
        'pro_id': project_id,
    }
    template_file = f"{app_name}/{module_path}/delete_org_release.html"
    return render(request, template_file, context)


@login_required
def permanent_deletion_org_release(request, org_id, org_release_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(OrgRelease, pk=org_release_id, active=False, deleted=False, **viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.deleted = True
        object.save()
        return redirect('list_org_releases', org_id=org_id)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'permanent_deletion_org_release',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,        
        'object': object,
        'page_title': f'Permanent Deletion Org Release',
        
        'project': project,
        'project_id': project_id,
        'pro_id': project_id,
    }
    template_file = f"{app_name}/{module_path}/permanent_deletion_org_release.html"
    return render(request, template_file, context)


@login_required
def restore_org_release(request,  org_id, org_release_id):
    user = request.user
    object = get_object_or_404(OrgRelease, pk=org_release_id, active=False,**viewable_dict)
    object.active = True
    object.save()
    return redirect('list_org_releases', org_id=org_id)
   


@login_required
def view_org_release(request, org_id, org_release_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    project = None
    project_id = None
    if 'project_id' in request.GET:
        project_id = request.GET.get('project_id')
        project = get_object_or_404(Project, pk=project_id, active=True, **viewable_dict)
    object = get_object_or_404(OrgRelease, pk=org_release_id, active=True,**viewable_dict)    

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'view_org_release',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,
        'object': object,
        'page_title': f'View Org Release',
        
        'project': project,
        'project_id': project_id,
        'pro_id': project_id,
    }
    template_file = f"{app_name}/{module_path}/view_org_release.html"
    return render(request, template_file, context)


@login_required
def ajax_search_org_release_predecessors(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from the request
            data = json.loads(request.body)
            query = data.get('query', '').strip()

            # Filter predecessors based on the query
            if query:
                predecessors = OrgRelease.objects.filter(name__icontains=query, active=True)[:10]
                result = [{'id': pred.id, 'name': pred.name, 'release_start_date': pred.release_start_date, 'release_end_date': pred.release_end_date} for pred in predecessors]
            else:
                result = []

            # Return JSON response
            return JsonResponse(result, safe=False)

        except Exception as e:
            # Return error response if something goes wrong
            return JsonResponse({'error': str(e)}, status=400)
    else:
        # If request is not POST, return bad request
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    
@login_required
def create_org_global_release(request, org_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    project = None
    project_id = None
    if 'project_id' in request.GET:
        project_id = request.GET.get('project_id')
        project = get_object_or_404(Project, pk=project_id, active=True, **viewable_dict)
    form = OrgReleaseForm()
    
    if request.method == 'POST':
        # Read and parse release data from POST request
        release_data = json.loads(request.POST.get('release_data'))

        # Extract fields from release_data
        year = release_data['year']
        iteration_length = release_data['iterationLength']
        start_date = release_data['startDate']
        releases = release_data['releases']
        
        logger.debug(f"Year: {year}")
        logger.debug(f"Iteration Length: {iteration_length}")
        logger.debug(f"Start Date: {start_date}")
        logger.debug(f"Release Data: {release_data}")
        
        
        # Check if releases already exist for the given year
        existing_releases = OrgRelease.objects.filter(year=year, org_id=org_id, active=True)
        logger.debug(f"Checking if releases already exist for year {year} for org {org_id}")
        logger.debug(f"Existing releases: {existing_releases}")
        if existing_releases.exists():
            #return JsonResponse({'error': 'Releases already exist for this year.'}, status=400)
            error_details = 'Releases already exist for this year.'
            logger.debug(f"Releases already exist for year {year} for org {org_id}")
        else:
            try:
                with transaction.atomic():
                    release_counter = 1
                    logger.debug(f"Creating global releases for year {year} for org {org_id}")
                    for release_info in releases:
                        logger.debug(f"TEST Release info: {release_info}")
                        # Create the release
                        release_name = f'{organization}-{year}-Release{release_counter}'
                        
                        quarter = release_info['quarter']
                        release_number = release_info['releaseNumber']
                        logger.debug(f"Creating release {release_name}")
                        logger.debug(f"Creating release {release_number}")
                        logger.debug(f"Creating release {quarter}")
                        major_version = str(year)[-2:]
                        release = OrgRelease.objects.create(
                            org_id=org_id,
                            name=f"{major_version}-Rel-{release_number}",
                            release_official_name=release_name,
                            quarter=release_info['quarter'],
                            year=year,                            
                            major_version=major_version,                            
                            release_start_date=release_info['startDate'],
                            release_end_date=release_info['endDate'],
                            apply_release_iteration_length=iteration_length,
                            version=f"{release_number}",
                        )
                        logger.debug(f"Release {release_name} {release.release_start_date} created successfully")

                        # Create iterations under the release
                        for iteration in release_info['iterations']:
                            iteration_number = iteration['iteration']
                            OrgIteration.objects.create(
                                org_release=release,
                                quarter=iteration['quarter'],
                                name = f'Iteration {iteration["iteration"]}',
                                iteration_number=iteration['iteration'],
                                iteration_start_date=iteration['startDate'],
                                iteration_end_date=iteration['startDate'],
                                start_day = iteration['startDay'],
                                end_day = iteration['endDay'],
                                version=f"{iteration_number}",
                            )

                        release_counter += 1
                return redirect('list_org_releases', org_id=org_id)
            except Exception as e:
                error_details = str(e)
                logger.error(f"Error creating global releases: {error_details}")
        
    else:
        form = OrgReleaseForm()

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'create_org_release',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,
        'form': form,
        'page_title': f'Create Org Release',
        'project': project,
        'project_id': project_id,
        'pro_id': project_id,
    }
    template_file = f"{app_name}/{module_path}/create_org_global_release.html"
    return render(request, template_file, context)