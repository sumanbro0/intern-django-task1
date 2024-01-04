from django_celery_beat.models import PeriodicTask, IntervalSchedule

def start_periodic_tasks():
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=1,
        period=IntervalSchedule.MINUTES,
    )

    task_name = 'Create notification every 1 minutes'
    task, created = PeriodicTask.objects.get_or_create(
        interval=schedule,
        name=task_name,
        defaults={'task': 'books.tasks.create_book'},
    )

    if not created and task.task != 'books.tasks.create_book':
        task.task = 'notifications.tasks.create_book'
        task.save()