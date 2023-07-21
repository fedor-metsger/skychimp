
from datetime import datetime

from django.core.management import BaseCommand
from django.db.models import Exists, OuterRef, Q

from mailing.models import Task, Client, Interval, Log

class Command(BaseCommand):

    def get_last_successful_log(self, t:Task, c:Client):
        '''
        Возвращает время последней удачной отправки рассылки клиенту
        '''
        try:
            return Log.objects.filter(client=c,
                                      task=t,
                                      status=Log.SUCCESS).latest('time')
        except Exception as e:
            print(e)
            return None

    def need_send(self, t:Task, l:Log):
        '''
        Проверяет, нужна ли сегодня рассылка
        '''
        def compare_weeks(d1, d2):
            '''
            Проверяет, что две даты попадают в одну календарную неделю
            '''
            if d1.year < d2.year:
                return True
            if d1.year == d2.year and d1.isocalendar()[1] < d2.isocalendar()[1]:
                return True

        if t.period == Task.DAILY:
            if l.time.date() < datetime.now().date():
                return True
        elif t.period == Task.WEEKLY:
            if compare_weeks(l.time, datetime.now()):
                return True
        else:
            if l.time.date().replace(day=1) < \
                    datetime.now().date().replace(day=1):
                return True
        return False

    def send_email(self, t:Task, c:Client):
        '''
        Отправляет письмо
        '''
        return Log.SUCCESS

    def log_result_to_db(self, t:Task, c:Client, s):
        '''
        Сохраняет результаты рассылки в БД
        '''
        l = Log(client=c, task=t, status=s, response="")
        l.save()

    def handle(self, *args, **options):

        now_time = datetime.utcnow().time()
        tasks = Task.objects.filter(
            Exists(
                Interval.objects.filter(start__lte=now_time, end__gte=now_time, task_id=OuterRef('pk'))
            )
        ).filter(status=Task.RUNNING).prefetch_related('clients')

        for t in tasks:
            print(t)
            for c in t.clients.all():
                print("\t" + str(c))
                last_successful_log = self.get_last_successful_log(t, c)
                if not last_successful_log or self.need_send(t, last_successful_log):
                    print("\tУдачной рассылки в данном периоде не было, запускаем")
                    success = self.send_email(t, c)
                    self.log_result_to_db(t, c, success)
                else:
                    print("\tРассылка в данном периоде состоялась, пропуск")

