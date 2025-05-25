from django.contrib.auth.models import User  # User modelini import qilish
from django.db import models

class Subject(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Question(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    text = models.TextField()
    image = models.ImageField(upload_to='questions/', blank=True, null=True)

    def __str__(self):
        return self.text[:50] + "..."

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class TestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    score = models.IntegerField()
    total = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def percentage(self):
        return round((self.score / self.total) * 100, 2)