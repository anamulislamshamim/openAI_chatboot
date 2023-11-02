from django.shortcuts import render
from django.http import JsonResponse


def chatboot(request):
    print(request.method)
    if request.method == 'POST':
        message = request.POST.get('message') 
        response = 'I am fine. What about you?'
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatboot.html')
