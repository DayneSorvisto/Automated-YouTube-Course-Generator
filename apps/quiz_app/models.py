from django.db import models
from apps.video_app.models import *

class QuestionManager(models.Manager):

    def quiz_validate(self, video_id, form):
        errors = {}
        questions = self.filter(video=Video.objects.get(id=video_id))
        for question in questions:
            if not str(question.id) in form:
                errors[str(question.id)] = 'Please enter an answer.'
        return errors

    def validate(self, form):
        errors = {}
        if len(form['question']) < 1:
            errors['question'] = 'Please enter a question.'
        if len(form['option1']) < 1:
            errors['option1'] = 'Please enter an answer.'
        if len(form['option2']) < 1:
            errors['option2'] = 'Please enter an answer.'
        if len(form['option3']) < 1:
            errors['option3'] = 'Please enter an answer.'
        if len(form['option4']) < 1:
            errors['option4'] = 'Please enter an answer.'
        if len(form['option5']) < 1:
            errors['option5'] = 'Please enter an answer.'
        if len(form['answer']) < 1:
            errors['answer'] = 'Please enter an answer.'
        return errors

    def create_question(self, video_id, form):
        new_question = self.create(question = form['question'], option1 = form['option1'], option2 = form['option2'], option3 = form['option3'], option4 = form['option4'], option5 = form['option5'], answer = form['answer'],video = Video.objects.get(id=video_id))
        return new_question
    
    def delete_question(self, question_id):
        self.get(id = question_id).delete()
        return self

    def edit_question(self, question_id, form):
        question = self.get(id = question_id)
        question.question = form['question']
        question.option1 = form['option1']
        question.option2 = form['option2']
        question.option3 = form['option3']
        question.option4 = form['option4']
        question.option5 = form['option5']
        question.answer = form['answer']
        question.save()
        return self

class Question(models.Model):
    question = models.CharField(max_length=255)
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    option5 = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
    video = models.ForeignKey(Video, related_name="questions")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = QuestionManager()
