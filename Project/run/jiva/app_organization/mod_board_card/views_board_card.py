
from app_organization.mod_app.all_view_imports import *
from app_organization.mod_board_card.models_board_card import *
from app_organization.mod_board_card.forms_board_card import *

from app_organization.mod_project_board.models_project_board import *

from app_common.mod_common.models_common import *

app_name = 'app_organization'
app_version = 'v1'

module_name = 'board_cards'
module_path = f'mod_board_card'

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
def list_board_cards(request, project_board_id):
    # take inputs
    # process inputs
    user = request.user       
    objects_count = 0    
    show_all = request.GET.get('all', '25')
    objects_per_page = int(show_all) if show_all != 'all' else 25
    pagination_options = [5, 10, 15, 25, 50, 100, 'all']
    selected_bulk_operations = None
    deleted_count = 0
    project_board = ProjectBoard.objects.get(id=project_board_id, active=True, 
                                                **first_viewable_dict)
    
    search_query = request.GET.get('search', '')
    if search_query:
        tobjects = BoardCard.objects.filter(name__icontains=search_query, 
                                            project_board_id=project_board_id, **viewable_dict).order_by('position')
    else:
        tobjects = BoardCard.objects.filter(active=True, project_board_id=project_board_id).order_by('position')
        deleted = BoardCard.objects.filter(active=False, deleted=False,
                                project_board_id=project_board_id,
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
                    object = get_object_or_404(BoardCard, pk=item, active=True, **viewable_dict)
                    object.active = False
                    object.save()
                    
                elif bulk_operation == 'bulk_done':
                    object = get_object_or_404(BoardCard, pk=item, active=True, **viewable_dict)
                    object.done = True
                    object.save()
                    
                elif bulk_operation == 'bulk_not_done':
                    object = get_object_or_404(BoardCard, pk=item, active=True, **viewable_dict)
                    object.done = False
                    object.save()
                    
                elif bulk_operation == 'bulk_blocked':  # Correct the operation check here
                    object = get_object_or_404(BoardCard, pk=item, active=True, **viewable_dict)
                    object.blocked = True
                    object.save()
                    
                else:
                    redirect('list_board_cards', project_board_id=project_board_id)
            return redirect('list_board_cards', project_board_id=project_board_id)
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_board_cards',
        'project_board': project_board,
        'project_board_id': project_board_id,
        'org_id': project_board.project.org.id,
        'project': project_board.project,
        'project_id': project_board.project.id,
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
        'page_title': f'Board_card List',
    }       
    template_file = f"{app_name}/{module_path}/list_board_cards.html"
    return render(request, template_file, context)





# ============================================================= #
@login_required
def list_deleted_board_cards(request, project_board_id):
    # take inputs
    # process inputs
    user = request.user       
    objects_count = 0    
    show_all = request.GET.get('all', '25')
    objects_per_page = int(show_all) if show_all != 'all' else 25
    pagination_options = [5, 10, 15, 25, 50, 100, 'all']
    selected_bulk_operations = None
    project_board = ProjectBoard.objects.get(id=project_board_id, active=True, 
                                                **first_viewable_dict)
    
    search_query = request.GET.get('search', '')
    if search_query:
        tobjects = BoardCard.objects.filter(name__icontains=search_query, 
                                            active=False, deleted=False,
                                            project_board_id=project_board_id, **viewable_dict).order_by('position')
    else:
        tobjects = BoardCard.objects.filter(active=False, deleted=False, project_board_id=project_board_id,
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
                        object = get_object_or_404(BoardCard, pk=item, active=False, **viewable_dict)
                        object.active = True
                        object.save()         
                    elif bulk_operation == 'bulk_erase':
                        object = get_object_or_404(BoardCard, pk=item, active=False, **viewable_dict)
                        object.active = False  
                        object.deleted = True             
                        object.save()    
                    else:
                        redirect('list_board_cards', project_board_id=project_board_id)
                redirect('list_board_cards', project_board_id=project_board_id)
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_deleted_board_cards',
        'project_board': project_board,
        'project_board_id': project_board_id,
        'org_id': project_board.project.org.id,
        'project': project_board.project,
        'project_id': project_board.project.id,
        'module_path': module_path,
        'user': user,
        'tobjects': tobjects,
        'page_obj': page_obj,
        'objects_count': objects_count,
        'objects_per_page': objects_per_page,
        'show_all': show_all,
        'pagination_options': pagination_options,
        'selected_bulk_operations': selected_bulk_operations,
        'page_title': f'Board_card List',
    }       
    template_file = f"{app_name}/{module_path}/list_deleted_board_cards.html"
    return render(request, template_file, context)



# Create View
@login_required
def create_board_card(request, project_board_id):
    user = request.user
    project_board = ProjectBoard.objects.get(id=project_board_id, active=True, 
                                                **first_viewable_dict)
    
    if request.method == 'POST':
        form = BoardCardForm(request.POST)
        if form.is_valid():
            form.instance.author = user
            form.instance.project_board_id = project_board_id
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list_board_cards', project_board_id=project_board_id)
    else:
        form = BoardCardForm()

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'create_board_card',
        'project_board': project_board,
        'project_board_id': project_board_id,
        'org_id': project_board.project.org.id,
        'project': project_board.project,
        'project_id': project_board.project.id,
        'module_path': module_path,
        'form': form,
        'page_title': f'Create Board Card',
    }
    template_file = f"{app_name}/{module_path}/create_board_card.html"
    return render(request, template_file, context)




