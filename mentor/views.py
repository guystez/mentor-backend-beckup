from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import openai
from django.contrib.auth.models import User
from mentor.models import Business, Checklist, Custom_checklist, Massage, Question, ReadReceipt, Tasks
from django.core.files.base import ContentFile
import base64
import uuid
from django.core.files.storage import default_storage
from django.http import JsonResponse

from datetime import datetime

import psycopg
from datetime import datetime, timedelta


@api_view(['GET'])
def get_access_of_specific_business(request):
    if request.method == "GET":
        username1 = request.GET.get('name')
        print(username1,'11111111')
        user = User.objects.filter(username=username1).first()
        print(user,"2222222")
        business_code= user.email
        print(business_code,'codeeeeeeeeeee')
        businesses = Business.objects.filter(business_code=business_code )
        print(businesses,'sssssss')
        all_businesses = []
        for item in businesses:
            

            business_dict = {
               
                'business_name':item.business_name,
                'business_code':item.business_code,
                'access':item.access,
                'id':item.id
            }
            print(item.access,'gggggggggg')
            all_businesses.append(business_dict)

        return JsonResponse({"all_businesses": all_businesses}, safe=False)

    return Response({"error": "Invalid request method"}, status=405)  # 405 Method Not Allowed




@api_view(['GET','POST'])
def get_post_access(request):
    if request.method == "POST":
        data = request.data  
        businessId = request.data.get('businessId')
        action = request.data.get('action')
        print(action,'actionnnn')
        print(businessId,'idddddd')
       
        business = Business.objects.filter(id=businessId)
        if action == 'give':
            business.update(access=True)
        if action == 'cancel':
             business.update(access=False)


        return JsonResponse({"business updated":"business updated"}, safe=False)

    if request.method == "GET":
        # username1 = request.GET.get('name')
        # user = User.objects.all()
        # business_codes= user.email
        businesses = Business.objects.all(
           

        )
        all_businesses = []
        for item in businesses:
            

            business_dict = {
               
                'business_name':item.business_name,
                'business_code':item.business_code,
                'access':item.access,
                'id':item.id
            }
            all_businesses.append(business_dict)

        return JsonResponse({"all_businesses": all_businesses}, safe=False)

    return Response({"error": "Invalid request method"}, status=405)  # 405 Method Not Allowed






@api_view(['GET'])
def get_areas(request):
    if request.method == "GET":
        data = request.data  
        username1 = request.GET.get('name')
        user = User.objects.filter(username=username1).first()

        if not user:
            return JsonResponse({"error": "User not found"}, status=404)

        business_code_of_user = user.email
        checklist_areas = Custom_checklist.objects.filter(business_code=business_code_of_user)
        
        # Use a set to store unique area values
        unique_areas = set()
        for area in checklist_areas:
            unique_areas.add(area.area)

        # Convert the set back to a list
        all_areas = list(unique_areas)

        return JsonResponse({"all_areas": all_areas}, safe=False)




@api_view(['GET','POST'])
def get_post_employee_tasks_for_employee(request):
    if request.method == "POST":
        data = request.data  
        username1 = request.data.get('name')
        task_id = request.data.get('task_id')
        user = User.objects.filter(username=username1).first()

        if not user:
            return JsonResponse({"error": "User not found"}, status=404)

        business_code_of_user = user.email
        new_task = Tasks.objects.filter(id=task_id)
        new_task.update(completed=True)

        return JsonResponse({"task created":"Task created"}, safe=False)

    if request.method == "GET":
        username1 = request.GET.get('name')
        user = User.objects.filter(username=username1).first()
        business_code_of_user = user.email
        business_tasks = Tasks.objects.filter(
            business_code=business_code_of_user,
            employee_id=user.id,
            completed=False

        )
        tasks_list = []
        for item in business_tasks:
            employee = User.objects.filter(id=item.employee_id).first()
            if employee:
                username_of_employee = employee.username  # Extract the username of the employee
            else:
                username_of_employee = None

            checklist_dict = {
                'text': item.text,
                'employee_username': username_of_employee,  
                'id':item.id,
                'completed':item.completed,
                'image':item.image.url if item.image else None,
            }
            tasks_list.append(checklist_dict)

        return JsonResponse({"tasks_list": tasks_list}, safe=False)

    return Response({"error": "Invalid request method"}, status=405)  # 405 Method Not Allowed





