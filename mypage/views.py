from django.shortcuts import render

from django.shortcuts import render

def member_info(request):
    return render(request, 'mypage/member_info.html')
