
from app_organization.mod_app.all_view_imports import *
from app_organization.mod_impact_map.models_impact_map import *
from app_organization.mod_impact_map.forms_impact_map import *

from app_organization.mod_impact_mapping.models_impact_mapping import *

from app_common.mod_common.models_common import *
from app_jivapms.mod_app.all_view_imports import *

app_name = 'app_organization'
app_version = 'v1'

module_name = 'impact_maps'
module_path = f'mod_impact_map'

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
def list_impact_maps(request, impact_mapping_id):
    # take inputs
    # process inputs
    user = request.user       
    objects_count = 0    
    show_all = request.GET.get('all', '25')
    objects_per_page = int(show_all) if show_all != 'all' else 25
    pagination_options = [5, 10, 15, 25, 50, 100, 'all']
    selected_bulk_operations = None
    deleted_count = 0
    impact_mapping = ImpactMapping.objects.get(id=impact_mapping_id, active=True, 
                                                **first_viewable_dict)
    organization = impact_mapping.organization
    search_query = request.GET.get('search', '')
    if search_query:
        tobjects = ImpactMap.objects.filter(name__icontains=search_query, 
                                            impact_map=impact_mapping, **viewable_dict).order_by('position')
    else:
        tobjects = ImpactMap.objects.filter(active=True, impact_map=impact_mapping).order_by('position')
        deleted = ImpactMap.objects.filter(active=False, deleted=False,
                                impact_map=impact_mapping,
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
                    object = get_object_or_404(ImpactMap, pk=item, active=True, **viewable_dict)
                    object.active = False
                    object.save()
                    
                elif bulk_operation == 'bulk_done':
                    object = get_object_or_404(ImpactMap, pk=item, active=True, **viewable_dict)
                    object.done = True
                    object.save()
                    
                elif bulk_operation == 'bulk_not_done':
                    object = get_object_or_404(ImpactMap, pk=item, active=True, **viewable_dict)
                    object.done = False
                    object.save()
                    
                elif bulk_operation == 'bulk_blocked':  # Correct the operation check here
                    object = get_object_or_404(ImpactMap, pk=item, active=True, **viewable_dict)
                    object.blocked = True
                    object.save()
                    
                else:
                    redirect('list_impact_maps', impact_map=impact_mapping)
            return redirect('list_impact_maps', impact_map=impact_mapping)
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_impact_maps',
        'impact_mapping': impact_mapping,
        'impact_mapping_id': impact_mapping_id,
        'org_id': organization.id,
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
        'page_title': f'Impact_map List',
    }       
    template_file = f"{app_name}/{module_path}/list_impact_maps.html"
    return render(request, template_file, context)





# ============================================================= #
@login_required
def list_deleted_impact_maps(request, impact_mapping_id):
    # take inputs
    # process inputs
    user = request.user       
    objects_count = 0    
    show_all = request.GET.get('all', '25')
    objects_per_page = int(show_all) if show_all != 'all' else 25
    pagination_options = [5, 10, 15, 25, 50, 100, 'all']
    selected_bulk_operations = None
    impact_mapping = ImpactMapping.objects.get(id=impact_mapping_id, active=True, 
                                                **first_viewable_dict)
    organization = impact_mapping.organization
    search_query = request.GET.get('search', '')
    if search_query:
        tobjects = ImpactMap.objects.filter(name__icontains=search_query, 
                                            active=False, deleted=False,
                                            impact_map=impact_mapping, **viewable_dict).order_by('position')
    else:
        tobjects = ImpactMap.objects.filter(active=False, deleted=False, impact_map=impact_mapping,
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
                        object = get_object_or_404(ImpactMap, pk=item, active=False, **viewable_dict)
                        object.active = True
                        object.save()         
                    elif bulk_operation == 'bulk_erase':
                        object = get_object_or_404(ImpactMap, pk=item, active=False, **viewable_dict)
                        object.active = False  
                        object.deleted = True             
                        object.save()    
                    else:
                        redirect('list_impact_maps', impact_map_id=impact_mapping.id)
                redirect('list_impact_maps', impact_map_id=impact_mapping)
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_deleted_impact_maps',
        'impact_mapping': impact_mapping,
        'impact_mapping_id': impact_mapping_id,
        'org_id': organization.id,
        'module_path': module_path,
        'user': user,
        'tobjects': tobjects,
        'page_obj': page_obj,
        'objects_count': objects_count,
        'objects_per_page': objects_per_page,
        'show_all': show_all,
        'pagination_options': pagination_options,
        'selected_bulk_operations': selected_bulk_operations,
        'page_title': f'Impact_map List',
    }       
    template_file = f"{app_name}/{module_path}/list_deleted_impact_maps.html"
    return render(request, template_file, context)



