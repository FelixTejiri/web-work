import datetime
from django.utils import timezone
from dashboard.models import Investment,Payment

class CronJobs():

    def cron_create_payment(self):

        if timezone.now().day == 10:

            investments=investments.objects.filter(expiration_date__gte=timezone.now(),is_active=True)

            for investment in investments:
                Payment.objects.create(investment=investment,amount=investment.amount)

    def cron_deactivate_investment(self):

        investments=Investment.objects.filter(is_active=True)
        for investment in investments:
            if investment.expiration_date < timezone.now():
                investment.is_active=False
                investment.save()

    
