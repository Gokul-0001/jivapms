from app_common.mod_app.all_view_imports import *
from app_organization.mod_app.all_view_imports import *
from app_organization.mod_org_image_map.models_org_image_map import *
from app_organization.mod_org_image_map.forms_org_image_map import *

from app_organization.mod_organization.models_organization import *

from app_common.mod_common.models_common import *
from app_jivapms.mod_app.all_view_imports import *

app_name = 'app_organization'
app_version = 'v1'

module_name = 'org_image_maps'
module_path = f'mod_org_image_map'

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
def list_org_image_maps(request, organization_id):
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
        tobjects = OrgImageMap.objects.filter(name__icontains=search_query, 
                                            organization_id=organization_id, **viewable_dict).order_by('position')
    else:
        tobjects = OrgImageMap.objects.filter(active=True, organization_id=organization_id).order_by('position')
        deleted = OrgImageMap.objects.filter(active=False, deleted=False,
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
                    object = get_object_or_404(OrgImageMap, pk=item, active=True, **viewable_dict)
                    object.active = False
                    object.save()
                    
                elif bulk_operation == 'bulk_done':
                    object = get_object_or_404(OrgImageMap, pk=item, active=True, **viewable_dict)
                    object.done = True
                    object.save()
                    
                elif bulk_operation == 'bulk_not_done':
                    object = get_object_or_404(OrgImageMap, pk=item, active=True, **viewable_dict)
                    object.done = False
                    object.save()
                    
                elif bulk_operation == 'bulk_blocked':  # Correct the operation check here
                    object = get_object_or_404(OrgImageMap, pk=item, active=True, **viewable_dict)
                    object.blocked = True
                    object.save()
                    
                else:
                    redirect('list_org_image_maps', organization_id=organization_id)
            return redirect('list_org_image_maps', organization_id=organization_id)
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_org_image_maps',
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
        'page_title': f'Org_image_map List',
    }       
    template_file = f"{app_name}/{module_path}/list_org_image_maps.html"
    return render(request, template_file, context)





# ============================================================= #
@login_required
def list_deleted_org_image_maps(request, organization_id):
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
        tobjects = OrgImageMap.objects.filter(name__icontains=search_query, 
                                            active=False, deleted=False,
                                            organization_id=organization_id, **viewable_dict).order_by('position')
    else:
        tobjects = OrgImageMap.objects.filter(active=False, deleted=False, organization_id=organization_id,
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
                        object = get_object_or_404(OrgImageMap, pk=item, active=False, **viewable_dict)
                        object.active = True
                        object.save()         
                    elif bulk_operation == 'bulk_erase':
                        object = get_object_or_404(OrgImageMap, pk=item, active=False, **viewable_dict)
                        object.active = False  
                        object.deleted = True             
                        object.save()    
                    else:
                        redirect('list_org_image_maps', organization_id=organization_id)
                redirect('list_org_image_maps', organization_id=organization_id)
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_deleted_org_image_maps',
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
        'page_title': f'Org_image_map List',
    }       
    template_file = f"{app_name}/{module_path}/list_deleted_org_image_maps.html"
    return render(request, template_file, context)



# Create View
@login_required
def create_org_image_map(request, organization_id):
    user = request.user
    organization = Organization.objects.get(id=organization_id, active=True, 
                                                **first_viewable_dict)
    
    if request.method == 'POST':
        form = OrgImageMapForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.author = user
            form.instance.organization_id = organization_id
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list_org_image_maps', organization_id=organization_id)
    else:
        form = OrgImageMapForm()

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'create_org_image_map',
        'organization': organization,
        'organization_id': organization_id,
        'org_id': organization_id,
        
        
        'module_path': module_path,
        'form': form,
        'page_title': f'Create Org Image Map',
    }
    template_file = f"{app_name}/{module_path}/create_org_image_map.html"
    return render(request, template_file, context)




