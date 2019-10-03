from django.db import models
from apps.user_app.models import User

class CourseManager(models.Manager):

    def validate(self, form):
        errors = {}
        if len(form['subject_id']) < 1 and len(form['subject_name']) < 3:
            errors['subject'] = 'Please select a subject'
        if len(form['category_id']) < 1 and len(form['category_name']) < 3:
            errors['category'] = 'Please select a category'
        if len(form['title']) < 3:
            errors['title'] = 'Please create a title'
        if len(form['description']) < 3:
            errors['description'] = 'Please create a description'
        return errors

    def create_course(self, user_id, category_id, subject_id, form):
        new_course = self.create(subject = Subject.objects.get(id=subject_id), category = Category.objects.get(id=category_id), title = form['title'], description = form['description'], author = User.objects.get(id = user_id))
        return new_course
    
    def delete_course(self, course_id):
        self.get(id = course_id).delete()
        return self

    def edit_course(self, course_id, form):
        course = self.get(id = course_id)
        course.subject = Subject.objects.get(id=form['subject_id'])
        course.category = Category.objects.get(id=form['category_id'])
        course.title = form['title']
        course.description = form['description']
        course.save()
        return self
    
    def like_course(self, course_id, user_id):
        users_liked = Course.objects.get(id=course_id).likes.all()
        for user in users_liked:
            if user.id == user_id:
                return
        course = self.get(id = course_id)
        course.likes.add(User.objects.get(id=user_id))
        return self
    
    def unlike_course(self, course_id, user_id):
        users_liked = Course.objects.get(id=course_id).likes.all()
        for user in users_liked:
            if user.id == user_id:
                course = self.get(id = course_id)
                course.likes.remove(User.objects.get(id=user_id))
        return self

class Category(models.Model):
    name = models.CharField(max_length=255)

class Subject(models.Model):
    name = models.CharField(max_length=255)

class Course(models.Model):
    title = models.CharField(max_length=255)
    subject = models.ForeignKey(Subject,related_name="courses")
    category = models.ForeignKey(Category,related_name="courses")
    description = models.CharField(max_length=255)
    likes = models.ManyToManyField(User, related_name="courses_liked")
    author = models.ForeignKey(User, related_name="courses_authored")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = CourseManager()

