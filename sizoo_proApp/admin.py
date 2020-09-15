from django.contrib import admin

from .models import UserInfo, ShoesExp, LineUp, ShoesData
# Register your models here.

admin.site.register(UserInfo)
admin.site.register(ShoesExp)
admin.site.register(LineUp)
admin.site.register(ShoesData)