import random
import string
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect,HttpRequest,HttpResponse
from django.urls import reverse
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.core.mail import send_mail
from dashboard.models import User, Referral
from .models import VerificationLink
from .forms import RegisterForm,LoginForm,ContactForm

# Create your views here.

def get_random_string(length):
    # Random string with the combination of lower and upper case
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def index(request):
    context={
        'slug':'index'
    }
    return render(request,"mainsite/index.html",context)

def register(request):
    register_form=RegisterForm()
    if request.method == 'POST':
        register_form=RegisterForm(request.POST)

        if register_form.is_valid():
            confirm_pass,pass_len=register_form.verify_passwords()

            if confirm_pass and pass_len:

                if register_form.email_check():
                    user=register_form.save()

                    try:
                        referrer=User.objects.get(pk=register_form.cleaned_data.get("referrer"))
                    except:
                        pass
                    else:
                        Referral.objects.create(referrer=referrer,referred=user)
                        
                    key=get_random_string(15)
                    VerificationLink.objects.create(user=user,key=make_password(key))

                    subject="Confirm Account Registration on SeQuenceFXinvest.com"

                    # msg_plain = render_to_string('mainsite/welcome-email.txt', {
                    #     'first_name': form.cleaned_data.get("first_name"),
                    #     'second_name': form.cleaned_data.get("last_name"),
                    #     'key': form.cleaned_data.get("key")
                    # })
                    msg_html = render_to_string('mainsite/welcome-email.html', {
                        'first_name': form.cleaned_data.get("first_name"),
                        'second_name': form.cleaned_data.get("last_name"),
                        'key': form.cleaned_data.get("key")
                    })

                    message="Hello {} {}, we're happy to have you on our platform. You're receiving this mail as a response to your registration on our site. However, there remains a final step of registration. We want you to kindly verify your account by clicking on the link below. That's it, all done! \n <a href='https://sequencefxinvest.com/verify?key={}'>Verify Account</a>".format(register_form.cleaned_data.get('first_name'),register_form.cleaned_data.get('last_name'),key)

                    # send_mail(
                    #     subject,
                    #     message,
                    #     'contact@sequencefxinvest.com',
                    #     [register_form.cleaned_data.get('email')],
                    #     fail_silently=False,
                    # )

                    send_mail(
                        subject,
                        message,
                        'contact@sequencefxinvest.com',
                        [register_form.cleaned_data.get('email')],
                        htlm_message=msg_html,
                        fail_silently=False,
                    )

                    info="You've been successfully registered, we just sent an email with a verifcation link, once you verify your account by clicking on the link, you'd be good to go!"
                    messages.success(request,info)
                    return HttpResponseRedirect(reverse('mainsite:info'))

                else:
                    register_form._errors['email']=register_form.error_messages['email_in_use'] 
                    
            else:
                if confirm_pass is False:
                    register_form._errors['password2']=register_form.error_messages['password_mismatch'],
                if pass_len is False:
                    register_form.errors['password']=register_form.error_messages['invalid_length']
    
    try:
        ref_id=request.GET['ref']
    except KeyError:
        context={
            'form':register_form,
            'slug':'register',
        }
    else:
        context={
            'ref_id':ref_id,
            'form':register_form,
            'slug':'register'
        }

    return render(request,"mainsite/register.html",context)

def login(request):
    login_form=LoginForm()
    if request.method == 'POST':
        login_form=LoginForm(request.POST)
        if login_form.is_valid():
            user=login_form.verify_login()
            if user:
                if user.is_verified:
                    request.session['user_id']=user.id
                    return HttpResponseRedirect(reverse('dashboard:index'))
                else:
                    messages.error(request,login_form.error_messages['unverified_user'])
                    return HttpResponseRedirect(reverse('mainsite:info'))
            else:
                login_form._errors['email']=login_form.error_messages['invalid_user']
        else:
            login_form._errors['email']=login_form.error_messages['invalid_user']

    return render(request,"mainsite/login.html",{'form':login_form,'slug':'login'})

def about_us(request):
    return render(request,"mainsite/about-us.html",{'slug':'about-us'})

def faqs(request):
    return render(request,"mainsite/faqs.html",{'slug':'faqs'})

def plans(request):
    return render(request,"mainsite/plans.html")

def verify_account(request):
    try:
        id=request.GET['id']
        key=request.GET["key"]

    except KeyError:
        error="This is an invalid verification link"
        request.session["error"]=error
        return HttpResponseRedirect(reverse("mainsite:error"))

    else:
        try:
            user = User.objects.get(pk=id)

        except User.DoesNotExist:
            error="This is an invalid verification link"
            request.session["error"]=error
            return HttpResponseRedirect(reverse("mainsite:error"))

        else:
            try:
                link=VerificationLink.objects.get(user=user,is_account_valid=False)
                if check_password(key,link.key):
                    pass
                else:
                    error="This is an invalid verification link"
                    request.session=error
                    return HttpResponseRedirect(reverse("mainsite:error"))

            except VerificationLink.DoesNotExist:
                error="This is an invalid verification link"
                request.session["error"]=error
                return HttpResponseRedirect(reverse("mainsite:error"))

            else:
                if user.is_verified == False:
                    user.is_verified == True
                    user.save()
                    link.is_account_valid=True
                    link.save()
                    info="Account Verification successfull, please proceed to login page"
                    request.session["info"]=info
                    return HttpResponseRedirect("mainsite:info")
                else:
                    error="This is an invalid verification link, user is already verified"
                    request.session["error"]=error
                    return HttpResponseRedirect(reverse("mainsite:error"))

def error(request):
    try:
        error=request.session["error"]
    except KeyError:
        error="You ran into an error hence this error page."
    else:
        pass
    return render(request,"mainsite/error.html",{"error":error})    

def info(request):
    try:
        info=request.session["info"]
    except KeyError:
        info="We are not so sure of what information we should be giving you now, how about you check back on the page that brought you here?"
    else:
        pass
    return render(request,"mainsite/info.html",{"info":info})  

def contact(request):
    if request.method == 'POST':
        contact_form=ContactForm(request.POST)
        if contact_form.is_valid():
            message = "{} \n{}".format(contact_form.cleaned_data.get("subject"),contact_form.cleaned_data.get("message"))
            send_mail(
                "Contact Form message from SeQuenceFXInvest.com",
                message,
                'SeQuenceFX@sequencefxinvest.com',
                contact_form.cleaned_data.get("email"),
                fail_silently=True,
            )
        else:
            pass
    else:
        return HttpResponseRedirect(reverse('mainsite:index'))
    return HttpResponse("success")


def academy(request):
    return render(request,"mainsite/academy.html",{'slug':'academy'})

def verify(requset):
    try:
        key=request.GET['key']
    except KeyError:
        messages.error(request,"Invalid Link")
        return HttpResponseRedirect(reverse('mainsite:error'))
    else:
        try:
            link=VerificationLink.objects.get(key=key)
        except VerificationLink.DoesNotExist:
            messages.error(request,"Invalid Link")
            return HttpResponseRedirect(reverse('mainsite:error'))
        else:
            if link.user.is_verified == True:
                messages.error(request,"Invalid Link")
                return HttpResponseRedirect(reverse('mainsite:error'))
            else:
                link.user.is_verified=True
                link.user.save()
                link.is_account_valid=True
                link.save()
                messages.success(request,"Verification Successfull! Please proceed to the login page and begin investing with us.")  
                return HttpResponseRedirect(reverse('mainsite:info'))
