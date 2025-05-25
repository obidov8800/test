from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from tests.views import home, test, register, profile  # Barcha kerakli funksiyalarni import qilish

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('test/<int:subject_id>/', test, name='test'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/register/', register, name='register'),
    path('profile/', profile, name='profile'),

]