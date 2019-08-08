from django.shortcuts import render, redirect, HttpResponse
from .models import Question
from apps.video_app.models import Video
from apps.course_app.models import Course, Category
from django.contrib import messages

def create_question_post(request, course_id, video_id):
    if 'user_id' in request.session and request.method == 'POST':
        errors = Question.objects.validate(request.POST)
        if not errors:
            question_id = Question.objects.create_question(video_id, request.POST).id
            return redirect(f'/course/{course_id}/video/{video_id}')
        else:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect(f'/course/{course_id}/video/{video_id}/edit_video_form')
    messages.error(request, 'You are not the author of this course', extra_tags='user_id')
    return redirect(f'/course/{course_id}/video/{video_id}/edit_video_form')

def edit_question_form(request, course_id, video_id, question_id):
    question = Question.objects.get(id=question_id)
    context = {
        'video': Video.objects.get(id=video_id),
        'course': Course.objects.get(id=course_id),
        'question': Question.objects.get(id=question_id),
        'categories': Category.objects.all(),
    }
    return render(request, "quiz_app/edit.html", context)

def edit_question_post(request, course_id, video_id, question_id):
    if 'user_id' in request.session and request.session['user_id'] == Video.objects.get(id=video_id).course.author.id and request.method == 'POST':
        errors = Question.objects.validate(request.POST)
        if not errors:
            Question.objects.edit_question(question_id, request.POST)
            return redirect(f'/course/{course_id}/video/{video_id}')
        else:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect(f'/course/{course_id}/video/{video_id}/edit_video_form')
    messages.error(request, 'You are not the author of this course', extra_tags='user_id')
    return redirect(f'/course/{course_id}/video/{video_id}/edit_video_form')

def delete_question(request, course_id, video_id, question_id):
    if 'user_id' in request.session and request.session['user_id'] == Video.objects.get(id=video_id).course.author.id:
        Question.objects.delete_question(question_id)
    return redirect(f'/course/{course_id}/video/{video_id}')