from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^(?P<course_id>\d+)/video/(?P<video_id>\d+)/create_question_post$', views.create_question_post),
    url(r'^(?P<course_id>\d+)/video/(?P<video_id>\d+)/question/(?P<question_id>\d+)/edit_question_form$', views.edit_question_form),    
    url(r'^(?P<course_id>\d+)/video/(?P<video_id>\d+)/question/(?P<question_id>\d+)/edit_question_post$', views.edit_question_post),
    url(r'^(?P<course_id>\d+)/video/(?P<video_id>\d+)/question/(?P<question_id>\d+)/delete_question$', views.delete_question),
]