@api_view(['GET','POST'])
def get_post_employee_tasks(request):
    if request.method == "POST":
        data = request.data  
        username1 = request.data.get('name')
        Task_text = request.data.get('Task_text')
        employee_id = request.data.get('employee_id')
        image_data = data.get('image', None)  # Get image data or None if not present

        user = User.objects.filter(username=username1).first()

        if not user:
            return JsonResponse({"error": "User not found"}, status=404)

        business_code_of_user = user.email

        # Only decode the base64 image if image_data exists
        image_decoded = None
        if image_data:
            format, imgstr = image_data.split(';base64,')
            if format:  # Check if format exists
                ext = format.split('/')[-1]
                image_decoded = ContentFile(base64.b64decode(imgstr), name=str(uuid.uuid4())[:10] + '.' + ext)

        new_task = Tasks.objects.create(
            business_code=business_code_of_user,
            employee_id=employee_id,
            text=Task_text,
            image=image_decoded,  # Will be None if no image data was provided
            completed=False
        )
        new_task.save()

        return JsonResponse({"task created": "Task created"}, safe=False)


    if request.method == "GET":
        username1 = request.GET.get('name')
        user = User.objects.filter(username=username1).first()
        business_code_of_user = user.email
        business_tasks = Tasks.objects.filter(
            business_code=business_code_of_user,

        )
        tasks_list = []
        for item in business_tasks:
            employee = User.objects.filter(id=item.employee_id).first()
            if employee:
                username_of_employee = employee.username  # Extract the username of the employee
            else:
                username_of_employee = None

            checklist_dict = {
                'text': item.text,
                'employee_username': username_of_employee,  
                'id':item.id,
                'completed':item.completed,
                'image':item.image.url if item.image else None,
               
            }
            tasks_list.append(checklist_dict)
            print(checklist_dict)
        return JsonResponse({"tasks_list": tasks_list}, safe=False)

    return Response({"error": "Invalid request method"}, status=405)  # 405 Method Not Allowed





@api_view(['DELETE'])
def edit_employees_delete(request,pk):
    if request.method == "DELETE":
            print(pk,'sssssssssssssssssssssss')
            username1 = request.GET.get('name')
            requesting_user = User.objects.filter(username=username1).first()
            if not requesting_user:
                return JsonResponse({"error": "Requesting user not found"}, status=404)
            try:
                employee = User.objects.get(id=pk)
                employee.delete()
                return JsonResponse({"success": "Employee deleted successfully"})
            except User.DoesNotExist:
                return JsonResponse({"error": "Employee not found"}, status=404)
            

@api_view(['GET'])
def edit_employees_get(request):
    if request.method == "GET":
        username1 = request.GET.get('name')
        user = User.objects.filter(username=username1).first()
        business_code_of_user = user.email
        employees_of_business = User.objects.filter(
            email=business_code_of_user,
            # is_staff=False
        )
        employee_list = []
        for employee in employees_of_business:
            checklist_dict = {
                'employee_username': employee.username,
                'employee_id': employee.id
            }
            employee_list.append(checklist_dict)

        return JsonResponse({"employee_list": employee_list}, safe=False)

    return Response({"error": "Invalid request method"}, status=405)  # 405 Method Not Allowed


@api_view(['GET','POST'])
def business_data(request):
    if request.method == "POST":
        data = request.data  
        username1 = request.data.get('name')
        data_update = request.data.get('data_update')
        user = User.objects.filter(username=username1).first()

        if not user:
            return JsonResponse({"error": "User not found"}, status=404)

        business_code_of_user = user.email
        Business.objects.filter(business_code=business_code_of_user).update(data=data_update)

        return JsonResponse({"success": "Data updated successfully"})

    if request.method == "GET":
        username1 = request.GET.get('name')
        user = User.objects.filter(username=username1).first()
        business_code_of_user = user.email
        business = Business.objects.filter(
            business_code=business_code_of_user
        )
        business_list = []
        for item in business:
            checklist_dict = {
                'data': item.data,
                "business_code":item.business_code
            }
            business_list.append(checklist_dict)

        return JsonResponse({"business": business_list}, safe=False)

    return Response({"error": "Invalid request method"}, status=405)  # 405 Method Not Allowed




