from django.shortcuts import render

# Create your views here.

def call_expert(request):
    return render(request, 'ChooseDesigner.html', {})

#CallSeniorDesigner
def call_senior_designer(request):
    return render(request, 'CallSeniorDesigner.html', {})

#call designer
def call_designer(request):
    return render(request, 'callEpertTwo.html', {})