from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("account/", views.user_page, name="account"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("calender/", views.calender, name="calender"),
    path("admin/", views.admin, name="admin"),
    path("forum/", views.forum, name="forum"),
    path('<str:name>/', views.some_account, name='custom_template'),
]
