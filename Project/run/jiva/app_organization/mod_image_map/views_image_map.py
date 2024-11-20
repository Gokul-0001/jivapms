from app_common.mod_app.all_view_imports import *
from app_organization.mod_app.all_view_imports import *
from app_organization.mod_image_map.models_image_map import *
from app_organization.mod_image_map.forms_image_map import *

from app_organization.mod_project.models_project import *

from app_common.mod_common.models_common import *
from app_jivapms.mod_app.all_view_imports import *

app_name = 'app_organization'
app_version = 'v1'

module_name = 'image_maps'
module_path = f'mod_image_map'

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
def list_image_maps(request, pro_id):
    # take inputs
    # process inputs
    user = request.user       
    objects_count = 0    
    show_all = request.GET.get('all', '25')
    objects_per_page = int(show_all) if show_all != 'all' else 25
    pagination_options = [5, 10, 15, 25, 50, 100, 'all']
    selected_bulk_operations = None
    deleted_count = 0
    project = Project.objects.get(id=pro_id, active=True, 
                                                **first_viewable_dict)
    
    search_query = request.GET.get('search', '')
    if search_query:
        tobjects = ImageMap.objects.filter(name__icontains=search_query, 
                                            pro_id=pro_id, **viewable_dict).order_by('position')
    else:
        tobjects = ImageMap.objects.filter(active=True, pro_id=pro_id, author=user).order_by('position')
        deleted = ImageMap.objects.filter(active=False, deleted=False,
                                pro_id=pro_id,
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
                    object = get_object_or_404(ImageMap, pk=item, active=True, **viewable_dict)
                    object.active = False
                    object.save()
                    
                elif bulk_operation == 'bulk_done':
                    object = get_object_or_404(ImageMap, pk=item, active=True, **viewable_dict)
                    object.done = True
                    object.save()
                    
                elif bulk_operation == 'bulk_not_done':
                    object = get_object_or_404(ImageMap, pk=item, active=True, **viewable_dict)
                    object.done = False
                    object.save()
                    
                elif bulk_operation == 'bulk_blocked':  # Correct the operation check here
                    object = get_object_or_404(ImageMap, pk=item, active=True, **viewable_dict)
                    object.blocked = True
                    object.save()
                    
                else:
                    redirect('list_image_maps', pro_id=pro_id)
            return redirect('list_image_maps', pro_id=pro_id)
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_image_maps',
        'project': project,
        'pro_id': pro_id,
        
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
        'page_title': f'Image_map List',
    }       
    template_file = f"{app_name}/{module_path}/list_image_maps.html"
    return render(request, template_file, context)





# ============================================================= #
@login_required
def list_deleted_image_maps(request, pro_id):
    # take inputs
    # process inputs
    user = request.user       
    objects_count = 0    
    show_all = request.GET.get('all', '25')
    objects_per_page = int(show_all) if show_all != 'all' else 25
    pagination_options = [5, 10, 15, 25, 50, 100, 'all']
    selected_bulk_operations = None
    project = Project.objects.get(id=pro_id, active=True, 
                                                **first_viewable_dict)
    
    search_query = request.GET.get('search', '')
    if search_query:
        tobjects = ImageMap.objects.filter(name__icontains=search_query, 
                                            active=False,
                                            pro_id=pro_id, **viewable_dict).order_by('position')
    else:
        tobjects = ImageMap.objects.filter(active=False, pro_id=pro_id,
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
                        object = get_object_or_404(ImageMap, pk=item, active=False, **viewable_dict)
                        object.active = True
                        object.save()         
                    elif bulk_operation == 'bulk_erase':
                        object = get_object_or_404(ImageMap, pk=item, active=False, **viewable_dict)
                        object.active = False  
                        object.deleted = True             
                        object.save()    
                    else:
                        redirect('list_image_maps', pro_id=pro_id)
                redirect('list_image_maps', pro_id=pro_id)
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_deleted_image_maps',
        'project': project,
        'pro_id': pro_id,
        
        'module_path': module_path,
        'user': user,
        'tobjects': tobjects,
        'page_obj': page_obj,
        'objects_count': objects_count,
        'objects_per_page': objects_per_page,
        'show_all': show_all,
        'pagination_options': pagination_options,
        'selected_bulk_operations': selected_bulk_operations,
        'page_title': f'Image_map List',
    }       
    template_file = f"{app_name}/{module_path}/list_deleted_image_maps.html"
    return render(request, template_file, context)