@api_view(['DELETE'])
def delete_tasks(request, pk):
    if request.method == "DELETE":
        username1 = request.GET.get('name')
        user = User.objects.filter(username=username1).first()
        business_code_of_user = user.email

        # Retrieve the task to delete
        task_to_delete = Tasks.objects.filter(id=pk, business_code=business_code_of_user).first()

        # If the task has an associated image, delete it
        if task_to_delete and task_to_delete.image:
            # Assuming `image` is a Django ImageField or FileField
            # This will use Django's default storage to delete the image
            default_storage.delete(task_to_delete.image.path)

        # Now delete the task from the database
        task_to_delete.delete()

        return Response({"message": "deleted-success"})

    return Response({"error": "Invalid request method"}, status=405)



@api_view(['DELETE'])
def delete_massage(request, pk):
    if request.method == "DELETE":
        username1 = request.GET.get('name')
        user = User.objects.filter(username=username1).first()
        business_code_of_user = user.email

        # Retrieve the massage to delete
        massage_to_delete = Massage.objects.filter(id=pk, business_code=business_code_of_user).first()

        # If the massage has an associated image, delete it
        if massage_to_delete and massage_to_delete.image:
            # Assuming `image` is a Django ImageField or FileField
            # This will use Django's default storage to delete the image
            default_storage.delete(massage_to_delete.image.path)

        # Now delete the massage from the database
        massage_to_delete.delete()

        return Response({"message": "deleted-success"})
        
    return Response({"error": "Invalid request method"}, status=405)  # 405 Method Not Allowed


@api_view(['POST'])
def mark_read(request):
    if request.method == "POST":
        data = request.data  
        username1 = request.data.get('name')
        user = User.objects.filter(username=username1).first()
        business_code_of_user = user.email
        massageId = data.get('massageId')
        
        # Fetch the massage object
        massage = Massage.objects.filter(business_code=business_code_of_user, id=massageId).first()
        
        # Check if the massage exists
        if massage:
            massage.mark_read += 1
            massage.save()

            # Create a new read receipt
            ReadReceipt.objects.create(massage=massage, user=user,business_code=business_code_of_user)

            return Response({"success": "massage updated"})
        else:
            return Response({"error": "massage not found"}, status=404)








# @api_view(['GET'])
# def get_massages_of_employee(request):
    
#     if request.method == "GET":
#         username1 = request.GET.get('name')
#         user = User.objects.filter(username=username1).first()

#         if not user:
#             return JsonResponse({"error": "User not found"}, status=404)

#         business_code_of_user = user.email
#         employee_massages = Massage.objects.filter(manager=True,business_code=business_code_of_user)

#         massages = []
#         for massage in employee_massages:
#             # Get the employee's name using the employee_id from the Massage model
#             employee = User.objects.filter(id=int(massage.employee_id)).first()
#             employee_name = employee.username if employee else "Unknown"
#             read_receipts = ReadReceipt.objects.filter(business_code=business_code_of_user, massage=massage)

#             read_users = [receipt.user.username for receipt in read_receipts]
#             print(read_users,'readdddddddddddddddddd')

#             massages_dict = {
#                 'massage': massage.text,
#                 'employee_name': employee_name,
#                 'id': massage.id,
#                 'manager':massage.manager,
#                 'mark_read':massage.mark_read,
#                 'read_by_users': read_users,
#                 'image':massage.image.url if massage.image else None,

#             }
#             massages.append(massages_dict)

#         return JsonResponse({"massages": massages}, safe=False)

#     return Response({"error": "Invalid request method"}, status=405)  # 405 Method Not Allowed

