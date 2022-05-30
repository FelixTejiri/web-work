from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from .models import User,Investment,ProofOfPayment,Payment,Notification,ReferralPayment,Notification
from mainsite.models import InvestmentPlan
from .forms import(
    UserInformationChangeForm,
    PasswordChangeForm,
    UploadForm,
    BankForm
)
from django.contrib import messages

# View functions

def create_notification(user,heading,text,mail_text=None,should_mail=True):

    if mail_text==None:
        mail_text=text
    if should_mail:
        send_mail(
            heading, 
            text,
            'SeQuenceFX@sequencefxinvest.com',
            [user.email],
            fail_silently=True,
        )
    return Notification.objects.create(user=user,heading=heading,text=text)



# Create your views here.

def index(request):
    try:
        user_id = request.session['user_id']
    
    except KeyError:
        return HttpResponseRedirect(reverse("mainsite:login"))

    else:
        try:
            user = User.objects.get(pk=user_id)

        except User.DoesNotExist:
            return HttpResponseRedirect(reverse("mainsite:login"))

        else:
            active_investments=len(Investment.objects.filter(pop__user=user,is_active=True))
            a_investments=Investment.objects.filter(pop__user=user,is_active=True)[:5]
            pending_investments=len(ProofOfPayment.objects.filter(user=user,is_valid=1))
            p_investments=ProofOfPayment.objects.filter(user=user,is_valid=1)[:5]
            total_payments=len(Payment.objects.filter(investment__pop__user=user))
            payments=Payment.objects.filter(investment__pop__user=user)[:5]
            context = {
                "user":user,
                "page_name":'Dashboard Overview',
                'slug':'index',
                'active_investments':active_investments,
                'pending_investments':pending_investments,
                'total_payments':total_payments,
                'a_investments':a_investments,
                'p_investments':p_investments,
                'payments':payments
                }
            return render(request,"dashboard/index.html",context)
    return render(request,"dashboard/index.html")


def logout(request):
    try:
        del request.session['user_id']
    except KeyError:
        pass
    else:
        pass
    return HttpResponseRedirect(reverse("mainsite:login"))

def account_info(request):
    try:
        uid=request.session['user_id']

    except KeyError:
        return HttpResponseRedirect(reverse('mainsite:login'))

    else:

        try:
            user=User.objects.get(pk=uid)

        except User.DoesNotExist:
            return HttpResponseRedirect(reverse('mainsite:login'))

        else: 

            change_form=UserInformationChangeForm(instance=user)
            bank_form=BankForm(instance=user)
            password_change_form=PasswordChangeForm()
            context={
                'form':change_form,
                'bank_form':bank_form,
                'pass_form':password_change_form,
                'page_name': 'User Account Information',
                'user':user,
                'slug':'account-info'
            }
            
            if request.method == "POST":
                try:
                    type=request.GET['type']

                except KeyError:
                    return HttpResponseRedirect(reverse('dashboard:account-info'))

                else:

                    if type == 'change-account-info':
                        change_form=UserInformationChangeForm(request.POST)

                        if change_form.is_valid():
                            user.first_name=change_form.cleaned_data.get('first_name')
                            user.last_name=change_form.cleaned_data.get('last_name')
                            user.phone_number=change_form.cleaned_data.get('phone_number')
                            user.save(force_update=True)

                            messages.success(request,"User information successfully updated")
                            context['form']=UserInformationChangeForm(instance=user)
                            return HttpResponseRedirect(reverse('dashboard:account-info'))

                        else:
                            messages.error(request,change_form.error_messages['invalid_input'])
                            return HttpResponseRedirect(reverse('dashboard:account-info'))
                    
                    elif type == 'change-pass':
                        pass_form=PasswordChangeForm(request.POST)

                        if pass_form.is_valid():
                            opass=pass_form.cleaned_data.get('old_password')
                            cpass=pass_form.cleaned_data.get('confirm_password')

                            if check_password(opass,user.password):
                                confirm_pass,pass_len=pass_form.verify_passwords()

                                if confirm_pass and pass_len:
                                    user.password=make_password(cpass)
                                    user.save(force_update=True)
                                    messages.success(request,'Account password changed successfully!')

                                else:
                                    if confirm_pass is False:
                                        messages.error(request,pass_form.error_messages['password_mismatch'])
                                    if pass_len is False:
                                        messages.error(request,pass_form.error_messages['invalid_length'])
                                    return HttpResponseRedirect(reverse('dashboard:account-info'))

                            else:
                                messages.error(request,pass_form.error_messages['wrong_password'])
                                return HttpResponseRedirect(reverse('dashboard:account-info'))

                        else:
                            messages.error(request,pass_form.error_messages['invalid_input'])
                            return HttpResponseRedirect(reverse('dashboard:account-info'))

                    elif type == 'bank-details':
                        change_form=BankForm(request.POST)

                        if change_form.is_valid():
                            user.bank_name=change_form.cleaned_data.get('bank_name')
                            user.bank_account_number=change_form.cleaned_data.get('bank_account_number')
                            user.bank_account_name=change_form.cleaned_data.get('bank_account_name')
                            user.save(force_update=True)
                            messages.success(request,"Bank Details Updated.")
                            return HttpResponseRedirect(reverse('dashboard:account-info'))

                        else:
                            messages.error(request,change_form.error_messages['invalid_input'])
                            return HttpResponseRedirect(reverse('dashboard:account-info'))

    change_form=UserInformationChangeForm(instance=user)
    bank_form=BankForm(instance=user)
    password_change_form=PasswordChangeForm()

    return render(request,"dashboard/account-info.html",context)

