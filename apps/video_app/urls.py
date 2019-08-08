from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^(?P<course_id>\d+)/video/create_video_form$', views.create_video_form),
    url(r'^(?P<course_id>\d+)/video/create_video_post$', views.create_video_post),
    url(r'^(?P<course_id>\d+)/video/(?P<video_id>\d+)$', views.read_video),
    url(r'^(?P<course_id>\d+)/video/(?P<video_id>\d+)/edit_video_form$', views.edit_video_form),
    url(r'^(?P<course_id>\d+)/video/(?P<video_id>\d+)/edit_video_post$', views.edit_video_post),
    url(r'^(?P<course_id>\d+)/video/(?P<video_id>\d+)/delete_video$', views.delete_video),
    url(r'^(?P<course_id>\d+)/video/(?P<video_id>\d+)/quiz_post$', views.quiz_post),
    url(r'^(?P<course_id>\d+)/video/(?P<video_id>\d+)/like_video$', views.like_video),
    url(r'^(?P<course_id>\d+)/video/(?P<video_id>\d+)/unlike_video$', views.unlike_video),
]