from django.db import models

class Scan(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255, default='pending')

class Progress(models.Model):
    scan = models.ForeignKey(Scan, related_name='progress', on_delete=models.CASCADE)
    progress_percentage = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)


#---------------------- OLD MODELS. DELETE LATER ----------------------#
class Department(models.Model):
    title = models.CharField(max_length=100)

class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    birthdate = models.DateField(null=True, blank=True)
    cv = models.FileField(null=True, blank=True)
