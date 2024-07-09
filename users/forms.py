#로그인 및 회원가입 폼 정의
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class signUpForm(UserCreationForm):
    email = forms.EmailField(lable='이메일', max_length=254, help_text='유효한 이메일 주소를 입력하세요.')
    
    class Meta:
        model = User
        fields = ('username' , 'email' , 'password1' , 'password2')
        lables = {
            'userame': '아이디',
            'password1': '비밀번호',
            'password2': '비밀번호 확인'
        }

    
class loginForm(forms.Form):
    login_username = forms.CharField(lable='아이디') #변수이름 설정 다시 생각
    login_password = forms.CharField(widget=forms.PasswordInput, label='비밀번호')