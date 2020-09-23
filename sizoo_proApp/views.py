from django.shortcuts import render

from django.shortcuts import redirect
from .models import UserInfo, LineUp, ShoesData, ServiceResult, ShoesExp
from django.contrib.auth.models import User
from django.contrib import auth
import re

from django.db.models import Model

from .predict.predict import predict
import json
from django.http import JsonResponse

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
    'ShoeData_CHECK': 'Sorry, we could not find this model'
    }


def shoerackLoad(shoesexp_user):
    
    # check point
    print("def__shoerackLoad")
    
    # variables for shoerackDict
    q = ShoesData.objects.all()
    t = {}
    for i in q:
        brand = i.Model_lineUp.LineUp_Brand
        if brand in t :
            t[brand].append(i.Model_name)
        else :
            t[brand] = [i.Model_name]
    
    shoeexpAll = ShoesExp.objects.filter(ShoesExp_User=shoesexp_user)
    shoeexpLineUp_list = []
    for i in range(len(shoeexpAll)):
        
        Model_name = shoeexpAll[i].ShoesExp_Shoe.Model_name
        shoeexpLineUp = ShoesData.objects.filter(Model_name=Model_name)[0].Model_lineUp
        shoeexpLineUp_list.append(shoeexpLineUp)
    
    # shoerackDict
    shoerackDict = {
        'sd': t,
        'shoesdata': zip(shoeexpLineUp_list, list(shoeexpAll)),
        'shoeexpAll': shoeexpAll
        }
    
    # result
    result = shoerackDict
    
    
    return result



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
        
        # shoesexp_user
        shoesexp_user = UserInfo.objects.filter(UserInfo_User=userinfo_user)[0]
        
        # shoerackDict
        shoerackDict = shoerackLoad(shoesexp_user)
        
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
        
        # shoesexp_user
        shoesexp_user = UserInfo.objects.filter(UserInfo_User=userinfo_user)[0]
        
        # shoerackDict
        shoerackDict = shoerackLoad(shoesexp_user)
        
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
    
    # user_id
    user_id = request.POST.get('user_id')   
    
    # shoesexp_user
    shoesexp_user = UserInfo.objects.filter(UserInfo_User_id=user_id)[0]
    
    # shoerackDict
    shoerackDict = shoerackLoad(shoesexp_user)
    
    # result
    result = render(request, 'shoerack.html', shoerackDict)
    
    if request.method == 'POST':
        
        if 'run_Add' in request.POST:
            
            # result
            result = shoeadd(request)
            
        if 'run_Delete' in request.POST:
            
            # result
            result = shoedelete(request)
        
        if 'run_AllDelete' in request.POST:
            
            # result
            result = shoeAlldelete(request)
        
        if 'run_Search' in request.POST:
            
            # result
            result = result(request)
    
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
    
    user_id = request.POST.get('user_id')    
    shoesexp_user = UserInfo.objects.filter(UserInfo_User_id=user_id)[0]
    shoeFromPost = request.POST.get('brand_model')
    shoesexp_shoe = ShoesData.objects.filter(Model_name=shoeFromPost)
    shoesexp_size = request.POST.get('size')
    
    
    try:
        if len(shoeFromPost) == 0:
            
            raise Exception('Shoe_CHECK')
        
        if shoesexp_size == None:
            
            raise Exception('Size_CHECK')
        
        if len(shoesexp_shoe) == 0:
            
            raise Exception('ShoeData_CHECK')
        
        
        # ShoesExp create
        ShoesExp.objects.create(
            ShoesExp_User = shoesexp_user,
            ShoesExp_Shoe = shoesexp_shoe[0],
            ShoesExp_Size = int(shoesexp_size)
            )
        
        # shoerackDict
        shoerackDict = shoerackLoad(shoesexp_user)
        
        # result
        result = render(request, 'shoerack.html', shoerackDict)
        
        
    except Exception as e:
        context['error']['state'] = True
        context['error']['msg'] = ERROR_MSG[e.args[0]]
        
        # shoerackDict
        shoerackDict = shoerackLoad(shoesexp_user)
        
        # result
        result = render(request, 'shoerack.html', shoerackDict)
    
    
    return result


