from django.shortcuts import render, redirect, HttpResponse
from .models import User
# TODO if the logic in profile method works, remove the below 2 imports
from apps.video_app.models import Video
from apps.course_app.models import Course, Category
from django.contrib import messages

def index(request):
    return render(request, 'user_app/index.html')

def register_user(request):
    # validate user information
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect("/")

    # register user
    request.session['user_id'] = User.objects.register_user(request.POST)
    return redirect("/course")

def login(request):
    # validate login info
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect("/")
        
    # login
    request.session['user_id'] = User.objects.get(email=request.POST['email']).id
    return redirect("/course")

def profile(request):
    # if not 'user_id' in request.session:
    #     messages.error(request, "Please log in", extra_tags="log_in")
    #     return redirect("/")
    user = User.objects.get(id=request.session['user_id'])
    # completed = Video.objects.filter(users_who_completed=user)
    # created = Course.objects.filter(author=user)
    # TODO does the below work instead of pulling data from other tables?
    context={
        "user": user,
        "completed": user.videos_completed.all(),
        "created": user.courses_authored.all(),
        'categories': Category.objects.all(),
    }
    return render(request, "user_app/profile.html", context)
# region redirects

def update_profile(request):
    user_id = request.session['user_id']
    User.objects.process_profile_update(request.POST, user_id)
    return redirect("/profile")

def logout(request):
    keys = []
    for key in request.session.keys():
        keys.append(key)
    for key in keys:
        del request.session[key]
    return redirect("/")
# endregion

def email_check(request):
    if User.objects.filter(email=request.POST['email']):
        return HttpResponse("That email is already in use")
    return HttpResponse("")
