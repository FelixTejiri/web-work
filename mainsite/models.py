from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class MainUser(AbstractUser):
    
    class Meta:
        verbose_name = "Main User"
        verbose_name_plural = "Main Users"

class InvestmentPlan(models.Model): 
 
    DAY_CHOICES=(
        (1,'First day'),
        (2,'Second day'),
        (3,'Third day'),
        (4,'Fourth day'),
        (5,'Fifth day'),
        (6,'Sixth day'),
        (7,'Seventh day'),
        (8,'Eight day'),
        (9,'Ninth day'),
        (10,'Tenth day'),
        (11,'Eleventh day'),
        (12,'Twelfth day'),
        (13,'Thirteenth day'),
        (14,'Fourteenth day'),
        (15,'Fifteenth day'),
        (16,'Sixteenth day'),
        (17,'Seventeenth day'),
        (18,'Eighteenth day'),
        (19,'Nineteenth day'),
        (20,'Twenteeth day'),
        (21,'Twenty-first day'),
        (22,'Twenty-second day'),
        (23,'Twenty-third day'),
        (24,'Twenty-fourth day'),
        (25,'Twenty-fifth day'),
        (26,'Twenty-sixth day'),
        (27,'Twenty-seventh day'),
        (28,'Twenty-eight day'),
        (29,'Twenty-ninth day'),
        (30,'Thirtieth day'),
        (31,'Thirty-first day'),
    )

    name = models.CharField(max_length=100)
    description = models.TextField(help_text="description of plan with all needed detials including duration and anything the client needs to know about the plan")
    roi = models.IntegerField(help_text="Return of investment in percentage")
    # first_payment_day=models.IntegerField(null=True,help_text="Day in the month for the first payment",choices=DAY_CHOICES,blank=True)
    # second_payment_date=models.IntegerField(null=True,help_text="Day in the month for the second payment",choices=DAY_CHOICES,blank=True)
    investment_duration=models.IntegerField(default=12,help_text="Duration of Investment in months")

    def __str__(self):
        return self.name

class VerificationLink(models.Model):
    user=models.OneToOneField("dashboard.User",on_delete=models.DO_NOTHING)
    key=models.CharField(max_length=100)
    is_account_valid=models.BooleanField(default=False)

    def __str__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)

class SiteSetting(models.Model):
    info=models.TextField()
    about=models.TextField()
    
class TeamMember(models.Model):
    name=models.CharField(max_length=30)
    position=models.CharField(max_length=30)
    description=models.CharField(max_length=100)
    image=models.ImageField(upload_to="images/team-members/")

    def __str__(self):
        return name

class UserMessage(models.Model):
    subject=models.CharField(max_length=50, help_text="Subject of the message")
    body=models.TextField(help_text="Body of the message")
    should_publish=models.BooleanField(default=True)

    def __str__(self):
        return self.subject


