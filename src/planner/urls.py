from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from .views import (LoginView, SignUpView, LogoutView, HomeView, DinnerPlanView, DinnerPlanUpdateView,
                   AjaxTodoView, AjaxTodoUpdateView, AjaxTodoInfoView, AjaxTodoDeleteView, AjaxWeatherView, 
                   ContactView, AccountView, AccountUpdateView)


urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('register/', SignUpView.as_view(), name='signup'),
    path('home/', HomeView.as_view(), name='home'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('create/', DinnerPlanView.as_view(), name='enter_plan'),
    path('create/<int:pk>/update', DinnerPlanUpdateView.as_view(), name='plan_update'),
    path('account/', AccountView.as_view(), name='account'),
    path('account/<int:pk>/update', AccountUpdateView.as_view(), name='account_update'),
    path('todo/', AjaxTodoView.as_view(), name='todo'),
    path('todo/<int:pk>/update', AjaxTodoUpdateView.as_view(), name='todo_update'),
    path('todo/<int:pk>/info', AjaxTodoInfoView.as_view(), name='todo_info'),
    path('todo/<int:pk>/delete', AjaxTodoDeleteView.as_view(), name='todo_delete'),
    path('weather/', AjaxWeatherView.as_view(), name='weather'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset_form.html'), 
        name='password_reset'),
    path('password-reset/done', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), 
        name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), 
        name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), 
        name='password_reset_complete'),
]
