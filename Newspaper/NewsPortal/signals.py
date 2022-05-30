from django.db.models.signals import *
from django.dispatch import receiver # импортируем нужный декоратор
from django.core.mail import *
from .models import *
from django.template.loader import *

@receiver(m2m_changed, sender=PostCategory)
def post(sender, instance, *args, **kwargs):
    url='http://127.0.0.1:8000/news/'
    for category in instance.postCategory.all():
        for subscriber in category.subscribers.filter():
            msg = EmailMultiAlternatives(
                subject=instance.title,
                body=instance.text,
                from_email='',
                to=[User.objects.get(pk=subscriber.id).email],
                )
            html_content = render_to_string(
                'subletter.html',
                {
                    'instance': instance,
                    'user': subscriber,
                    'category': category,
                    'url': url
                }
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()

@receiver(post_save, sender=User)
def post(created, instance, *args, **kwargs):
    if created:
        msg = EmailMultiAlternatives(
            subject="Hello",
            body=instance.username,
            from_email='',
            to=[User.objects.get(pk=instance.id).email],
            )   
        html_content = render_to_string(
            'welcome.html',
            {
                'instance': instance,
                'user': User.objects.get(pk=instance.id),
            }
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()