# Create View
@login_required
def create_impact_map(request, impact_mapping_id):
    user = request.user
    impact_mapping = ImpactMapping.objects.get(id=impact_mapping_id, active=True, 
                                                **first_viewable_dict)
    organization = impact_mapping.organization
    if request.method == 'POST':
        form = ImpactMapForm(request.POST)
        if form.is_valid():
            form.instance.author = user
            form.instance.impact_mapping_id = impact_mapping_id
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list_impact_maps', impact_map=impact_mapping)
    else:
        form = ImpactMapForm()

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'create_impact_map',
        'impact_mapping': impact_mapping,
        'impact_mapping_id': impact_mapping_id,
        'org_id': organization.id,
        'module_path': module_path,
        'form': form,
        'page_title': f'Create Impact Map',
    }
    template_file = f"{app_name}/{module_path}/create_impact_map.html"
    return render(request, template_file, context)




# Edit
@login_required
def edit_impact_map(request, impact_mapping_id, impact_map_id):
    user = request.user
    impact_mapping = ImpactMapping.objects.get(id=impact_mapping_id, active=True, 
                                                **first_viewable_dict)
    organization = impact_mapping.organization
    object = get_object_or_404(ImpactMap, pk=impact_map_id, active=True,**viewable_dict)
    if request.method == 'POST':
        form = ImpactMapForm(request.POST, instance=object)
        if form.is_valid():
            form.instance.author = user
            form.instance.impact_mapping_id = impact_mapping_id
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        #return redirect('list_impact_maps', impact_mapping_id=impact_mapping.id)
        return redirect('view_tree_table_mapping', organization_id=organization.id, impact_mapping_id=impact_mapping.id, )
    else:
        form = ImpactMapForm(instance=object)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'edit_impact_map',
        'impact_mapping': impact_mapping,
        'impact_mapping_id': impact_mapping_id,
        'org_id': organization.id,
        'module_path': module_path,
        'form': form,
        'object': object,
        'page_title': f'Edit Impact Map',
    }
    template_file = f"{app_name}/{module_path}/edit_impact_map.html"
    return render(request, template_file, context)



@login_required
def delete_impact_map(request, impact_mapping_id, impact_map_id):
    user = request.user
    impact_mapping = ImpactMapping.objects.get(id=impact_mapping_id, active=True, 
                                                **first_viewable_dict)
    organization = impact_mapping.organization
    object = get_object_or_404(ImpactMap, pk=impact_map_id, active=True,**viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.save()
        return redirect('list_impact_maps', impact_map=impact_mapping)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'delete_impact_map',
        'impact_mapping': impact_mapping,
        'impact_mapping_id': impact_mapping_id,
        'org_id': organization.id,
        'module_path': module_path,        
        'object': object,
        'page_title': f'Delete Impact Map',
    }
    template_file = f"{app_name}/{module_path}/delete_impact_map.html"
    return render(request, template_file, context)


@login_required
def permanent_deletion_impact_map(request, impact_mapping_id, impact_map_id):
    user = request.user
    impact_mapping = ImpactMapping.objects.get(id=impact_mapping_id, active=True, 
                                                **first_viewable_dict)
    organization = impact_mapping.organization
    object = get_object_or_404(ImpactMap, pk=impact_map_id, active=False, deleted=False, **viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.deleted = True
        object.save()
        return redirect('list_impact_maps', impact_map=impact_mapping)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'permanent_deletion_impact_map',
        'impact_mapping': impact_mapping,
        'impact_mapping_id': impact_mapping_id,
        'org_id': organization.id,
        'module_path': module_path,        
        'object': object,
        'page_title': f'Permanent Deletion Impact Map',
    }
    template_file = f"{app_name}/{module_path}/permanent_deletion_impact_map.html"
    return render(request, template_file, context)


@login_required
def restore_impact_map(request,  impact_mapping_id, impact_map_id):
    user = request.user
    impact_mapping = ImpactMapping.objects.get(id=impact_mapping_id, active=True)
    organization = impact_mapping.organization
    object = get_object_or_404(ImpactMap, pk=impact_map_id, active=False,**viewable_dict)
    object.active = True
    object.save()
    return redirect('list_impact_maps', impact_map=impact_mapping)
   


@login_required
def view_impact_map(request, impact_mapping_id, impact_map_id):
    user = request.user
    impact_mapping = ImpactMapping.objects.get(id=impact_mapping_id, active=True, 
                                                **first_viewable_dict)
    organization = impact_mapping.organization
    object = get_object_or_404(ImpactMap, pk=impact_map_id, active=True,**viewable_dict)    

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'view_impact_map',
        'impact_mapping': impact_mapping,
        'impact_mapping_id': impact_mapping_id,
        'org_id': organization.id,
        'module_path': module_path,
        'object': object,
        'page_title': f'View Impact Map',
    }
    template_file = f"{app_name}/{module_path}/view_impact_map.html"
    return render(request, template_file, context)


