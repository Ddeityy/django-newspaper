from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from .models import post_category, User
from django.template.loader import render_to_string

@receiver(m2m_changed, sender=post_category)
def post(sender, instance, *args, **kwargs):
    url='http://127.0.0.1:8000/news/'
    for category in instance.post_category.all():
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