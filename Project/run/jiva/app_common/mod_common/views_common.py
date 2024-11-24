# this basic import
from app_common.mod_app.all_view_imports import *

# # models
# from app_automate.models_app.models_automate import *
# from app_automate.models_app.models_backlogs import *
# from app_automate.models_app.models_orgs import *
# from app_automate.models_app.models_foundations import *
# # forms
# from app_automate.forms_app.forms_backlogs import *
# from app_automate.forms_app.forms_orgs import *

app_name = 'app_automate'
app_version = 'v1'  
@login_required
def ajax_update_model_list_sorted(request):
    if request.method == 'POST':
        ajax_data = request.POST['sorted_list_data']
        model_name = request.POST['model_name']
        given_app_name = app_name
        if 'app_name' in request.POST:            
            given_app_name = request.POST['app_name']
        new_data = ajax_data.replace("[",'')
        new_data = new_data.replace("]",'')
        sorted_list = new_data.split(",")
        seq = 1
        
        #model_class = globals()[model_name]
        model_class = apps.get_model(given_app_name, model_name)
        print(f">>> === AJAX UPDATE SORTED === <<<")
        for item in sorted_list:
            str = item.replace('"','')
            position = str.split('_')
            print(f">>> === AJAX UPDATE SORTED {position} === <<<")
            model_class.objects.filter(pk=position[0]).update(position=seq, author=request.user)
            seq = seq + 1
        context = {'page': 'Sorted Value', 
                   'active_tab': 'sorted_value',
                   'ajax_data': ajax_data}
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


# @login_required
# def ajax_save_element_text(request):
#     if request.method == 'POST':
#         text_data = request.POST.get('text')
#         object_id = request.POST.get('id')
#         model_name = request.POST.get('model_name')
#         field_name = request.POST.get('field_name')
#         got_app_name = request.POST.get('app_name', app_name)  # Default to a specific app if not provided

#         try:
#             model_class = apps.get_model(got_app_name, model_name)
#             # Update the specified object
#             fields_update = {field_name: text_data}
#             obj = model_class.objects.filter(id=object_id).update(**fields_update, author=request.user)
#             return JsonResponse({'status': 'success', 'updated_records': obj})
#         except LookupError:
#             return JsonResponse({'status': 'error', 'message': 'Model not found.'})
#         except model_class.DoesNotExist:
#             return JsonResponse({'status': 'error', 'message': 'Object not found.'})
#         except Exception as e:
#             return JsonResponse({'status': 'error', 'message': str(e)})

#     return JsonResponse({'status': 'error', 'message': 'Invalid request'})


@login_required
def ajax_save_element_text(request):
    if request.method == 'POST':
        text_data = request.POST.get('text')
        object_id = request.POST.get('id')
        model_name = request.POST.get('model_name')
        field_name = request.POST.get('field_name')
        got_app_name = request.POST.get('app_name', 'default_app_name')  # Default app if not provided

        try:
            # Get the model class
            model_class = apps.get_model(got_app_name, model_name)

            # Fetch the object to be updated
            obj = model_class.objects.get(id=object_id)

            # Handle DateTimeField specifically
            field_type = model_class._meta.get_field(field_name).get_internal_type()
            if field_type == 'DateTimeField':
                # Convert the input string to a timezone-aware datetime
                naive_date = datetime.strptime(text_data, '%Y-%m-%d')  # Adjust format if necessary
                aware_date = make_aware(naive_date, timezone=pytz.UTC)  # Use UTC or your preferred timezone
                setattr(obj, field_name, aware_date)
            else:
                # For other fields, simply set the value
                setattr(obj, field_name, text_data)

            # Set the author field if applicable
            obj.author = request.user

            # Save the updated object
            obj.save()

            return JsonResponse({'status': 'success', 'message': 'Field updated successfully'})
        except LookupError:
            return JsonResponse({'status': 'error', 'message': 'Model not found.'})
        except model_class.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Object not found.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


@login_required
def ajax_save_related_model(request):
    if request.method == 'POST':
        text_data = request.POST.get('text')  # New text data to be saved
        parent_object_id = request.POST.get('parent_id')  # ID of the parent object (e.g., Organization)
        parent_model_name = request.POST.get('parent_model')  # Model name of the parent object (e.g., Organization)
        parent_model_key = request.POST.get('parent_model_key')  # Field name to link the parent object (e.g., 'organization')
        child_model_name = request.POST.get('child_model')  # Model name of the child object (e.g., OrganizationDetail)
        field_name = request.POST.get('field_name')  # Field name to update
        app_name = request.POST.get('app_name')  # App name

        try:
            # Step 1: Get the parent model class dynamically
            parent_model_class = apps.get_model(app_name, parent_model_name)
            print(f"Parent model class found: {parent_model_class}")

            # Step 2: Fetch the parent object (e.g., Organization)
            parent_obj = parent_model_class.objects.get(id=parent_object_id)
            print(f"Parent object found: {parent_obj}")

            # Step 3: Get the child model class dynamically
            child_model_class = apps.get_model(app_name, child_model_name)
            print(f"Child model class found: {child_model_class}")

            # Step 4: Check if the child object exists for the given parent
            # Assuming there is a ForeignKey or OneToOneField from OrganizationDetail to Organization
            kwargs = {parent_model_key: parent_obj}
            child_obj, created = child_model_class.objects.get_or_create(**kwargs)  # Assuming 'organization' is the ForeignKey

            if created:
                print(f"New {child_model_name} object created for Parent ID {parent_object_id}")
            else:
                print(f"{child_model_name} object exists for Parent ID {parent_object_id}")

            # Step 5: Update the specific field in the child object
            if hasattr(child_obj, field_name):
                setattr(child_obj, field_name, text_data)
                child_obj.save()
                print(f"{field_name} updated for {child_model_name} object.")
                return JsonResponse({'status': 'success', 'created': created, 'updated_records': 1})
            else:
                return JsonResponse({'status': 'error', 'message': f"Field '{field_name}' not found in model '{child_model_name}'."})

        except parent_model_class.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': f'{parent_model_name} not found.'})
        except child_model_class.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': f'{child_model_name} not found.'})
        except LookupError:
            return JsonResponse({'status': 'error', 'message': 'Model not found.'})
        except IntegrityError as e:
            print(f"IntegrityError: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)})
        except Exception as e:
            print(f"Error: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})




@login_required
def ajax_update_task_done_state(request):
    if request.method == 'POST':
        user = request.user
        id = request.POST.get('id', None)
        done = request.POST.get('done', None)
        
        model_name = request.POST['model_name']
        given_app_name = app_name
        if 'app_name' in request.POST:            
            given_app_name = request.POST['app_name']
        
        model_class = apps.get_model(given_app_name, model_name)
        if id and done:
            object = model_class.objects.filter(id=id).first()
            if object:
                object.done = done.lower() == 'true'
                object.save()
                return JsonResponse({'success': True})      

    return JsonResponse({'success': False})