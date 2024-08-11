from django.urls import path
from . import views

app_name = "users_user"

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('mypage/', views.mypage_view, name='mypage'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    path('friend/<str:username>/', views.friend_list, name='friend_list'),
    path('friend/profile/<str:username>/', views.friend_profile_view, name='friend_profile'),
    path('friend/delete/<str:username>/', views.delete_friend, name='delete_friend'), 
    # path('change_pw/', views.change_pw, name='change_pw'),
    path('search/', views.search, name='search'),
    path('notifications/', views.notification, name='notification'),  # 알람 리스트
    path('notifications/read/', views.mark_notifications_as_read, name='mark_notifications_as_read'),  # 알람 읽음 처리

    
]