@api_view(['POST','GET'])
def massages(request):
    if request.method == "POST":
        data = request.data
        username1 = request.data.get('name')
        user = User.objects.filter(username=username1).first()
        business_code_of_user = user.email
        text = data.get('text')
        manager = data.get('manager')
        mark_read = data.get('mark_read')
        
        image_data = data.get('image', None)  # Get image data or None if not present

        if image_data:  # Check if image_data exists
            format, imgstr = image_data.split(';base64,')
            if format:  # Check if format exists
                ext = format.split('/')[-1]
                image_decoded = ContentFile(base64.b64decode(imgstr), name=str(uuid.uuid4())[:10] + '.' + ext)
            else:
                image_decoded = None
        else:
            image_decoded = None

        # Use the image_decoded value, which will be None if no image data was provided
        create_massage = Massage.objects.create(
            business_code=business_code_of_user,
            employee_id=user.id,
            completed=False,
            text=text,
            manager=manager,
            mark_read=mark_read,
            image=image_decoded
        )
        create_massage.save()     
        return Response({"success": "Tasks updated"})

    if request.method == "GET":
        username1 = request.GET.get('name')
        user = User.objects.filter(username=username1).first()

        if not user:
            return JsonResponse({"error": "User not found"}, status=404)

        business_code_of_user = user.email
        employee_massages = Massage.objects.filter(business_code=business_code_of_user)

        massages = []
        for massage in employee_massages:
            # Check if the current user is the sender of the message, and if the current user is not a manager
            if massage.employee_id == user.id and not user.is_staff:
                continue  # Skip this message as the user is the sender and is not a manager

            # Get the employee's name using the employee_id from the Massage model
            employee = User.objects.filter(id=int(massage.employee_id)).first()
            employee_name = employee.username if employee else "Unknown"
            read_receipts = ReadReceipt.objects.filter(business_code=business_code_of_user, massage=massage)

            read_users = [receipt.user.username for receipt in read_receipts]

            massages_dict = {
                'massage': massage.text,
                'employee_name': employee_name,
                'id': massage.id,
                'manager': massage.manager,
                'mark_read': massage.mark_read,
                'read_by_users': read_users,
                'image': massage.image.url if massage.image else None,
            }
            massages.append(massages_dict)

        return JsonResponse({"massages": massages}, safe=False)


    return Response({"error": "Invalid request method"}, status=405)  # 405 Method Not Allowed



@api_view(['GET'])
def completed_check_list_yesterday(request):
    if request.method == "GET":
        username1 = request.GET.get('name')
        date = request.GET.get('date')
        user = User.objects.filter(username=username1).first()
        business_code_of_user = user.email
        date=date  
        if len(date) == 0:
            return JsonResponse({"error": "User not found"}, status=404)

        # Fetch all areas from the Custom_checklist model
        custom_checklist_areas = Custom_checklist.objects.filter(
            business_code=business_code_of_user
        ).values_list('area', flat=True).distinct()

        # Fetch all areas from the Checklist model for yesterday's date
        completed_areas_for_date = Checklist.objects.filter(
            business_code=business_code_of_user,
            created_at__date=date
        ).values_list('area', flat=True).distinct()

        checklists_list = []
        for area in custom_checklist_areas:
            checklist_dict = {
                'area': area,
                'not_completed_yesterday': area not in completed_areas_for_date
            }
            checklists_list.append(checklist_dict)

        return JsonResponse({"checklists": checklists_list}, safe=False)

    return Response({"error": "Invalid request method"}, status=405)  # 405 Method Not Allowed






@api_view(['GET'])
def completed_check_list(request):
    if request.method == "GET":
        username1 = request.GET.get('name')
        user = User.objects.filter(username=username1).first()
        business_code_of_user = user.email
        today = datetime.now().date()

        # Fetch all areas from the Custom_checklist model
        custom_checklist_areas = Custom_checklist.objects.filter(
            business_code=business_code_of_user
        ).values_list('area', flat=True).distinct()

        # Fetch all areas from the Checklist model for today's date
        completed_areas_today = Checklist.objects.filter(
            business_code=business_code_of_user,
            created_at__date=today
        ).values_list('area', flat=True).distinct()

        checklists_list = []
        for area in custom_checklist_areas:
            checklist_dict = {
                'area': area,
                'not_completed_today': area not in completed_areas_today
            }
            checklists_list.append(checklist_dict)

        return JsonResponse({"checklists": checklists_list}, safe=False)

    return Response({"error": "Invalid request method"}, status=405)  # 405 Method Not Allowed








