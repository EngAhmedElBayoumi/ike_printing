from django.shortcuts import render
from dragon.models import working_setting as dragon_working_setting
from senior_dragon.models import working_setting as senior_dragon_working_setting

# Create your views here.

def call_expert(request):
    return render(request, 'ChooseDesigner.html', {})

#CallSeniorDesigner
def call_senior_designer(request):
    return render(request, 'CallSeniorDesigner.html', {})

#call designer
def call_designer(request):
    return render(request, 'callEpertTwo.html', {})

