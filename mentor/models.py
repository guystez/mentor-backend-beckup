from django.db import models

from django.contrib.auth.models import User



class Business(models.Model):
    business_type = models.TextField()
    business_name = models.TextField()
    business_code = models.TextField()
    access = models.BooleanField()
    data = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.business_name} ({self.business_code})"


class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    business = models.ForeignKey(Business, related_name='employees', on_delete=models.CASCADE)

class Question(models.Model):
    employee_id = models.TextField()
    question_text = models.TextField()
    business_code = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Checklist(models.Model):
    employee_id = models.TextField()
    task_id = models.IntegerField()
    text = models.TextField()
    area = models.TextField()
    business_code = models.TextField()
    finish_time = models.TextField()
    completed = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)


class Custom_checklist(models.Model):
    employee_id = models.TextField()
    text = models.TextField()
    area = models.TextField()
    business_code = models.TextField()
    finish_time = models.TextField()
    completed = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)



class Massage(models.Model):
    employee_id = models.TextField()
    text = models.TextField()
    business_code = models.TextField()
    completed = models.BooleanField()
    image = models.ImageField(blank=True, null=True)
    manager = models.BooleanField()
    mark_read = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


class ReadReceipt(models.Model):
    massage = models.ForeignKey(Massage, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    business_code = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Tasks(models.Model):
    employee_id = models.TextField()
    text = models.TextField()
    business_code = models.TextField()
    image = models.ImageField(blank=True, null=True)
    completed = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

class Answer(models.Model):
    question = models.OneToOneField(Question, related_name='answer', on_delete=models.CASCADE)
    answer_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