@api_view(['GET'])
def get_uncomplete_task_auto(request):
    if request.method == "GET":
        username1 = request.GET.get('name')
        area = request.GET.get('area')
        today = datetime.now().date()
      
        user = User.objects.filter(username=username1).first()
        business_code_of_user = user.email
        
        # Fetch relevant checklists
        relevant_checklists = Checklist.objects.filter(
            business_code=business_code_of_user,
            created_at__date=today,
            completed=False
        )
        
        # Fetch related Custom_checklist items
        custom_checklist_ids = [checklist.task_id for checklist in relevant_checklists]
        custom_checklists = Custom_checklist.objects.filter(id__in=custom_checklist_ids)
        custom_checklist_dict = {item.id: item for item in custom_checklists}
        
        checklists_list = []
        for checklist in relevant_checklists:
            custom_checklist = custom_checklist_dict.get(checklist.task_id)
            if custom_checklist:
                checklistitem_text = custom_checklist.text

                # Fetch the employee name for the current checklist
                employee = User.objects.filter(id=checklist.employee_id).first()
                employee_name = employee.username if employee else "Unknown"
                print(employee_name, 'aaaaaaaaa')
                
                checklist_dict = {
                    'id': checklist.id,
                    'business_code': checklist.business_code,
                    'text': checklistitem_text,  # Use the fetched text here
                    'area': checklist.area,
                    'finish_time': checklist.finish_time,
                    'completed': checklist.completed,
                    'employee_name': employee_name
                }
                checklists_list.append(checklist_dict)
        
        return JsonResponse({"checklists": checklists_list}, safe=False)

    return Response({"error": "Invalid request method"}, status=405)







