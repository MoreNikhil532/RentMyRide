from django.urls import path
from home import views
urlpatterns = [
    path("", views.action,name="action"),
    path("home/", views.home,name="home"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.loginPage, name="login"),
    path("TnC/", views.TnC,name="TnC"),
    path("logout/", views.logoutPage,name="logout"),
    path("register/", views.register,name="register"),
    path("dashboard/", views.dashboard,name="dashboard"),
    path("changePassword/", views.changePassword,name="changePassword"),
    path('delete_account/', views.delete_account, name='delete_account'),

]