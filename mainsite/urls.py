from django.urls import path
from . import views

app_name = 'mainsite'
urlpatterns = [
    path('',views.index,name='index'),
    path('about-us/',views.about_us,name='about-us'),
    path("login/",views.login,name="login"),
    path("register/",views.register,name="register"),
    path("contact/",views.contact,name="contact"),
    path("academy/",views.academy,name="academy"),
    path("faqs/",views.faqs,name="faqs"),
    path("info/",views.info,name="info"),
    path("error/",views.error,name="error"),
    path("contact/",views.contact,name="contact"),
]