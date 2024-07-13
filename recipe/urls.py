from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import create_recipe_view, recipe_list_view, recipe_detail_view, edit_recipe_view, delete_recipe_view
#레시피 하면 떠오르는 기능들 작성 crud
#유저의 경우 회원가입, 로그인, 로그아웃

urlpatterns = [
    path('create_recipe/', login_required(create_recipe_view), name='create_recipe'),
    path('recipe_list/', recipe_list_view, name='recipe_list'),
    path('recipe/<int:pk>/', recipe_detail_view, name='recipe_detail'),
    path('edit_recipe/', login_required(edit_recipe_view), name='edit_recipe'),
    path('delete_recipe/', login_required(delete_recipe_view), name='delete_recipe'),
]


from django.urls import path
from .views import home, signup_view, login_view, logout_view

app_name = "user"

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
