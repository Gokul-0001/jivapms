
from app_organization.mod_app.all_view_imports import *
from app_organization.mod_impact_mapping.models_impact_mapping import *
from app_organization.mod_impact_mapping.forms_impact_mapping import *

from app_organization.mod_organization.models_organization import *

from app_common.mod_common.models_common import *

app_name = 'app_organization'
app_version = 'v1'

module_name = 'impact_mappings'
module_path = f'mod_impact_mapping'

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
def list_impact_mappings(request, organization_id):
    # take inputs
    # process inputs
    user = request.user       
    objects_count = 0    
    show_all = request.GET.get('all', '25')
    objects_per_page = int(show_all) if show_all != 'all' else 25
    pagination_options = [5, 10, 15, 25, 50, 100, 'all']
    selected_bulk_operations = None
    deleted_count = 0
    organization = Organization.objects.get(id=organization_id, active=True, 
                                                **first_viewable_dict)
    
    search_query = request.GET.get('search', '')
    if search_query:
        tobjects = ImpactMapping.objects.filter(name__icontains=search_query, 
                                            organization_id=organization_id, **viewable_dict).order_by('position')
    else:
        tobjects = ImpactMapping.objects.filter(active=True, organization_id=organization_id).order_by('position')
        deleted = ImpactMapping.objects.filter(active=False, deleted=False,
                                organization_id=organization_id,
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
                    object = get_object_or_404(ImpactMapping, pk=item, active=True, **viewable_dict)
                    object.active = False
                    object.save()
                    
                elif bulk_operation == 'bulk_done':
                    object = get_object_or_404(ImpactMapping, pk=item, active=True, **viewable_dict)
                    object.done = True
                    object.save()
                    
                elif bulk_operation == 'bulk_not_done':
                    object = get_object_or_404(ImpactMapping, pk=item, active=True, **viewable_dict)
                    object.done = False
                    object.save()
                    
                elif bulk_operation == 'bulk_blocked':  # Correct the operation check here
                    object = get_object_or_404(ImpactMapping, pk=item, active=True, **viewable_dict)
                    object.blocked = True
                    object.save()
                    
                else:
                    redirect('list_impact_mappings', organization_id=organization_id)
            return redirect('list_impact_mappings', organization_id=organization_id)
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_impact_mappings',
        'organization': organization,
        'organization_id': organization_id,
        'org_id': organization_id,
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
        'page_title': f'Impact_mapping List',
    }       
    template_file = f"{app_name}/{module_path}/list_impact_mappings.html"
    return render(request, template_file, context)





# ============================================================= #
@login_required
def list_deleted_impact_mappings(request, organization_id):
    # take inputs
    # process inputs
    user = request.user       
    objects_count = 0    
    show_all = request.GET.get('all', '25')
    objects_per_page = int(show_all) if show_all != 'all' else 25
    pagination_options = [5, 10, 15, 25, 50, 100, 'all']
    selected_bulk_operations = None
    organization = Organization.objects.get(id=organization_id, active=True, 
                                                **first_viewable_dict)
    
    search_query = request.GET.get('search', '')
    if search_query:
        tobjects = ImpactMapping.objects.filter(name__icontains=search_query, 
                                            active=False, deleted=False,
                                            organization_id=organization_id, **viewable_dict).order_by('position')
    else:
        tobjects = ImpactMapping.objects.filter(active=False, deleted=False, organization_id=organization_id,
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
                        object = get_object_or_404(ImpactMapping, pk=item, active=False, **viewable_dict)
                        object.active = True
                        object.save()         
                    elif bulk_operation == 'bulk_erase':
                        object = get_object_or_404(ImpactMapping, pk=item, active=False, **viewable_dict)
                        object.active = False  
                        object.deleted = True             
                        object.save()    
                    else:
                        redirect('list_impact_mappings', organization_id=organization_id)
                redirect('list_impact_mappings', organization_id=organization_id)
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_deleted_impact_mappings',
        'organization': organization,
        'organization_id': organization_id,
        'org_id': organization_id,
        'module_path': module_path,
        'user': user,
        'tobjects': tobjects,
        'page_obj': page_obj,
        'objects_count': objects_count,
        'objects_per_page': objects_per_page,
        'show_all': show_all,
        'pagination_options': pagination_options,
        'selected_bulk_operations': selected_bulk_operations,
        'page_title': f'Impact_mapping List',
    }       
    template_file = f"{app_name}/{module_path}/list_deleted_impact_mappings.html"
    return render(request, template_file, context)



