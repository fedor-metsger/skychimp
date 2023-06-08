
from django.db import models

# Create your models here.
# class Period(models.Model):
#     slug = models.CharField(max_length=20, verbose_name="slug")
#     description = models.CharField(max_length=20, verbose_name="описание")
#
#     def __str__(self):
#         return f'{self.description}'
#
#     class Meta:
#         verbose_name = "периодичность"
#
# class Status(models.Model):
#     slug = models.CharField(max_length=20, verbose_name="slug")
#     description = models.CharField(max_length=20, verbose_name="описание")
#
#     def __str__(self):
#         return f'{self.description}'
#
#     class Meta:
#         verbose_name = "статус"

class Task(models.Model):
    title = models.CharField(max_length=100, verbose_name="название")
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    PERIOD_CHOICES = [
        (DAILY, "ежедневно"),
        (WEEKLY, "еженедельно"),
        (MONTHLY, "ежемесячно"),
    ]
    period = models.CharField(
        max_length=7,
        choices=PERIOD_CHOICES,
        default=DAILY,
    )
    # period = models.ForeignKey(Period, on_delete=models.CASCADE, verbose_name="периодичность")
    CREATED = "created"
    RUNNING = "running"
    FINISHED = "finished"
    STATUS_CHOICES = [
        (CREATED, "создана"),
        (RUNNING, "запущена"),
        (FINISHED, "завершена"),
    ]
    status = models.CharField(
        max_length=8,
        choices=STATUS_CHOICES,
        default=CREATED,
    )
    # status = models.ForeignKey(Status, on_delete=models.CASCADE, verbose_name="статус")
    subject = models.CharField(max_length=100, verbose_name="тема")
    body = models.TextField(null=True, blank=True, verbose_name="текст сообщения")

    def __str__(self):
        # return f'Task({self.title}, {self.period}, {self.status}'
        return f'{self.title}'

    class Meta:
        verbose_name = 'задание'
        verbose_name_plural = 'задания'

class TimeWindow(models.Model):
    task = models.ForeignKey(Task, verbose_name="задание", on_delete=models.CASCADE)
    start = models.TextField(verbose_name="начало интервала")
    end = models.TimeField(verbose_name="конец интервала")

    def __str__(self):
        return f'TimeWindow({self.start} - {self.end})'

    class Meta:
        verbose_name = 'интервал'
        verbose_name_plural = 'интервалы'

class Client(models.Model):
    name = models.CharField(max_length=100, verbose_name="ФИО")
    email = models .EmailField(verbose_name="e-mail")
    description = models.TextField(verbose_name='комментарий')
    tasks = models.ManyToManyField(Task, verbose_name="назначение")

    def __str__(self):
        return f'Client({self.name})'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'
        ordering = ['name']

class Log(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="клиент")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name="задание")
    time = models.DateTimeField(verbose_name="время")
    status = models.IntegerField(verbose_name="статус")
    response = models.TextField(verbose_name="ответ сервера")

    def __str__(self):
        return f'Log({self.client}, {self.task}, {self.time}, {self.status})'

    class Meta:
        verbose_name = 'попытка'
        verbose_name_plural = 'попытки'

