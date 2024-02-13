from random import randint

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView
from django.contrib.sites.shortcuts import get_current_site

from django.core.mail import send_mail
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.utils.crypto import get_random_string
from django.views import View
from django.views.generic import CreateView, UpdateView

from users.forms import UserRegisterForm, UserForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        new_user = form.save()
        token = get_random_string(length=50)
        new_user.verification_token = token
        new_user.save()
        current_site = get_current_site(self.request)
        mail_subject = 'Подтвердите ваш аккаунт'
        message = (
            f'Поздравляем, Вы зарегистрировались на нашем портале!\n'
            f'Для завершения регистрации и подтверждения вашей электронной почты, '
            f'пожалуйста, кликните по следующей ссылке:\n'
            f'http://{current_site.domain}{reverse("users:verify_email", kwargs={"uid": new_user.pk, "token": token})}'
        )
        send_mail(
            subject=mail_subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email]
        )
        return response


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('catalog:index')


class VerifyEmailView(View):
    def get(self, request, uid, token):
        try:
            user = get_object_or_404(User, pk=uid, verification_token=token)
            user.is_active = True
            user.save()
            return render(request,
                          'users/registration_success.html')
        except User.DoesNotExist:
            return render(request, 'users/registration_failed.html')


class CustomPasswordResetView(PasswordResetView):
    template_name = 'users/password_reset.html'

    def form_valid(self, form):
        new_password = ''.join([str(randint(0, 9)) for _ in range(12)])
        email = form.cleaned_data['email']
        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()

        send_mail(
            subject='Восстановление пароля',
            message=f'Ваш новый пароль: {new_password}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return redirect('users:login')
