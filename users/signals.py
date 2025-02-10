from django.db.models.signals import post_save, pre_save, m2m_changed, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings

# @receiver(post_save,sender=User)
# def send_activation_email(sender,instance,created,**kwargs):
#     if created:
#         token=default_token_generator.make_token(instance)
#         activation_url=f'{settings.FORNTEND_URL}/users/activate/{instance.id}/{token}/'

#         subject='Activate your account'
#         message=f'Hi {instance.username},\n\n Please activate your account by clicking the link below {activation_url}\n\n'
#         receipient_list=[instance.email]

#         try:
#             send_mail(
#                 subject,
#                 message,
#                 settings.EMAIL_HOST_USER,
#                 receipient_list,
#                 # fail_silently=False,
#             )
#         except Exception as e:
#             print(f'Failed to send email to {instance.email}:{str(e)}')


@receiver(post_save, sender=User)
def send_activation_email(sender, instance, created, **kwargs):
    if created:
        token = default_token_generator.make_token(instance)
        activation_url = f"{settings.FRONTEND_URL}/users/activate/{instance.id}/{token}/"

        subject = 'Activate Your Account'
        message = f'Hi {instance.username},\n\nPlease activate your account by clicking the link below:\n{
            activation_url}\n\nThank You!'
        recipient_list = [instance.email]

        try:
            send_mail(subject, message,
                      'mohsinibnaftab@gmail.com', recipient_list)
        except Exception as e:
            print(f"Failed to send email to {instance.email}: {str(e)}")
