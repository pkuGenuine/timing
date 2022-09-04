from django.db import models

from account.models import Account


class DailyTask(models.Model):

    class Meta:
        unique_together = ['user', 'title']

    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    title = models.CharField(max_length=15)
    active = models.BooleanField(default=True)
    label = models.CharField(max_length=15, default='')

    def __str__(self):
        return self.title


class DailyTaskRecord(models.Model):

    class Meta:
        unique_together = ['date', 'task']

    class RecordStatus(models.IntegerChoices):
        UNCHECK = (0, 'uncheck')
        CHECKED = (1, 'checked')

    date = models.DateField()
    task = models.ForeignKey(DailyTask, on_delete=models.CASCADE)
    remark = models.CharField(max_length=63, default='')
    status = models.SmallIntegerField(choices=RecordStatus.choices,
                                      default=RecordStatus.CHECKED)
