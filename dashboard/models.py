import datetime
from django.db import models
from django.utils import timezone
from mainsite.models import InvestmentPlan 
from django.contrib.auth.hashers import make_password, check_password
 
# Create your models here.

class User(models.Model):

    def set_password(self,password):
        enc_pass=make_password(password)
        self.password=enc_pass
        return password
 
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(blank=True,unique=True)
    password = models.CharField(max_length=300)
    country = models.CharField(max_length=50,null=True,blank=True)
    phone_number = models.CharField(max_length=50,null=True,blank=True)
    bank_name = models.CharField(max_length=20,null=True,blank=True)
    bank_account_number = models.CharField(max_length=20,null=True,blank=True)
    bank_account_name=models.CharField(max_length=50,null=True,blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return "{} - {} {}".format(self.email,self.first_name,self.last_name)

class ProofOfPayment(models.Model):

    STATES = (
        (1,"Pending"),
        (2,"Invalid"),
        (3,"Valid")
    )

    def get_default_plan():
        try:
            plan=InvestmentPlan.objects.order_by('id')[0]
        except:
            pass
        else:
            return plan.id

    def get_default_user():
        try:
            user=User.objects.order_by('id')[0]
        except:
            pass
        else:
            return user.id

    user=models.ForeignKey(User,default=get_default_user,on_delete=models.DO_NOTHING)
    investment_plan = models.ForeignKey(InvestmentPlan,on_delete=models.DO_NOTHING,default=get_default_plan,blank=False)
    file=models.FileField(upload_to="files/pop/")
    is_valid = models.IntegerField(default=1,choices=STATES)
    extra=models.TextField(null=True,blank=True)
    amount=models.FloatField(default=0.00)
    date=models.DateField(default=timezone.now)

    def __str__(self):
        return "{} {} - {}".format(self.user.first_name,self.user.last_name,self.investment_plan.name)

class Investment(models.Model):

    STATES = (
        (True, "Active"),
        (False, "Inactive")
    )

    def get_expiration_time():
        time = timezone.now() + datetime.timedelta(days=365)
        return time

    pop=models.OneToOneField(ProofOfPayment,on_delete=models.DO_NOTHING,default=1)
    activation_date = models.DateTimeField(default=timezone.now)
    expiration_date = models.DateTimeField(default=get_expiration_time)
    is_active = models.BooleanField(default=False,choices=STATES)
    amount=models.FloatField(default=0.00)

    @property
    def user(self):
        return self.pop.user
    
    @property
    def investment_plan(self):
        return self.pop.investment_plan

    def __str__(self):
        return self.pop.user.__str__()


class Payment(models.Model):

    CHOICES=(
        (1,"Paid"),
        (2,"Unpaid"),
        (3,"Pending")
        )
    investment=models.ForeignKey(Investment,on_delete=models.DO_NOTHING)
    date=models.DateField(default=timezone.now)
    amount=models.FloatField()
    status=models.IntegerField(default=2,choices=CHOICES)

    @property
    def bank_account_name(self):
        return self.investment.pop.user.bank_account_name

    @property
    def bank_account_number(self):
        return self.investment.pop.user.bank_account_number

    @property
    def bank_name(self):
        return self.investment.pop.user.bank_name
    
    @property
    def user(self):
        return self.investment.pop.user

class Notification(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    text=models.TextField()
    heading=models.CharField(max_length=250)
    datetime=models.DateTimeField(default=timezone.now)
    is_read=models.BooleanField(default=False)

class Referral(models.Model):
    referrer=models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name="my_referrals")
    referred=models.ForeignKey(User,on_delete=models.DO_NOTHING, related_name="my_referrers")

    def __str__(self):
        return "Referrer - {}".format(self.referrer.email)

class ReferralPayment(models.Model):

    CHOICES=(
        (1,"Paid"),
        (2,"Unpaid"),
        (3,"Pending")
        )

    referral=models.ForeignKey(Referral,on_delete=models.DO_NOTHING)
    amount=models.FloatField(default=0.0)
    status=models.IntegerField(choices=CHOICES, default=2)
    date=models.DateField(default=timezone.now)

    @property
    def bank_account_name(self):
        return self.referral.referrer.bank_account_name

    @property
    def bank_account_number(self):
        return self.referral.referrer.bank_account_number

    @property
    def bank_name(self):
        return self.referral.referrer.bank_name
    
    @property
    def user(self):
        return self.referral.referrer