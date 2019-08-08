from django.db import models
from apps.user_app.models import User
from apps.course_app.models import Course

class VideoManager(models.Manager):
    
    def validate(self, form):
        errors = {}
        if len(form['title']) < 3:
            errors['title'] = 'Please enter a title.'
        if len(form['url']) < 30:
            errors['url'] = 'Please enter a valid URL ex \'https://www.youtube.com/watch?v=VIDEO ID.'
        if len(form['description']) < 3:
            errors['description'] = 'Please create a description'
        return errors

    def create_video(self, course_id, form):
        thumbnail = "https://img.youtube.com/vi/" + form['url'].split('=')[-1] + "/0.jpg" #splits the video id out of the full url then concats to the YouTube thumbnail path
        url = "https://www.youtube.com/embed/" + form['url'].split('=')[-1] #splits the video id out of the full url then concats to the YouTube embed path
        new_video = self.create(title = form['title'], thumbnail = thumbnail, url = url, description = form['description'], course = Course.objects.get(id = course_id))
        return new_video
    
    def delete_video(self, video_id):
        self.get(id = video_id).delete()
        return self

    def edit_video(self, video_id, form):
        video = self.get(id = video_id)
        video.title = form['title']
        video.url = form['url']
        video.description = form['description']
        video.save()
        return self

    def like_video(self, video_id, user_id):
        users_liked = Video.objects.get(id=video_id).likes.all()
        for user in users_liked:
            if user.id == user_id:
                return
        video = self.get(id=video_id)
        video.likes.add(User.objects.get(id=user_id))
        return self

    def unlike_video(self, video_id, user_id):
        users_liked = Video.objects.get(id=video_id).likes.all()
        for user in users_liked:
            if user.id == user_id:
                video = self.get(id=video_id)
                video.likes.remove(User.objects.get(id=user_id))
        return self
   
class Video(models.Model):
    title = models.CharField(max_length=255)
    thumbnail = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    likes = models.ManyToManyField(User, related_name="videos_liked")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    course = models.ForeignKey(Course, related_name='videos')
    users_completed = models.ManyToManyField(User, related_name="videos_completed")
    objects = VideoManager()