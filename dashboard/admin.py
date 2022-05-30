import datetime
from django.utils import timezone
from django.contrib import admin, messages
from django.utils.translation import ngettext
from .models import User, ProofOfPayment,Investment,Payment,Referral,ReferralPayment
from .views import create_notification

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display=['first_name','last_name','email']
    list_display_links = ['first_name','last_name','email',]

class ProofOfPaymentAdmin(admin.ModelAdmin):

    def validate_proof_of_payment(self,request,queryset):
        try:
            updated = queryset.update(is_valid=3)
        except:
            self.message_user(request=request,message=ngettext(
                'We experienced an error while trying to validate %d selected proof of payment',
                'We experienced an error while trying to validate %d selected proof of payments',
                updated
            ) % updated,level=messages.ERROR)
        else:
            self.message_user(request,message=ngettext(
                '%d proof of payment was successfully validated',
                '%d proof of payments were successfully validated',
                updated
            ) % updated, level=messages.SUCCESS)

            for query in queryset:
                months=query.investment_plan.investment_duration
        
                if months == 12:
                    ex_date=timezone.now() + datetime.timedelta(days=365)
                else:
                    ex_date=timezone.now() + datetime.timedelta(days=(months*30)+3)

                amount= round((query.investment_plan.roi/100)*query.amount)
                Investment.objects.create(pop=query,is_active=True,amount=amount,expiration_date=ex_date)

                try:
                    referral=Referral.objects.get(referred=query.user)
                except:
                    pass
                else:
                    try:
                        investments=Investment.objects.filter(pop__user=query.user)
                        if len(investments) == 1:
                            investment=investments[0]
                            amount=round(investment.pop.amount*0.04)
                            ReferralPayment.objects.create(referral=referral,amount=amount)
                    except:
                        raise # for testing, change to pass or continue during development
                    else:
                        self.message_user(request,message="A Referral Payment has been created for a user who referred another user. Check the Referral Payment page to make the appriopriate payments.")

                        user=referral.referrer
                        heading="Referral Program reward"
                        text="You are due to receive a payment of {} within 5 working days as a reward for referring us to a user who has invested with us".format(amount)
                        mail_text="Hello {} {}, You are due to receive a payment of {} within 5 working days as an award for referring us to a user who has invested with us.\n Keep up referring us to other users for investments to keep getting rewards like this.".format(referral.referred.first_name, referral.referred.last_name, amount)

                        create_notification(user,heading,text,mail_text=mail_text)

                user=query.user
                heading="Investment with SeQuenceFX confirmed"
                text="Your Upload of your proof of payment document has been confirmed. You're now eligible to receive a monthly roi based on the package chosen for the agreed time duration."
                mail_text="Hello {} {}, thank you for choosing us as your investment platform.\nYou're receiving this mail as a response to our confirmation of your payment of {} for the {} investment plan.\n We'd be in touch as it regards your bi-weekly payment of the agreed roi (according to your package choice).\n Thank you for choosing SeQuenceFX.".format(user.first_name,user.last_name,query.amount,query.investment_plan.name)

                create_notification(user,heading,text,mail_text=mail_text)


    validate_proof_of_payment.short_description = "Validate selected POP(s)"

    def invalidate_proof_of_payment(self,request,queryset):
        try:
            updated = queryset.update(is_valid=2)
        except:
            self.message_user(request=request,message=ngettext(
                'We experienced an error while trying to invalidate %d selected proof of payment',
                'We experienced an error while trying to invalidate %d selected proof of payments',
                updated
            ) % updated,level=messages.ERROR)
        else:
            self.message_user(request,message=ngettext(
                '%d proof of payment was successfully invalidated',
                '%d proof of payments were successfully invalidated',
                updated
            ) % updated, level=messages.SUCCESS)
    invalidate_proof_of_payment.short_description = "Invalidate selected POP(s)"

    list_display=["user",'investment_plan','amount','is_valid','file','date']
    list_display_links=['user','amount','is_valid','file']
    actions=['validate_proof_of_payment','invalidate_proof_of_payment']
    list_filter=['is_valid']

class InvestmentAdmin(admin.ModelAdmin):

    list_display=['user','investment_plan','activation_date','expiration_date','is_active']

class PaymentAdmin(admin.ModelAdmin):

    def register_payment(self,request,queryset):
        try:
            updated = queryset.update(status=1)
        except:
            self.message_user(request=request,message=ngettext(
                'We experienced an error while trying to register %d selected payment',
                'We experienced an error while trying to register %d selected payments',
                updated
            ) % updated,level=messages.ERROR)
        else:
            self.message_user(request,message=ngettext(
                '%d payment was successfully registered',
                '%d payments were successfully registered',
                updated
            ) % updated, level=messages.SUCCESS)

    register_payment.short_description = "Register selected payment(s)"

    def register_payment_as_pending(self,request,queryset):
        try:
            updated = queryset.update(status=3)
        except:
            self.message_user(request=request,message=ngettext(
                'We experienced an error while trying to register %d selected payment as pending',
                'We experienced an error while trying to register %d selected payments as pending',
                updated
            ) % updated,level=messages.ERROR)
        else:
            self.message_user(request,message=ngettext(
                '%d payment was successfully registered as pending',
                '%d payments were successfully registered as pending',
                updated
            ) % updated, level=messages.SUCCESS)

    register_payment_as_pending.short_description = "Register selected payment(s) as pending"

    list_display=['user','bank_account_number','bank_name','bank_account_name','amount','status']
    actions=['register_payment','register_payment_as_pending']
    list_filter=['status']

class ReferralPaymentAdmin(admin.ModelAdmin):

    def register_payment(self,request,queryset):
        try:
            updated = queryset.update(status=1)
        except:
            self.message_user(request=request,message=ngettext(
                'We experienced an error while trying to register %d selected payment',
                'We experienced an error while trying to register %d selected payments',
                updated
            ) % updated,level=messages.ERROR)
        else:
            self.message_user(request,message=ngettext(
                '%d payment was successfully registered',
                '%d payments were successfully registered',
                updated
            ) % updated, level=messages.SUCCESS)

    register_payment.short_description = "Register selected payment(s)"

    def register_payment_as_pending(self,request,queryset):
        try:
            updated = queryset.update(status=3)
        except:
            self.message_user(request=request,message=ngettext(
                'We experienced an error while trying to register %d selected payment as pending',
                'We experienced an error while trying to register %d selected payments as pending',
                updated
            ) % updated,level=messages.ERROR)
        else:
            self.message_user(request,message=ngettext(
                '%d payment was successfully registered as pending',
                '%d payments were successfully registered as pending',
                updated
            ) % updated, level=messages.SUCCESS)

    register_payment_as_pending.short_description = "Register selected payment(s) as pending"

    list_display=['user','bank_account_number','bank_name','bank_account_name','amount','status']
    actions=['register_payment','register_payment_as_pending']
    list_filter=['status']


admin.site.register(User,UserAdmin)
admin.site.register(ProofOfPayment,ProofOfPaymentAdmin)
admin.site.register(Investment,InvestmentAdmin)
admin.site.register(Payment,PaymentAdmin)
admin.site.register(ReferralPayment,ReferralPaymentAdmin)
 