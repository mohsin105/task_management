from django.db import models

# Create your models here.

class Project(models.Model):
    name=models.CharField(max_length=250)
    start_date=models.DateField()

class Employee(models.Model):
    name=models.CharField(max_length=250)
    email=models.EmailField(unique=True)

class Task(models.Model):
    project=models.ForeignKey(Project,on_delete=models.CASCADE, default=1,related_name='task_list')
    assigned_to=models.ManyToManyField(Employee,related_name='tasks')
    # manytomany field value is not needed to be provided when creating object in shell
    title=models.CharField(max_length=250)
    description=models.TextField()
    due_date=models.DateField()
    is_completed=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


class TaskDetail(models.Model):
    HIGH='H'
    MEDIUM='M'
    LOW='L'
    PRIORITY_OPTIONS=((HIGH,'High'),
                      (MEDIUM,'Medium'),
                      (LOW,'Low'))
    
    task=models.OneToOneField(Task,on_delete=models.CASCADE,related_name='details')
    # task field takes a Task object as value, not the id of Task object, when creating a taskdeatil object using shell
    # but in vs code, during model declaration, default= key argument takes the id of object, not object itself.
    assigned_to=models.CharField(max_length=250)
    priority=models.CharField(max_length=1,choices=PRIORITY_OPTIONS,default=LOW)