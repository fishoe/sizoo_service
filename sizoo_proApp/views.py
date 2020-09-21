
from django.shortcuts import render

from django.shortcuts import redirect
from .models import UserInfo, LineUp, ShoesData, ServiceResult, ShoesExp
from django.contrib.auth.models import User
from django.contrib import auth
import re

# Create your views here.


ERROR_MSG = {
    # ID
    'ID_EXIST': 'This ID already exists',
    'ID_NOT_EXIST': 'ID does not exist',
    'ID_LENGTH': 'ID must be between 3 and 12 characters',
    
    # PW
    'PW_CHECK': 'This PW incorrect',
    'PW_LENGTH': 'PW must be between 6 and 12 characters',
    
    # ID&PW
    'ID_PW_MISSING': 'Please check your ID or PW',
    
    # Gender
    'Gender_CHECK': 'Please check your gender',
    
    # EMAIL
    'EMAIL_EXIST': 'This Email already exists',
    'EMAIL_CHECK': 'This Email format is invalid',
    
    # Shoes
    'Shoe_CHECK': 'Please check model number',
    'Size_CHECK': 'Please check size selection',
    
    # ShoesData
    'ShoeData_CHECK': 'Sorry, we could not find this model',
    }


def home(request):
    
    # check point
    print("def__home")
    
    # result
    result = render(request, 'home.html')
    
    if request.method == 'POST':
        
        if 'run_Login' in request.POST:     
            
            # result
            result = login(request)
            
        if 'run_SignUp' in request.POST:    
            
            # result
            result = signup(request)
    
    
    return result


def login(request):
    
    # check point
    print("def__login")
    
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
        
        # All Brands from LineUp
        lineupAll = LineUp.objects.all()
        
        # All Shoes from ShesData
        shoesdataAll = ShoesData.objects.all()
        
        # shoerackDict
        shoerackDict = {'lineupAll':lineupAll, 'shoesdataAll':shoesdataAll}
        
        # result
        result = render(request, 'shoerack.html', shoerackDict)
        
        
    except Exception as e:
        context['error']['state'] = True
        context['error']['msg'] = ERROR_MSG[e.args[0]]
        
        # result
        result = render(request, 'home.html', context)
    
    
    return result


def signup(request):
    
    # check point
    print("def__signup")
    
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
        
        # login
        auth.login(request, userinfo_user)
        
        # All Brands from LineUp
        lineupAll = LineUp.objects.all()
        
        # All Shoes from ShesData
        shoesdataAll = ShoesData.objects.all()
        
        # shoerackDict
        shoerackDict = {'lineupAll':lineupAll, 'shoesdataAll':shoesdataAll}
        
        # result
        result = render(request, 'shoerack.html', shoerackDict)
        
        
    except Exception as e:
        context['error']['state'] = True
        context['error']['msg'] = ERROR_MSG[e.args[0]]
        
        # result
        result = render(request, 'home.html', context)
    
    
    return result


def logout(request):
    
    # check point
    print("def__logout")
    
    auth.logout(request)
    
    return redirect('home')


def shoerack(request):
    
    # check point
    print("def__shoerack")
    
    # result
    result = render(request, 'shoerack.html')
    
    if request.method == 'POST':
        
        if 'run_Login' in request.POST:
            
            # result
            result = login(request)
            
        if 'run_Add' in request.POST:
            
            # result
            result = shoeadd(request)
    
    
    return result 



def shoeadd(request):
    
    # check point
    print("def__shoeadd")
    
    context = {
        'error': {
            'state': False,
            'msg': ''
        },
    }
    
    # shoesexp_user = UserInfo.objects.get(pk=userpk_pk)
    
    shoeFromPost = request.POST['model_name']
    
    shoesexp_size = request.POST.get('shoes_size')
    shoes_search = ShoesData.objects.filter(Model_name=shoeFromPost)
    
    # shoesexp_shoe = ShoesData.objects.get(Model_name=shoeFromPost).Line_Up_models.all()
    
    try:
        if len(shoeFromPost) == 0:
            
            raise Exception('Shoe_CHECK')
        
        if shoesexp_size == None:
            
            raise Exception('Size_CHECK')
        
        if len(shoes_search) == 0:
            
            raise Exception('ShoeData_CHECK')
        
        # # ShoesExp create
        # ShoesExp.objects.create(
        #     ShoesExp_User = shoesexp_user,
        #     ShoesExp_Shoe = shoesexp_shoe,
        #     ShoesExp_Size = int(shoesexp_size)
        #     )
        
        result = redirect('shoerack')
        
        
    except Exception as e:
        context['error']['state'] = True
        context['error']['msg'] = ERROR_MSG[e.args[0]]
        
        # result
        result = render(request, 'shoerack.html', context)
    
    
    return result


def shoedelete(request, shoe_context):
    
    shoe_context['state'] = False
    
    return render(request, 'shoerack.html', shoe_context)


def shoemeasure(request):
    
    # shoesexp_user = UserInfo.objects.get(UserInfo_User=User)
    # ShoesExp.objects.create(
    #     ShoesExp_User = shoesexp_user,
    #     ShoesExp_Shoe = shoe_context['shoesexp_shoe'], 
    #     ShoesExp_Size = shoe_context['shoesexp_size']
    # )
    
    return render(request, 'result.html')


def result(request):
    
    if request.method == 'POST':
        
        if 'run_Re_shoerack' in request.POST:
            
            result = render(request, 'shoerack.html')
    
    
    return result