# Create View
@login_required
def create_impact_mapping(request, organization_id):
    user = request.user
    organization = Organization.objects.get(id=organization_id, active=True, 
                                                **first_viewable_dict)
    
    if request.method == 'POST':
        form = ImpactMappingForm(request.POST)
        if form.is_valid():
            form.instance.author = user
            form.instance.organization_id = organization_id
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list_impact_mappings', organization_id=organization_id)
    else:
        form = ImpactMappingForm()

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'create_impact_mapping',
        'organization': organization,
        'organization_id': organization_id,
        'org_id': organization_id,
        'module_path': module_path,
        'form': form,
        'page_title': f'Create Impact Mapping',
    }
    template_file = f"{app_name}/{module_path}/create_impact_mapping.html"
    return render(request, template_file, context)




# Edit
@login_required
def edit_impact_mapping(request, organization_id, impact_mapping_id):
    user = request.user
    organization = Organization.objects.get(id=organization_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(ImpactMapping, pk=impact_mapping_id, active=True,**viewable_dict)
    if request.method == 'POST':
        form = ImpactMappingForm(request.POST, instance=object)
        if form.is_valid():
            form.instance.author = user
            form.instance.organization_id = organization_id
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list_impact_mappings', organization_id=organization_id)
    else:
        form = ImpactMappingForm(instance=object)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'edit_impact_mapping',
        'organization': organization,
        'organization_id': organization_id,
        'org_id': organization_id,
        'module_path': module_path,
        'form': form,
        'object': object,
        'page_title': f'Edit Impact Mapping',
    }
    template_file = f"{app_name}/{module_path}/edit_impact_mapping.html"
    return render(request, template_file, context)



