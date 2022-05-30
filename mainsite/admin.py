from django.contrib import admin
from dashboard.models import User,ProofOfPayment
from .models import MainUser,InvestmentPlan,VerificationLink,UserMessage
from django.core.mail import send_mail
# Register your models here.
 
class InvestmentPlanAdmin(admin.ModelAdmin):
    list_display=['name','roi','investment_duration']

class UserMessageAdmin(admin.ModelAdmin):
    list_display=['subject','body']

    def save_model(self,request,obj,form,change):
        super().save_model(request,obj,form,change)
        if form.cleaned_data.get("should_publish") ==True:
            users=User.objects.all()
            for user in users:
                send_mail(
                    form.cleaned_data.get("subject"),
                    form.cleaned_data.get("body"),
                    'SeQuenceFX@sequencefxinvest.com',
                    [user.email],
                    fail_silently=True,
                )

admin.site.register(MainUser)
admin.site.register(InvestmentPlan,InvestmentPlanAdmin)
admin.site.register(VerificationLink)
admin.site.register(UserMessage,UserMessageAdmin) 
 