from django.urls import path
from .api import views

urlpatterns = [
    path('login', views.LoginView.as_view(), name='get-login-token'),
    path('refresh/token', views.RefreshTokenView.as_view(), name='refresh-token'),
    path('register', views.RegisterAPI.as_view(), name='register-user-api'),
    path('send/code', views.SendCodeAPI.as_view(), name='send-code-api'),
    path('verify/code', views.VerifyCodeAPI.as_view(), name='verify-code-api'),
    path('reset-password', views.ResetPasswordAPI.as_view(), name='reset-password-api'),
    path('profile', views.UserAPI.as_view(), name='user profile'),
    path('type/', views.UserTypeView.as_view(), name='system types'),
    path('file', views.UserImageView.as_view(), name='users file'),
    # project api
    path('project/', views.ProjectView.as_view(), name='project'),
    # project document api
    path('project/file/', views.ProjectDocumentView.as_view(), name='project file'),
]