# Edit
@login_required
def edit_board_card(request, project_board_id, board_card_id):
    user = request.user
    project_board = ProjectBoard.objects.get(id=project_board_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(BoardCard, pk=board_card_id, active=True,**viewable_dict)
    if request.method == 'POST':
        form = BoardCardForm(request.POST, instance=object)
        if form.is_valid():
            form.instance.author = user
            form.instance.project_board_id = project_board_id
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list_board_cards', project_board_id=project_board_id)
    else:
        form = BoardCardForm(instance=object)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'edit_board_card',
        'project_board': project_board,
        'project_board_id': project_board_id,
        'org_id': project_board.project.org.id,
        'project': project_board.project,
        'project_id': project_board.project.id,
        'module_path': module_path,
        'form': form,
        'object': object,
        'page_title': f'Edit Board Card',
    }
    template_file = f"{app_name}/{module_path}/edit_board_card.html"
    return render(request, template_file, context)



@login_required
def delete_board_card(request, project_board_id, board_card_id):
    user = request.user
    project_board = ProjectBoard.objects.get(id=project_board_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(BoardCard, pk=board_card_id, active=True,**viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.save()
        return redirect('list_board_cards', project_board_id=project_board_id)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'delete_board_card',
        'project_board': project_board,
        'project_board_id': project_board_id,
        'org_id': project_board.project.org.id,
        'project': project_board.project,
        'project_id': project_board.project.id,
        'module_path': module_path,        
        'object': object,
        'page_title': f'Delete Board Card',
    }
    template_file = f"{app_name}/{module_path}/delete_board_card.html"
    return render(request, template_file, context)


@login_required
def permanent_deletion_board_card(request, project_board_id, board_card_id):
    user = request.user
    project_board = ProjectBoard.objects.get(id=project_board_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(BoardCard, pk=board_card_id, active=False, deleted=False, **viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.deleted = True
        object.save()
        return redirect('list_board_cards', project_board_id=project_board_id)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'permanent_deletion_board_card',
        'project_board': project_board,
        'project_board_id': project_board_id,
        'org_id': project_board.project.org.id,
        'project': project_board.project,
        'project_id': project_board.project.id,
        'module_path': module_path,        
        'object': object,
        'page_title': f'Permanent Deletion Board Card',
    }
    template_file = f"{app_name}/{module_path}/permanent_deletion_board_card.html"
    return render(request, template_file, context)


@login_required
def restore_board_card(request,  project_board_id, board_card_id):
    user = request.user
    object = get_object_or_404(BoardCard, pk=board_card_id, active=False,**viewable_dict)
    object.active = True
    object.save()
    return redirect('list_board_cards', project_board_id=project_board_id)
   


@login_required
def view_board_card(request, project_board_id, board_card_id):
    user = request.user
    project_board = ProjectBoard.objects.get(id=project_board_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(BoardCard, pk=board_card_id, active=True,**viewable_dict)    

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'view_board_card',
        'project_board': project_board,
        'project_board_id': project_board_id,
        'org_id': project_board.project.org.id,
        'project': project_board.project,
        'project_id': project_board.project.id,
        'module_path': module_path,
        'object': object,
        'page_title': f'View Board Card',
    }
    template_file = f"{app_name}/{module_path}/view_board_card.html"
    return render(request, template_file, context)


@login_required
def board_card_settings(request, project_board_id):
    # take inputs
    # process inputs
    user = request.user       
    objects_count = 0    
    project_board = ProjectBoard.objects.get(id=project_board_id, active=True, 
                                                **first_viewable_dict)
    project = project_board.project
    org = project.org

    # create the board card settings if it does not exist
    board_card_settings, created = BoardCard.objects.get_or_create(
        project_board=project_board,
        defaults={  # Set default values only when creating a new record
            "display_card_id": True,
            "display_card_size": True,
            "display_card_priority": True,
            "display_card_project": True,
            "display_card_iteration": True,
            "display_card_assignee": False,
            "display_card_release": False,
            "display_card_status": False,
            "display_card_type": False,
            "display_card_aging": False,
            "display_card_due_date": False,
            "display_card_summary": False,
            "author": user,  # Set the user who first accesses the settings
        }
    )
    # Extract only BooleanField names
    skip_fields = {'active', 'deleted', 'blocked', 'done', 'approved'}

    boolean_fields = [
        field.name for field in BoardCard._meta.fields
        if isinstance(field, models.BooleanField) and field.name not in skip_fields
    ]


    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'board_card_settings',
        'project_board': project_board,
        'project_board_id': project_board_id,
        'org_id': project_board.project.org.id,
        'project': project_board.project,
        'project_id': project_board.project.id,
        'module_path': module_path,
        'user': user,
        'board_card_settings': board_card_settings,
        'boolean_fields': boolean_fields,
        'page_title': f'Card Settings',
    }       
    template_file = f"{app_name}/{module_path}/board_card_settings.html"
    return render(request, template_file, context)

