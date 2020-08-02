from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt
from datetime import datetime
from django.core.paginator import Paginator

from django.forms.models import model_to_dict # Need for sortation

def index(request):
    return render(request, "home.html")

# DASHBOARD PAGE
def dashboard(request):
    if 'user_id' not in request.session:
        jobs = Job.objects.filter(executor=None).order_by('-created_at')
        paginator = Paginator(jobs, 4)
        page = request.GET.get('page')
        jobs = paginator.get_page(page)
        context = {
            'users' : User.objects.all(),
            'all_categories': Category.objects.all(),
            'jobs': jobs
        }
        return render(request, 'dashboard.html', context)
    else:
        jobs = Job.objects.filter(executor=None).order_by('-created_at')
        paginator = Paginator(jobs, 4)
        page = request.GET.get('page')
        jobs = paginator.get_page(page)
        context = {
            'cur_user':  User.objects.get(id = request.session['user_id']),
            'users' : User.objects.all(),
            'all_categories': Category.objects.all().order_by('name'),
            'jobs': jobs
        }
        return render(request, 'dashboard.html', context)

def proccess_category(request):
    if request.POST['category'] == 'all':
        return redirect("/dashboard")
    else:
        needed_category = Category.objects.get(name = request.POST['category'])
        return redirect(f"/dashboard/show/{needed_category.name}")

def view_category(request, category_name):
    needed_category = Category.objects.get(name = category_name)
    category_jobs = needed_category.job.all()
    paginator = Paginator(category_jobs, 4)
    page = request.GET.get('page')
    category_jobs = paginator.get_page(page)
    context = {
        'cur_user':  User.objects.get(id = request.session['user_id']),
        'users' : User.objects.all(),
        'all_categories': Category.objects.exclude(name = needed_category.name),
        'jobs': category_jobs,
        'active_category': needed_category
    }
    return render(request, 'category.html', context)








# REGISTRATION
def create(request):
    if request.method == "GET":
        return render(request, "register.html")
    else:
        request.session.clear()
        request.session['first_name'] = request.POST['first_name']
        request.session['last_name'] = request.POST['last_name']
        request.session['birth_date'] = request.POST['birth_date']
        request.session['email'] = request.POST['email']
        errors = User.objects.validator(request.POST)	
        if len(errors)>0:													
            for value in errors.values():											
                messages.error(request, value)											
            return redirect('/register')
        new_user = User.objects.register(request.POST)
        request.session.clear()
        request.session['user_id'] = new_user.id
        first_i = new_user.first_name[0]
        last_i = new_user.last_name[0]
        initials = first_i + last_i
        request.session['initials'] = initials
        return redirect('/')

# LOGIN
def login(request):
    if request.method == "GET":
        if 'first_name' in request.session:
            request.session.clear()
            return render(request, "login.html")
        else:
            return render(request, "login.html")
    else:
        result = User.objects.authenticate(request.POST['email'],request.POST['password']) # Checking login
        if result == False:
            messages.error(request, "Email or passwort do not match.")
            return redirect('/login')
        else:
            user = User.objects.get(email = request.POST['email'])
            request.session['user_id'] = user.id
            first_i = user.first_name[0]
            last_i = user.last_name[0]
            initials = first_i + last_i
            request.session['initials'] = initials
            return redirect('/')
        


# LOGOUT
def logout(request):
    request.session.clear()
    return redirect("/login")

# VIEW JOB
def view_job(request, job_id):
    if 'user_id' in request.session:
        if len(Job.objects.filter(id = job_id)) > 0:
            context = {
                'cur_user': User.objects.get(id = request.session['user_id']),
                'needed_job':Job.objects.get(id = job_id)
            }
            return render(request, 'view_job.html', context)
        else:
            return redirect('/dashboard')
    else:
        context = {
            'needed_job':Job.objects.get(id = job_id)
        }
        return render(request, 'view_job.html', context)


