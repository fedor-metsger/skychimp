
from datetime import datetime

from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.db.models import Exists, OuterRef

from mailing.models import Task, Client, Interval, Log

class EmailManager():
    crontab_status = False

    @staticmethod
    def get_last_successful_log(t:Task, c:Client):
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

    @staticmethod
    def need_send(t:Task, l:Log):
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

    @staticmethod
    def send_single_email(t:Task, c:Client):
        '''
        Отправляет письмо
        '''
        return Log.SUCCESS

    @staticmethod
    def log_result_to_db(t:Task, c:Client, s):
        '''
        Сохраняет результаты рассылки в БД
        '''
        l = Log(client=c, task=t, status=s, response="")
        l.save()

    @staticmethod
    def run_sending():

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
                last_successful_log = EmailManager.get_last_successful_log(t, c)
                if not last_successful_log or EmailManager.need_send(t, last_successful_log):
                    print("\tУдачной рассылки в данном периоде не было, запускаем")
                    success = EmailManager.send_single_email(t, c)
                    EmailManager.log_result_to_db(t, c, success)
                else:
                    print("\tРассылка в данном периоде состоялась, пропуск")

    @staticmethod
    def send_emails(request):
        if request.user.is_superuser != True:
            raise PermissionDenied()

        EmailManager.run_sending()

        return redirect('index')

    @staticmethod
    def switch_crontab(request):
        if request.user.is_superuser != True:
            raise PermissionDenied()
        EmailManager.crontab_status = not EmailManager.crontab_status
        return redirect('index')