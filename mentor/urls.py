from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static 


app_name = 'mentor'

urlpatterns = [

path('search/', views.api_gpt, name='api_gpt'),
path('business_insert_db/', views.create_business, name='create_business'),
path('get_all_questiones/', views.employee_questiones, name='employee_questiones'),
path('most_asked_question/', views.most_asked_question, name='most_asked_question'),
path('create_check_list/', views.check_list, name='check_list'),
path('get_areas/', views.get_areas, name='get_areas'),
path('update_checklist/', views.update_check_list, name='update_check_list'),
path('new_day_checklist/', views.new_day_checklist, name='new_day_checklist'),
path('get_uncomplete_task/', views.get_uncomplete_task, name='get_uncomplete_task'),
path('get_uncomplete_task_auto/', views.get_uncomplete_task_auto, name='get_uncomplete_task_auto'),
path('check_completed/', views.completed_check_list, name='completed_check_list'),
path('check_completed_yesterday/', views.completed_check_list_yesterday, name='completed_check_list_yesterday'),
path('post_massages/', views.massages, name='massages'),
path('get_massages/', views.massages, name='massages'),
# path('get_massages_of_employee/', views.get_massages_of_employee, name='get_massages_of_employee'),
path('get_employee_tasks/', views.get_post_employee_tasks, name='get_post_employee_tasks'),
path('post_employee_tasks/', views.get_post_employee_tasks, name='get_post_employee_tasks'),
path('get_employee_tasks_for_employee/', views.get_post_employee_tasks_for_employee, name='get_post_employee_tasks_for_employee'),
path('mark_read/', views.mark_read, name='mark_read'),
path('post_employee_tasks_for_employee/', views.get_post_employee_tasks_for_employee, name='get_post_employee_tasks_for_employee'),
path('get_business_data/', views.business_data, name='get_business_data'),
path('update_business_data/', views.business_data, name='business_data'),
path('get_all_business_access/', views.get_post_access, name='get_access'),
path('get_access_of_specific_business/', views.get_access_of_specific_business, name='get_access_of_specific_business'),
path('post_all_business_access/', views.get_post_access, name='post_access'),
path('edit_employees_get/', views.edit_employees_get, name='edit_employees'),
path("edit_employees_delete/<pk>/", views.edit_employees_delete, name= "delete_employees"),
path("delete_checklist_item/<pk>/", views.delete_checklist_item, name= "delete_checklist_item"),
path("delete_massage/<pk>/", views.delete_massage, name= "delete_massage"),
path("delete_tasks/<pk>/", views.delete_tasks, name= "delete_tasks"),



]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


