
from django.urls import path, include, re_path
from KidsStepShop import views
from django.views.generic import RedirectView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_views
from KidsStepShop.forms import ResetPasswordForm
from django.conf.urls import url
from django.views.generic import RedirectView


urlpatterns = [
    path('', views.index, name='index'),
    re_path('basket', views.basket, name='basket'),
    path('order', views.order, name='order'),
    path('search', views.search, name='search'),
    path('order_done/<article>', views.order_done, name='order_done'),
    path('db_hendler', views.db_hendler, name='db_hendler'),

    re_path('managment', views.managment, name='managment'),

    path('registration/registration', views.signup, name='signup'),
    path('registration/sign_in', views.loginUser, name='sign_in'),
    path('registration/logout', views.logoutUser, name='logout'),
    path('registration/password_reset',
         auth_views.PasswordResetView.as_view(form_class=ResetPasswordForm), name='password_reset'),

    path('registration/password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('registration/reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('registration/reset/done/',
         auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('accounts/profile', views.profile, name='profile'),
    path('<id_gender>/', views.type, name='type'),
    path('<id_gender>/<id_type>', views.footwear, name='footwear'),
    path('<id_gender>/<id_type>/<id>', views.footwear_detail, name='footwear_detail'),

]
