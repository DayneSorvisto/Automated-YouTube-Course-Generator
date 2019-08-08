from django.shortcuts import render, redirect, HttpResponse
from apps.video_app.models import Video
from apps.course_app.models import Course, Subject, Category
from apps.quiz_app.models import Question
from apps.user_app.models import User
from django.contrib import messages

def create_video_form(request, course_id):
    context = {
        'course': Course.objects.get(id=course_id),
        'categories': Category.objects.all(),
    }
    return render(request, "video_app/create.html", context)

def create_video_post(request, course_id):
    if 'user_id' in request.session and request.method == 'POST':
        errors = Video.objects.validate(request.POST)
        if not errors:
            video_id = Video.objects.create_video(course_id, request.POST).id
            return redirect(f'/course/{course_id}/video/{video_id}')
        else:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect(f'/course/{course_id}/create_video_form')
    messages.error(request, 'You are not the author of this course', extra_tags='user_id')
    return redirect(f'/course/{course_id}')

def read_video(request, course_id, video_id):
    quiz_passed = False
    course_passed = False
    author = False
    course_liked = False
    users_passed = Video.objects.get(id=video_id).users_completed.all()
    if 'user_id' in request.session:
        for user in users_passed:
            if user.id == request.session['user_id']:
                quiz_passed = True
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
        'video': Video.objects.get(id=video_id),
        'course': Course.objects.get(id=course_id),
        'author': author,
        'questions': Question.objects.filter(video = Video.objects.filter(id=video_id)),
        'category': Category.objects.all(),
        'quiz_passed': quiz_passed,
        'course_passed': course_passed,
        'course_liked': course_liked,
    }
    return render(request, "video_app/read.html", context)

def delete_video(request, course_id, video_id):
    if 'user_id' in request.session and request.session['user_id'] == Video.objects.get(id=video_id).course.author.id:
        Video.objects.delete_video(video_id)
    return redirect(f'/course/{course_id}')

def edit_video_form(request, course_id, video_id):
    if 'user_id' in request.session and request.session['user_id'] == Video.objects.get(id=video_id).course.author.id:
        video = Video.objects.get(id=video_id)
        context = {
            'video': Video.objects.get(id=video_id),
            'course': Course.objects.get(id=course_id),
            'questions': Question.objects.filter(video = Video.objects.get(id=video_id)),
            'categories': Category.objects.all(),
        }
        return render(request, "video_app/edit.html", context)
    messages.error(request, 'You are not the author of this video', extra_tags='user_id')
    return redirect(f'/course/{course_id}/video/{video_id}')

def edit_video_post(request, course_id, video_id):
    if 'user_id' in request.session and request.session['user_id'] == Video.objects.get(id=video_id).course.author.id and request.method == 'POST':
        errors = Video.objects.validate(request.POST)
        if not errors:
            Video.objects.edit_video(video_id, request.POST)
            return redirect(f'/course/{course_id}/video/{video_id}')
        else:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect(f'/course/{course_id}/edit_video_form')
    messages.error(request, 'You are not the author of this course', extra_tags='user_id')
    return redirect(f'/course/{course_id}/video/{video_id}')

def quiz_post(request, course_id, video_id):
    if 'user_id' in request.session and request.method == 'POST':
        errors = Question.objects.quiz_validate(video_id, request.POST)
        if not errors:
            questions = Question.objects.filter(video=Video.objects.get(id=video_id))
            total = len(questions)
            correct = 0
            for question in questions:
                if request.POST[str(question.id)] == question.answer:
                    correct +=1
            if correct == total:
                video = Video.objects.get(id=video_id)
                video.users_completed.add(User.objects.get(id=request.session['user_id']))
                video.save()
            else:
                messages.error(request, 'You did not pass the quiz', extra_tags='pass')
            return redirect(f'/course/{course_id}/video/{video_id}')
        else:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect(f'/course/{course_id}/video/{video_id}')
    messages.error(request, 'Something went wrong', extra_tags='user_id')
    return redirect(f'/course/{course_id}/video/{video_id}')

def like_video(request, course_id, video_id):
    if 'user_id' in request.session:
        Video.objects.like_video(video_id, request.session['user_id'])
    return redirect(f'/course/{course_id}/video/{video_id}')

def unlike_video(request, course_id, video_id):
    if 'user_id' in request.session:
        Video.objects.unlike_video(video_id, request.session['user_id'])
    return redirect(f'/course/{course_id}/video/{video_id}')