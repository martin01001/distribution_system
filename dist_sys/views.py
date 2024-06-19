import json
from django.http import JsonResponse
from django.shortcuts import render
from core import main
# Create your views here.

def home(request):
    return render(request, "index.html")



def form(request):
    return render(request, "form.html")


def get_result(request):
    if request.method == "POST":
        data = json.loads(request.body)  
        result = main.start_find_solution(data)
        return JsonResponse(result)

