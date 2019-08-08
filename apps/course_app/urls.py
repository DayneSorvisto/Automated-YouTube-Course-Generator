from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$', views.index),
    url(r'^create_course_form$', views.create_course_form),
    url(r'^create_course_post$', views.create_course_post),
    url(r'^(?P<course_id>\d+)$', views.read_course),
    url(r'^select_crs/(?P<cat_id>\d+)$', views.get_cat_id),
    url(r'^(?P<course_id>\d+)/edit_course_form$', views.edit_course_form),
    url(r'^(?P<course_id>\d+)/edit_course_post$', views.edit_course_post),
    url(r'^(?P<course_id>\d+)/delete_course$', views.delete_course),
    url(r'^(?P<course_id>\d+)/like_course$', views.like_course),
    url(r'^(?P<course_id>\d+)/unlike_course$', views.unlike_course),
]