# Create View
@login_required
def create_image_map(request, pro_id):
    user = request.user
    project = Project.objects.get(id=pro_id, active=True, 
                                                **first_viewable_dict)
    
    if request.method == 'POST':
        form = ImageMapForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.author = user
            form.instance.pro_id = pro_id
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list_image_maps', pro_id=pro_id)
    else:
        form = ImageMapForm()

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'create_image_map',
        'project': project,
        'pro_id': pro_id,
        
        'module_path': module_path,
        'form': form,
        'page_title': f'Create Image Map',
    }
    template_file = f"{app_name}/{module_path}/create_image_map.html"
    return render(request, template_file, context)




# Edit
@login_required
def edit_image_map(request, pro_id, image_map_id):
    user = request.user
    project = Project.objects.get(id=pro_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(ImageMap, pk=image_map_id, active=True,**viewable_dict)
    if request.method == 'POST':
        form = ImageMapForm(request.POST, request.FILES, instance=object)
        if form.is_valid():
            form.instance.author = user
            form.instance.pro_id = pro_id
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list_image_maps', pro_id=pro_id)
    else:
        form = ImageMapForm(instance=object)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'edit_image_map',
        'project': project,
        'pro_id': pro_id,
        'org_id': project.org.id,
        'org': project.org,
        
        'module_path': module_path,
        'form': form,
        'object': object,
        'page_title': f'Edit Image Map',
    }
    template_file = f"{app_name}/{module_path}/edit_image_map.html"
    return render(request, template_file, context)

@login_required
def image_map_editor(request, pro_id, image_map_id):
    user = request.user
    project = get_object_or_404(Project, id=pro_id, active=True)
    image_map = get_object_or_404(ImageMap, pk=image_map_id, active=True, pro_id=pro_id)

    if request.method == 'POST':
        # Parse submitted areas data
        areas_data = json.loads(request.POST.get('areas', '[]'))
        print(f"Submitted Areas Data: {areas_data}")  # Debugging
        # Validate areas_data to remove any empty entries
        valid_areas = [
            area for area in areas_data
            if area.get('shape') and area.get('coords') and area.get('link')
        ]
        # Clear existing areas and add new ones
        ImageMapArea.objects.filter(image_map=image_map).delete()
        for area in areas_data:
            try:
                ImageMapArea.objects.filter(image_map=image_map).delete()
                for area in valid_areas:
                    ImageMapArea.objects.create(
                        image_map=image_map,
                        shape=area['shape'],
                        coords=area['coords'],
                        link=area.get('link', ''),
                        hover_text=area.get('description', ''),
                    )
            except KeyError as e:
                print(f"Missing key {e} in area data: {area}")
                return JsonResponse({'error': f"Missing key: {e}"}, status=400)

        return redirect('list_image_maps', pro_id=pro_id)

    # Retrieve existing areas for the image map
    # Retrieve existing areas
    areas = [
        {
            'id': area.id,  # Include ID here
            'shape': area.shape,
            'coords': area.coords,
            'link': area.link,
            'description': area.hover_text,
        }
        for area in image_map.areas.filter(active=True)  # Filter active areas
    ]

    context = {
        'image_map': image_map,
        'areas': json.dumps(areas), 
        'project': project,
        'object': project,
        'pro_id': pro_id,
        'org_id': project.org.id,
        'org': project.org,
        'module_path': module_path,
        'parent_page': '___PARENTPAGE___',
        'page': 'image_map_editor',
        'page_title': f'Image Map Editor',
    }
    template_file = f"{app_name}/{module_path}/image_map_editor.html"
    return render(request, template_file, context)


