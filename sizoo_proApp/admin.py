from django.contrib import admin

from .models import UserInfo, LineUp, ShoesData, ServiceResult, ShoesExp
# Register your models here.

admin.site.register(UserInfo)
admin.site.register(LineUp)
admin.site.register(ShoesData)
admin.site.register(ServiceResult)
admin.site.register(ShoesExp)