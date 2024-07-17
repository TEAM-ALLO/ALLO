from django.urls import path
from .views import home, signup_view, login_view, logout_view, mypage_view, profile_edit_view

app_name = "users_user"

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('mypage/', mypage_view, name='mypage'),
    path('profile/edit/', profile_edit_view, name='profile_edit'),
]