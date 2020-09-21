from django.db import models

from django.contrib.auth.models import User
# Create your models here.

class UserInfo(models.Model):
    # own variables
    UserInfo_User = models.OneToOneField(User, on_delete=models.CASCADE, related_name='UserInfo_User')#쟝고 기본 유저정보 상속
    UserInfo_Gender = models.IntegerField() #유저 성별 정보
    UserInfo_Email = models.CharField(max_length=255) #유저 이메일

class LineUp(models.Model):
    # own variables
    LineUp_Brand = models.CharField(max_length=255)
    LineUp_Model_Code = models.CharField(max_length=255) #라인업 고유 코드
    
    #lineup attribute
    LineUp_Width = models.IntegerField() #라인업 고유 수치
    LineUp_Length = models.IntegerField() #라인업 고유 수치

class ShoesData(models.Model):
    Model_name = models.CharField(max_length=255)
    Model_code = models.CharField(max_length=255,unique=True)
    Model_lineUp = models.ForeignKey(LineUp, on_delete = models.DO_NOTHING, related_name='Line_Up_models')
    
    # variables from UserInfo 
    # ShoesData_ID = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='ShoesData_ID')#외래키 쓰면 안됩니다. 
    # ShoesData_Gender = models.ForeignKey(UserInfo, on_delete=models.DO_NOTHING, related_name='ShoesData_Gender')#슈 젠더가 왜 유저의 키를 받죠?
    
    # variables from ShoesExp
    # ShoesData_Brand = models.ForeignKey(ShoesExp, on_delete=models.DO_NOTHING, related_name='ShoesData_Brand')
    # ShoesData_Model_Num = models.ForeignKey(ShoesExp, on_delete=models.DO_NOTHING, related_name='ShoesData_Model_Num')
    # ShoesData_Size = models.ForeignKey(ShoesExp, on_delete=models.DO_NOTHING, related_name='ShoesData_Size')
    
    # * How connect Shoes Model Infomations? *
    
    # variables from LineUp
    
    # ShoesData_Width = models.ForeignKey(LineUp, on_delete=models.CASCADE, related_name='ShoesData_Width')
    # ShoesData_Length = models.ForeignKey(LineUp, on_delete=models.CASCADE, related_name='ShoesData_Length')
    # ShoesData_Toehil = models.ForeignKey(LineUp, on_delete=models.CASCADE, related_name='ShoesData_Toehil')


class ServiceResult(models.Model):
    User = models.ForeignKey(UserInfo,on_delete = models.DO_NOTHING,related_name='usedUser') # 서비스 이용 유저
    tgtShoe = models.ForeignKey(ShoesData,on_delete = models.DO_NOTHING,related_name='tgts') # 이용 유저 타겟 신발
    result = models.IntegerField() #결과

class ShoesExp(models.Model):
    '''
    사용자가 어떤 신발을 어떤 사이즈로 신었는지에 대해서 기록하는 부분입니다.
    외래키로 사용자 정보 & 신발 정보 둘다 외래키로 받고
    신발 사이즈에 대한것만 따로 기록하면 됩니다.
    밑에 신발 라인업에도 브랜드가 있고 신발 정보에도 브랜드가 있어요.
    '''
    # variable from UserInfo 
    # ShoesExp_ID = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='ShoesExp_ID')#신발 경험
    # foreign key from shoe, user
    ShoesExp_User = models.ForeignKey(UserInfo, on_delete = models.DO_NOTHING, related_name='user_shoes', null=True) #원본 객체가 지워져도 여기 정보는 지워지면 안됩니다.
    ShoesExp_vuser = models.IntegerField(max_length=255,null=True)

    ShoesExp_Shoe = models.ForeignKey(ShoesData, on_delete = models.DO_NOTHING, related_name='exps') #이하 동문
    
    # own variables
    '''
    여기도 비슷하게 사이즈 말고는
    다른 정보는 생략해도 될거에요.
    중복된 정보를 최소화합시다.
    '''
    # ShoesExp_Brand = models.CharField(max_length=255)
    # ShoesExp_Model_Num = models.CharField(max_length=255)
    ShoesExp_Size = models.IntegerField() #이거 빼고는 다 날려도 될거 같아요