# Edit
@login_required
def edit_org_image_map(request, organization_id, org_image_map_id):
    user = request.user
    organization = Organization.objects.get(id=organization_id, active=True, 
                                                **first_viewable_dict)
    
    org_image_map = get_object_or_404(OrgImageMap, pk=org_image_map_id, active=True,**viewable_dict)
    if request.method == 'POST':
        form = OrgImageMapForm(request.POST, request.FILES, instance=org_image_map)
        if form.is_valid():
            form.instance.author = user
            form.instance.organization_id = organization_id
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list_org_image_maps', organization_id=organization_id)
    else:
        form = OrgImageMapForm(instance=org_image_map)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'edit_org_image_map',
        'organization': organization,
        'organization_id': organization_id,
        'org_id': organization_id,
        'org_image_map_id': org_image_map_id,
        'org_image_map': org_image_map,
        'object': org_image_map,
        
        'module_path': module_path,
        'form': form,
        'page_title': f'Edit Org Image Map',
    }
    template_file = f"{app_name}/{module_path}/edit_org_image_map.html"
    return render(request, template_file, context)



@login_required
def delete_org_image_map(request, organization_id, org_image_map_id):
    user = request.user
    organization = Organization.objects.get(id=organization_id, active=True, 
                                                **first_viewable_dict)
    
    org_image_map = get_object_or_404(OrgImageMap, pk=org_image_map_id, active=True,**viewable_dict)
    object = org_image_map
    if request.method == 'POST':
        object.active = False
        object.save()
        return redirect('list_org_image_maps', organization_id=organization_id)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'delete_org_image_map',
        'organization': organization,
        'organization_id': organization_id,
        'org_id': organization_id,
        'org_image_map_id': org_image_map_id,
        'org_image_map': org_image_map,
        'object': org_image_map,
        
        'module_path': module_path,        
        'page_title': f'Delete Org Image Map',
    }
    template_file = f"{app_name}/{module_path}/delete_org_image_map.html"
    return render(request, template_file, context)


@login_required
def permanent_deletion_org_image_map(request, organization_id, org_image_map_id):
    user = request.user
    organization = Organization.objects.get(id=organization_id, active=True, 
                                                **first_viewable_dict)
    
    org_image_map = get_object_or_404(OrgImageMap, pk=org_image_map_id, active=False, deleted=False, **viewable_dict)
    object = org_image_map
    if request.method == 'POST':
        object.active = False
        object.deleted = True
        object.save()
        return redirect('list_org_image_maps', organization_id=organization_id)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'permanent_deletion_org_image_map',
        'organization': organization,
        'organization_id': organization_id,
        'org_id': organization_id,
        'org_image_map_id': org_image_map_id,
        'org_image_map': org_image_map,
        'object': org_image_map,
        
        'module_path': module_path,        
        'page_title': f'Permanent Deletion Org Image Map',
    }
    template_file = f"{app_name}/{module_path}/permanent_deletion_org_image_map.html"
    return render(request, template_file, context)


@login_required
def restore_org_image_map(request,  organization_id, org_image_map_id):
    user = request.user
    object = get_object_or_404(OrgImageMap, pk=org_image_map_id, active=False,**viewable_dict)
    object.active = True
    object.save()
    return redirect('list_org_image_maps', organization_id=organization_id)
   



@login_required
def view_org_image_map(request, organization_id, org_image_map_id):
    user = request.user
    organization = get_object_or_404(Organization, id=organization_id, active=True)
    org_image_map = get_object_or_404(OrgImageMap, pk=org_image_map_id, active=True, organization_id=organization_id)
    object = org_image_map

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'view_image_map',
        'organization': organization,
        'organization_id': organization_id,
        'org_id': organization_id,
        'org_image_map_id': org_image_map_id,
        'org_image_map': org_image_map,
        'object': org_image_map,
        
        'module_path': module_path,
        'page_title': f'View Org Image Map',
    }
    template_file = f"{app_name}/{module_path}/view_org_image_map.html"
    return render(request, template_file, context)


