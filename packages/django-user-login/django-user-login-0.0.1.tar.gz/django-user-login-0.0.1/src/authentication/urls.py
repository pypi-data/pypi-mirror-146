from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view_js),
    path('logout/', views.logout_view, name='logout'),
    path('logoutJS/', views.logout_view_js, name="logoutJS"),

    path('register/', views.register),
    path('register/cancel/', views.cancelRegistration),
    path('register/resend/', views.resendVerificationCode),
    path('register/verify/', views.verifyRegistration),

    path('recover/', views.recover),
    path('recover/cancel/', views.cancelRecovery),
    path('recover/resend/', views.resendRecoveryCode),
    path('recover/verify/', views.verifyRecovery),
    path('recover/changepassword/', views.changepassword),
    
]
