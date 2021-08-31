
from django.contrib import admin

from django.urls import path, include, re_path
from KidsStepShop import views
from django.views.generic import RedirectView
from django.conf.urls.i18n import i18n_patterns
from django.contrib.auth import views as auth_views
from KidsStepShop.forms import ResetPasswordForm


urlpatterns = i18n_patterns(
    path('index/', views.index, name='index'),
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('search/', views.search, name='search'),
    path('db_handler', views.db_handler, name='db_handler'),
    path('basket', views.basket, name='basket'),
    path('order', views.order, name='order'),
    path('managment', views.managment, name='managment'),


    path('sign_in/', views.loginUser, name='sign_in'),
    path('logout/', views.logoutUser, name='logout'),
    path('registration', views.signup, name='signup'),
    path('password_reset/', auth_views.PasswordResetView.as_view(form_class=ResetPasswordForm), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('accounts/profile', views.profile, name='profile'),
    path('<id_gender>/', views.type, name='type'),
    path('<id_gender>/<id_type>', views.footwear, name='footwear'),
    path('<id_gender>/<id_type>/<id>', views.footwear_detail, name='footwear_detail'),



    # path(r'^chaining/', include('smart_selects.urls')),


)