# helper files
# image map code


@login_required
def generate_visual_image_map_code(request, organization_id, org_image_map_id):
    user = request.user
    organization = get_object_or_404(Organization, id=organization_id, active=True)
    org_image_map = get_object_or_404(OrgImageMap, pk=org_image_map_id, active=True, organization_id=organization_id)

    # Fetch areas and prepare HTML generation
    areas = [
        {
            'shape': area.shape,
            'coords': area.coords,
            'link': area.link,
            'description': area.hover_text,
        }
        for area in org_image_map.areas.filter(active=True)
    ]

    # Generate HTML with scaling logic
    html_code = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{org_image_map.name}</title>
        <style>
            #image-map-container {{
                position: relative;
                display: inline-block;
                width: 100%;
                max-width: 100%; /* Ensure it scales within the parent container */
            }}
            #image-map {{
                width: 100%;
                display: block;
            }}
            #shapes-container {{
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                pointer-events: auto; /* Allow interactions for child elements */
            }}
            .shape {{
                position: absolute;
                pointer-events: auto;
                display: block; /* Make <a> tags behave as block elements */
                text-decoration: none; /* Remove underline for links */
                border: 1px solid transparent; /* Default border for shapes */
                transition: background-color 0.3s, border 0.3s;
            }}
            .shape:hover {{
                background-color: rgba(0, 255, 0, 0.4);
                border: 1px solid red;
            }}
        </style>
    </head>
    <body>
        <div id="image-map-container">
            <img id="image-map" src="{org_image_map.image.url}" alt="{org_image_map.name}">
            <div id="shapes-container"></div>
        </div>
        <script>
            document.addEventListener("DOMContentLoaded", function () {{
                const originalWidth = {org_image_map.original_width};
                const originalHeight = {org_image_map.original_height};
                const areas = {areas};
                const shapesContainer = document.getElementById('shapes-container');
                const imageMap = document.getElementById('image-map');

                // Function to scale and render shapes
                function renderShapes() {{
                    // Clear existing shapes
                    shapesContainer.innerHTML = "";

                    const renderedWidth = imageMap.offsetWidth;
                    const renderedHeight = (originalHeight / originalWidth) * renderedWidth;

                    const scaleX = renderedWidth / originalWidth;
                    const scaleY = renderedHeight / originalHeight;

                    areas.forEach((area) => {{
                        const coords = area.coords.split(',').map(Number);
                        let element = null;

                        if (area.shape === 'rect') {{
                            const [x, y, width, height] = coords.map((value, index) =>
                                index % 2 === 0 ? value * scaleX : value * scaleY
                            );

                            // Create a clickable link wrapped around the shape
                            element = document.createElement('a');
                            element.href = area.link;
                            element.target = '_blank';
                            element.classList.add('shape');
                            element.style.left = `${{x}}px`;
                            element.style.top = `${{y}}px`;
                            element.style.width = `${{width}}px`;
                            element.style.height = `${{height}}px`;
                        }} else if (area.shape === 'circle') {{
                            const [x, y, radius] = coords.map((value, index) =>
                                index === 2 ? value * scaleX : value * (index === 0 ? scaleX : scaleY)
                            );

                            // Create a clickable link wrapped around the shape
                            element = document.createElement('a');
                            element.href = area.link;
                            element.target = '_blank';
                            element.classList.add('shape');
                            element.style.left = `${{x - radius}}px`;
                            element.style.top = `${{y - radius}}px`;
                            element.style.width = `${{2 * radius}}px`;
                            element.style.height = `${{2 * radius}}px`;
                            element.style.borderRadius = '50%';
                        }}

                        if (element) {{
                            // Append the shape to the container
                            shapesContainer.appendChild(element);
                        }}
                    }});
                }}

                // Initial render
                renderShapes();

                // Re-render shapes on window resize
                window.addEventListener('resize', () => {{
                    renderShapes();
                }});
            }});
        </script>
    </body>
    </html>
    """

    # Pass the generated HTML code to the template
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'view_image_map',
        'page_title': f'Image Map Code',
        'html_code': html_code,
        'organization': organization,
        'organization_id': organization_id,
        'org_id': organization_id,
        'org_image_map_id': org_image_map_id,
        'org_image_map': org_image_map,
        'object': org_image_map,
        
        'org_id': organization_id,
        'org': organization,
    }

    template_file = f"{app_name}/{module_path}/image_map_code.html"
    return render(request, template_file, context)



@login_required
def image_map_editor(request, organization_id, org_image_map_id):
    user = request.user
    organization = get_object_or_404(Organization, id=organization_id, active=True)
    org_image_map = get_object_or_404(OrgImageMap, pk=org_image_map_id, active=True, organization_id=organization_id)

    if request.method == 'POST':
        # Parse submitted areas data
        areas_data = json.loads(request.POST.get('areas', '[]'))
        print(f"Submitted Areas Data: {areas_data}")  # Debugging
        # Validate areas_data to remove any empty entries
        valid_areas = [
            area for area in areas_data
            if area.get('shape') and area.get('coords') and area.get('link')
        ]
        # set the image_map orginal width and height
        org_image_map.original_height = int(request.POST.get('original_height', 0))
        org_image_map.original_width = int(request.POST.get('original_width', 0))

        print(f">>> === image_map.original_width: {org_image_map.original_width} === <<<")
        print(f">>> === image_map.original_height: {org_image_map.original_height} === <<<")
        org_image_map.save()
        # Clear existing areas and add new ones
        ImageMapArea.objects.filter(image_map=org_image_map).delete()
        for area in areas_data:
            try:
                ImageMapArea.objects.filter(image_map=org_image_map).delete()
                for area in valid_areas:
                    ImageMapArea.objects.create(
                        image_map=org_image_map,
                        shape=area['shape'],
                        coords=area['coords'],
                        link=area.get('link', ''),
                        hover_text=area.get('description', ''),
                    )
            except KeyError as e:
                print(f"Missing key {e} in area data: {area}")
                return JsonResponse({'error': f"Missing key: {e}"}, status=400)

        return redirect('list_org_image_maps', organization_id=organization_id)

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
        for area in org_image_map.areas.filter(active=True)  # Filter active areas
    ]

    context = {
        'org_image_map': org_image_map,
        'areas': json.dumps(areas), 
        'organization': organization,
        'organization_id': organization_id,
        'org_id': organization_id,
        'org_image_map_id': org_image_map_id,
        'org_image_map': org_image_map,
        'object': org_image_map,
        
        'module_path': module_path,
        'parent_page': '___PARENTPAGE___',
        'page': 'image_map_editor',
        'page_title': f'Image Map Editor',
    }
    template_file = f"{app_name}/{module_path}/image_map_editor.html"
    return render(request, template_file, context)


@login_required
def view_visual_image_map(request, organization_id, org_image_map_id):
    user = request.user
    organization = get_object_or_404(Organization, id=organization_id, active=True)
    org_image_map = get_object_or_404(OrgImageMap, pk=org_image_map_id, active=True, organization_id=organization_id)
    areas = [
        {
            'shape': area.shape,
            'coords': area.coords,
            'link': area.link,
            'description': area.hover_text,
        }
        for area in org_image_map.areas.filter(active=True)
    ]
  
    context = {
        'image_map': org_image_map,
        'areas': json.dumps(areas), 
        'organization': organization,
        'organization_id': organization_id,
        'org_id': organization_id,
        'org_image_map_id': org_image_map_id,
        'org_image_map': org_image_map,
        'object': org_image_map,
        
        'module_path': module_path,
        'parent_page': '___PARENTPAGE___',
        'page': 'image_map_editor',
        'page_title': f'Image Map Editor',
       
        
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