# CREATE NEW JOB
def create_new_job(request):
    if request.method == "GET":
        context = {
            'all_categories': Category.objects.all(),
            'cur_user': User.objects.get(id = request.session['user_id']),
        }
        return render(request, "create_job.html", context)

    else:
        errors = Job.objects.job_validator(request.POST)	
        if len(errors)>0:													
            for value in errors.values():											
                messages.error(request, value)											
            return redirect('/create_new_job')
        poster = User.objects.get(id = request.session['user_id'])
        
        this_job = Job.objects.create(title = request.POST['title'], description = request.POST['description'], location = request.POST['location'],poster = poster)
        categories = request.POST.getlist('category')
        if len(categories) > 0:
            for i in categories:
                needed_category = Category.objects.get(id = i)
                this_job.categories.add(needed_category)
                this_job.save()

        if len(request.POST['other']) > 0:
            cur_category = Category.objects.create(name = request.POST['other'])
            this_job.categories.add(cur_category)
            this_job.save()
        messages.success(request, "Job Successfully Created!")
        return redirect('/dashboard')

# ADD JOB TO USER
def add_job(request, job_id):
    user = User.objects.get(id = request.session['user_id'])
    job = Job.objects.get(id =job_id)
    job.executor = user
    job.save()
    messages.success(request, "Job successfully added to your active jobs!")
    # return redirect(f'/user/{user.id}/profile')
    return redirect('/dashboard')

# DONE WITH JOB
def done_job(request, job_id):
    job = Job.objects.get(id =job_id)
    job.delete()
    return redirect('/dashboard')

# GIVE UP JOB
def giveup_job(request, job_id):
    user = User.objects.get(id = request.session['user_id'])
    job = Job.objects.get(id =job_id)
    job.executor = None
    job.save()
    messages.success(request, "You gave up this job!")
    return redirect(f'/user/{user.id}/profile')

# EDIT JOB
def edit_job(request, job_id):
    if request.method == "GET":
        context = {
            'cur_user': User.objects.get(id = request.session['user_id']),
            'needed_job': Job.objects.get(id = job_id),
            'all_categories': Category.objects.all()
        }
        return render(request, "edit_job.html", context)
    else:
        print(request.POST)
        errors = Job.objects.job_validator(request.POST)	
        if len(errors)>0:													
            for value in errors.values():											
                messages.error(request, value)											
            return redirect('/create_new_job')
        edited_job = Job.objects.get(id = job_id)
        edited_job.title = request.POST['title']
        edited_job.description = request.POST['description']
        edited_job.location = request.POST['location']
        categories = request.POST.getlist('category')
        if len(categories) > 0:
            for i in categories:
                needed_category = Category.objects.get(id = i)
                edited_job.categories.add(needed_category)
                edited_job.save()
        edited_job.save()
        messages.success(request, "Job Successfully Updated!")
        return redirect('/dashboard')

# REMOVE JOB
def remove_job(request, job_id):
    job = Job.objects.get(id =job_id)
    if job.poster.id == request.session['user_id']:
        job.delete()
    messages.success(request, "Job removed from table!")
    return redirect('/dashboard')

# REMOVE CATEGORY
def remove_category(request, category_id, job_id):
    category = Category.objects.get(id =category_id)
    job = Job.objects.get(id =job_id)
    if job.poster.id == request.session['user_id']:
        job.categories.remove(category)
        job.save()
    return redirect(f'/edit_job/{job_id}')



# VIEW USER PROFILE
def profile(request, user_id):
    if request.method == 'GET':
        needed_user = User.objects.get(id = user_id)
        all_posted_jobs = needed_user.poster.all()
        all_active_jobs = needed_user.executor.all()
        first_i = needed_user.first_name[0]
        last_i = needed_user.last_name[0]
        initials = first_i + last_i
        context = {
            'user': needed_user,
            'initials': initials,
            'all_posted_jobs': all_posted_jobs, 
            'all_active_jobs': all_active_jobs
        }
        return render(request, 'user_profile.html', context)  
    else:
        user_id = request.session['user_id']
        return redirect(f'/user/{user_id}/profile')

def all_users(request):
    context = {
        'cur_user':  User.objects.get(id = request.session['user_id']),
        'users' : User.objects.all(),
        'all_jobs' : Job.objects.all().order_by('-created_at'),
    }
    return render(request, 'all_users.html', context)



def add_comment(request, job_id):
    if request.method == "POST":
        new_comment = Comment.objects.create(comment = request.POST['comment'], poster = User.objects.get(id = request.session['user_id']), job = Job.objects.get(id = job_id))
        print("COMMENT", new_comment)
        return redirect(f'/view/{job_id}')
    print("COMMENT OUTSIDE", new_comment)
    return redirect('/dashboard')




