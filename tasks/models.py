from django.db import models
from django.db.models.signals import post_save,pre_save,m2m_changed,post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.

class Project(models.Model):
    name=models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    start_date=models.DateField()

    def __str__(self):
        return self.name



class Task(models.Model):
    STATUS_CHOICES=[
        ('PENDING','Pending'),
        ('IN_PROGRESS','In Progress'),
        ('COMPLETED','Completed')
    ]
    project=models.ForeignKey(Project,on_delete=models.CASCADE, default=1,related_name='task_list')
    # assigned_to=models.ManyToManyField(Employee,related_name='tasks')
    assigned_to=models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='tasks')
    # manytomany field value is not needed to be provided when creating object in shell
    status=models.CharField(max_length=15,choices=STATUS_CHOICES, default="PENDING")
    title=models.CharField(max_length=250)
    description=models.TextField()
    due_date=models.DateField()
    
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class TaskDetail(models.Model):
    HIGH='H'
    MEDIUM='M'
    LOW='L'
    PRIORITY_OPTIONS=((HIGH,'High'),
                      (MEDIUM,'Medium'),
                      (LOW,'Low'))
    asset=models.ImageField(upload_to='tasks_asset',blank=True,null=True,default='tasks_asset/default_img.jpg')
    task=models.OneToOneField(Task,on_delete=models.DO_NOTHING,related_name='details')
    # task field takes a Task object as value, not the id of Task object, when creating a taskdeatil object using shell
    # but in vs code, during model declaration, default= key argument takes the id of object, not object itself.
    # assigned_to=models.CharField(max_length=250)
    priority=models.CharField(max_length=1,choices=PRIORITY_OPTIONS,default=LOW)
    notes=models.TextField(blank=True,null=True)

    def __str__(self):
        return f'Details for task {self.task.title}'

# Signals

# @receiver(post_save,sender=Task)
# def notify_task_creation(sender,instance,created,**kwargs):
#     print('sender',sender) 
#     print('instance', instance)
#     print(kwargs)
#     print(created)
#     if created:
#         instance.is_completed=True
#         instance.save()
    
    #created is True if the instance is newly created, False if not. 
    #post_save itself is a save function. so another save() inside post_save() will 
    #be a recursion. hence the condition of created. means the inner save() will occur only when 
    #the instance is newly created. 

# @receiver(pre_save,sender=Task)
# def notify_task_before_creation(sender,instance,**kwargs):
#     print('sender',sender)
#     print('instance',instance)
#     print(kwargs)

#     instance.is_completed=True


# @receiver(m2m_changed,sender=Task.assigned_to.through)
# def notify_employee_on_task_creation(sender,instance,action,**kwargs):
#     if action=='post_add':
#         assigned_emails=[emp.email for emp in instance.assigned_to.all()]

#         print('Receivers ', assigned_emails)

#         send_mail(
#                 "New task assigned",
#                 f"You have been tasked with new task: {instance.title}",
#                 "mohsinibnaftab@gmail.com",
#                 assigned_emails,
#                 fail_silently=False,
#             )


# @receiver(post_delete,sender=Task)
# def delete_associate_task(sender,instance,**kwargs):
#     if instance.details:
#         instance.details.delete()
#         print("Deleted successfull!!")
        