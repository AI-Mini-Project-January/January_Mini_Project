from django.shortcuts import render

from django.shortcuts import render

def member_info(request):
    return render(request, 'mypage/member_info.html')

def member_edit(request):
    return render(request, 'mypage/member_edit.html')