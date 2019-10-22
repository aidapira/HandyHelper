from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import *


def index(request):
    return render(request, 'job_manager_app/index.html')


def user(request):
    # User processor
    errors = User.objects.validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags="register")
        return redirect('/')
    else:
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        matched_email = User.objects.filter(email=request.POST["email"])
        if len(matched_email) > 1:
            messages.error(request, 'Email already exists')
            return redirect('/')
        pw_hash = bcrypt.hashpw(
            request.POST["password"].encode(), bcrypt.gensalt())
        new_user = User.objects.create(
            first_name=first_name, last_name=last_name, email=email, password=pw_hash)
        request.session["new_user_id"] = new_user.id
    return redirect('/jobs/new')


def registration(request):
    context = {
        "reg_user": User.objects.get(id=request.session["new_user_id"])
    }
    return render(request, 'job_manager_app/new_jobs.html', context)


def login_process(request):
    matched_user = User.objects.filter(email=request.POST['email'])
    print(matched_user)
    if len(matched_user) < 1:
        messages.error(
            request, 'Email or password does not match', extra_tags="login")
        return redirect('/')
    if bcrypt.checkpw(request.POST['password'].encode(), matched_user[0].password.encode()):
        request.session['email'] = request.POST['email']
        request.session['new_user_id'] = matched_user[0].id
        return redirect('/login')
    else:
        messages.error(request, 'Email or password do not match',
                       extra_tags="login")
        return redirect('/')
    return redirect('/')


def login(request):
    context = {
        "reg_user": User.objects.filter(email=request.session["email"])[0],
    }
    return render(request, 'job_manager_app/new_jobs.html', context)


def logout(request):
    request.session.clear()
    return redirect('/')


def job_process(request):
    errors = User.objects.jobmanager(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/jobs/new')
    user = User.objects.get(id=request.session["new_user_id"])
    Job.objects.create(
        job=request.POST["job"], description=request.POST["description"], user=user, location=request.POST["location"])
    # Category.categories.add(request.POST["choice"])
    return redirect('/dashboard')


def jobs(request):
    current_user = User.objects.get(id=request.session["new_user_id"])
    context = {
        "reg_user": User.objects.get(id=request.session["new_user_id"]),
        "jobs": Job.objects.all(),
    }
    return render(request, 'job_manager_app/jobs.html', context)


def remove_job(request, jobid):
    selected_job = Job.objects.get(id=jobid)
    selected_job.delete()
    return redirect('/dashboard')


def edit_job(request, jobid):
    context = {
        "reg_user": User.objects.get(id=request.session["new_user_id"]),
        "edited_job": Job.objects.get(id=jobid)
    }
    return render(request, 'job_manager_app/edit_job.html', context)


def update(request, jobid):
    errors = User.objects.jobmanager(request.POST)
    job_id = jobid
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/jobs/edit/' + job_id)
    else:
        updated_job = Job.objects.get(id=jobid)
        updated_job.job = request.POST["job"]
        updated_job.description = request.POST["description"]
        updated_job.location = request.POST["location"]
        updated_job.save()
    return redirect('/dashboard')


def granted(request, jobid):
    granted_job = Job.objects.get(id=jobid)
    granted_job.isgranted = True
    granted_job.save()
    return redirect('/dashboard')


def add(request, jobid):
    added_job = Job.objects.get(id=jobid)
    added_job.isadded = True
    added_job.save()
    return redirect('/dashboard')


def giveup(request, jobid):
    gaveup_job = Job.objects.get(id=jobid)
    gaveup_job.isadded = False
    gaveup_job.save()
    return redirect('/dashboard')


def details(request, jobid):
    current_user = User.objects.get(id=request.session["new_user_id"])
    context = {
        "reg_user": User.objects.get(id=request.session["new_user_id"]),
        "selected_job": Job.objects.get(id=jobid)
    }
    return render(request, 'job_manager_app/view_details.html', context)



