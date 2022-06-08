import logging
 
from django.conf import settings
from datetime import datetime
from django.core.mail import EmailMultiAlternatives
from NewsPortal.models import * 
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django.template.loader import *
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
 
 
logger = logging.getLogger(__name__)
 
 
# наша задача по выводу текста на экран
def send_weekly_mail():
    for category in Category.objects.all():
        news_from_each_category = []
        week_number_last = datetime.now().isocalendar()[1] - 1
        for news in Post.objects.filter(postCategory=category.id,
            creation_timedate__week=week_number_last).values('pk', 'title', 'creation_timedate', 'postCategory__name'):
            date_format = news.get("creation_timedate").strftime("%m/%d/%Y")
            article =   (f'http://127.0.0.1:8000/news/{news.get("pk")}, {news.get("title")},'
                         f'Category: {news.get("postCategory__name")}, Date: {date_format}')
            news_from_each_category.append(article)
            
    for subscriber in category.subscribers.all():
        html_content = render_to_string(
                'weekly.html', {'user': subscriber,
                                'text': news_from_each_category,
                                'category_name': category.name,
                                'week_number_last': week_number_last})
        msg = EmailMultiAlternatives(
            subject=f'Greetings, {subscriber.username}, herea are the new articles from the last week.',
            from_email='',
            to=[subscriber.email]
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()



# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)
 
 
class Command(BaseCommand):
    help = "Runs apscheduler."
 
    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")
        
        # добавляем работу нашему задачнику
        scheduler.add_job(
            send_weekly_mail,
            trigger=CronTrigger(day_of_week="mon", hour="00", minute="00"),  # То же, что и интервал, но задача тригера таким образом более понятна django
            id="send_weekly_mail",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'send_weekly_mail'.")
 
        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )
 
        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")