@api_view(['GET'])
def get_uncomplete_task(request):
    if request.method == "GET":
        username1 = request.GET.get('name')
        area = request.GET.get('area')
        date = request.GET.get('date')
        try:
            date = datetime.strptime(date, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            return JsonResponse({"error": "Invalid date format"}, status=400)
      
        user = User.objects.filter(username=username1).first()
        business_code_of_user = user.email
        
        # Fetch relevant checklists
        relevant_checklists = Checklist.objects.filter(
            business_code=business_code_of_user,
            area=area,
            created_at__date=date,
            completed=False
        )
        
        # Fetch related Custom_checklist items
        custom_checklist_ids = [checklist.task_id for checklist in relevant_checklists]
        custom_checklists = Custom_checklist.objects.filter(id__in=custom_checklist_ids)
        custom_checklist_dict = {item.id: item for item in custom_checklists}
        
        checklists_list = []
        for checklist in relevant_checklists:
            custom_checklist = custom_checklist_dict.get(checklist.task_id)
            if custom_checklist:
                checklistitem_text = custom_checklist.text

                # Fetch the employee name for the current checklist
                employee = User.objects.filter(id=checklist.employee_id).first()
                employee_name = employee.username if employee else "Unknown"
                print(employee_name, 'aaaaaaaaa')
                
                checklist_dict = {
                    'id': checklist.id,
                    'business_code': checklist.business_code,
                    'text': checklistitem_text,  # Use the fetched text here
                    'area': checklist.area,
                    'finish_time': checklist.finish_time,
                    'completed': checklist.completed,
                    'employee_name': employee_name
                }
                checklists_list.append(checklist_dict)
        
        return JsonResponse({"checklists": checklists_list}, safe=False)

    return Response({"error": "Invalid request method"}, status=405)




@api_view(['DELETE'])
def delete_checklist_item(request,pk):
    if request.method == "DELETE":
        print(pk,'pkkkkk')
        data = request.data  
        username1 = request.GET.get('name')
        user = User.objects.filter(username=username1).first()
        business_code_of_user = user.email
        print(business_code_of_user,'qqqqqqqqq')
        deletedprod = Custom_checklist.objects.filter(id=pk, business_code=business_code_of_user)
        deletedprod.delete()
        return Response({"deleted-success"})
        
    return Response({"error": "Invalid request method"}, status=405)  # 405 Method Not Allowed





@api_view(['POST','GET'])
def update_check_list(request):
    if request.method == "POST":
        data = request.data  
        username1 = request.data.get('name')
        area = request.data.get('area')
        print(area,'area in updated checklist')
        user = User.objects.filter(username=username1).first()
        business_code_of_user = user.email
     
        text = data.get('text')
        completedTasks = data.get('completedTasks')
      
        
        for task_id, is_completed in completedTasks.items():
            print(f"Task ID: {task_id}")
            if is_completed:
                print("True")
                compleated_checklist = Checklist.objects.create(business_code=business_code_of_user, task_id=task_id,completed=True,employee_id=user.id,area=area)
                compleated_checklist.save()
            else:
                print("False")
                compleated_checklist = Checklist.objects.create(business_code=business_code_of_user, task_id=task_id,completed=False,employee_id=user.id,area=area)
                compleated_checklist.save()
        return Response({"success": "Tasks updated"})
        
    return Response({"error": "Invalid request method"}, status=405)  # 405 Method Not Allowed


from rest_framework import status

@api_view(['POST', 'GET'])
def new_day_checklist(request):
    if request.method == "POST":
        data = request.data  
        username = data.get('name')  # Changed 'name' to 'username' to match the client-side code

        # Check if user exists
        user = User.objects.filter(username=username).first()
        if not user:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        business_code_of_user = user.email

        # Fetch relevant checklists
        relevant_checklists = Custom_checklist.objects.filter(business_code=business_code_of_user)
        if not relevant_checklists.exists():
            return Response({"error": "No relevant checklists found"}, status=status.HTTP_404_NOT_FOUND)

        # Create new checklists
        for checklist in relevant_checklists:
            new_checklist = Checklist.objects.create(
                business_code=business_code_of_user,
                text=checklist.text,
                area=checklist.area,
                finish_time=checklist.finish_time,
                completed=False,
                created_at=datetime.now()
            )
            new_checklist.save()

        return Response({"message": "new-day-checklist-created"}, status=status.HTTP_201_CREATED)

    # Handle GET or other methods if needed





@api_view(['POST','GET'])
def check_list(request):
    if request.method == "POST":
        data = request.data  
        username1 = request.data.get('name')
        user = User.objects.filter(username=username1).first()
        business_code_of_user = user.email
        text = data.get('text')
        area = data.get('area')
        print(area,'aaaaaaaaa')
        finish_time = data.get('finish_time')
        creation=Custom_checklist.objects.create(business_code=business_code_of_user,text=text,area=area,finish_time=finish_time,completed = False)
        creation.save()
        return Response("new checklist sucessfully created")
    if request.method == "GET":
        username1 = request.GET.get('name')
        area = request.GET.get('area')
        user = User.objects.filter(username=username1).first()
        business_code_of_user = user.email
        today = datetime.now().date()
        relevant_checklists = Custom_checklist.objects.filter(
            business_code=business_code_of_user,
            area=area,
             # filter by today's date
        )
        
        checklists_list = []
        for checklist in relevant_checklists:
            checklist_dict = {
                'id': checklist.id,
                'business_code': checklist.business_code,
                'text': checklist.text,
                'area': checklist.area,
                'finish_time': checklist.finish_time,
                'completed': checklist.completed
            }
            checklists_list.append(checklist_dict)
        
        return JsonResponse({"checklists": checklists_list}, safe=False)


    return Response({"error": "Invalid request method"}, status=405)  # 405 Method Not Allowed



@api_view(['POST'])
def most_asked_question(request):
    if request.method == "POST":
        selected_date = request.data.get('selected_date')
        name = request.data.get('name')
        user = User.objects.filter(username=name).first()  
        business_code_of_user = user.email
        print(business_code_of_user,'gggggggggg')
        selected_date = datetime.strptime(selected_date, '%Y-%m-%d')  # Convert the string to a datetime object
        print(selected_date,'dateeeeeeee')
        # Fetch all questions related to the selected date
        all_questions = Question.objects.filter(
            created_at__month=selected_date.month,
            created_at__year=selected_date.year,
            business_code=business_code_of_user
        )

        # Prepare the data
        questions_text = [question.question_text for question in all_questions]
        print(questions_text,'frfrfrfrfrfrfrfrfrfrrfrfrfrfrf')

        # Prepare the message for GPT-3.5 Turbo
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": f"what is the info that users search most from the following data(use no more than 20 words to respond):{questions_text}"
            }
        ]

        # Send the message to GPT-3.5 Turbo
        openai.api_key = "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"
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages
        )

        # Extract the generated text
        generated_text = response.choices[0].message['content']

        return Response({"most_asked": generated_text})

    return Response({"error": "Invalid request method"}, status=405)  # 405 Method Not Allowed










