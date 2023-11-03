from django.shortcuts import render, redirect
from django.http import JsonResponse
import openai
import os
from dotenv import load_dotenv
from django.contrib import auth 
from django.contrib.auth.models import User
from .models import Chatboot
from django.utils import timezone
from django.contrib.auth.decorators import login_required


load_dotenv()
open_api_key = os.environ.get('OPENAI_KEY')
openai.api_key = open_api_key


def ask_openai(question):
    response = openai.Completion.create(
        model = "text-davinci-003",
        prompt = question,
        max_tokens = 150,
        n = 1,
        stop = None,
        temperature = 0.7,
    )
    print(response)
    answer = response.choices[0].text.lstrip()
    return answer

# @login_required
def chatboot(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    chats = Chatboot.objects.filter(user=request.user)
    if request.method == 'POST':
        message = request.POST.get('message') 
        response = ask_openai(message)
        chat = Chatboot(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatboot.html', {'chats': chats})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            return redirect('chatboot')
        else:
            error_message = 'Invalid user!'
            return render(request, 'login.html', {'error_message': error_message})
        
    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1) 
                user.save()
                auth.login(request, user)
                return redirect('chatboot')
            except:
                error_message = "Error creating account"
                return render(request, 'register.html', {'error_message': error_message})
        else:
            error_message = "Password does not match!"
            return render(request, 'register.html', {'error_message': error_message})
        
    return render(request, 'register.html')


def logout(request):
    auth.logout(request)
    return redirect('login')