def investment_plans(request):

    try:
        uid=request.session['user_id']

    except KeyError:
        return HttpResponseRedirect(reverse('mainsite:login'))

    else:
        try:
            user=User.objects.get(pk=uid)

        except User.DoesNotExist:
            return HttpResponseRedirect(reverse('mainsite:login'))

        else:
            investment_plans=InvestmentPlan.objects.all()
            context={
                'slug':'investment-plans',
                'user':user,
                'page_name':'Investment Plans',
                'investment_plans':investment_plans
            }
    return render(request,"dashboard/investment-plans.html",context)

def upload_pop(request):

    try:
        uid=request.session['user_id']

    except KeyError:
        return HttpResponseRedirect(reverse('mainsite:login'))

    else:
        try:
            user=User.objects.get(pk=uid)

        except User.DoesNotExist:
            return HttpResponseRedirect(reverse('mainsite:login'))

        else:
            if request.method == 'POST':
                upload_pop=UploadForm(request.POST,request.FILES)

                if upload_pop.is_valid():
                    pop=upload_pop.save()
                    pop.user=user
                    pop.save()
                    messages.success(request,"Upload Successfull, our personell will evaluate your payment and confirm it ASAP! You'd receive an email upon confirmation or otherwise shortly")
                else:
                    messages.error(request,upload_pop.errors)
                    return HttpResponseRedirect(reverse('dashboard:upload-pop'))
            
            upload_form=UploadForm()
            context={
                'form':upload_form,
                'page_name':"Upload Proof of Payment",
                'user':user,
                'slug':'upload-pop'
            }

    return render(request,"dashboard/upload-pop.html",context)

def notifications(request):
    try:
        uid=request.session['user_id']

    except KeyError:
        return HttpResponseRedirect(reverse('mainsite:login'))

    else:
        try:
            user=User.objects.get(pk=uid)

        except User.DoesNotExist:
            return HttpResponseRedirect(reverse('mainsite:login'))

        else:

            notifications=Notification.objects.filter(user=user).order_by('-datetime')

            notifications.update(is_read=True)

            context={
                'page_name':'Notifications',
                'user':user,
                'slug':'notifications',
                'notifications':notifications
            }
    return render(request,"dashboard/notifications.html",context)

def active_investments(request):

    try:
        user_id = request.session['user_id']
    
    except KeyError:
        return HttpResponseRedirect(reverse("mainsite:login"))

    else:
        try:
            user = User.objects.get(pk=user_id)

        except User.DoesNotExist:
            return HttpResponseRedirect(reverse("mainsite:login"))
        
        else:

            investments=Investment.objects.filter(pop__user=user,is_active=True)
            context={
                'page_name':'Active Investments',
                'slug':'active-investments',
                'investments':investments,
                'user':user
            }
            return render(request,"dashboard/active-investments.html",context)

def pending_investments(request):
    try:
        user_id = request.session['user_id']
    
    except KeyError:
        return HttpResponseRedirect(reverse("mainsite:login"))

    else:
        try:
            user = User.objects.get(pk=user_id)

        except User.DoesNotExist:
            return HttpResponseRedirect(reverse("mainsite:login"))
        
        else:

            investments=ProofOfPayment.objects.filter(user=user,is_valid=1)
            context={
                'page_name':'Pending Investments',
                'slug':'pending-investments',
                'investments':investments,
                'user':user
            }
    return render(request,"dashboard/pending-investments.html",context)

def payment_history(request):
    try:
        user_id = request.session['user_id']
    
    except KeyError:
        return HttpResponseRedirect(reverse("mainsite:login"))

    else:
        try:
            user = User.objects.get(pk=user_id)

        except User.DoesNotExist:
            return HttpResponseRedirect(reverse("mainsite:login"))
        
        else:

            payments=Payment.objects.filter(investment__pop__user=user)
            context={
                'page_name':'Payment History',
                'slug':'payment-history',
                'payments':payments,
                'user':user
            }
    return render(request,"dashboard/payment-history.html",context)

def deposit(request):

    try:
        user_id = request.session['user_id']
    
    except KeyError:
        return HttpResponseRedirect(reverse("mainsite:login"))

    else:
        try:
            user = User.objects.get(pk=user_id)

        except User.DoesNotExist:
            return HttpResponseRedirect(reverse("mainsite:login"))
        
        else:
            pass

    context={
                'page_name':'Make Deposit',
                'slug':'make-deposit',
                'user':user
            }
    return render(request,"dashboard/deposit.html",context)

def referral_program(request):

    try:
        user_id = request.session['user_id']
    
    except KeyError:
        return HttpResponseRedirect(reverse("mainsite:login"))

    else:
        try:
            user = User.objects.get(pk=user_id)

        except User.DoesNotExist:
            return HttpResponseRedirect(reverse("mainsite:login"))
        
        else:
            pass

    context={
                'page_name':'Our Referral Program',
                'slug':'referral-program',
                'user':user
            }
    return render(request,"dashboard/referral-program.html",context)

def referral_payments(request):

    try:
        user_id = request.session['user_id']
    
    except KeyError:
        return HttpResponseRedirect(reverse("mainsite:login"))

    else:
        try:
            user = User.objects.get(pk=user_id)

        except User.DoesNotExist:
            return HttpResponseRedirect(reverse("mainsite:login"))
        
        else:
            payments=ReferralPayment.objects.filter(referral__referrer=user)

    context={
                'page_name':'Your Referral Payments',
                'slug':'referral-payments',
                'user':user,
                'payments':payments
            }
    return render(request,"dashboard/referral-payments.html",context)

