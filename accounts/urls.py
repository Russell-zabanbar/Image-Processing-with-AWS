# urls.py
from django.urls import path
from accounts.views import AuthView, UserRegisterVerifyCodeView, LogoutView
app_name = 'auth'

urlpatterns = [
    path('login/', AuthView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('verify_code/', UserRegisterVerifyCodeView.as_view(), name='verify_code')
]