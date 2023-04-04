from django.urls import path, include

from . import views


urlpatterns = [
    path('registration/', views.RegistrationView.as_view()),
    path('activate/<str:email>/<str:activation_code>/', views.ActivationView.as_view(), name='activate'),
    path('login/', views.LoginView.as_view()),
    path('change_password/', views.ChangePasswordView.as_view()),
    path('forgot_password/', views.ForgotPasswordView.as_view()),
    path('forgot_password_complete/',views.ForgotPasswordCompleteView.as_view()),
    path('accounts/google/login/', views.GoogleLogin.as_view(), name='google_login'),
    path('accounts/logout/', views.GoogleLogout.as_view(), name='logout'),

]