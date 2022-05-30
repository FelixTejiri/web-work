from django.urls import path
from . import views

app_name = 'dashboard'
urlpatterns = [
    path("",views.index,name="index"),
    path("logout/",views.logout,name="logout"),
    path("account-info",views.account_info,name="account-info"),
    path("investment-plans",views.investment_plans,name="investment-plans"),
    path("upload-pop",views.upload_pop,name="upload-pop"),
    path("active-investments",views.active_investments,name="active-investments"),
    path("pending-investments",views.pending_investments,name="pending-investments"),
    path("payment-history",views.payment_history,name="payment-history"),
    path("notifications",views.notifications,name="notifications"),
    path("deposit",views.deposit,name="deposit"),
    path("referral-program",views.referral_program,name="referral-program"),
    path("referral-payments",views.referral_payments,name="referral-payments")
]