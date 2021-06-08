from django.urls import path, include
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name="Home"),
    path('accounts/complete_profile', views.complete_profile, name="complete_profile"),
    path('accounts/profile', views.profile, name="profile"),
    path('users/<str:uname>', views.view_profile, name="view_profile"),
    path('accounts/update_basic_info', views.update_basic_info, name="update_basic_info"),
    path('accounts/update_other_info', views.update_other_info, name="update_other_info"),
    path('accounts/check_username_availability', csrf_exempt(views.check_username_availability), name="check_username_availability"),
    path('accounts/upload_img', views.upload_img, name="upload_img"),
    path('accounts/remove_profile', views.remove_profile, name="remove_profile"),
    # path('login/', views.loginPage, name="loginPage"),
    # path('login/authenticate', views.loginUser, name="loginUser"),
    # path('logout', views.logoutUser, name="logoutUser"),
    # path('signup/', views.signUp, name="signUp"),
    # path('signupUser/', views.signupUser, name="signupUser"),   
    # path('account/', views.account, name="accountPage"),
    # path('account/forgot_password', views.forgotPassword, name="forgotPassword"),
    # path('account/forgot_password_successful', views.forgotPasswordSuccessful, name="forgotPasswordSuccessful"),
    # path('account/change_password', views.changePassword, name="changePassword"),
    # path('account/change_password_successful', views.changePasswordSuccessful, name="changePasswordSuccessful"),

]