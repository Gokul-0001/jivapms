
from app_organization.mod_app.all_view_imports import *
from app_jivapms.mod_app.all_view_imports import *
from app_organization.mod_ops_value_stream.models_ops_value_stream import *
from app_organization.mod_ops_value_stream.forms_ops_value_stream import *
from app_organization.mod_ops_value_stream_step.models_ops_value_stream_step import *
from app_organization.mod_organization.models_organization import *

from app_common.mod_common.models_common import *

app_name = 'app_organization'
app_version = 'v1'

module_name = 'ops_value_streams'
module_path = f'mod_ops_value_stream'

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
def list_ops_value_streams(request, org_id):
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
    
    search_query = request.GET.get('search', '')
    if search_query:
        tobjects = OpsValueStream.objects.filter(name__icontains=search_query, 
                                            org_id=org_id, **viewable_dict).order_by('position')
    else:
        tobjects = OpsValueStream.objects.filter(active=True, org_id=org_id).order_by('position')
        deleted = OpsValueStream.objects.filter(active=False, deleted=False,
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
                    object = get_object_or_404(OpsValueStream, pk=item, active=True, **viewable_dict)
                    object.active = False
                    object.save()
                    
                elif bulk_operation == 'bulk_done':
                    object = get_object_or_404(OpsValueStream, pk=item, active=True, **viewable_dict)
                    object.done = True
                    object.save()
                    
                elif bulk_operation == 'bulk_not_done':
                    object = get_object_or_404(OpsValueStream, pk=item, active=True, **viewable_dict)
                    object.done = False
                    object.save()
                    
                elif bulk_operation == 'bulk_blocked':  # Correct the operation check here
                    object = get_object_or_404(OpsValueStream, pk=item, active=True, **viewable_dict)
                    object.blocked = True
                    object.save()
                    
                else:
                    redirect('list_ops_value_streams', org_id=org_id)
            return redirect('list_ops_value_streams', org_id=org_id)
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_ops_value_streams',
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
        'page_title': f'Ops_value_stream List',
    }       
    template_file = f"{app_name}/{module_path}/list_ops_value_streams.html"
    return render(request, template_file, context)





# ============================================================= #
@login_required
def list_deleted_ops_value_streams(request, org_id):
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
    
    search_query = request.GET.get('search', '')
    if search_query:
        tobjects = OpsValueStream.objects.filter(name__icontains=search_query, 
                                            active=False,
                                            org_id=org_id, **viewable_dict).order_by('position')
    else:
        tobjects = OpsValueStream.objects.filter(active=False, org_id=org_id,
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
                        object = get_object_or_404(OpsValueStream, pk=item, active=False, **viewable_dict)
                        object.active = True
                        object.save()         
                    elif bulk_operation == 'bulk_erase':
                        object = get_object_or_404(OpsValueStream, pk=item, active=False, **viewable_dict)
                        object.active = False  
                        object.deleted = True             
                        object.save()    
                    else:
                        redirect('list_ops_value_streams', org_id=org_id)
                redirect('list_ops_value_streams', org_id=org_id)
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_deleted_ops_value_streams',
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
        'page_title': f'Ops_value_stream List',
    }       
    template_file = f"{app_name}/{module_path}/list_deleted_ops_value_streams.html"
    return render(request, template_file, context)



# Create View
@login_required
def create_ops_value_stream(request, org_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    
    if request.method == 'POST':
        form = OpsValueStreamForm(request.POST)
        if form.is_valid():
            form.instance.author = user
            form.instance.org_id = org_id
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list_ops_value_streams', org_id=org_id)
    else:
        form = OpsValueStreamForm()

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'create_ops_value_stream',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,
        'form': form,
        'page_title': f'Create Ops Value Stream',
    }
    template_file = f"{app_name}/{module_path}/create_ops_value_stream.html"
    return render(request, template_file, context)




# Edit
@login_required
def edit_ops_value_stream(request, org_id, ops_value_stream_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(OpsValueStream, pk=ops_value_stream_id, active=True,**viewable_dict)
    if request.method == 'POST':
        form = OpsValueStreamForm(request.POST, instance=object)
        if form.is_valid():
            form.instance.author = user
            form.instance.org_id = org_id
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list_ops_value_streams', org_id=org_id)
    else:
        form = OpsValueStreamForm(instance=object)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'edit_ops_value_stream',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,
        'form': form,
        'object': object,
        'page_title': f'Edit Ops Value Stream',
    }
    template_file = f"{app_name}/{module_path}/edit_ops_value_stream.html"
    return render(request, template_file, context)



@login_required
def delete_ops_value_stream(request, org_id, ops_value_stream_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(OpsValueStream, pk=ops_value_stream_id, active=True,**viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.save()
        return redirect('list_ops_value_streams', org_id=org_id)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'delete_ops_value_stream',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,        
        'object': object,
        'page_title': f'Delete Ops Value Stream',
    }
    template_file = f"{app_name}/{module_path}/delete_ops_value_stream.html"
    return render(request, template_file, context)


@login_required
def permanent_deletion_ops_value_stream(request, org_id, ops_value_stream_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(OpsValueStream, pk=ops_value_stream_id, active=False, deleted=False, **viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.deleted = True
        object.save()
        return redirect('list_ops_value_streams', org_id=org_id)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'permanent_deletion_ops_value_stream',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,        
        'object': object,
        'page_title': f'Permanent Deletion Ops Value Stream',
    }
    template_file = f"{app_name}/{module_path}/permanent_deletion_ops_value_stream.html"
    return render(request, template_file, context)


@login_required
def restore_ops_value_stream(request,  org_id, ops_value_stream_id):
    user = request.user
    object = get_object_or_404(OpsValueStream, pk=ops_value_stream_id, active=False,**viewable_dict)
    object.active = True
    object.save()
    return redirect('list_ops_value_streams', org_id=org_id)
   


@login_required
def view_ops_value_stream(request, org_id, ops_value_stream_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(OpsValueStream, pk=ops_value_stream_id, active=True,**viewable_dict)    

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'view_ops_value_stream',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,
        'object': object,
        'page_title': f'View Ops Value Stream',
    }
    template_file = f"{app_name}/{module_path}/view_ops_value_stream.html"
    return render(request, template_file, context)


@login_required
def view_ovs(request, org_id, ops_value_stream_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(OpsValueStream, pk=ops_value_stream_id, active=True,**viewable_dict)    
    
    # Fetch related OpsValueStreamStep objects
    steps = OpsValueStreamStep.objects.filter(ops=object).order_by('position')
    steps_data = [
        {
            "id": step.id,
            "name": step.name or f"Step {step.id}",  # Default name if none exists
            "value": step.value,
            "delay": step.delay
        }
        for step in steps
    ]
    check_data = []

    # Filter and clean the `steps` to ensure no extra steps are added
    valid_steps = list(filter(lambda step: step.id is not None and step.name, steps))

    for i, step in enumerate(valid_steps):
        check_data.append({
            "id": step.id,
            "name": step.name or f"Step {step.id}",
            "value": step.value,
            "delay": step.delay,
            "next_id": valid_steps[i + 1].id if i + 1 < len(valid_steps) else None,
            "next_name": valid_steps[i + 1].name if i + 1 < len(valid_steps) else None,
        })

    #logger.debug(f">>> === steps_data: {steps_data} === <<<")
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'View OVS',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,
        'object': object,
        'steps_data': steps_data,
        'check_data': check_data,
        'page_title': f'View OVS',
    }
    template_file = f"{app_name}/{module_path}/view_ovs.html"
    return render(request, template_file, context)