@login_required
def delete_impact_mapping(request, organization_id, impact_mapping_id):
    user = request.user
    organization = Organization.objects.get(id=organization_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(ImpactMapping, pk=impact_mapping_id, active=True,**viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.save()
        return redirect('list_impact_mappings', organization_id=organization_id)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'delete_impact_mapping',
        'organization': organization,
        'organization_id': organization_id,
        'org_id': organization_id,
        'module_path': module_path,        
        'object': object,
        'page_title': f'Delete Impact Mapping',
    }
    template_file = f"{app_name}/{module_path}/delete_impact_mapping.html"
    return render(request, template_file, context)


@login_required
def permanent_deletion_impact_mapping(request, organization_id, impact_mapping_id):
    user = request.user
    organization = Organization.objects.get(id=organization_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(ImpactMapping, pk=impact_mapping_id, active=False, deleted=False, **viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.deleted = True
        object.save()
        return redirect('list_impact_mappings', organization_id=organization_id)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'permanent_deletion_impact_mapping',
        'organization': organization,
        'organization_id': organization_id,
        'org_id': organization_id,
        'module_path': module_path,        
        'object': object,
        'page_title': f'Permanent Deletion Impact Mapping',
    }
    template_file = f"{app_name}/{module_path}/permanent_deletion_impact_mapping.html"
    return render(request, template_file, context)


@login_required
def restore_impact_mapping(request,  organization_id, impact_mapping_id):
    user = request.user
    object = get_object_or_404(ImpactMapping, pk=impact_mapping_id, active=False,**viewable_dict)
    object.active = True
    object.save()
    return redirect('list_impact_mappings', organization_id=organization_id)
   


@login_required
def view_impact_mapping(request, organization_id, impact_mapping_id):
    user = request.user
    organization = Organization.objects.get(id=organization_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(ImpactMapping, pk=impact_mapping_id, active=True,**viewable_dict)    

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'view_impact_mapping',
        'organization': organization,
        'organization_id': organization_id,
        'org_id': organization_id,
        'module_path': module_path,
        'object': object,
        'page_title': f'View Impact Mapping',
    }
    template_file = f"{app_name}/{module_path}/view_impact_mapping.html"
    return render(request, template_file, context)

@login_required
def editor_impact_mapping(request, organization_id, impact_mapping_id):
    user = request.user

    # Validate Organization
    organization = Organization.objects.get(id=organization_id, active=True, **first_viewable_dict)

    # Validate ImpactMapping
    impact_mapping = get_object_or_404(ImpactMapping, pk=impact_mapping_id, active=True, **viewable_dict)

    # Fetch root nodes (nodes with no parent)
    root_nodes = ImpactMap.objects.filter(parent__isnull=True, impact_map=impact_mapping).order_by('position')
 

    # Recursive function to map nodes
    def map_node(node):
        return {
            'id': node.id,
            'text': node.name,
            'data': {'node_type': node.node_type, 'link_text': node.link_text, 'description': node.description},
            'state': {'opened': True},  # Adjust as needed
            'icon': 'fas fa-project-diagram' if node.node_type == 'Root' else None,
            'type': node.node_type,  # Add the type field
            'position': node.position,
            'children': [map_node(child) for child in node.get_children()]
        }

    # Build tree data starting from root nodes
    tree_data = [map_node(node) for node in root_nodes]

    # Add default root node if no data exists
    tree_data_from_db = True
    if not tree_data:
        tree_data_from_db = False
        tree_data = [{
            'id': 'root',
            'text': impact_mapping.name,
            'data': {'node_type': 'Root'},
            'state': {'opened': True},
            'type': 'root',
            'position': 0,
            'children': []
        }]
        

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'editor_impact_mapping',
        'organization': organization,
        'organization_id': organization_id,
        'org_id': organization_id,
        'tree_data': json.dumps(tree_data),  # Convert tree data to JSON
        'tree_data_from_db': tree_data_from_db,
        'module_path': module_path,
        'object': impact_mapping,
        'page_title': f'Editor Impact Mapping',
    }

    template_file = f"{app_name}/{module_path}/editor_impact_mapping.html"
    return render(request, template_file, context)


@login_required
def ajax_save_impact_mappings(request):
    if request.method == 'POST':
        try:
            # Parse incoming data
            organization_id = request.POST.get('organization_id')
            impact_mapping_id = request.POST.get('impact_mapping_id')
            tree_data = json.loads(request.POST.get('impact_map', '[]'))

            # Validate ImpactMapping
            impact_mapping = get_object_or_404(ImpactMapping, pk=impact_mapping_id, organization_id=organization_id)

            # Clear existing ImpactMap nodes for this mapping
            with transaction.atomic():
                ImpactMap.objects.filter(impact_map=impact_mapping).delete()  # Use reverse relation for the filter

                # Recursive function to save nodes
                def save_node(node, parent=None):
                    node_type = node.get('data', {}).get('node_type')  # Safely get node_type
                    link_text = node.get('data', {}).get('link_text')
                    description = node.get('data', {}).get('description')
                    if not node_type:
                        raise ValueError(f"Node missing 'node_type': {node}")

                    # Create the ImpactMap node
                    impact_map_node = ImpactMap.objects.create(
                        name=node['text'],
                        node_type=node_type,
                        link_text=link_text,
                        description=description,
                        parent=parent
                    )

                    # Associate the root node with the ImpactMapping
                    if parent is None:  # Root node
                        impact_mapping.impact_map = impact_map_node
                        impact_mapping.save()

                    # Recursively save child nodes
                    for child in node.get('children', []):
                        save_node(child, parent=impact_map_node)

                # Save all root nodes
                for root_node in tree_data:
                    save_node(root_node)

            return JsonResponse({'status': 'success', 'message': 'Impact Mapping saved successfully!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


@login_required
def view_tree_table_mapping(request, organization_id, impact_mapping_id):
    user = request.user

    # Validate Organization
    organization = Organization.objects.get(id=organization_id, active=True, **first_viewable_dict)

    # Validate ImpactMapping
    impact_mapping = get_object_or_404(ImpactMapping, pk=impact_mapping_id, active=True, **viewable_dict)

    # Fetch root nodes (nodes with no parent)
    root_nodes = ImpactMap.objects.filter(parent__isnull=True, impact_map=impact_mapping).order_by('position')
 

    # Recursive function to map nodes
    def map_node(node):
        return {
            'id': node.id,            
            'text': node.name,
            'data': {'parent_db_id': impact_mapping.id, 'this_db_id': node.id, 'node_type': node.node_type, 'description': node.description},
            'state': {'opened': True},  # Adjust as needed
            'icon': 'fas fa-project-diagram' if node.node_type == 'Root' else None,
            'type': node.node_type,  # Add the type field
            'position': node.position,
            'children': [map_node(child) for child in node.get_children()]
        }

    # Build tree data starting from root nodes
    tree_data = [map_node(node) for node in root_nodes]

    # Add default root node if no data exists
    tree_data_from_db = True
    if not tree_data:
        tree_data_from_db = False
        tree_data = [{
            'id': 'root',
            'text': impact_mapping.name,
            'data': {'node_type': 'Root'},
            'state': {'opened': True},
            'type': 'root',
            'position': 0,
            'children': []
        }]
        

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'view_tree_table_mapping',
        'organization': organization,
        'organization_id': organization_id,
        'org_id': organization_id,
        'tree_data': json.dumps(tree_data),  # Convert tree data to JSON
        'tree_data_from_db': tree_data_from_db,
        'module_path': module_path,
        'object': impact_mapping,
        'page_title': f'Tree Table Impact Mapping',
    }

    template_file = f"{app_name}/{module_path}/view_tree_table_mapping.html"
    return render(request, template_file, context)
