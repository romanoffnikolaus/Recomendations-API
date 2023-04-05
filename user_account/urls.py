from django.urls import path

from . import views


urlpatterns = [
    path('registration/', views.RegistrationView.as_view()),
    path('activate/<str:email>/<str:activation_code>/', views.ActivationView.as_view(), name='activate'),
    path('change_password/', views.ChangePasswordView.as_view()),
    path('forgot_password/', views.ForgotPasswordView.as_view()),
    path('forgot_password_complete/',views.ForgotPasswordCompleteView.as_view()),
    path('login/', views.LoginDefaultView.as_view(), name='login')

]