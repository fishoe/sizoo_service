from django.db import models

from django.contrib.auth.models import User
# Create your models here.

class UserInfo(models.Model):
    # own variables
    UserInfo_User = models.OneToOneField(User, on_delete=models.CASCADE, related_name='UserInfo_User')
    
    UserInfo_Gender = models.IntegerField()
    UserInfo_Email = models.CharField(max_length=255)

class ShoesExp(models.Model):
    # variable from UserInfo 
    ShoesExp_ID = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='ShoesExp_ID')
    
    # own variables
    ShoesExp_Brand = models.CharField(max_length=255)
    ShoesExp_Model_Num = models.CharField(max_length=255)
    ShoesExp_Size = models.IntegerField()

class LineUp(models.Model):
    # own variables
    LineUp_Brand = models.CharField(max_length=255)
    LineUp_Model_Num = models.CharField(max_length=255)
    LineUp_Width = models.IntegerField()
    LineUp_Length = models.IntegerField()
    LineUp_Toehil = models.IntegerField()

class ShoesData(models.Model):
    # variables from UserInfo 
    ShoesData_ID = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='ShoesData_ID') 
    ShoesData_Gender = models.ForeignKey(UserInfo, on_delete=models.DO_NOTHING, related_name='ShoesData_Gender')
    
    # variables from ShoesExp
    ShoesData_Brand = models.ForeignKey(ShoesExp, on_delete=models.DO_NOTHING, related_name='ShoesData_Brand')
    ShoesData_Model_Num = models.ForeignKey(ShoesExp, on_delete=models.DO_NOTHING, related_name='ShoesData_Model_Num')
    ShoesData_Size = models.ForeignKey(ShoesExp, on_delete=models.DO_NOTHING, related_name='ShoesData_Size')
    
    # * How connect Shoes Model Infomations? *
    
    # variables from LineUp
    ShoesData_Width = models.ForeignKey(LineUp, on_delete=models.CASCADE, related_name='ShoesData_Width')
    ShoesData_Length = models.ForeignKey(LineUp, on_delete=models.CASCADE, related_name='ShoesData_Length')
    ShoesData_Toehil = models.ForeignKey(LineUp, on_delete=models.CASCADE, related_name='ShoesData_Toehil')

