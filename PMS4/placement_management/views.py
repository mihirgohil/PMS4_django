from django.shortcuts import render

# Create your views here.

def showDemoPage(request):
    return render(request, "demo.html")

def showBase(request):
    return render(request, "college_template/base_template.html")
