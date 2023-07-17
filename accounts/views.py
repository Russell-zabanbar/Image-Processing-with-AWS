from django import views
from django.shortcuts import render, redirect
from accounts.forms import UserRegisterForm, VerifyCodeForm
import random
from django.contrib import messages
from accounts.models import OtpCode, CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout, authenticate
from django.core.exceptions import ObjectDoesNotExist

class AuthView(views.View):
    form_class = UserRegisterForm
    template_name = 'accounts/login.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            random_code = random.randint(1000, 9999)
            print(random_code)
            # send_otp_code(form.cleaned_data['phone'], random_code)
            OtpCode.objects.create(phone_number=form.cleaned_data['phone_number'], code=random_code)
            request.session['user_registration_info'] = {
                'phone_number': form.cleaned_data['phone_number'],
            }
            messages.success(request, 'we sent you a code', 'success')
            return redirect('auth:verify_code')
        return render(request, self.template_name, {'form': form})


class UserRegisterVerifyCodeView(views.View):
    form_class = VerifyCodeForm
    template_name = 'accounts/verify_code.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        phone_number = request.session['user_registration_info']['phone_number']

        code_instance = OtpCode.objects.get(phone_number=phone_number)
        form = self.form_class(request.POST)

        if form.is_valid():
            cd = form.cleaned_data

            if cd['code'] == code_instance.code:
                try:
                    user = CustomUser.objects.get(phone_number=phone_number)
                except ObjectDoesNotExist:
                    user = None
                if user is not None:
                    login(request, user)
                    messages.success(request, 'you are login', 'success')
                else:
                    CustomUser.objects.create_user(phone_number=phone_number)
                    messages.success(request, 'you registered.', 'success')

                code_instance.delete()
                return redirect('detect:order_list')
            else:
                messages.error(request, 'this code is wrong', 'danger')
                return redirect('auth:verify_code')
        return render(request, self.template_name, {'form': self.form_class})


class LogoutView(views.View):
    def get(self, request):
        logout(request)
        messages.success(request, 'you logged out successfully', 'success')
        return redirect('auth:login')
