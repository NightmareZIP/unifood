#подключаем библиотеки
from django.db import models
from worker.models import Worker


class EventType(models.Model):

    color = models.CharField(max_length=10)
    name = models.CharField(max_length=255)

    def __str__(self):
        return '%s' % self.name

class Event(models.Model):
    event_name = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        Worker, related_name='worker_by', on_delete=models.CASCADE)
    created_for = models.ForeignKey(
        Worker, related_name='worker_for', on_delete=models.CASCADE)
    comment = models.TextField()
    period = models.IntegerField(default=0)
    date_from = models.DateTimeField()
    date_to = models.DateTimeField()
    # TODO add members
    # members
    event_type = models.ForeignKey(
        EventType, related_name='event', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.company.name}:{self.menu_item.name}'
