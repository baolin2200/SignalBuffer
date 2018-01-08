from django.shortcuts import render,HttpResponse
from django.views.decorators.cache import cache_page
# Create your views here.
from app01 import models
import time


# 超时时间(秒)
# @cache_page(60 * 15)
def users(request):
    ctime = str(time.time())
    print(ctime)
    # return HttpResponse(ctime)
    return render(request,"users.html", {"ctime":ctime})


def adduser(request):
    models.UserInfo.objects.create(username="zhangsan",)

    return HttpResponse("创建数据成功！")