def shoedelete(request):
    
    # check point
    print("def__shoedelete")
    
    # shoesexp user
    shoesexp_user_pk = request.POST.get('shoesexp_user_pk')
    
    print(ShoesExp.objects.filter(pk=shoesexp_user_pk))
    # shoedelete
    ShoesExp.objects.filter(pk=shoesexp_user_pk).delete()
    
    # user_id
    user_id = request.POST.get('user_id')
    
    # shoesexp_user
    shoesexp_user = UserInfo.objects.filter(UserInfo_User_id=user_id)[0]
    
    # shoerackDict
    shoerackDict = shoerackLoad(shoesexp_user)
    
    # result
    result = render(request, 'shoerack.html', shoerackDict)
    
    
    return result


def shoeAlldelete(request):
    
    # check point
    print("def__shoeAlldelete")
    
    # user_id
    user_id = request.POST.get('user_id')   
    
    # shoesexp_user
    shoesexp_user = UserInfo.objects.filter(UserInfo_User_id=user_id)[0]
    # shoeexpAll = ShoesExp.objects.filter(ShoesExp_User=shoesexp_user)
    
    # shoerackDict
    shoerackDict = shoerackLoad(shoesexp_user)
    
    # shoealldelete
    for i in range(len(shoerackDict['shoeexpAll'])):
    
        shoerackDict['shoeexpAll'][i].delete()
    
    # update shoerackDict
    shoerackDict = shoerackLoad(shoesexp_user)
    
    # result
    result = render(request, 'shoerack.html', shoerackDict)
    
    return result


# def result(request):
    
#     # check point
#     print("def__result")
    
#     # user
#     user_id = request.POST.get('user_id')   
    
#     # shoesexp_user
#     shoesexp_user = UserInfo.objects.filter(UserInfo_User_id=user_id)[0]
    
#     # shoerackDict
#     shoerackDict = shoerackLoad(shoesexp_user)
    
#     # result
#     result = render(request, 'result.html', shoerackDict)
    
#     if request.method == 'POST':
        
#         if 'find_size' in request.POST:
            
#             result = findSize(request)
            
#         if 'find_size' in request.POST:
            
#             result = shoerack(request)
    
    
#     return result


def result(request):
    print("def__result")

    shoerackDict={}

    q = ShoesData.objects.all()
    t = {}
    for i in q:
        brand = i.Model_lineUp.LineUp_Brand
        if brand in t :
            t[brand].append(i.Model_name)
        else :
            t[brand] = [i.Model_name]

    shoerackDict['sd'] = t

    if request.method == 'POST' : #AJAX part
        req_json = eval(request.body)
        #print(req_json)
        tgt = req_json['target']
        if tgt is None:
            #print(request.body)
            return JsonResponse({'size':-1})
        user_pk = UserInfo.objects.get(UserInfo_User__username=request.user).pk
        res = predict(user_pk, tgt)
        try:
            q = ServiceResult.objects.get(User_id=user_pk,tgtShoe=ShoesData.objects.get(Model_name=tgt))
            q.result=res
            q.save()
        except ServiceResult.DoesNotExist as e:
            q = ServiceResult.objects.create(User_id=user_pk,tgtShoe=ShoesData.objects.get(Model_name=tgt),result=res)
            q.save()

        return JsonResponse({'size': res})

    q = ShoesExp.objects.filter(ShoesExp_User__UserInfo_User__username=request.user)

    t=[]
    for i in q :
        t.append((i.ShoesExp_Shoe.Model_lineUp.LineUp_Brand,i.ShoesExp_Shoe.Model_name,i.ShoesExp_Size))
    shoerackDict['myract'] = t

    result = render(request, 'result.html', shoerackDict)

    # check point
    # user = request.POST.get('user')
    # tgt = request.POST.get('tgt')
    # result = predict(user, tgt)

    return result

def findSize(request):
    
    # check point
    print("def__findSize")
    
    # user = request.POST.get('user_id')
    # tgt = request.POST.get('tgt', None)

    # if (tgt == None):
    #     return redirect('result.html')
    
    # predDict = {
    #     'pred' : predict(user, tgt)
    # }

    # result = render(request, 'result.html', predict)
    
    return result
