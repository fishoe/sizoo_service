from django.shortcuts import render

from django.shortcuts import redirect
from .models import UserInfo, ShoesExp, LineUp, ShoesData
from django.contrib.auth.models import User
from django.contrib import auth
import re
# Create your views here.


ERROR_MSG = {
    # ID
    'ID_EXIST': 'This ID already exists.',
    'ID_NOT_EXIST': 'ID does not exist.',
    'ID_LENGTH': 'ID must be between 3 and 12 characters',
    
    # PW
    'PW_CHECK': 'This PW incorrect.',
    'PW_LENGTH': 'PW must be between 6 and 12 characters',
    
    # ID&PW
    'ID_PW_MISSING': 'Please check your ID or PW.',
    
    # Gender
    'Gender_CHECK': 'Please check your gender.',
    
    # EMAIL
    'EMAIL_EXIST': 'This Email already exists.',
    'EMAIL_CHECK': 'This Email format is invalid'
}


def login(request):
    context = {
        'error': {
            'state': False,
            'msg': ''
        },
    }
    
    # django User variables
    user_id = request.POST['user_id']
    user_pw = request.POST['user_pw']
    
    # some variables before try function
    user_search = User.objects.filter(username=user_id)
    userinfo_user = auth.authenticate(username=user_id, password=user_pw)
    
    
    try:
        # ID&PW validate inspection
        if not (user_id and user_pw):
            
            raise Exception('ID_PW_MISSING')
        
        # ID validate inspection
        if len(user_search) == 0:
            
            raise Exception('ID_NOT_EXIST')
        
        # PW validate inspection
        if userinfo_user == None:
            
            raise Exception('PW_CHECK')
        
        # login
        auth.login(request, userinfo_user)
        
        # result
        result = render(request, 'login.html')
        
        
    except Exception as e:
        context['error']['state'] = True
        context['error']['msg'] = ERROR_MSG[e.args[0]]
        
        # result
        result = render(request, 'home.html', context)
    
    
    return result


def signup(request):
    
    context = {
        'error': {
            'state': False,
            'msg': ''
        }
    }
    
    # django User variables
    user_id = request.POST['user_id']
    user_pw = request.POST['user_pw']
    
    # User check variables 
    user_pw_check = request.POST['user_pw_check']
    
    # UserInfo variables
    userinfo_gender = request.POST.get('user_gender')
    userinfo_email = request.POST['user_email']
    
    # some variables before try function
    user_search = User.objects.filter(username=user_id)
    email_search = UserInfo.objects.filter(UserInfo_Email=userinfo_email)
    email_check = re.compile(r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$').match(userinfo_email)
    
    
    try:
        # ID&PW validate inspection
        if not (user_id and user_pw):
            
            raise Exception('ID_PW_MISSING')
        
        # ID validate inspection
        if len(user_search) != 0:
            
            raise Exception('ID_EXIST')
        
        if (len(user_id)<3) or (len(user_id)>12):
            
            raise Exception('ID_LENGTH')
        
        # PW validate inspection
        if (len(user_pw)<6) or (len(user_pw)>12):
            
            raise Exception('PW_LENGTH')
        
        if user_pw != user_pw_check:
            
            raise Exception('PW_CHECK')
        
        # Gender validate inspection
        if userinfo_gender == None:
            
            raise Exception('Gender_CHECK')
        
        # Email validate inspection 
        if len(email_search) != 0:
            
            raise Exception('EMAIL_EXIST')
        
        if email_check == None:
            
            raise Exception('EMAIL_CHECK')
        
        # create userinfo_user through django User
        userinfo_user = User.objects.create_user(username=user_id, password=user_pw)
        
        # UserInfo create 
        UserInfo.objects.create(
            UserInfo_User = userinfo_user,
            UserInfo_Gender = int(userinfo_gender), 
            UserInfo_Email = userinfo_email
            )
        
        # send to '???' class variables 
        # ???_?? = UserInfo.objects.get(pk=user_id)
        
        # login after signup
        auth.login(request, userinfo_user)                                      
        
        # result
        result = render(request, 'login.html')
        
        
    except Exception as e:
        context['error']['state'] = True
        context['error']['msg'] = ERROR_MSG[e.args[0]]
        
        # result
        result = render(request, 'home.html', context)
    
    
    return result


def home(request):
    
    result = render(request, 'home.html')
    
    if request.method == 'POST':
        
        if 'Login' in request.POST:
            
            result = login(request)
        
        
        if 'SignUp' in request.POST:
            
            result = signup(request)
    
    
    return result


def logout(request):
    
    auth.logout(request)
    
    return redirect('home')