@api_view(['GET'])
def employee_questiones(request):
    if request.method == "GET":
        username1 = request.GET.get('name')
        user = User.objects.filter(username=username1).first()
        if not user:
            return Response({"error": "User not found"}, status=404)

        business_code_of_user = user.email

        # Fetch all questions related to the business code
        all_questions = Question.objects.filter(business_code=business_code_of_user)

        # Prepare the data
        data2 = []
        for question in all_questions:
            employee_id = question.employee_id
            employee = User.objects.filter(id=employee_id).first()
            if employee:
                employee_name = employee.username
                timestamp = question.created_at  # Get the timestamp from the Question model
                data2.append({
                    'employee_name': employee_name,
                    'question_text': question.question_text,
                    'timestamp': timestamp  # Add the timestamp to the data
                })

        return JsonResponse(data2, safe=False)

    return Response({"error": "Invalid request method"}, status=405)  # 405 Method Not Allowed





@api_view(['POST','GET'])
def create_business(request):
    if request.method == "POST":
        data = request.data  
        business_name = data.get('business_name')
        business_code = data.get('business_code')
        business_type = data.get('business_type')
        business_data = data.get('business_data')
        creation=Business.objects.create(business_name=business_name,business_code=business_code,business_type=business_type,data=business_data,access=False)
        creation.save()
        return Response("new business sucessfully created")
    if request.method == "GET":
        username1 = request.GET.get('name')
        user = User.objects.filter(username=username1).first()
        is_superuser=user.is_superuser
        print(is_superuser,'superrrr222')
        is_staff = user.is_staff
        if is_staff == True:
            print('is_staff=true')
        else:
            print('is_staff=flase')
        business_code_of_user = user.email
        business = Business.objects.filter(business_code= business_code_of_user).first()
        business_name = business.business_name
        data2={
            "business_name": business_name,
            "is_staff": is_staff,
            "is_superuser":is_superuser

        }

        return Response(data2)

    return Response({"error": "Invalid request method"}, status=405)  # 405 Method Not Allowed
        
# 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

@api_view(['POST'])
def api_gpt(request):
    username=request.data.get('username')
    # business_code =request.data.get("business_code")
    # print(business_code,'wwwwwwwwwwwww')
    # print(username,'username')
    user = User.objects.filter(username=username).first()
    business_code_of_user = user.email
    print(business_code_of_user,'usercodeeeeeeeee')
    business = Business.objects.filter(business_code= business_code_of_user).first()
    business_data = business.data
    print(user,'user')
    print(business_data,"business_data")
    userid=user.id
    print(userid,'userid')
    

    openai.api_key = "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"
    
    if request.method == "POST":
        data = request.data  # In DRF, request.data contains parsed content
        query = data.get('query')
        employee_question = Question.objects.create(employee_id=userid,question_text=query,business_code=business_code_of_user)
        employee_question.save()
        rules = 'Extract from the data the relevant information according to the provided input. Rules: if the input is in different language than the data, try to translate the input to the data language . Return the answer in the same language of the provided input always . No more than 30 words. input:'
        
        
        if query:
            print(query)
            messages = [{"role": "assistant", "content": rules+query+'data:'+business_data
                   
    }]

        response = openai.ChatCompletion.create(
          model="gpt-4",
          messages=messages
        )

        generated_text = response.choices[0].message['content']
        data1 = {"answer": generated_text}
        print("data:", data1)
        
        return Response(data1)
    return Response({"error": "Invalid request method"}, status=405)  # 405 Method Not Allowed
