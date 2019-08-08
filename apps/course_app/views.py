from django.shortcuts import render, redirect, HttpResponse
from apps.course_app.models import Course, Subject, Category
from apps.video_app.models import Video
from django.contrib import messages

def index(request):
    if 'cat_id' in request.session:
        context={
        "category": Category.objects.all(),
        "courses": Course.objects.all().order_by('-created_at')[:6],
        'cat_crs': Course.objects.filter(category=Category.objects.get(id=request.session['cat_id'])),
        'cat_selected': True,
        }
        del request.session['cat_id']
    else:
        context={
            "category": Category.objects.all(),
            "courses": Course.objects.all().order_by('-created_at')[:6],
            'cat_selected': False,
        }
    return render(request, "course_app/courses.html", context)

def create_course_form(request):
    context = {
        'categories': Category.objects.all(),
        'subjects': Subject.objects.all(),
    }
    return render(request, "course_app/create.html", context)

def create_course_post(request):
    if 'user_id' in request.session and request.method == 'POST': #user is logged in and method is post
        errors = Course.objects.validate(request.POST)
        if not errors:
            if request.POST['subject_id'] != 'add': #subject chosen
                if request.POST['category_id'] != 'add': #subject chosen category chosen
                    subject_id = request.POST['subject_id']
                    category_id = request.POST['category_id']
                else: #subject chosen category added
                    subject_id = request.POST['subject_id']
                    category_id = Category.objects.create(name = request.POST['category_name']).id
            else: #subject added
                if request.POST['category_id'] != 'add': #subject added category chosen
                    subject_id = Subject.objects.create(name = request.POST['subject_name']).id
                    category_id = request.POST['category_id']
                else: #subject added category added
                    subject_id = Subject.objects.create(name = request.POST['subject_name']).id
                    category_id = Category.objects.create(name = request.POST['category_name']).id
            course_id = Course.objects.create_course(request.session['user_id'], category_id, subject_id, request.POST).id
        else:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/course/create_course_form')
        return redirect(f'/course/{course_id}')
    messages.error(request, 'You are not logged in', extra_tags='user_id')
    return redirect('/')

def read_course(request, course_id):
    course_passed = False
    author = False
    course_liked = False
    if 'user_id' in request.session:
        #check if author        
        if request.session['user_id'] == Course.objects.get(id=course_id).author.id:
            author = True
        #check if passed
        course_videos = Video.objects.filter(course=Course.objects.get(id=course_id))
        total = 0
        for video in course_videos:
            if len(video.questions.all()) > 0:
                total +=1
        correct = 0
        for video in course_videos:
            users_passed = video.users_completed.all()
            for user in users_passed:
                if user.id == request.session['user_id']:
                    correct += 1
        if total != 0:
            if correct == total:
                course_passed = True
        users_liked = Course.objects.get(id=course_id).likes.all()
        for user in users_liked:
            if user.id == request.session['user_id']:
                course_liked = True
    context = {
        'course': Course.objects.get(id=course_id),
        'category': Category.objects.all(),
        'author': author,
        'course_passed': course_passed,
        'course_liked': course_liked,
    }
    return render(request, "course_app/read.html", context)

def delete_course(request, course_id):
    if Course.objects.filter(id=course_id) and request.session['user_id'] == Course.objects.get(id=course_id).author.id:
        Course.objects.get(id=course_id).delete()
    return redirect('/course')

def edit_course_form(request, course_id):
    if 'user_id' in request.session and request.session['user_id'] == Course.objects.get(id=course_id).author.id:
        course = Course.objects.get(id = course_id)
        context = {
            'course_id': course.id,
            'title': course.title,
            'subject': course.subject,
            'category': course.category,
            'description': course.description,
            'categories': Category.objects.all(),
            'subjects': Subject.objects.all(),
        }
        return render(request, "course_app/edit.html", context)
    messages.error(request, 'You are not the author of this course', extra_tags='user_id')
    return redirect(f'/course/{course_id}')

def edit_course_post(request, course_id):
    if 'user_id' in request.session and request.session['user_id'] == Course.objects.get(id=course_id).author.id and request.method == 'POST':
        errors = Course.objects.validate(request.POST)
        if not errors:
            Course.objects.edit_course(course_id, request.POST)
            return redirect(f'/course/{course_id}')
        else:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect(f'/course/{course_id}/edit_course_form')
    messages.error(request, 'You are not the author of this course.', extra_tags='user_id')
    return redirect(f'/course/{course_id}')

def like_course(request, course_id):
    if 'user_id' in request.session:
        Course.objects.like_course(course_id, request.session['user_id'])
    return redirect(f'/course/{course_id}')

def unlike_course(request, course_id):
    if 'user_id' in request.session:
        Course.objects.unlike_course(course_id, request.session['user_id'])
    return redirect(f'/course/{course_id}')

def get_cat_id(request, cat_id):
    request.session['cat_id'] = cat_id
    return redirect('/course')