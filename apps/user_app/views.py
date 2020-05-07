from django.shortcuts import render, redirect, HttpResponse
from .models import User
# TODO if the logic in profile method works, remove the below 2 imports
from apps.video_app.models import Video
from apps.course_app.models import Course, Category
from django.contrib import messages
from mailchimp3 import MailChimp

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
    #add to mailchimp mailing list
    email = request.POST['email']
    client = MailChimp(mc_api="685f293a60cf0527c9255794b55602fe-us19",mc_user="daynesorvisto")
    try:
        client.lists.members.create('7f8f2c9947', {'email_address' : email,'status':'subscribed'})
    except Exception as e:
        print(e) 
        return redirect("/course")
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
        "is_premium" : user.is_premium,
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
