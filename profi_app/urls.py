from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.create),
    path('login', views.login),
    path('logout', views.logout),

    path('dashboard', views.dashboard),
    path('dashboard/show', views.proccess_category),
    path('dashboard/show/<str:category_name>', views.view_category),

    path('create_new_job', views.create_new_job),
    path('all_users', views.all_users),

    path('user/<int:user_id>/profile/', views.profile),
    
    path('add_job/<int:job_id>', views.add_job),
    path('done_job/<int:job_id>', views.done_job),
    path('giveup_job/<int:job_id>', views.giveup_job),
    path('view/<int:job_id>', views.view_job),
    path('edit_job/<int:job_id>', views.edit_job),
    path('remove_job/<int:job_id>', views.remove_job),
    path('remove_category/<int:category_id>/<int:job_id>', views.remove_category),


    path('add_comment/<int:job_id>', views.add_comment)
]
