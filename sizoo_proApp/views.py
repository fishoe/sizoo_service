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

def signup(request):
    
    context = {
        'error': {
            'state': False,
            'msg': ''
        }
    }
    
    
    if request.method == "POST":
        
        # django User variables
        user_id = request.POST['user_id']
        user_pw = request.POST['user_pw']
        
        # User check variables 
        user_pw_check = request.POST['user_pw_check']
        
        # UserInfo variabls
        userinfo_gender = int(request.POST['user_gender'])
        userinfo_email = request.POST['user_email']
        
        # 파동권 코드는 나빠요 ㅠㅠ
        # 예외 처리로 해결해주세요
        # try & except로 파동권 최소화         
        # ID&PW validate inspection Start Line
        if (user_id and user_pw):
            
            # duplicate user searching variable
            user_search = User.objects.filter(username=user_id)
            
            
            if len(user_search) == 0:
                
                
                if (len(user_id)>2) and (len(user_id)<13):
                    
                    
                    if (len(user_pw)>5) and (len(user_pw)<13):
                        
                        
                        if user_pw == user_pw_check:
                            
                            
                            if len(userinfo_gender) != 0:
                                
                                # search duplicate email
                                email_search = UserInfo.objects.filter(UserInfo_Email=userinfo_email)
                                
                                
                                if len(email_search) == 0:
                                    
                                    # check email format through Regular Expression
                                    EMAIL_CHECK = re.compile(r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
                                    email_check = EMAIL_CHECK.match(userinfo_email)
                                    
                                    if email_check != None:
                                        
                                        # create userinfo_user through django User
                                        userinfo_user = User.objects.create_user(username=user_id, password=user_pw)
                                        
                                        
                                        # send to '???' class variables 
                                        #ShoesExp_ID = UserInfo.objects.get(pk=user_id)
                                        
                                        
                                        # UserInfo create 
                                        UserInfo.objects.create(
                                            UserInfo_User = userinfo_user,
                                            UserInfo_Gender = userinfo_gender, 
                                            UserInfo_Email = userinfo_email
                                            )
                                        
                                        # login after signup
                                        auth.login(request, userinfo_user)
                                        
                                    else:
                                        context['error']['state'] = True
                                        context['error']['msg'] = ERROR_MSG['EMAIL_CHECK']                                        
                                else:
                                    context['error']['state'] = True
                                    context['error']['msg'] = ERROR_MSG['EMAIL_EXIST']
                            else:
                                context['error']['state'] = True
                                context['error']['msg'] = ERROR_MSG['Gender_CHECK']
                        else:
                            context['error']['state'] = True
                            context['error']['msg'] = ERROR_MSG['PW_CHECK']
                        
                    else:
                        context['error']['state'] = True
                        context['error']['msg'] = ERROR_MSG['PW_LENGTH']
                    
                else:
                    context['error']['state'] = True
                    context['error']['msg'] = ERROR_MSG['ID_LENGTH']
                
            else:
                context['error']['state'] = True
                context['error']['msg'] = ERROR_MSG['ID_EXIST']
            
        else:
            context['error']['state'] = True
            context['error']['msg'] = ERROR_MSG['ID_PW_MISSING']
    
    return render(request, 'login.html', context)


def login(request):
    context = {
        'error': {
            'state': False,
            'msg': ''
        },
    }
    
    
    if request.method == 'POST':
        
        # django User variables
        user_id = request.POST['user_id']
        user_pw = request.POST['user_pw']
        
        # duplicate user searching variable
        user_search = User.objects.filter(username=user_id)
        
        if (user_id and user_pw):
            
            
            if len(user_search) != 0:
                
                userinfo_user = auth.authenticate(username=user_id, password=user_pw)
                
                
                if userinfo_user != None:
                    
                    auth.login(request, userinfo_user)
                    
                    result = render(request, 'login.html')
                else:
                    context['error']['state'] = True
                    context['error']['msg'] = ERROR_MSG['PW_CHECK']
            else:
                context['error']['state'] = True
                context['error']['msg'] = ERROR_MSG['ID_NOT_EXIST']
        else:
            context['error']['state'] = True
            context['error']['msg'] = ERROR_MSG['ID_PW_MISSING']

        # 예외처리 예시 코드입니다.
        # 
        # try :
        #     if not (user_id and user_pw) :
        #         raise Exception('PW_CHECK')
            
        #     if len(user_search) == 0:
        #         raise Exception('ID_NOT_EXIST')
            
        #     if userinfo_user == None :
        #         raise Exception('ID_PW_MISSING')
            
        #     auth.login(request, userinfo_user)
                    
        #     result = render(request, 'login.html')
        # except Exception as e:
        #     context['error']['state'] = True
        #     context['error']['msg'] = ERROR_MSG[e.args]
    

    result = render(request, 'home.html')
    
    return result


def home(request):
    
    if request.method == 'POST':
        if 'SignUp' in request.POST:
            result = signup(request)
        elif 'Login' in request.POST:
            result = login(request)
        
    result = render(request, 'home.html')
    
    return result


def logout(request):
    
    auth.logout(request)
    
    return redirect('home')