@login_required
def view_visual_image_map(request, pro_id, image_map_id):
    user = request.user
    project = get_object_or_404(Project, id=pro_id, active=True)

    image_map = get_object_or_404(ImageMap, pk=image_map_id, active=True, pro_id=pro_id)
    areas = [
        {
            'shape': area.shape,
            'coords': area.coords,
            'link': area.link,
            'description': area.hover_text,
        }
        for area in image_map.areas.filter(active=True)
    ]
  
    context = {
        'image_map': image_map,
        'areas': json.dumps(areas), 
        'project': project,
        'object': project,
        'pro_id': pro_id,
        'org_id': project.org.id,
        'org': project.org,
        'module_path': module_path,
        'parent_page': '___PARENTPAGE___',
        'page': 'image_map_editor',
        'page_title': f'Image Map Editor',
        
        'image_map': image_map,
        
    }
    template_file = f"{app_name}/{module_path}/view_visual_image_map.html"
    return render(request, template_file, context)


@login_required
@require_http_methods(["PUT"])  # Allow only PUT requests
def update_area(request, area_id):
    try:
        # Parse the incoming JSON data
        data = json.loads(request.body)
        link = data.get('link', '').strip()
        description = data.get('description', '').strip()

        # Validate the data
        if not link:
            return HttpResponseBadRequest(json.dumps({'error': 'Link is required.'}), content_type='application/json')

        # Find the area to update
        area = ImageMapArea.objects.get(id=area_id)

        # Update the area
        area.link = link
        area.hover_text = description
        area.save()

        # Return success response
        return JsonResponse({'success': True, 'message': 'Area updated successfully.'})
    except ImageMapArea.DoesNotExist:
        return HttpResponseBadRequest(json.dumps({'error': 'Area not found.'}), content_type='application/json')
    except json.JSONDecodeError:
        return HttpResponseBadRequest(json.dumps({'error': 'Invalid JSON data.'}), content_type='application/json')
    except Exception as e:
        return HttpResponseBadRequest(json.dumps({'error': str(e)}), content_type='application/json')

@login_required
def delete_area(request, area_id):
    print(f">>> === area_id: {area_id} === <<<")
    
    try:
        # Fetch the area object
        area = ImageMapArea.objects.get(id=area_id)

        # Update the active flag to False
        area.active = False
        area.save()

        logger.debug(f">>> === AREA: {area} ==> {area.active} === <<<")    

        # Return success response
        return JsonResponse({'success': True, 'message': 'Area deleted successfully.'})
    except ImageMapArea.DoesNotExist:
        return HttpResponseBadRequest(json.dumps({'error': 'Area not found.'}), content_type='application/json')
    except Exception as e:
        return HttpResponseBadRequest(json.dumps({'error': str(e)}), content_type='application/json')

@login_required
def delete_image_map(request, pro_id, image_map_id):
    user = request.user
    project = Project.objects.get(id=pro_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(ImageMap, pk=image_map_id, active=True,**viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.save()
        return redirect('list_image_maps', pro_id=pro_id)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'delete_image_map',
        'project': project,
        'pro_id': pro_id,
        
        'module_path': module_path,        
        'object': object,
        'page_title': f'Delete Image Map',
    }
    template_file = f"{app_name}/{module_path}/delete_image_map.html"
    return render(request, template_file, context)


@login_required
def permanent_deletion_image_map(request, pro_id, image_map_id):
    user = request.user
    project = Project.objects.get(id=pro_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(ImageMap, pk=image_map_id, active=False, deleted=False, **viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.deleted = True
        object.save()
        return redirect('list_image_maps', pro_id=pro_id)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'permanent_deletion_image_map',
        'project': project,
        'pro_id': pro_id,
        
        'module_path': module_path,        
        'object': object,
        'page_title': f'Permanent Deletion Image Map',
    }
    template_file = f"{app_name}/{module_path}/permanent_deletion_image_map.html"
    return render(request, template_file, context)


@login_required
def restore_image_map(request,  pro_id, image_map_id):
    user = request.user
    object = get_object_or_404(ImageMap, pk=image_map_id, active=False,**viewable_dict)
    object.active = True
    object.save()
    return redirect('list_image_maps', pro_id=pro_id)
   


@login_required
def view_image_map(request, pro_id, image_map_id):
    user = request.user
    project = Project.objects.get(id=pro_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(ImageMap, pk=image_map_id, active=True,**viewable_dict)    

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'view_image_map',
        'project': project,
        'pro_id': pro_id,
        
        'module_path': module_path,
        'object': object,
        'page_title': f'View Image Map',
    }
    template_file = f"{app_name}/{module_path}/view_image_map.html"
    return render(request, template_file, context)


